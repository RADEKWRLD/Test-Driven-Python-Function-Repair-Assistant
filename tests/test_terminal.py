from pathlib import Path
from typing import Any

from repair_assistant.terminal import (
    GROUP_DIVIDER,
    format_benchmark_cases,
    format_code_changes,
    format_task_progress,
    select_benchmark_cases,
)


def test_terminal_shows_numbered_original_and_successful_snapshot_lines(tmp_path: Path) -> None:
    original = tmp_path / "original_code/solution.py"
    original.parent.mkdir()
    original.write_text("def f():\n    return 0\n", encoding="utf-8")
    final = tmp_path / "repair_attempts/02/solution.py"
    final.parent.mkdir(parents=True)
    final.write_text("def f():\n    # private-value\n    return 1\n", encoding="utf-8")
    # The saved final attempt, rather than a later change to the workspace, is shown.
    workspace = tmp_path / "workspace/solution.py"
    workspace.parent.mkdir()
    workspace.write_text("incorrect workspace text", encoding="utf-8")

    text = format_code_changes(
        tmp_path,
        {
            "outcome": "passed",
            "attempts": 2,
            "final_public_passed": True,
            "final_hidden_passed": True,
        },
        secrets=("private-value",),
    )
    assert "公开测试 PASS | 隐藏测试 PASS" in text
    assert "- L2:     return 0" in text
    assert "+ L3:     return 1" in text
    assert "private-value" not in text
    assert "incorrect workspace text" not in text
    assert "修复成功后的" in text


def test_public_pass_hidden_failure_is_not_called_a_success(tmp_path: Path) -> None:
    for directory, code in (("original_code", "return 0"), ("workspace", "return 1")):
        path = tmp_path / directory / "solution.py"
        path.parent.mkdir()
        path.write_text(f"def f():\n    {code}\n", encoding="utf-8")
    text = format_code_changes(
        tmp_path,
        {"outcome": "failed", "final_public_passed": True, "final_hidden_passed": False},
    )
    assert "修复结果：未成功" in text  # noqa: RUF001
    assert "隐藏测试 FAIL" in text
    assert "尚未修复成功" in text
    assert "修复成功后的" not in text
    assert "- L2:     return 0" in text
    assert "+ L2:     return 1" in text


def test_missing_snapshots_and_execution_errors_do_not_break_output(tmp_path: Path) -> None:
    assert "快照不可读取" in format_code_changes(tmp_path, {"outcome": "failed"})
    assert "执行异常" in format_code_changes(tmp_path, {"outcome": "error"})


def test_case_selection_uses_first_matching_run_and_excludes_first_passes_and_errors() -> None:
    def row(strategy: str, name: str, attempts: int, first: bool, outcome: str) -> dict[str, Any]:
        return {
            "strategy": strategy,
            "task_id": name,
            "run_id": name,
            "repetition": 1,
            "attempts": attempts,
            "first_public_passed": first,
            "first_hidden_passed": first,
            "outcome": outcome,
        }

    rows = [
        row("single-shot", "a-error", 1, False, "error"),
        row("single-shot", "a-fail", 1, False, "failed"),
        row("single-shot", "a-pass", 1, True, "passed"),
    ]
    for strategy, prefix in (("retry-without-feedback", "b"), ("test-feedback", "c")):
        rows.extend(
            [
                row(strategy, f"{prefix}-first-pass", 1, True, "passed"),
                row(strategy, f"{prefix}-no-retry", 1, False, "failed"),
                row(strategy, f"{prefix}-error", 2, False, "error"),
                row(strategy, f"{prefix}-repaired", 2, False, "passed"),
                row(strategy, f"{prefix}-failed", 3, False, "failed"),
                row(strategy, f"{prefix}-later-repaired", 3, False, "passed"),
            ]
        )
    selected = select_benchmark_cases(rows)
    assert [
        [case["task_id"] if case is not None else None for case in group.values()]
        for group in selected.values()
    ] == [["a-fail", "a-pass"], ["b-repaired", "b-failed"], ["c-repaired", "c-failed"]]


def test_missing_cases_are_explicit_and_groups_have_two_divider_lines(tmp_path: Path) -> None:
    text = format_benchmark_cases(tmp_path, [])
    assert text.count("本次未出现符合条件的案例") == 6
    assert text.count(GROUP_DIVIDER) == 2
    assert text.index("group A") < text.index("group B") < text.index("group C")


def test_progress_spacing_and_group_name_for_each_task() -> None:
    previous = {"strategy": "single-shot", "task_id": "same", "repetition": 1, "outcome": "passed"}
    same_stage = format_task_progress(previous, previous)
    assert same_stage.startswith("\nA组")
    different_task = format_task_progress({**previous, "task_id": "other"}, previous)
    assert different_task.startswith("\n\nA组")
    different_group = format_task_progress({**previous, "strategy": "test-feedback"}, previous)
    assert different_group.startswith("\n" + GROUP_DIVIDER + "\n\nC组")
