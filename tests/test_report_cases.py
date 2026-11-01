# ruff: noqa: RUF001

import json
from pathlib import Path
from typing import Any

import pytest

from repair_assistant.report_cases import (
    render_public_hidden_failure_cases,
    select_public_hidden_failure_cases,
)

B = "retry-without-feedback"
C = "test-feedback"


def _row(strategy: str = B, run_id: str = "run-1", **overrides: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "strategy": strategy,
        "run_id": run_id,
        "task_id": "same-task",
        "repetition": 2,
        "outcome": "failed",
        "attempts": 3,
        "first_public_passed": False,
        "final_public_passed": True,
        "first_hidden_passed": False,
        "final_hidden_passed": False,
        "public_pass_by_attempt": [False, False, True],
        "hidden_cases": {"final": {"test_hidden.py::test_generalization": "failed"}},
    }
    row.update(overrides)
    return row


def _verification(passed: bool, stdout: str, stderr: str = "") -> dict[str, Any]:
    return {
        "passed": passed,
        "cases": {"test_hidden.py::test_generalization": "passed" if passed else "failed"},
        "command_result": {
            "exit_code": 0 if passed else 1,
            "timed_out": False,
            "stdout": stdout,
            "stderr": stderr,
        },
    }


def _event(kind: str, **payload: Any) -> dict[str, Any]:
    return {"type": kind, "payload": payload}


def _artifacts(
    root: Path,
    row: dict[str, Any],
    *,
    grouped: bool = True,
    corrupt: bool = False,
) -> Path:
    group = "group_b" if row["strategy"] == B else "group_c"
    run_id = str(row["run_id"])
    directory = root / "runs" / group / run_id if grouped else root / "runs" / run_id
    original = directory / "original_code" / "solution.py"
    original.parent.mkdir(parents=True)
    original.write_text("def example():\n    return 0\n", encoding="utf-8")
    for number in range(1, row["attempts"] + 1):
        snapshot = directory / "repair_attempts" / f"{number:02d}" / "solution.py"
        snapshot.parent.mkdir(parents=True)
        snapshot.write_text(f"def example():\n    return {number}\n", encoding="utf-8")
    events = [
        _event(
            "shared_first_inherited",
            public_verification=_verification(False, "shared first failure"),
        ),
    ]
    for number in range(1, row["attempts"] + 1):
        if number > 1:
            events.append(
                _event(
                    "repair_public_verification",
                    attempt=number,
                    **_verification(number == row["attempts"], f"public attempt {number}"),
                )
            )
        if row["strategy"] == C and number < row["attempts"]:
            events.append(
                _event("feedback_added", attempt=number, content=f"actual feedback {number}")
            )
    events.append(
        _event(
            "hidden_verification",
            stage="final",
            **_verification(False, "hidden-assertion-payload", "hidden stderr"),
        )
    )
    lines = [json.dumps(event) for event in events]
    if corrupt:
        lines.insert(1, "not a json event")
        lines.insert(2, json.dumps({"type": "broken", "payload": []}))
    (directory / "events.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return directory


def test_selection_keeps_actual_input_order_and_same_task_in_both_arms() -> None:
    c = _row(C, "z-first-c")
    b = _row(B, "z-first-b")
    rows = [c, b, _row(B, "a-later-b"), _row(C, "a-later-c")]
    selected = select_public_hidden_failure_cases(rows)
    assert list(selected) == [B, C]
    assert selected[B] is b
    assert selected[C] is c
    assert b["task_id"] == c["task_id"]


@pytest.mark.parametrize(
    "overrides",
    [
        {"strategy": "single-shot"},
        {"attempts": True},
        {"attempts": "3"},
        {"attempts": 1},
        {"attempts": 2.5},
        {"first_public_passed": True},
        {"first_public_passed": 0},
        {"final_public_passed": False},
        {"final_hidden_passed": True},
        {"outcome": "error"},
        {"outcome": "passed"},
        {"status": "model_error"},
        {"timed_out": True},
        {"protected_test_violation": True},
        {"workspace_policy_violation": True},
        {"infrastructure_error": True},
        {"error_type": "TimeoutError"},
        {"hidden_cases": {"final": {"t": "error"}}},
        {"hidden_cases": {"final": {"t": "timeout", "u": "not_run"}}},
        {"hidden_cases": {"final": {"t": "passed", "u": "error"}}},
        {"hidden_cases": {"final": {"t": "passed"}}},
    ],
)
def test_selection_excludes_ineligible_runs(overrides: dict[str, Any]) -> None:
    assert select_public_hidden_failure_cases([_row(**overrides)]) == {B: None, C: None}


def test_selection_can_use_known_assertion_failure_even_with_additional_case_error() -> None:
    row = _row(hidden_cases={"final": {"t": "failed", "u": "error"}})
    assert select_public_hidden_failure_cases([row])[B] is row


def test_no_matching_case_does_not_substitute_a_first_attempt_pass(tmp_path: Path) -> None:
    row = _row(first_public_passed=True)
    result = "\n".join(render_public_hidden_failure_cases([row], tmp_path))
    assert result.startswith("## 错误分析（自动选例）")
    assert result.count("本组没有符合条件的案例") == 2
    assert "第 1 次提交" not in result


def test_full_trace_has_original_to_first_and_all_successive_diffs(tmp_path: Path) -> None:
    row = _row(C)
    _artifacts(tmp_path, row)
    result = "\n".join(render_public_hidden_failure_cases([row], tmp_path))
    assert "def example():\n    return 0" in result
    assert "--- original_code/solution.py" in result
    assert "+++ repair_attempts/01/solution.py" in result
    assert "--- repair_attempts/01/solution.py" in result
    assert "+++ repair_attempts/02/solution.py" in result
    assert "--- repair_attempts/02/solution.py" in result
    assert "+++ repair_attempts/03/solution.py" in result
    assert "-    return 0\n+    return 1" in result
    assert "| 1 | FAIL | FAIL |" in result
    assert "| 2 | FAIL | 未评分 |" in result
    assert "| 3 | PASS | FAIL |" in result
    assert "| 2 | FAIL | PASS |" not in result
    assert "shared first failure" in result
    assert "public attempt 2" in result
    assert "public attempt 3" in result
    assert "actual feedback 1" in result
    assert "actual feedback 2" in result
    assert "hidden-assertion-payload" in result
    assert "hidden stderr" in result
    assert "test_hidden.py::test_generalization" in result


def test_b_diagnostics_are_controller_only_while_c_shows_recorded_feedback(tmp_path: Path) -> None:
    b = _row(B, "b")
    c = _row(C, "c")
    _artifacts(tmp_path, b)
    _artifacts(tmp_path, c)
    result = "\n".join(render_public_hidden_failure_cases([b, c], tmp_path))
    b_section, c_section = result.split("### C 组：", 1)
    assert "上述具体诊断仅供控制器判停及报告使用" in b_section
    assert "actual feedback" not in b_section
    assert "实际加入第 2 次模型请求的公开反馈" in c_section
    assert "actual feedback 1" in c_section
    assert "隐藏诊断不提供给修复模型" in b_section
    assert "隐藏诊断不提供给修复模型" in c_section


def test_custom_report_directory_links_back_to_actual_evidence(tmp_path: Path) -> None:
    experiment = tmp_path / "experiment data"
    report_dir = tmp_path / "export" / "report"
    row = _row(B)
    _artifacts(experiment, row)
    result = "\n".join(render_public_hidden_failure_cases([row], experiment, report_dir=report_dir))
    assert "../../experiment%20data/runs/group_b/run-1/events.jsonl" in result
    assert "../../experiment%20data/runs/group_b/run-1/original_code/solution.py" in result
    assert "../../experiment%20data/runs/group_b/run-1/repair_attempts/03/solution.py" in result


def test_legacy_flat_run_directory_is_resolved(tmp_path: Path) -> None:
    row = _row(B)
    _artifacts(tmp_path, row, grouped=False)
    result = "\n".join(render_public_hidden_failure_cases([row], tmp_path))
    assert "runs/run-1/events.jsonl" in result
    assert "shared first failure" in result
    assert "group_b" not in result


def test_missing_evidence_is_reported_without_skipping_selected_case(tmp_path: Path) -> None:
    first = _row(C, "missing")
    later = _row(C, "complete")
    _artifacts(tmp_path, later)
    result = "\n".join(render_public_hidden_failure_cases([first, later], tmp_path))
    assert "运行：missing" in result
    assert "运行：complete" not in result
    assert "事件日志不可用" in result
    assert "原始代码不可用" in result
    assert "差异不可用" in result
    assert "模型反馈证据不可用" in result
    assert "未找到对应的测试事件" in result
    assert "hidden-assertion-payload" not in result


def test_corrupt_event_lines_do_not_hide_remaining_valid_evidence(tmp_path: Path) -> None:
    row = _row(C)
    _artifacts(tmp_path, row, corrupt=True)
    result = "\n".join(render_public_hidden_failure_cases([row], tmp_path))
    assert "事件日志第 2 行损坏" in result
    assert "事件日志第 3 行损坏" in result
    assert "shared first failure" in result
    assert "actual feedback 1" in result
    assert "hidden-assertion-payload" in result


def test_missing_middle_snapshot_never_splices_nonconsecutive_diffs(tmp_path: Path) -> None:
    row = _row(B)
    directory = _artifacts(tmp_path, row)
    (directory / "repair_attempts" / "02" / "solution.py").unlink()
    result = "\n".join(render_public_hidden_failure_cases([row], tmp_path))
    assert result.count("差异不可用") == 2
    assert "+    return 3" not in result
    assert "public attempt 3" in result


def test_public_first_final_verification_is_used_as_fallback(tmp_path: Path) -> None:
    row = _row(C, attempts=2, public_pass_by_attempt=[False, True])
    directory = _artifacts(tmp_path, row)
    events = [
        _event("public_verification", stage="first", **_verification(False, "fallback-first")),
        _event("public_verification", stage="final", **_verification(True, "fallback-final")),
    ]
    (directory / "events.jsonl").write_text("\n".join(map(json.dumps, events)), encoding="utf-8")
    result = "\n".join(render_public_hidden_failure_cases([row], tmp_path))
    assert "fallback-first" in result
    assert "fallback-final" in result
    assert "模型反馈证据不可用" in result
    assert "最终隐藏评分证据" in result
    assert "test_hidden.py::test_generalization" in result
    assert "执行证据不可用" in result


def test_unreadable_utf8_snapshot_and_malformed_command_are_explicit(tmp_path: Path) -> None:
    row = _row(C)
    directory = _artifacts(tmp_path, row)
    (directory / "original_code" / "solution.py").write_bytes(b"\xff")
    (directory / "events.jsonl").write_text(
        json.dumps(_event("repair_public_verification", attempt=2, command_result="malformed")),
        encoding="utf-8",
    )
    result = "\n".join(render_public_hidden_failure_cases([row], tmp_path))
    assert "UnicodeDecodeError" in result
    assert "缺少有效的 command_result" in result


def test_identifiers_are_html_escaped_and_fences_and_bearers_are_safe(tmp_path: Path) -> None:
    row = _row(C, task_id="<script>alert(1)</script>")
    directory = _artifacts(tmp_path, row)
    events = [
        _event(
            "feedback_added",
            attempt=1,
            content=(
                "before\n`````\n<script>code-like text</script>\nBearer abc.secret-token\nafter"
            ),
        )
    ]
    (directory / "events.jsonl").write_text("\n".join(map(json.dumps, events)), encoding="utf-8")
    result = "\n".join(render_public_hidden_failure_cases([row], tmp_path))
    assert "&lt;script&gt;alert" in result
    assert "任务：<script>" not in result
    assert "``````text\nbefore\n`````" in result
    assert "Bearer [REDACTED]" in result
    assert "abc.secret-token" not in result


def test_run_id_cannot_read_outside_experiment_runs(tmp_path: Path) -> None:
    result = "\n".join(render_public_hidden_failure_cases([_row(run_id="../../outside")], tmp_path))
    assert "运行目录不可用" in result
    assert "代码快照" not in result
