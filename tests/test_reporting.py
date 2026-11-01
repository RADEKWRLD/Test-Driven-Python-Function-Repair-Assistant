# ruff: noqa: RUF001

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from repair_assistant.evaluation import aggregate_summaries
from repair_assistant.reporting import generate_experiment_report


def test_course_report_has_six_figures_csv_and_automatic_analysis(tmp_path: Path) -> None:
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
    assert "错误分析（自动选例）" in text
    assert "人工填写" not in text
    assert "### B 组：retry-without-feedback" in text
    assert "### C 组：test-feedback" in text
    assert text.count("本组没有符合条件的案例") == 2
    assert "100.0%" in text
    assert "每成功 token" in text
    assert "120.000" in text
    assert "bootstrap" not in text
    assert not (output.parent / "report.html").exists()
    assert not (output.parent / "case-studies.md").exists()
    assert len(list((output.parent / "figures").glob("*.svg"))) == 6
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


def _case_row(strategy: str, run_id: str, **overrides: Any) -> dict[str, Any]:
    return {
        "strategy": strategy,
        "run_id": run_id,
        "task_id": f"task-{run_id}",
        "repetition": 1,
        "outcome": "failed",
        "attempts": 2,
        "first_public_passed": False,
        "final_public_passed": True,
        "first_hidden_passed": False,
        "final_hidden_passed": False,
        "public_pass_by_attempt": [False, True],
        "hidden_cases": {"final": {"test_hidden.py::test_boundary": "failed"}},
        **overrides,
    }


def _write_case_artifacts(root: Path, row: dict[str, Any]) -> None:
    run_id = str(row["run_id"])
    group = "group_b" if row["strategy"] == "retry-without-feedback" else "group_c"
    directory = root / "runs" / group / run_id
    original = directory / "original_code" / "solution.py"
    original.parent.mkdir(parents=True)
    original.write_text(f"def example():\n    return 'original-{run_id}'\n", encoding="utf-8")

    def verification(passed: bool, diagnostic: str) -> dict[str, Any]:
        return {
            "passed": passed,
            "cases": {"test_hidden.py::test_boundary": "passed" if passed else "failed"},
            "command_result": {
                "exit_code": 0 if passed else 1,
                "timed_out": False,
                "stdout": diagnostic,
                "stderr": "",
            },
        }

    events: list[dict[str, Any]] = [
        {
            "type": "shared_first_inherited",
            "payload": {
                "attempt": 1,
                "public_verification": verification(
                    bool(row["first_public_passed"]), f"PUBLIC-FIRST:{run_id}"
                ),
            },
        }
    ]
    attempts = int(row["attempts"])
    for number in range(1, attempts + 1):
        snapshot = directory / "repair_attempts" / f"{number:02d}" / "solution.py"
        snapshot.parent.mkdir(parents=True)
        snapshot.write_text(
            f"def example():\n    return 'candidate-{run_id}-{number}'\n", encoding="utf-8"
        )
        if number > 1:
            events.append(
                {
                    "type": "repair_public_verification",
                    "payload": {
                        "attempt": number,
                        **verification(
                            number == attempts and bool(row["final_public_passed"]),
                            f"PUBLIC-{number}:{run_id}",
                        ),
                    },
                }
            )
        if number < attempts and row["strategy"] == "test-feedback":
            events.append(
                {
                    "type": "feedback_added",
                    "payload": {"attempt": number, "content": f"FEEDBACK-{number}:{run_id}"},
                }
            )
    for stage in ("first", "final"):
        events.append(
            {
                "type": "hidden_verification",
                "payload": {
                    "stage": stage,
                    **verification(False, f"HIDDEN-{stage.upper()}:{run_id}"),
                },
            }
        )
    (directory / "events.jsonl").write_text(
        "\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8"
    )


def test_report_automatically_embeds_first_eligible_bc_evidence_from_source_dir(
    tmp_path: Path,
) -> None:
    b = "retry-without-feedback"
    c = "test-feedback"
    excluded = [
        _case_row(
            b,
            "excluded-initial",
            attempts=1,
            first_public_passed=True,
            public_pass_by_attempt=[True],
        ),
        _case_row(c, "excluded-infra", outcome="error", status="model_error"),
        _case_row(
            b, "excluded-public", final_public_passed=False, public_pass_by_attempt=[False, False]
        ),
    ]
    selected = [_case_row(c, "z-first-c"), _case_row(b, "z-first-b")]
    later = [_case_row(b, "a-later-b"), _case_row(c, "a-later-c")]
    rows = [*excluded, *selected, *later]
    source_dir = tmp_path / "experiment data"
    for row in rows:
        _write_case_artifacts(source_dir, row)

    report = {**aggregate_summaries(rows), "raw_runs": rows}
    output = generate_experiment_report(
        report, tmp_path / "export" / "report", source_dir=source_dir
    )
    text = output.read_text(encoding="utf-8")
    assert "错误分析（自动选例）" in text
    assert "人工填写" not in text
    assert "本组没有符合条件的案例" not in text
    for strategy, run_id, group in ((b, "z-first-b", "group_b"), (c, "z-first-c", "group_c")):
        assert strategy in text
        assert f"任务：task-{run_id}；运行：{run_id}" in text
        assert f"-    return 'original-{run_id}'\n+    return 'candidate-{run_id}-1'" in text
        assert f"-    return 'candidate-{run_id}-1'\n+    return 'candidate-{run_id}-2'" in text
        assert f"PUBLIC-FIRST:{run_id}" in text
        assert f"PUBLIC-2:{run_id}" in text
        assert f"HIDDEN-FINAL:{run_id}" in text
        assert f"HIDDEN-FIRST:{run_id}" not in text
        prefix = f"../../experiment%20data/runs/{group}/{run_id}"
        assert f"{prefix}/events.jsonl" in text
        assert f"{prefix}/repair_attempts/02/solution.py" in text
    assert "test_hidden.py::test_boundary" in text
    assert text.count("| 1 | FAIL | FAIL |") == 2
    assert text.count("| 2 | PASS | FAIL |") == 2
    assert "FEEDBACK-1:z-first-c" in text
    for row in [*excluded, *later]:
        assert str(row["run_id"]) not in text


def test_report_keeps_case_when_some_log_evidence_is_missing_or_malformed(tmp_path: Path) -> None:
    row = _case_row("test-feedback", "damaged")
    _write_case_artifacts(tmp_path, row)
    directory = tmp_path / "runs/group_c/damaged"
    events = directory / "events.jsonl"
    with events.open("a", encoding="utf-8") as stream:
        stream.write("not-json\n")
        for kind in ("feedback_added", "attempt_completed", "shared_first_inherited"):
            stream.write(json.dumps({"type": kind, "payload": {}}) + "\n")
    (directory / "original_code/solution.py").write_bytes(b"\xff")
    output = generate_experiment_report({"raw_runs": [row]}, tmp_path)
    text = output.read_text(encoding="utf-8")
    assert "运行：damaged" in text
    assert "损坏，已跳过" in text
    assert "原始代码不可用" in text
    assert "HIDDEN-FINAL:damaged" in text
