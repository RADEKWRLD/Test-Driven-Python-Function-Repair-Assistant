"""Evidence-only Markdown case studies from completed experiment artifacts."""

# ruff: noqa: RUF001

from __future__ import annotations

import difflib
import html
import json
import os
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from urllib.parse import quote

from repair_assistant.output_paths import resolve_run_directory
from repair_assistant.redaction import redact

STRATEGIES = ("retry-without-feedback", "test-feedback")


def _eligible(row: Mapping[str, Any]) -> bool:
    attempts = row.get("attempts")
    if (
        row.get("outcome") != "failed"
        or row.get("strategy") not in STRATEGIES
        or not isinstance(attempts, int)
        or isinstance(attempts, bool)
        or attempts < 2
        or row.get("first_public_passed") is not False
        or row.get("final_public_passed") is not True
        or row.get("final_hidden_passed") is not False
    ):
        return False
    if (
        any(
            row.get(key)
            for key in (
                "timed_out",
                "protected_test_violation",
                "workspace_policy_violation",
                "infrastructure_error",
                "infrastructure_errors",
                "error_type",
            )
        )
        or "error" in str(row.get("status", "")).lower()
    ):
        return False
    hidden = row.get("hidden_cases")
    final = hidden.get("final") if isinstance(hidden, Mapping) else None
    if isinstance(final, Mapping) and final:
        states = {str(value).lower() for value in final.values()}
        if "failed" not in states:
            return False
    return True


def select_public_hidden_failure_cases(
    rows: Sequence[Mapping[str, Any]],
) -> dict[str, Mapping[str, Any] | None]:
    """Select each repair arm's first eligible row in recorded input order."""
    selected: dict[str, Mapping[str, Any] | None] = dict.fromkeys(STRATEGIES)
    for row in rows:
        if _eligible(row):
            strategy = str(row["strategy"])
            if selected[strategy] is None:
                selected[strategy] = row
    return selected


def _plain(value: Any) -> str:
    text = html.escape(str(redact(str(value))), quote=True).replace("\n", " ").replace("\r", " ")
    return re.sub(r"([\\`*_\[\]{}()|#])", r"\\\1", text)


def _fenced(text: str, language: str = "text") -> list[str]:
    text = str(redact(text))
    longest = max((len(match.group()) for match in re.finditer(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return [f"{fence}{language}", text.rstrip("\n"), fence, ""]


def _link(label: str, path: Path, report_dir: Path) -> str:
    relative = os.path.relpath(path.resolve(), report_dir.resolve())
    return f"[{label}](<{quote(relative, safe='/._-')}>)"


def _read_text(path: Path) -> tuple[str | None, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except (OSError, UnicodeError) as exc:
        return None, f"不可用（{type(exc).__name__}）"


def read_run_events(run_dir: Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Read valid persisted events, retaining warnings for missing/corrupt evidence."""
    content, error = _read_text(run_dir / "events.jsonl")
    if content is None:
        return [], [f"事件日志{error}；不能据此补造反馈或执行结果。"]
    events: list[dict[str, Any]] = []
    issues = []
    for number, line in enumerate(content.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
            if (
                not isinstance(event, dict)
                or not isinstance(event.get("type"), str)
                or not isinstance(event.get("payload"), dict)
            ):
                raise ValueError("invalid event shape")
        except (ValueError, TypeError):
            issues.append(f"事件日志第 {number} 行损坏，已跳过；该行证据不可用。")
        else:
            events.append(event)
    return events, issues


def _event_evidence(
    events: Sequence[Mapping[str, Any]],
    attempts: int,
) -> tuple[dict[int, Mapping[str, Any]], dict[int, list[str]], Mapping[str, Any] | None]:
    public: dict[int, Mapping[str, Any]] = {}
    fallback: dict[int, Mapping[str, Any]] = {}
    feedback: dict[int, list[str]] = {}
    hidden = None
    for event in events:
        payload = event["payload"]
        kind = event["type"]
        attempt = payload.get("attempt")
        valid_attempt = isinstance(attempt, int) and not isinstance(attempt, bool)
        if kind == "shared_first_inherited":
            verification = payload.get("public_verification")
            if isinstance(verification, Mapping):
                public[1] = verification
        elif kind == "repair_public_verification" and valid_attempt:
            public[attempt] = payload
        elif kind == "public_verification":
            if payload.get("stage") == "first":
                fallback[1] = payload
            elif payload.get("stage") == "final":
                fallback[attempts] = payload
        elif kind == "feedback_added" and valid_attempt:
            content = payload.get("content")
            if isinstance(content, str):
                feedback.setdefault(attempt, []).append(content)
        elif kind == "hidden_verification" and payload.get("stage") == "final":
            hidden = payload
    for number, verification in fallback.items():
        public.setdefault(number, verification)
    return public, feedback, hidden


def _status(value: Any) -> str:
    return "PASS" if value is True else "FAIL" if value is False else "不可用"


def _verification_lines(verification: Mapping[str, Any] | None) -> list[str]:
    if verification is None:
        return ["执行证据不可用：未找到对应的测试事件。", ""]
    command = verification.get("command_result")
    if not isinstance(command, Mapping):
        return ["执行证据不可用：测试事件缺少有效的 command_result。", ""]
    lines = [
        f"日志结果：{_status(verification.get('passed'))}；"
        f"退出码：{_plain(command.get('exit_code', '不可用'))}；"
        f"超时：{_plain(command.get('timed_out', '不可用'))}。",
        "",
    ]
    for stream in ("stdout", "stderr"):
        lines.extend([f"{stream}：", ""])
        value = command.get(stream)
        if isinstance(value, str):
            lines.extend(_fenced(value if value else "（空）"))
        else:
            lines.extend(["不可用：日志未记录此输出。", ""])
    return lines


def _case_lines(
    row: Mapping[str, Any],
    strategy: str,
    experiment_dir: Path,
    report_dir: Path,
) -> list[str]:
    attempts = row["attempts"]
    run_id = str(row.get("run_id", ""))
    run_dir = resolve_run_directory(experiment_dir, strategy, run_id)
    # Invalid IDs must not redirect report reading outside the experiment's runs.
    if not run_id or not run_dir.resolve().is_relative_to((experiment_dir / "runs").resolve()):
        return ["运行目录不可用：run_id 缺失或越过实验 runs 目录。", ""]
    event_path = run_dir / "events.jsonl"
    events, issues = read_run_events(run_dir)
    public, feedback, final_hidden = _event_evidence(events, attempts)
    lines = [
        f"任务：{_plain(row.get('task_id', '不可用'))}；运行：{_plain(run_id)}；"
        f"重复：{_plain(row.get('repetition', '不可用'))}；提交次数：{attempts}。",
        "",
        _link("事件日志", event_path, report_dir),
        "",
        *issues,
        "",
        "| 提交 | 公开测试 | 隐藏测试（离线评分） |",
        "| --- | --- | --- |",
    ]
    by_attempt = row.get("public_pass_by_attempt")
    for number in range(1, attempts + 1):
        if number == 1:
            public_value, hidden_value = (
                row.get("first_public_passed"),
                row.get("first_hidden_passed"),
            )
        elif number == attempts:
            public_value, hidden_value = (
                row.get("final_public_passed"),
                row.get("final_hidden_passed"),
            )
        else:
            public_value = public.get(number, {}).get("passed")
            if isinstance(by_attempt, list) and len(by_attempt) >= number:
                public_value = by_attempt[number - 1]
            hidden_value = None
        hidden_status = _status(hidden_value) if number in (1, attempts) else "未评分"
        lines.append(f"| {number} | {_status(public_value)} | {hidden_status} |")
    lines.extend(["", "首轮与最终隐藏结果均为离线评分；隐藏诊断不提供给修复模型。", ""])
    original_path = run_dir / "original_code" / "solution.py"
    previous, error = _read_text(original_path)
    previous_name = "original_code/solution.py"
    lines.extend(["#### 修改前原始代码", "", _link("原始代码", original_path, report_dir), ""])
    if previous is None:
        lines.extend([f"原始代码{error}。", ""])
    else:
        lines.extend(_fenced(previous, "python"))
    for number in range(1, attempts + 1):
        snapshot = run_dir / "repair_attempts" / f"{number:02d}" / "solution.py"
        current, error = _read_text(snapshot)
        current_name = f"repair_attempts/{number:02d}/solution.py"
        lines.extend(
            [
                f"#### 第 {number} 次提交",
                "",
                _link("代码快照", snapshot, report_dir),
                "",
                "相对原始代码的修改：" if number == 1 else "相对上次提交的修改：",
                "",
            ]
        )
        if previous is None or current is None:
            reason = error if current is None else "不可用（上一份代码快照缺失）"
            lines.extend([f"差异{reason}；不从其他提交推测缺失代码。", ""])
        else:
            delta = "\n".join(
                difflib.unified_diff(
                    previous.splitlines(),
                    current.splitlines(),
                    fromfile=previous_name,
                    tofile=current_name,
                    lineterm="",
                )
            )
            lines.extend(_fenced(delta, "diff") if delta else ["与上一份代码相同（未修改）。", ""])
        previous, previous_name = current, current_name
        lines.extend(["控制器记录的公开测试诊断：", ""])
        lines.extend(_verification_lines(public.get(number)))
        if strategy == STRATEGIES[0]:
            lines.extend(["B 组：上述具体诊断仅供控制器判停及报告使用，不作为模型的测试反馈。", ""])
            if feedback.get(number):
                lines.extend(["日志存在异常 feedback_added 记录，应核查 B 组协议执行。", ""])
        elif number < attempts:
            contents = feedback.get(number)
            if contents:
                lines.extend(
                    [f"实际加入第 {number + 1} 次模型请求的公开反馈（feedback_added）：", ""]
                )
                for content in contents:
                    lines.extend(_fenced(content))
            else:
                lines.extend(
                    ["模型反馈证据不可用：未找到 feedback_added 记录，不能确认实际传入的反馈。", ""]
                )
        else:
            lines.extend(["这是最后一次提交，不再进行下一次修复。", ""])
    lines.extend(["#### 最终隐藏评分证据", ""])
    final_cases = final_hidden.get("cases") if final_hidden is not None else None
    if not isinstance(final_cases, Mapping):
        hidden_cases = row.get("hidden_cases")
        final_cases = hidden_cases.get("final") if isinstance(hidden_cases, Mapping) else None
    failures = (
        [str(name) for name, state in final_cases.items() if state == "failed"]
        if isinstance(final_cases, Mapping)
        else []
    )
    lines.extend(["失败测试名：", ""])
    lines.extend(
        _fenced("\n".join(failures)) if failures else ["不可用：未记录可确认的失败测试名。", ""]
    )
    lines.extend(_verification_lines(final_hidden))
    lines.extend(
        [
            "按汇总记录，追加修复后公开测试通过，但最终隐藏测试仍失败。"
            "这表明已满足所测公开约束，尚不能按当前评分认定完整修复。"
            "该现象本身不能证明过拟合；具体原因还需核对需求与隐藏测试期望是否一致。",
            "",
        ]
    )
    return lines


def render_public_hidden_failure_cases(
    rows: Sequence[Mapping[str, Any]],
    experiment_dir: Path,
    *,
    report_dir: Path | None = None,
) -> list[str]:
    """Render selected cases using only persisted logs and solution snapshots."""
    report_dir = experiment_dir if report_dir is None else report_dir
    lines = [
        "## 错误分析（自动选例）",
        "",
        "按实际记录顺序，分别选择 B、C 组首个：首轮公开失败、提交至少两次、"
        "最终公开通过且隐藏失败的运行。排除基础设施错误、超时及测试保护或工作区违规；"
        "仅有执行错误而无失败用例的隐藏记录不作为断言失败案例。",
        "",
        "以下内容直接提取已保存的代码与日志，不额外调用模型；"
        "缺失的实际值、期望值或失败原因不作推测。隐藏诊断仅用于本报告，不回流修复过程。",
        "",
    ]
    selected = select_public_hidden_failure_cases(rows)
    for label, strategy in zip(("B", "C"), STRATEGIES, strict=True):
        lines.extend([f"### {label} 组：{strategy}", ""])
        row = selected[strategy]
        if row is None:
            lines.extend(["本组没有符合条件的案例；不以首轮公开已通过或其他运行替代。", ""])
        else:
            lines.extend(_case_lines(row, strategy, experiment_dir, report_dir))
    return lines
