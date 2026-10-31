"""Show changed source lines after a run has finished independent scoring."""

# ruff: noqa: RUF001

from collections.abc import Mapping, Sequence
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from repair_assistant.output_paths import resolve_run_directory
from repair_assistant.redaction import redact

GROUPS = {
    "single-shot": "A组（group A）",
    "retry-without-feedback": "B组（group B）",
    "test-feedback": "C组（group C）",
}
GROUP_DIVIDER = "=" * 64 + "\n" + "=" * 64


def _status(value: object) -> str:
    return "PASS" if value is True else "FAIL" if value is False else "UNKNOWN"


def format_task_progress(row: Mapping[str, Any], previous: Mapping[str, Any] | None = None) -> str:
    prefix = ""
    if previous is not None:
        same_task = (row.get("task_id"), row.get("repetition")) == (
            previous.get("task_id"),
            previous.get("repetition"),
        )
        prefix = "\n" if same_task else "\n\n"
        if row["strategy"] != previous["strategy"]:
            prefix += GROUP_DIVIDER + "\n" + prefix
    strategy = row["strategy"]
    return (
        f"{prefix}{GROUPS[strategy]}\n"
        f"r{row['repetition']:02d} {strategy:24} {row['task_id']:28} {row['outcome']}"
    )


def select_benchmark_cases(
    rows: Sequence[Mapping[str, Any]],
) -> dict[str, dict[str, Mapping[str, Any] | None]]:
    selected: dict[str, dict[str, Mapping[str, Any] | None]] = {}
    for strategy in GROUPS:
        labels = (
            ("一次修复未成功", "一次修复成功")
            if strategy == "single-shot"
            else ("首次未成功，后续修复成功", "首次未成功，后续仍未成功")
        )
        cases: dict[str, Mapping[str, Any] | None] = dict.fromkeys(labels)
        for row in rows:
            if row.get("strategy") != strategy or row.get("outcome") not in {"passed", "failed"}:
                continue
            attempts = row.get("attempts", 0)
            if not isinstance(attempts, int):
                continue
            if strategy == "single-shot":
                if attempts != 1:
                    continue
                label = labels[1] if row["outcome"] == "passed" else labels[0]
            else:
                first_failed = (
                    row.get("first_public_passed") is False
                    or row.get("first_hidden_passed") is False
                )
                if attempts < 2 or not first_failed:
                    continue
                label = labels[0] if row["outcome"] == "passed" else labels[1]
            if cases[label] is None:
                cases[label] = row
        selected[strategy] = cases
    return selected


def format_benchmark_cases(
    directory: Path, rows: Sequence[Mapping[str, Any]], *, secrets: Sequence[str] = ()
) -> str:
    groups = []
    for strategy, cases in select_benchmark_cases(rows).items():
        sections = []
        for label, row in cases.items():
            if row is None:
                sections.append(f"{label}：本次未出现符合条件的案例。")
                continue
            heading = format_task_progress(row)
            first_public = row.get("first_public_passed")
            first_hidden = row.get("first_hidden_passed")
            sections.append(
                f"案例：{label}\n{heading}\n"
                f"首次公开 {_status(first_public)} | 首次隐藏 {_status(first_hidden)} | "
                f"提交次数 {row['attempts']}\n"
                + format_code_changes(
                    resolve_run_directory(directory, strategy, row["run_id"]), row, secrets=secrets
                )
            )
        groups.append(f"{GROUPS[strategy]} | {strategy}\n" + "\n\n\n".join(sections))
    separator = "\n\n" + GROUP_DIVIDER + "\n\n"
    text = "\n\n终端案例汇总（按实际记录顺序选取，每组最多两个）\n\n" + separator.join(groups)
    return str(redact(text, secrets=secrets))


def format_code_changes(
    run_dir: Path, summary: Mapping[str, Any], *, secrets: Sequence[str] = ()
) -> str:
    outcome = summary.get("outcome")
    if outcome not in {"passed", "failed"}:
        return "执行异常：未得到完整评估结果，不将已有代码标记为修复成功。"

    passed = outcome == "passed"
    lines = [
        f"修复结果：{'成功' if passed else '未成功'} | "
        f"公开测试 {_status(summary.get('final_public_passed'))} | "
        f"隐藏测试 {_status(summary.get('final_hidden_passed'))}"
    ]
    attempts = summary.get("attempts")
    final = (
        run_dir / "repair_attempts" / f"{attempts:02d}" / "solution.py"
        if isinstance(attempts, int) and attempts > 0
        else run_dir / "workspace" / "solution.py"
    )
    try:
        before = (
            (run_dir / "original_code" / "solution.py").read_text(encoding="utf-8").splitlines()
        )
        after = final.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return "\n".join([*lines, "代码快照不可读取，无法显示修改行；请查看该任务目录。"])

    removed: list[str] = []
    added: list[str] = []
    for tag, old_start, old_end, new_start, new_end in SequenceMatcher(
        a=before, b=after, autojunk=False
    ).get_opcodes():
        if tag == "equal":
            continue
        removed.extend(f"- L{index + 1}: {before[index]}" for index in range(old_start, old_end))
        added.extend(f"+ L{index + 1}: {after[index]}" for index in range(new_start, new_end))

    if removed or added:
        lines.extend(
            [
                "修改前 solution.py（涉及修改的原始行）：",
                *(removed or ["  无删除行，本次仅新增代码。"]),
                "修复成功后的 solution.py（修改行）："
                if passed
                else "最终候选 solution.py（修改行，尚未修复成功）：",
                *(added or ["  无新增行，本次仅删除代码。"]),
            ]
        )
    else:
        lines.append("solution.py 未发生代码行变化。")
    return str(redact("\n".join(lines), secrets=secrets))
