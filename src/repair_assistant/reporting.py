"""Course report: raw CSV, one Markdown document and four small SVG figures."""

# ruff: noqa: RUF001

from __future__ import annotations

import csv
import html
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from repair_assistant.evaluation import aggregate_summaries

STRATEGIES = ("single-shot", "retry-without-feedback", "test-feedback")
LABELS = {
    "single-shot": "A 单次修复",
    "retry-without-feedback": "B 无诊断重试",
    "test-feedback": "C 测试反馈",
}
COLORS = ("#4e79a7", "#f28e2b", "#59a14f")


def _number(value: object) -> float | None:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _format(value: object, *, percent: bool = False) -> str:
    number = _number(value)
    if number is None:
        return "N/A"
    return f"{number:.1%}" if percent else f"{number:.3f}"


def _chart(
    path: Path,
    title: str,
    metrics: Mapping[str, Any],
    panels: Sequence[tuple[str, str, bool, float]],
) -> None:
    width, height = 1000, 100 + 150 * len(panels)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">',
        f"<title>{html.escape(title)}</title>",
        '<rect width="100%" height="100%" fill="white"/>',
        '<g font-family="Arial, sans-serif" fill="#182230">',
        f'<text x="30" y="35" font-size="22">{html.escape(title)}</text>',
    ]
    for panel, (label, key, percent, scale) in enumerate(panels):
        y0 = 75 + panel * 150
        values = [_number(metrics.get(strategy, {}).get(key)) for strategy in STRATEGIES]
        values = [value / scale if value is not None else None for value in values]
        peak = 1.0 if percent else max([v for v in values if v is not None] + [1.0])
        parts.append(f'<text x="30" y="{y0}" font-size="16">{html.escape(label)}</text>')
        for index, (strategy, value) in enumerate(zip(STRATEGIES, values, strict=True)):
            y = y0 + 18 + index * 28
            parts.extend(
                [
                    f'<text x="30" y="{y + 15}" font-size="13">{LABELS[strategy]}</text>',
                    f'<rect x="230" y="{y}" width="550" height="19" fill="#eef1f4"/>',
                ]
            )
            if value is not None:
                parts.append(
                    f'<rect x="230" y="{y}" width="{550 * value / peak:.2f}" '
                    f'height="19" fill="{COLORS[index]}"/>'
                )
            parts.append(
                f'<text x="800" y="{y + 15}" font-size="13">'
                f"{_format(value, percent=percent)}</text>"
            )
    parts.extend(["</g>", "</svg>"])
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def _csv(path: Path, fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def generate_experiment_report(report: Mapping[str, Any], output_dir: Path) -> Path:
    output_dir = output_dir.resolve()
    figures = output_dir / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    rows = [dict(row) for row in report.get("raw_runs", [])]
    data = {**report, **aggregate_summaries(rows), "raw_runs": rows}
    metrics = data["strategies"]
    (output_dir / "report.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    raw_fields = [
        "run_id",
        "task_id",
        "strategy",
        "repetition",
        "outcome",
        "status",
        "attempts",
        "first_public_passed",
        "final_public_passed",
        "first_hidden_passed",
        "final_hidden_passed",
        "timed_out",
        "hidden_regression",
        "test_version",
        "protected_test_violation",
        "workspace_policy_violation",
        "duration_ms",
        "test_runtime_ms",
        "model_calls",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "model_latency_ms",
        "currency_cost",
        "currency",
        "error_type",
        "error_message",
    ]
    _csv(output_dir / "raw-runs.csv", raw_fields, [{**row, **row.get("cost", {})} for row in rows])
    metric_fields = sorted({key for item in metrics.values() for key in item})
    _csv(
        output_dir / "strategy-metrics.csv",
        ["strategy", *metric_fields],
        [{"strategy": strategy, **item} for strategy, item in metrics.items()],
    )
    function_rows = []
    for row in rows:
        stages = row.get("hidden_cases", {})
        names = sorted({name for stage in stages.values() for name in stage})
        for name in names:
            function_rows.append(
                {
                    **{
                        key: row.get(key, "")
                        for key in ("run_id", "task_id", "strategy", "repetition")
                    },
                    "test_function": name,
                    **{
                        stage: stages.get(stage, {}).get(name, "not_run")
                        for stage in ("baseline", "first", "final")
                    },
                }
            )
    _csv(
        output_dir / "test-results.csv",
        [
            "run_id",
            "task_id",
            "strategy",
            "repetition",
            "test_function",
            "baseline",
            "first",
            "final",
        ],
        function_rows,
    )
    charts = [
        (
            "hidden-pass-rates.svg",
            "首次与最终隐藏测试通过率",
            [
                ("首次隐藏通过率", "first_hidden_pass_rate", True, 1),
                ("最终隐藏通过率", "final_hidden_pass_rate", True, 1),
            ],
        ),
        (
            "public-hidden-gap.svg",
            "最终公开与隐藏测试通过率",
            [
                ("公开通过率", "final_public_pass_rate", True, 1),
                ("隐藏通过率", "final_hidden_pass_rate", True, 1),
            ],
        ),
        (
            "reliability.svg",
            "超时、功能回归与测试保护",
            [
                ("超时率", "timeout_rate", True, 1),
                ("发生测试函数回归的 run 占比", "function_regression_rate", True, 1),
                ("测试保护违规率", "protected_test_violation_rate", True, 1),
            ],
        ),
        (
            "cost.svg",
            "实际调用、用量与耗时",
            [
                ("平均模型调用次数", "average_model_calls", False, 1),
                ("平均 token", "average_total_tokens", False, 1),
                ("平均整题耗时（秒）", "average_duration_ms", False, 1000),
            ],
        ),
    ]
    for filename, title, panels in charts:
        _chart(figures / filename, title, metrics, panels)
    planned = report.get("design", {}).get("planned_runs", len(rows))
    lines = [
        "# 三组修复实验报告",
        "",
        f"已记录 {len(rows)} / {planned} 个 run；有效运行 {data['valid_runs']}，"
        f"基础设施异常 {data['infrastructure_errors']}。",
        "",
        "A 组一次提交，B/C 组最多三次总提交。隐藏测试仅在修复停止后评分。",
        "主指标为最终整题隐藏测试通过率；正常修复失败和代码超时保留在分母中，基础设施异常单列。",
        "",
        "## 效果与可靠性",
        "",
        "| 策略 | 有效 run | 首次隐藏 | 最终隐藏 | 最终公开 | 超时率 | 功能回归率 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for strategy in STRATEGIES:
        if strategy not in metrics:
            continue
        item = metrics[strategy]
        values = [LABELS[strategy], str(item["runs"])] + [
            _format(item.get(key), percent=True)
            for key in (
                "first_hidden_pass_rate",
                "final_hidden_pass_rate",
                "final_public_pass_rate",
                "timeout_rate",
                "function_regression_rate",
            )
        ]
        lines.append("| " + " | ".join(values) + " |")
    comparison = data["feedback_comparison"]
    lines.extend(
        [
            "",
            f"C−B 同题配对差：{_format(comparison['hidden_pass_rate_difference'], percent=True)}，"
            f"共 {comparison['paired_runs']} 对。此处仅报告描述性差异。",
            "",
        ]
    )
    lines.extend(
        [
            "",
            "## 实际成本",
            "",
            "| 策略 | 模型调用总数 | 输入 token | 输出 token | 平均整题秒数 | 金额 | 币种 |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for strategy in STRATEGIES:
        if strategy not in metrics:
            continue
        item = metrics[strategy]
        duration = _number(item.get("average_duration_ms"))
        values = [
            LABELS[strategy],
            *[
                _format(item.get(key))
                for key in ("model_calls", "prompt_tokens", "completion_tokens")
            ],
            _format(duration / 1000 if duration is not None else None),
            f"{item['currency_cost']:.8f}"
            if _number(item.get("currency_cost")) is not None
            else "N/A",
            str(item.get("currency") or "N/A"),
        ]
        lines.append("| " + " | ".join(values) + " |")
    lines.extend(
        [
            "",
            "金额按提供的日期、模型和单价计算；缺少价格或用量时为 N/A，不代表零费用。",
            "成本包含已记录的基础设施失败请求。不同图表指标分别使用自己的刻度。",
            "",
            "## 错误分析（人工填写）",
            "",
            "从 raw-runs.csv 与每轮日志中选择 3～4 个真实案例，分别分析：",
            "",
            "1. 测试反馈后成功修复。",
            "2. 用完预算仍未修好。",
            "3. 公开通过但隐藏失败。",
            "4. 实际发生的回归或超时（没有则明确未观察到）。",
            "",
            "每例记录题目、run_id、初始缺陷、逐轮代码差异、公开反馈、最终结果和原因。",
            "不得编造案例；小样本和全部首轮通过不能证明反馈有效。",
            "",
            "## 关键图表",
            "",
        ]
    )
    for filename, title, _ in charts:
        lines.extend([f"![{title}](figures/{filename})", ""])
    lines.extend(
        [
            "## 原始记录",
            "",
            "- raw-runs.csv：逐 run 结果与实际调用成本。",
            "- strategy-metrics.csv：三组汇总。",
            "- test-results.csv：隐藏测试函数的通过/失败变化。",
            "- results.jsonl：每次运行结束立即保存的结果（由 benchmark 生成）。",
            "- 本实验的逐题记录按 A/B/C 分别保存在 runs/group_a/、runs/group_b/、"
            "runs/group_c/，每条记录含 events.jsonl、summary.json、"
            "original_code/、repair_attempts/ 与 workspace/。",
            "",
        ]
    )
    output = output_dir / "report.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    return output
