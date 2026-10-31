import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from repair_assistant.benchmark import run_benchmark
from repair_assistant.model import ScriptedModel
from repair_assistant.run import RunExecutionError


def test_batch_saves_each_result_and_skips_saved_failures_on_continuation(
    tmp_path: Path,
    monkeypatch: Any,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = Path(__file__).resolve().parents[1]
    task = root / "benchmarks/tasks/chunk-list"
    calls: list[str] = []

    class Service:
        def __init__(self, **kwargs: Any) -> None:
            self.data_dir = kwargs["data_dir"]

        def execute(self, **kwargs: Any) -> SimpleNamespace:
            strategy = kwargs["strategy"].value
            run_id = kwargs["run_id"]
            calls.append(strategy)
            # A previous result must already be durable before the next job begins.
            if len(calls) > 1:
                saved = self.data_dir / "results.jsonl"
                assert saved.read_text(encoding="utf-8").strip()
            summary = {
                "task_id": "chunk-list",
                "run_id": run_id,
                "strategy": strategy,
                "outcome": "failed",
                "attempts": 2,
                "first_public_passed": False,
                "first_hidden_passed": False,
                "final_public_passed": False,
                "final_hidden_passed": False,
            }
            if strategy == "retry-without-feedback":
                raise RunExecutionError({**summary, "outcome": "error", "status": "model_error"})
            run_dir = self.data_dir / "runs" / "group_c" / run_id
            run_dir.mkdir(parents=True, exist_ok=True)
            for folder, value in (("original_code", 0), ("repair_attempts/02", 1)):
                code = run_dir / folder / "solution.py"
                code.parent.mkdir(parents=True)
                code.write_text(f"def f():\n    return {value}\n", encoding="utf-8")
            (run_dir / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
            return SimpleNamespace(run_dir=run_dir)

    monkeypatch.setattr("repair_assistant.benchmark.RunService", Service)
    options: dict[str, Any] = {
        "schedule": [(1, "retry-without-feedback", task), (1, "test-feedback", task)],
        "model_factory": lambda: ScriptedModel([]),
        "image": "test",
        "data_dir": tmp_path,
        "seed": 42,
        "repetitions": 1,
        "pricing": None,
    }
    directory = run_benchmark(**options)
    assert directory.parent == tmp_path / "experiments"
    rows = [json.loads(line) for line in (directory / "results.jsonl").read_text().splitlines()]
    assert [row["outcome"] for row in rows] == ["error", "failed"]
    assert len(calls) == 2
    assert (directory / "runs/group_c" / f"{directory.name}_002" / "summary.json").is_file()
    output = capsys.readouterr().out
    assert "- L2:     return 0" in output
    assert "+ L2:     return 1" in output
    assert "尚未修复成功" in output
    assert output.count("- L2:     return 0") == 1
    assert output.index("- L2:     return 0") > output.index("终端案例汇总")
    assert "B组" in output and "C组" in output
    run_benchmark(**options, resume=directory)
    assert len(calls) == 2  # Both infrastructure error and ordinary repair failure are skipped.
    assert not (directory / "progress.json").exists()
    assert not (directory / ".benchmark.lock").exists()
    with pytest.raises(ValueError, match="configuration"):
        run_benchmark(**{**options, "seed": 43}, resume=directory)

    # An interruption after saving a run but before appending its batch row must
    # leave that run's evidence intact when the missing job is executed again.
    previous = directory / "runs/group_c" / f"{directory.name}_002" / "summary.json"
    previous_text = previous.read_text(encoding="utf-8")
    (directory / "results.jsonl").write_text(json.dumps(rows[0]) + "\n", encoding="utf-8")
    run_benchmark(**options, resume=directory)
    assert len(calls) == 3
    assert previous.read_text(encoding="utf-8") == previous_text
    assert (directory / "runs/group_c" / f"{directory.name}_003" / "summary.json").is_file()
