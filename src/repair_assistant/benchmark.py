"""Run a batch, save each result immediately, and skip recorded jobs on continuation."""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from repair_assistant.agent import MAX_ATTEMPTS, PROTOCOL_NAME, RepairStrategy
from repair_assistant.costs import Pricing
from repair_assistant.evaluation import aggregate_summaries
from repair_assistant.model import ModelAdapter
from repair_assistant.output_paths import create_output_directory, create_run_directory
from repair_assistant.redaction import redact
from repair_assistant.reporting import generate_experiment_report
from repair_assistant.run import RunExecutionError, RunService
from repair_assistant.task import TaskSpec
from repair_assistant.terminal import format_benchmark_cases, format_task_progress


def run_benchmark(
    *,
    schedule: Sequence[tuple[int, str, Path]],
    model_factory: Callable[[], ModelAdapter],
    image: str,
    data_dir: Path,
    seed: int,
    repetitions: int,
    pricing: Pricing | None,
    resume: Path | None = None,
) -> Path:
    model = model_factory()
    data_dir = data_dir.resolve()
    tasks = {str(path): TaskSpec.load(path) for _, _, path in schedule}
    config = {
        "implementation": "course-simple-v2",
        "repair_protocol": PROTOCOL_NAME,
        "max_attempts": MAX_ATTEMPTS,
        "model": model.name,
        "provider": model.provider,
        "model_options": {
            key: getattr(model, key, None) for key in ("base_url", "max_tokens", "timeout_seconds")
        },
        "thinking_mode": "disabled" if model.provider == "deepseek" else "server-controlled",
        "image": image,
        "repetitions": repetitions,
        "randomization_seed": seed,
        "data_dir": str(data_dir),
        "pricing": pricing.to_dict() if pricing else None,
        "jobs": [[r, s, tasks[str(p)].task_id, tasks[str(p)].test_version] for r, s, p in schedule],
    }
    directory = resume.resolve() if resume else create_output_directory(data_dir / "experiments")
    config_file = directory / "config.json"
    results_file = directory / "results.jsonl"
    rows: list[dict[str, Any]] = []
    if resume:
        if not config_file.is_file():
            raise ValueError("resume requires a simplified batch with config.json")
        if json.loads(config_file.read_text(encoding="utf-8")) != config:
            raise ValueError("batch configuration changed; create a new experiment")
        if results_file.exists():
            rows = [
                json.loads(line)
                for line in results_file.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
    else:
        config_file.write_text(
            json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    completed = {(row["task_id"], row["strategy"], row["repetition"]) for row in rows}
    print(f"Experiment: {directory}", flush=True)
    service = RunService(data_dir=directory, image=image, pricing=pricing)
    previous_row: dict[str, Any] | None = None
    try:
        for repetition, strategy_value, task_path in schedule:
            task = tasks[str(task_path)]
            identity = (task.task_id, strategy_value, repetition)
            if identity in completed:
                continue
            run_id = create_run_directory(directory, strategy_value, prefix=directory.name).name
            try:
                result = service.execute(
                    task=task,
                    model=model_factory(),
                    strategy=RepairStrategy(strategy_value),
                    max_attempts=MAX_ATTEMPTS,
                    run_id=run_id,
                )
                row = json.loads((result.run_dir / "summary.json").read_text(encoding="utf-8"))
            except RunExecutionError as exc:
                row = dict(exc.summary)
            except Exception as exc:
                row = {
                    "run_id": run_id,
                    "task_id": task.task_id,
                    "strategy": strategy_value,
                    "outcome": "error",
                    "status": "execution_error",
                    "error_type": type(exc).__name__,
                    "error_message": redact(str(exc), secrets=model.sensitive_values),
                    "cost": {"currency_cost": None},
                }
            row.update(task_id=task.task_id, strategy=strategy_value, repetition=repetition)
            with results_file.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
            rows.append(row)
            completed.add(identity)
            print(format_task_progress(row, previous_row), flush=True)
            previous_row = row
    finally:
        report = aggregate_summaries(rows)
        report.update(
            raw_runs=rows,
            design={**config, "planned_runs": len(schedule)},
            created_at=datetime.now(UTC).isoformat(),
        )
        generate_experiment_report(report, directory)
    print(format_benchmark_cases(directory, rows, secrets=model.sensitive_values), flush=True)
    return directory
