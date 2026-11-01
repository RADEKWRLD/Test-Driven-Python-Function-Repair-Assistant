import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from repair_assistant.evaluation import aggregate_summaries
from repair_assistant.reporting import generate_experiment_report


def test_course_report_has_four_figures_csv_and_manual_analysis(tmp_path: Path) -> None:
    rows = [
        {
            "run_id": strategy,
            "strategy": strategy,
            "task_id": "t",
            "repetition": 1,
            "outcome": "passed" if strategy == "test-feedback" else "failed",
            "public_pass_by_attempt": [strategy == "test-feedback"],
            "first_hidden_passed": False,
            "final_hidden_passed": strategy == "test-feedback",
            "final_public_passed": True,
            "duration_ms": 1000,
            "hidden_cases": {
                "baseline": {"test_x::test_a": "passed"},
                "first": {"test_x::test_a": "failed"},
                "final": {"test_x::test_a": "passed"},
            },
            "cost": {
                "model_calls": 1,
                "total_tokens": 120,
                "prompt_tokens": 100,
                "completion_tokens": 20,
                "model_latency_ms": 50,
                "currency_cost": 0.001,
                "currency": "CNY",
            },
        }
        for strategy in ("single-shot", "retry-without-feedback", "test-feedback")
    ]
    report = {**aggregate_summaries(rows), "raw_runs": rows}
    output = generate_experiment_report(report, tmp_path / "course-report")
    assert output.name == "report.md"
    text = output.read_text(encoding="utf-8")
    assert "人工填写" in text
    assert "100.0%" in text
    assert "每成功 token" in text
    assert "120.000" in text
    assert "bootstrap" not in text
    assert not (output.parent / "report.html").exists()
    assert not (output.parent / "case-studies.md").exists()
    assert len(list((output.parent / "figures").glob("*.svg"))) == 5
    for image in (output.parent / "figures").glob("*.svg"):
        assert ET.parse(image).getroot().tag.endswith("svg")
    with (output.parent / "test-results.csv").open(encoding="utf-8") as stream:
        tests = list(csv.DictReader(stream))
    assert len(tests) == 3
    assert tests[0]["test_function"] == "test_x::test_a"
    assert (output.parent / "raw-runs.csv").is_file()
    assert (output.parent / "strategy-metrics.csv").is_file()
    history_lines = (
        (output.parent / "feedbackeval-repair-histories.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    assert len(history_lines) == 3
    assert json.loads(history_lines[0])["repair_results"][0]["repair_history"] == []
    assert json.loads((output.parent / "report.json").read_text())["valid_runs"] == 3


def test_infrastructure_errors_are_visible_and_not_fake_repair_failures(tmp_path: Path) -> None:
    rows = [
        {
            "strategy": "test-feedback",
            "outcome": "error",
            "run_id": "bad",
            "task_id": "t",
            "status": "model_error",
            "cost": {"currency_cost": None},
        }
    ]
    report = {**aggregate_summaries(rows), "raw_runs": rows}
    metrics = report["strategies"]["test-feedback"]
    assert report["valid_runs"] == 0
    assert metrics["infrastructure_errors"] == 1
    assert metrics["final_hidden_pass_rate"] is None
    output = generate_experiment_report(report, tmp_path / "errors-only")
    assert "N/A" in output.read_text(encoding="utf-8")
