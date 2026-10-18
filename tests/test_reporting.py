import json
import xml.etree.ElementTree as ET
from pathlib import Path

from repair_assistant.evaluation import aggregate_summaries
from repair_assistant.reporting import generate_experiment_report


def _run(
    strategy: str,
    task: str,
    repetition: int,
    *,
    first_hidden: bool,
    final_hidden: bool,
    final_public: bool,
    attempts: int,
) -> dict[str, object]:
    return {
        "run_id": f"{strategy}-{task}-{repetition}",
        "strategy": strategy,
        "task_id": task,
        "repetition": repetition,
        "attempts": attempts,
        "outcome": "passed" if final_public and final_hidden else "failed",
        "first_public_passed": first_hidden,
        "final_public_passed": final_public,
        "first_hidden_passed": first_hidden,
        "final_hidden_passed": final_hidden,
        "hidden_improvement": not first_hidden and final_hidden,
        "hidden_regression": first_hidden and not final_hidden,
        "timed_out": False,
        "protected_test_violation": False,
        "workspace_policy_violation": False,
        "cost": {
            "model_calls": attempts,
            "prompt_tokens": attempts * 100,
            "completion_tokens": attempts * 20,
            "total_tokens": attempts * 120,
            "model_latency_ms": attempts * 50,
        },
    }


def test_generate_experiment_report_creates_detailed_artifacts(tmp_path: Path) -> None:
    rows = [
        _run(
            strategy,
            task,
            repetition,
            first_hidden=False,
            final_hidden=(strategy == "test-feedback" or task == "task-a"),
            final_public=True,
            attempts=1 if strategy == "single-shot" else 3,
        )
        for repetition in (1, 2)
        for task in ("task-a", "task-b")
        for strategy in ("single-shot", "retry-without-feedback", "test-feedback")
    ]
    report = aggregate_summaries(rows)
    report["raw_runs"] = rows
    report["design"] = {
        "repair_protocol": "shared-public-test-stopping-v2",
        "repetitions": 2,
        "randomization_seed": 42,
    }

    index = generate_experiment_report(report, tmp_path / "visual-report")

    assert index.is_file()
    assert "反馈主效应" in index.read_text(encoding="utf-8")
    manifest = json.loads((index.parent / "manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["figures"]) == 10
    for relative in manifest["figures"]:
        figure = index.parent / relative
        assert figure.stat().st_size > 500
        assert ET.parse(figure).getroot().tag.endswith("svg")
    assert len((index.parent / "raw-runs.csv").read_text().splitlines()) == len(rows) + 1
    assert "test-feedback" in (index.parent / "strategy-metrics.csv").read_text()
    assert "bootstrap 95% CI" in (index.parent / "report.md").read_text(encoding="utf-8")
