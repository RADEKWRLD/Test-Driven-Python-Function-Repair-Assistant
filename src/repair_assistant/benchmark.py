"""Run a batch, save each result immediately, and skip recorded jobs on continuation."""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from repair_assistant.agent import (
    MAX_ATTEMPTS,
    PROTOCOL_NAME,
    AttemptCost,
    RepairStrategy,
    SharedFirstAttempt,
)
from repair_assistant.costs import Pricing
from repair_assistant.evaluation import aggregate_summaries
from repair_assistant.model import ModelAdapter
from repair_assistant.output_paths import create_output_directory, create_run_directory
from repair_assistant.redaction import redact
from repair_assistant.reporting import generate_experiment_report
from repair_assistant.run import RunExecutionError, RunResult, RunService, SharedFirstSeed
from repair_assistant.task import TaskSpec
from repair_assistant.terminal import format_benchmark_cases, format_task_progress
from repair_assistant.types import CommandResult, VerificationResult


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
        "implementation": "shared-first-fork-v4",
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
        for repetition, task_path, branch_order in _execution_units(schedule):
            task = tasks[str(task_path)]
            a_identity = (task.task_id, RepairStrategy.SINGLE_SHOT.value, repetition)
            a_row = next(
                (
                    row
                    for row in rows
                    if (row.get("task_id"), row.get("strategy"), row.get("repetition"))
                    == a_identity
                ),
                None,
            )
            fork_seed: SharedFirstSeed | None = None
            if a_row is None:
                a_row, result = _execute_one(
                    service=service,
                    directory=directory,
                    task=task,
                    model_factory=model_factory,
                    strategy=RepairStrategy.SINGLE_SHOT,
                    repetition=repetition,
                    secrets=model.sensitive_values,
                )
                _append_result(results_file, a_row)
                rows.append(a_row)
                completed.add(a_identity)
                print(format_task_progress(a_row, previous_row), flush=True)
                previous_row = a_row
                if result is not None:
                    fork_seed = _seed_from_result(result, a_row)
            elif a_row.get("outcome") in {"passed", "failed"}:
                fork_seed = _seed_from_saved(directory, a_row)

            for strategy_value in branch_order:
                identity = (task.task_id, strategy_value, repetition)
                if identity in completed:
                    continue
                if fork_seed is None:
                    row = _shared_first_error_row(task, strategy_value, repetition, a_row)
                else:
                    row, _ = _execute_one(
                        service=service,
                        directory=directory,
                        task=task,
                        model_factory=model_factory,
                        strategy=RepairStrategy(strategy_value),
                        repetition=repetition,
                        secrets=model.sensitive_values,
                        shared_first=fork_seed,
                    )
                _append_result(results_file, row)
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


def _execution_units(
    schedule: Sequence[tuple[int, str, Path]],
) -> list[tuple[int, Path, tuple[str, ...]]]:
    units: dict[tuple[int, str], tuple[Path, list[str]]] = {}
    for repetition, strategy, task_path in schedule:
        key = (repetition, str(task_path))
        if key not in units:
            units[key] = (task_path, [])
        if strategy != RepairStrategy.SINGLE_SHOT.value:
            units[key][1].append(strategy)
    required = {
        RepairStrategy.RETRY_WITHOUT_FEEDBACK.value,
        RepairStrategy.TEST_FEEDBACK.value,
    }
    result = []
    for (repetition, _), (task_path, branches) in units.items():
        if set(branches) != required or len(branches) != 2:
            raise ValueError("shared-first benchmark requires one B and one C branch per task")
        result.append((repetition, task_path, tuple(branches)))
    return result


def _execute_one(
    *,
    service: RunService,
    directory: Path,
    task: TaskSpec,
    model_factory: Callable[[], ModelAdapter],
    strategy: RepairStrategy,
    repetition: int,
    secrets: Sequence[str],
    shared_first: SharedFirstSeed | None = None,
) -> tuple[dict[str, Any], RunResult | None]:
    run_id = create_run_directory(directory, strategy.value, prefix=directory.name).name
    result = None
    try:
        result = service.execute(
            task=task,
            model=model_factory(),
            strategy=strategy,
            max_attempts=MAX_ATTEMPTS,
            run_id=run_id,
            shared_first=shared_first,
        )
        row = json.loads((result.run_dir / "summary.json").read_text(encoding="utf-8"))
    except RunExecutionError as exc:
        row = dict(exc.summary)
    except Exception as exc:
        row = {
            "run_id": run_id,
            "task_id": task.task_id,
            "strategy": strategy.value,
            "outcome": "error",
            "status": "execution_error",
            "error_type": type(exc).__name__,
            "error_message": redact(str(exc), secrets=secrets),
            "cost": {"currency_cost": None},
        }
    row.update(task_id=task.task_id, strategy=strategy.value, repetition=repetition)
    return row, result


def _append_result(path: Path, row: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def _seed_from_result(result: RunResult, row: dict[str, Any]) -> SharedFirstSeed:
    first = result.agent.attempts[0]
    return SharedFirstSeed(
        attempt=SharedFirstAttempt(
            origin_run_id=result.run_id,
            status=first.status,
            final_message=first.final_message,
            cost=first.cost,
            public_verification=result.first_public,
        ),
        solution_path=first.snapshot / "solution.py",
        cost=dict(row.get("cost", {})),
    )


def _seed_from_saved(directory: Path, row: dict[str, Any]) -> SharedFirstSeed:
    run_id = str(row["run_id"])
    run_dir = directory / "runs" / "group_a" / run_id
    events = [
        json.loads(line)
        for line in (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if line
    ]
    verification_payload = next(
        event["payload"]
        for event in events
        if event.get("type") == "public_verification"
        and event.get("payload", {}).get("stage") == "first"
    )
    completed = next(
        event["payload"]
        for event in events
        if event.get("type") == "attempt_completed" and event.get("payload", {}).get("attempt") == 1
    )
    response: dict[str, Any] = next(
        (
            event["payload"]
            for event in events
            if event.get("type") == "model_response"
            and event.get("payload", {}).get("attempt") == 1
        ),
        {},
    )
    command = verification_payload["command_result"]
    verification = VerificationResult(
        passed=bool(verification_payload["passed"]),
        command_result=CommandResult(**command),
        protected_files_unchanged=bool(verification_payload["protected_files_unchanged"]),
        workspace_policy_compliant=bool(verification_payload["workspace_policy_compliant"]),
        violations=tuple(verification_payload.get("violations", [])),
        cases=dict(verification_payload.get("cases", {})),
        case_results_complete=bool(verification_payload.get("case_results_complete", False)),
    )
    cost = completed["cost"]
    return SharedFirstSeed(
        attempt=SharedFirstAttempt(
            origin_run_id=run_id,
            status=str(completed["status"]),
            final_message=response.get("content"),
            cost=AttemptCost(
                model_calls=int(cost["model_calls"]),
                prompt_tokens=int(cost["prompt_tokens"]),
                completion_tokens=int(cost["completion_tokens"]),
                total_tokens=int(cost["total_tokens"]),
                latency_ms=int(cost["latency_ms"]),
            ),
            public_verification=verification,
        ),
        solution_path=run_dir / "repair_attempts/01/solution.py",
        cost=dict(row.get("cost", {})),
    )


def _shared_first_error_row(
    task: TaskSpec,
    strategy: str,
    repetition: int,
    shared_row: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "run_id": f"shared-first-error-{task.task_id}-r{repetition:02d}-{strategy}",
        "task_id": task.task_id,
        "strategy": strategy,
        "repetition": repetition,
        "outcome": "error",
        "status": "shared_first_error",
        "error_type": "SharedFirstError",
        "error_message": "the shared first submission did not produce reusable evidence",
        "shared_first_run_id": shared_row.get("run_id") if shared_row else None,
        "cost": {"currency_cost": None},
    }
