"""Dependency-free SVG, CSV, HTML, and Markdown experiment reporting."""

# ruff: noqa: RUF001

from __future__ import annotations

import csv
import html
import json
import math
import random
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

STRATEGY_ORDER = ("single-shot", "retry-without-feedback", "test-feedback")
STRATEGY_LABELS = {
    "single-shot": "Single shot",
    "retry-without-feedback": "Retry, no feedback",
    "test-feedback": "Test feedback",
}
COLORS = {
    "single-shot": "#4E79A7",
    "retry-without-feedback": "#F28E2B",
    "test-feedback": "#59A14F",
    "first": "#9C9C9C",
    "final": "#4E79A7",
    "public": "#76B7B2",
    "hidden": "#E15759",
    "improved": "#59A14F",
    "regressed": "#E15759",
    "stable_pass": "#4E79A7",
    "stable_fail": "#BAB0AC",
}
TEXT = "#182230"
MUTED = "#5E6B7A"
GRID = "#D9DEE5"
BACKGROUND = "#FFFFFF"


def generate_experiment_report(report: Mapping[str, Any], output_dir: Path) -> Path:
    """Create a self-contained visual report directory and return its HTML index."""
    output_dir = output_dir.resolve()
    figures = output_dir / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    (output_dir / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    rows = _raw_runs(report)
    metrics = _strategy_metrics(report)
    protocol = _protocol_name(report)

    _write_csvs(rows, metrics, output_dir)
    chart_builders: list[tuple[str, str, Callable[[Path], None]]] = [
        (
            "feedback-effect.svg",
            "核心效应：测试反馈相对无反馈重试",
            lambda path: _feedback_effect_chart(rows, path),
        ),
        (
            "hidden-pass-rates.svg",
            "首次与最终隐藏测试通过率",
            lambda path: _hidden_rate_chart(rows, path),
        ),
        (
            "public-hidden-gap.svg",
            "最终公开—隐藏测试差距",
            lambda path: _public_hidden_chart(rows, path),
        ),
        (
            "repair-transitions.svg",
            "隐藏测试改善、回归与稳定状态",
            lambda path: _transition_chart(rows, path),
        ),
        (
            "reliability.svg",
            "超时与策略违规率",
            lambda path: _reliability_chart(rows, path),
        ),
        (
            "cost-efficiency.svg",
            "调用与成本效率",
            lambda path: _cost_chart(metrics, path),
        ),
        (
            "token-composition.svg",
            "Prompt 与 Completion token 构成",
            lambda path: _token_chart(metrics, path),
        ),
        (
            "task-heatmap.svg",
            "逐题最终隐藏测试通过率",
            lambda path: _task_heatmap(rows, path),
        ),
        (
            "repetition-trend.svg",
            "跨重复实验的隐藏通过率趋势",
            lambda path: _repetition_chart(rows, path),
        ),
        (
            "attempt-distribution.svg",
            "实际提交次数分布",
            lambda path: _attempt_chart(rows, protocol, path),
        ),
    ]
    for filename, _title, builder in chart_builders:
        builder(figures / filename)

    effect = _paired_effect(rows)
    _write_markdown(report, metrics, chart_builders, effect, output_dir / "report.md")
    _write_html(report, metrics, chart_builders, effect, output_dir / "report.html")
    manifest = {
        "schema_version": 1,
        "figures": [f"figures/{filename}" for filename, _title, _builder in chart_builders],
        "tables": ["raw-runs.csv", "strategy-metrics.csv"],
        "documents": ["report.json", "report.html", "report.md"],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return output_dir / "report.html"


class _Svg:
    def __init__(self, width: int, height: int, title: str, description: str) -> None:
        self.width = width
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img">',
            f"<title>{html.escape(title)}</title>",
            f"<desc>{html.escape(description)}</desc>",
            f'<rect width="{width}" height="{height}" fill="{BACKGROUND}"/>',
        ]

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        *,
        stroke: str = GRID,
        width: float = 1,
        dash: str | None = None,
    ) -> None:
        dashed = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{width}"{dashed}/>'
        )

    def rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        *,
        fill: str,
        stroke: str = "none",
        radius: float = 0,
    ) -> None:
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(width, 0):.1f}" '
            f'height="{max(height, 0):.1f}" rx="{radius:.1f}" fill="{fill}" '
            f'stroke="{stroke}"/>'
        )

    def circle(self, x: float, y: float, radius: float, *, fill: str) -> None:
        self.parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{fill}"/>')

    def polyline(self, points: Sequence[tuple[float, float]], *, stroke: str) -> None:
        encoded = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.parts.append(
            f'<polyline points="{encoded}" fill="none" stroke="{stroke}" '
            'stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
        )

    def text(
        self,
        x: float,
        y: float,
        value: object,
        *,
        size: int = 14,
        anchor: str = "start",
        fill: str = TEXT,
        weight: int = 400,
        rotate: int | None = None,
    ) -> None:
        transform = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate else ""
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}"{transform}>{html.escape(str(value))}</text>'
        )

    def save(self, path: Path) -> None:
        self.parts.append("</svg>")
        path.write_text("\n".join(self.parts) + "\n", encoding="utf-8")


def _title(svg: _Svg, title: str, subtitle: str) -> None:
    svg.text(48, 40, title, size=24, weight=500)
    svg.text(48, 66, subtitle, size=13, fill=MUTED)


def _strategies(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    available = {str(row.get("strategy", "")) for row in rows}
    ordered = [item for item in STRATEGY_ORDER if item in available]
    return ordered + sorted(available - set(ordered))


def _raw_runs(report: Mapping[str, Any]) -> list[dict[str, Any]]:
    value = report.get("raw_runs", [])
    return (
        [dict(row) for row in value if isinstance(row, Mapping)] if isinstance(value, list) else []
    )


def _strategy_metrics(report: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    value = report.get("strategies", {})
    if not isinstance(value, Mapping):
        return {}
    return {str(key): dict(item) for key, item in value.items() if isinstance(item, Mapping)}


def _rate(rows: Sequence[Mapping[str, Any]], key: str) -> float:
    return sum(bool(row.get(key)) for row in rows) / len(rows) if rows else 0.0


def _group(rows: Sequence[Mapping[str, Any]]) -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("strategy", "unknown"))].append(row)
    return grouped


def _wilson(successes: int, total: int) -> tuple[float, float]:
    if total == 0:
        return 0.0, 0.0
    z = 1.959963984540054
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    margin = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return max(0.0, center - margin), min(1.0, center + margin)


def _grouped_rate_chart(
    rows: Sequence[Mapping[str, Any]],
    path: Path,
    *,
    title: str,
    subtitle: str,
    series: Sequence[tuple[str, str, str]],
    intervals: bool = False,
) -> None:
    width, height = 1200, 650
    svg = _Svg(width, height, title, subtitle)
    _title(svg, title, subtitle)
    strategies = _strategies(rows)
    grouped = _group(rows)
    left, right, top, bottom = 105, 45, 120, 105
    plot_w, plot_h = width - left - right, height - top - bottom
    for tick in range(5):
        value = tick / 4
        y = top + plot_h * (1 - value)
        svg.line(left, y, width - right, y)
        svg.text(left - 12, y + 5, f"{value:.0%}", anchor="end", fill=MUTED)
    group_w = plot_w / max(len(strategies), 1)
    bar_w = min(90.0, group_w * 0.7 / max(len(series), 1))
    for index, strategy in enumerate(strategies):
        center = left + group_w * (index + 0.5)
        items = grouped[strategy]
        for series_index, (_label, key, color) in enumerate(series):
            value = _rate(items, key)
            x = center + (series_index - (len(series) - 1) / 2) * bar_w - bar_w * 0.42
            y = top + plot_h * (1 - value)
            svg.rect(x, y, bar_w * 0.84, plot_h * value, fill=color, radius=3)
            svg.text(x + bar_w * 0.42, y - 9, f"{value:.1%}", anchor="middle", size=13)
            if intervals:
                successes = sum(bool(row.get(key)) for row in items)
                low, high = _wilson(successes, len(items))
                y_low = top + plot_h * (1 - low)
                y_high = top + plot_h * (1 - high)
                mid_x = x + bar_w * 0.42
                svg.line(mid_x, y_high, mid_x, y_low, stroke=TEXT, width=1.5)
                svg.line(mid_x - 6, y_high, mid_x + 6, y_high, stroke=TEXT, width=1.5)
                svg.line(mid_x - 6, y_low, mid_x + 6, y_low, stroke=TEXT, width=1.5)
        svg.text(center, height - 66, STRATEGY_LABELS.get(strategy, strategy), anchor="middle")
        svg.text(center, height - 44, f"n={len(items)}", anchor="middle", size=12, fill=MUTED)
    legend_x = left
    for label, _key, color in series:
        svg.rect(legend_x, 88, 14, 14, fill=color, radius=2)
        svg.text(legend_x + 21, 100, label, size=13)
        legend_x += 150
    svg.save(path)


def _hidden_rate_chart(rows: Sequence[Mapping[str, Any]], path: Path) -> None:
    _grouped_rate_chart(
        rows,
        path,
        title="首次与最终隐藏测试通过率",
        subtitle="误差线为 Wilson 95% 置信区间；最终隐藏通过率是主指标",
        series=(
            ("首次隐藏", "first_hidden_passed", COLORS["first"]),
            ("最终隐藏", "final_hidden_passed", COLORS["final"]),
        ),
        intervals=True,
    )


def _public_hidden_chart(rows: Sequence[Mapping[str, Any]], path: Path) -> None:
    _grouped_rate_chart(
        rows,
        path,
        title="最终公开—隐藏测试差距",
        subtitle="公开通过但隐藏失败会扩大差距；差距越小通常代表泛化更稳定",
        series=(
            ("最终公开", "final_public_passed", COLORS["public"]),
            ("最终隐藏", "final_hidden_passed", COLORS["hidden"]),
        ),
    )


def _reliability_chart(rows: Sequence[Mapping[str, Any]], path: Path) -> None:
    _grouped_rate_chart(
        rows,
        path,
        title="可靠性与策略违规",
        subtitle="分别统计超时、受保护测试变化和 solution.py 之外的 workspace 变化",
        series=(
            ("超时", "timed_out", "#E15759"),
            ("测试保护违规", "protected_test_violation", "#B07AA1"),
            ("Workspace 违规", "workspace_policy_violation", "#F28E2B"),
        ),
    )


def _transition_chart(rows: Sequence[Mapping[str, Any]], path: Path) -> None:
    width, height = 1200, 600
    title = "隐藏测试状态迁移"
    svg = _Svg(width, height, title, "首次到最终的改善、回归、稳定通过和稳定失败")
    _title(svg, title, "每根横条合计 100%；改善是真正修复，回归表示破坏原有正确功能")
    grouped = _group(rows)
    strategies = _strategies(rows)
    categories = (
        ("improved", "改善", COLORS["improved"]),
        ("stable_pass", "稳定通过", COLORS["stable_pass"]),
        ("regressed", "回归", COLORS["regressed"]),
        ("stable_fail", "稳定失败", COLORS["stable_fail"]),
    )
    left, plot_w = 220, 910
    for index, strategy in enumerate(strategies):
        y = 145 + index * 105
        items = grouped[strategy]
        counts: Counter[str] = Counter()
        for row in items:
            first = bool(row.get("first_hidden_passed"))
            final = bool(row.get("final_hidden_passed"))
            state = (
                "improved"
                if not first and final
                else "regressed"
                if first and not final
                else "stable_pass"
                if first
                else "stable_fail"
            )
            counts[state] += 1
        svg.text(left - 18, y + 30, STRATEGY_LABELS.get(strategy, strategy), anchor="end")
        cursor = float(left)
        for key, _label, color in categories:
            proportion = counts[key] / len(items) if items else 0
            segment = plot_w * proportion
            svg.rect(cursor, y, segment, 48, fill=color)
            if segment >= 55:
                svg.text(
                    cursor + segment / 2,
                    y + 30,
                    f"{counts[key]} ({proportion:.0%})",
                    anchor="middle",
                    size=12,
                    fill="#FFFFFF" if key != "stable_fail" else TEXT,
                    weight=500,
                )
            cursor += segment
    legend_x = left
    for _key, label, color in categories:
        svg.rect(legend_x, 490, 15, 15, fill=color)
        svg.text(legend_x + 22, 503, label, size=13)
        legend_x += 175
    svg.save(path)


def _paired_effect(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    indexed: dict[tuple[str, int, str], Mapping[str, Any]] = {}
    for row in rows:
        task = str(row.get("task_id", ""))
        repetition = _integer(row.get("repetition"), 0)
        strategy = str(row.get("strategy", ""))
        indexed[(task, repetition, strategy)] = row
    differences_by_task: dict[str, list[int]] = defaultdict(list)
    for task, repetition, strategy in indexed:
        if strategy != "test-feedback":
            continue
        feedback = indexed[(task, repetition, strategy)]
        retry = indexed.get((task, repetition, "retry-without-feedback"))
        if retry is not None:
            differences_by_task[task].append(
                int(bool(feedback.get("final_hidden_passed")))
                - int(bool(retry.get("final_hidden_passed")))
            )
    differences = [value for values in differences_by_task.values() for value in values]
    if not differences:
        return {"pairs": 0, "effect": None, "low": None, "high": None}
    task_means = [sum(values) / len(values) for values in differences_by_task.values()]
    effect = sum(task_means) / len(task_means)
    rng = random.Random(20261018)
    samples = []
    for _ in range(5000):
        sample = [task_means[rng.randrange(len(task_means))] for _ in task_means]
        samples.append(sum(sample) / len(sample))
    samples.sort()
    low = samples[int(len(samples) * 0.025)]
    high = samples[min(len(samples) - 1, int(len(samples) * 0.975))]
    return {
        "pairs": len(differences),
        "tasks": len(task_means),
        "effect": effect,
        "low": low,
        "high": high,
        "wins": differences.count(1),
        "ties": differences.count(0),
        "losses": differences.count(-1),
    }


def _feedback_effect_chart(rows: Sequence[Mapping[str, Any]], path: Path) -> None:
    width, height = 1200, 520
    title = "测试反馈的配对主效应"
    svg = _Svg(width, height, title, "测试反馈减去无反馈重试的最终隐藏通过结果")
    _title(svg, title, "同一任务 × 重复编号配对；区间按任务聚类 bootstrap，避免把重复误当独立题目")
    effect = _paired_effect(rows)
    if effect["effect"] is None:
        svg.text(width / 2, height / 2, "缺少可配对的两组运行数据", anchor="middle", size=20)
        svg.save(path)
        return
    left, right, y = 130, 70, 225
    axis_w = width - left - right
    svg.line(left, y, width - right, y, stroke=TEXT, width=2)
    for value in (-1.0, -0.5, 0.0, 0.5, 1.0):
        x = left + (value + 1) / 2 * axis_w
        svg.line(x, y - 10, x, y + 10, stroke=TEXT)
        svg.text(x, y + 36, f"{value:+.0%}", anchor="middle", fill=MUTED)
    zero_x = left + axis_w / 2
    svg.line(zero_x, 130, zero_x, 315, stroke=GRID, width=2, dash="5 5")
    low = float(effect["low"])
    high = float(effect["high"])
    estimate = float(effect["effect"])
    x_low = left + (low + 1) / 2 * axis_w
    x_high = left + (high + 1) / 2 * axis_w
    x_estimate = left + (estimate + 1) / 2 * axis_w
    svg.line(x_low, y, x_high, y, stroke=COLORS["test-feedback"], width=9)
    svg.circle(x_estimate, y, 12, fill=COLORS["test-feedback"])
    svg.text(
        x_estimate,
        y - 30,
        f"{estimate:+.1%}  [95% CI {low:+.1%}, {high:+.1%}]",
        anchor="middle",
        size=16,
        weight=500,
    )
    counts = (
        ("反馈组胜", int(effect.get("wins", 0)), COLORS["improved"]),
        ("持平", int(effect.get("ties", 0)), COLORS["stable_fail"]),
        ("反馈组负", int(effect.get("losses", 0)), COLORS["regressed"]),
    )
    total = int(effect["pairs"])
    box_w = 260
    start = (width - len(counts) * box_w) / 2
    for index, (label, count, color) in enumerate(counts):
        x = start + index * box_w
        svg.rect(x + 8, 360, box_w - 16, 68, fill="#F4F6F8", radius=7)
        svg.rect(x + 8, 360, 7, 68, fill=color, radius=3)
        svg.text(x + 30, 385, label, size=13, fill=MUTED)
        svg.text(x + 30, 414, f"{count} / {total}", size=22, weight=500)
    svg.save(path)


def _cost_chart(metrics: Mapping[str, Mapping[str, Any]], path: Path) -> None:
    panels = (
        ("平均模型调用", "average_model_calls", " calls"),
        ("平均总 token", "average_total_tokens", ""),
        ("每成功 token", "tokens_per_success", ""),
        ("平均模型延迟", "average_model_latency_ms", " ms"),
    )
    width, height = 1200, 720
    svg = _Svg(width, height, "调用与成本效率", "四项成本指标使用各自刻度")
    _title(svg, "调用与成本效率", "各面板独立刻度；每成功 token 在没有成功 run 时显示 N/A")
    strategies = [item for item in STRATEGY_ORDER if item in metrics]
    for panel_index, (label, key, suffix) in enumerate(panels):
        col, row = panel_index % 2, panel_index // 2
        x0, y0 = 70 + col * 570, 105 + row * 285
        panel_w, panel_h = 500, 205
        values = [_number(metrics[s].get(key)) for s in strategies]
        valid = [value for value in values if value is not None]
        maximum = max(valid, default=1.0) or 1.0
        svg.text(x0, y0, label, size=16, weight=500)
        for index, (strategy, value) in enumerate(zip(strategies, values, strict=True)):
            y = y0 + 42 + index * 51
            svg.text(x0, y + 18, STRATEGY_LABELS[strategy], size=12)
            bar_x, bar_w = x0 + 175, panel_w - 175
            svg.rect(bar_x, y, bar_w, 25, fill="#EEF1F4", radius=3)
            if value is not None:
                svg.rect(
                    bar_x,
                    y,
                    bar_w * value / maximum,
                    25,
                    fill=COLORS[strategy],
                    radius=3,
                )
                svg.text(bar_x + 7, y + 18, f"{value:,.1f}{suffix}", size=12, weight=500)
            else:
                svg.text(bar_x + 7, y + 18, "N/A", size=12, fill=MUTED)
        if col == 0:
            svg.line(620, y0 - 10, 620, y0 + panel_h, stroke=GRID)
        if row == 0:
            svg.line(55, 385, 1145, 385, stroke=GRID)
    svg.save(path)


def _token_chart(metrics: Mapping[str, Mapping[str, Any]], path: Path) -> None:
    width, height = 1200, 600
    svg = _Svg(width, height, "Token 构成", "每个策略的 prompt 与 completion token 总量")
    _title(svg, "Prompt 与 Completion token 构成", "显示总量与构成；同时结合运行数解读")
    strategies = [item for item in STRATEGY_ORDER if item in metrics]
    totals = [
        (_number(metrics[s].get("prompt_tokens")) or 0.0)
        + (_number(metrics[s].get("completion_tokens")) or 0.0)
        for s in strategies
    ]
    maximum = max(totals, default=1.0) or 1.0
    left, top, plot_w = 250, 140, 850
    for index, strategy in enumerate(strategies):
        y = top + index * 110
        prompt = _number(metrics[strategy].get("prompt_tokens")) or 0.0
        completion = _number(metrics[strategy].get("completion_tokens")) or 0.0
        total = prompt + completion
        svg.text(left - 20, y + 30, STRATEGY_LABELS[strategy], anchor="end")
        prompt_w = plot_w * prompt / maximum
        completion_w = plot_w * completion / maximum
        svg.rect(left, y, prompt_w, 46, fill="#4E79A7")
        svg.rect(left + prompt_w, y, completion_w, 46, fill="#F28E2B")
        svg.text(left + total / maximum * plot_w + 10, y + 29, f"{total:,.0f}", size=13)
    svg.rect(left, 490, 15, 15, fill="#4E79A7")
    svg.text(left + 22, 503, "Prompt", size=13)
    svg.rect(left + 130, 490, 15, 15, fill="#F28E2B")
    svg.text(left + 152, 503, "Completion", size=13)
    svg.save(path)


def _task_heatmap(rows: Sequence[Mapping[str, Any]], path: Path) -> None:
    tasks = sorted({str(row.get("task_id", "unknown")) for row in rows})
    strategies = _strategies(rows)
    width = max(1100, 360 + len(tasks) * 150)
    height = 260 + len(strategies) * 95
    svg = _Svg(width, height, "逐题最终隐藏测试通过率", "按策略和任务聚合重复实验")
    _title(svg, "逐题最终隐藏测试通过率", "每格为该任务跨重复的最终隐藏通过比例")
    left, top, cell_w, cell_h = 260, 150, (width - 310) / max(len(tasks), 1), 72
    for col, task in enumerate(tasks):
        svg.text(left + (col + 0.5) * cell_w, top - 18, task, anchor="middle", size=12)
    for row_index, strategy in enumerate(strategies):
        y = top + row_index * cell_h
        svg.text(left - 18, y + 42, STRATEGY_LABELS[strategy], anchor="end", size=13)
        for col, task in enumerate(tasks):
            items = [
                item
                for item in rows
                if item.get("strategy") == strategy and str(item.get("task_id")) == task
            ]
            value = _rate(items, "final_hidden_passed")
            fill = _blend("#F2F4F7", COLORS[strategy], value)
            x = left + col * cell_w
            svg.rect(x + 2, y + 2, cell_w - 4, cell_h - 4, fill=fill, radius=3)
            svg.text(
                x + cell_w / 2,
                y + 37,
                f"{value:.0%}",
                anchor="middle",
                size=15,
                weight=500,
                fill=TEXT if value < 0.6 else "#FFFFFF",
            )
            svg.text(
                x + cell_w / 2,
                y + 57,
                f"n={len(items)}",
                anchor="middle",
                size=11,
                fill=TEXT if value < 0.6 else "#FFFFFF",
            )
    svg.save(path)


def _repetition_chart(rows: Sequence[Mapping[str, Any]], path: Path) -> None:
    width, height = 1200, 650
    svg = _Svg(width, height, "跨重复实验趋势", "每个重复编号内跨任务的最终隐藏通过率")
    _title(svg, "跨重复实验的隐藏通过率趋势", "用于观察随机波动、顺序效应和异常重复")
    repetitions = sorted({_integer(row.get("repetition"), 0) for row in rows})
    strategies = _strategies(rows)
    left, right, top, bottom = 100, 50, 130, 105
    plot_w, plot_h = width - left - right, height - top - bottom
    for tick in range(5):
        value = tick / 4
        y = top + plot_h * (1 - value)
        svg.line(left, y, width - right, y)
        svg.text(left - 12, y + 5, f"{value:.0%}", anchor="end", fill=MUTED)
    for strategy in strategies:
        points = []
        for index, repetition in enumerate(repetitions):
            items = [
                row
                for row in rows
                if row.get("strategy") == strategy
                and _integer(row.get("repetition"), 0) == repetition
            ]
            value = _rate(items, "final_hidden_passed")
            x = left + (index + 0.5) * plot_w / max(len(repetitions), 1)
            y = top + plot_h * (1 - value)
            points.append((x, y))
        if points:
            svg.polyline(points, stroke=COLORS[strategy])
            for x, y in points:
                svg.circle(x, y, 6, fill=COLORS[strategy])
    for index, repetition in enumerate(repetitions):
        x = left + (index + 0.5) * plot_w / max(len(repetitions), 1)
        svg.text(x, height - 70, repetition, anchor="middle")
    svg.text(width / 2, height - 35, "重复编号", anchor="middle", fill=MUTED)
    legend_x = left
    for strategy in strategies:
        svg.line(legend_x, 94, legend_x + 25, 94, stroke=COLORS[strategy], width=3)
        svg.text(legend_x + 34, 99, STRATEGY_LABELS[strategy], size=13)
        legend_x += 245
    svg.save(path)


def _attempt_chart(rows: Sequence[Mapping[str, Any]], protocol: str, path: Path) -> None:
    width, height = 1200, 650
    svg = _Svg(width, height, "实际提交次数分布", "按策略统计每个 run 的提交次数")
    subtitle = (
        "两个多次提交组都在公开测试通过时停止，最多使用配置预算"
        if protocol == "shared-public-test-stopping-v2"
        else "旧版或未声明协议；不同策略可能采用不同停止规则，不能直接比较成本"
    )
    _title(svg, "实际提交次数分布", subtitle)
    strategies = _strategies(rows)
    max_attempts = max((_integer(row.get("attempts"), 0) for row in rows), default=1)
    left, right, top, bottom = 100, 50, 130, 105
    plot_w, plot_h = width - left - right, height - top - bottom
    grouped = _group(rows)
    peak = max(
        (
            sum(_integer(row.get("attempts"), 0) == attempt for row in grouped[strategy])
            for strategy in strategies
            for attempt in range(1, max_attempts + 1)
        ),
        default=1,
    )
    for tick in range(5):
        value = peak * tick / 4
        y = top + plot_h * (1 - tick / 4)
        svg.line(left, y, width - right, y)
        svg.text(left - 12, y + 5, f"{value:.0f}", anchor="end", fill=MUTED)
    group_w = plot_w / max(max_attempts, 1)
    bar_w = group_w * 0.72 / max(len(strategies), 1)
    for attempt in range(1, max_attempts + 1):
        center = left + (attempt - 0.5) * group_w
        for index, strategy in enumerate(strategies):
            count = sum(_integer(row.get("attempts"), 0) == attempt for row in grouped[strategy])
            x = center + (index - (len(strategies) - 1) / 2) * bar_w - bar_w * 0.42
            bar_h = plot_h * count / peak
            svg.rect(x, top + plot_h - bar_h, bar_w * 0.84, bar_h, fill=COLORS[strategy])
            if count:
                svg.text(x + bar_w * 0.42, top + plot_h - bar_h - 8, count, anchor="middle")
        svg.text(center, height - 70, attempt, anchor="middle")
    svg.text(width / 2, height - 35, "提交次数", anchor="middle", fill=MUTED)
    svg.save(path)


def _write_csvs(
    rows: Sequence[Mapping[str, Any]],
    metrics: Mapping[str, Mapping[str, Any]],
    output_dir: Path,
) -> None:
    raw_fields = (
        "run_id",
        "task_id",
        "repetition",
        "strategy",
        "attempts",
        "outcome",
        "first_public_passed",
        "final_public_passed",
        "first_hidden_passed",
        "final_hidden_passed",
        "hidden_improvement",
        "hidden_regression",
        "timed_out",
        "protected_test_violation",
        "workspace_policy_violation",
        "model_calls",
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "model_latency_ms",
    )
    with (output_dir / "raw-runs.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=raw_fields)
        writer.writeheader()
        for row in rows:
            flat = {key: row.get(key, "") for key in raw_fields}
            cost = row.get("cost", {})
            if isinstance(cost, Mapping):
                for key in (
                    "model_calls",
                    "prompt_tokens",
                    "completion_tokens",
                    "total_tokens",
                    "model_latency_ms",
                ):
                    flat[key] = cost.get(key, 0)
            writer.writerow(flat)
    metric_fields = sorted({key for item in metrics.values() for key in item})
    with (output_dir / "strategy-metrics.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["strategy", *metric_fields])
        writer.writeheader()
        for strategy in STRATEGY_ORDER:
            if strategy in metrics:
                writer.writerow({"strategy": strategy, **metrics[strategy]})


def _write_markdown(
    report: Mapping[str, Any],
    metrics: Mapping[str, Mapping[str, Any]],
    charts: Sequence[tuple[str, str, Callable[[Path], None]]],
    effect: Mapping[str, Any],
    path: Path,
) -> None:
    protocol = _protocol_name(report)
    lines = [
        "# 实验可视化报告",
        "",
        f"总运行数：{report.get('runs', 0)}",
        f"实验协议：`{protocol}`",
        "",
    ]
    if effect.get("effect") is not None:
        lines.extend(
            [
                "## 核心效应",
                "",
                (
                    "`test-feedback - retry-without-feedback` 的最终隐藏通过率配对差为 "
                    f"**{float(effect['effect']):+.1%}** "
                    f"（任务聚类 bootstrap 95% CI {float(effect['low']):+.1%} 到 "
                    f"{float(effect['high']):+.1%}，{effect.get('tasks', 0)} 道任务、"
                    f"n={effect['pairs']} 对）。"
                ),
                "",
            ]
        )
    lines.extend(["## 策略汇总", "", _markdown_table(metrics), "", "## 图表", ""])
    for filename, title, _builder in charts:
        lines.extend([f"### {title}", "", f"![{title}](figures/{filename})", ""])
    lines.extend(
        [
            "## 可复核数据",
            "",
            "- `raw-runs.csv`：逐 run 明细",
            "- `strategy-metrics.csv`：按策略聚合指标",
            "- `manifest.json`：产物清单",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_html(
    report: Mapping[str, Any],
    metrics: Mapping[str, Mapping[str, Any]],
    charts: Sequence[tuple[str, str, Callable[[Path], None]]],
    effect: Mapping[str, Any],
    path: Path,
) -> None:
    effect_text = "缺少配对数据"
    if effect.get("effect") is not None:
        effect_text = (
            f"{float(effect['effect']):+.1%} "
            f"[95% CI {float(effect['low']):+.1%}, {float(effect['high']):+.1%}]"
        )
    protocol = _protocol_name(report)
    cards = "".join(
        f'<section><h2>{html.escape(title)}</h2><img src="figures/{filename}" '
        f'alt="{html.escape(title)}"></section>'
        for filename, title, _builder in charts
    )
    document = f"""<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>实验可视化报告</title><style>
body{{font-family:Arial,sans-serif;margin:0;background:#f4f6f8;color:{TEXT}}}
main{{max-width:1280px;margin:auto;padding:32px}} header{{margin-bottom:28px}}
.summary{{display:flex;gap:16px;flex-wrap:wrap}}
.summary div{{background:white;padding:16px 20px;border-radius:8px;min-width:180px}}
.value{{font-size:24px;font-weight:600;margin-top:6px}}
section{{background:white;margin:20px 0;padding:18px;border-radius:10px}}
h1{{margin:0 0 10px}} h2{{font-size:18px;margin:0 0 12px}}
img{{width:100%;height:auto;display:block}}
table{{border-collapse:collapse;width:100%;background:white}}
th,td{{padding:10px;border-bottom:1px solid #dde2e8;text-align:right}}
th:first-child,td:first-child{{text-align:left}} a{{color:#235d9f}}
@media(max-width:600px){{main{{padding:14px}}section{{padding:8px}}}}
</style></head><body><main><header><h1>测试驱动 Python 函数修复实验</h1>
<p>完整对照实验的效果、泛化、可靠性与成本视图。</p><div class="summary">
<div>总运行数<div class="value">{html.escape(str(report.get("runs", 0)))}</div></div>
<div>反馈主效应<div class="value">{html.escape(effect_text)}</div></div>
<div>配对样本<div class="value">{html.escape(str(effect.get("pairs", 0)))}</div></div>
<div>实验协议<div class="value">{html.escape(protocol)}</div></div>
</div></header>{cards}<section><h2>策略汇总</h2>{_html_table(metrics)}</section>
<p><a href="raw-runs.csv">逐 run CSV</a> ·
<a href="strategy-metrics.csv">策略指标 CSV</a> ·
<a href="report.md">Markdown 报告</a></p>
</main></body></html>"""
    path.write_text(document, encoding="utf-8")


def _markdown_table(metrics: Mapping[str, Mapping[str, Any]]) -> str:
    headers = ("策略", "Runs", "最终公开", "最终隐藏", "公隐差距", "隐藏提升", "每成功 token")
    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for strategy in STRATEGY_ORDER:
        if strategy not in metrics:
            continue
        item = metrics[strategy]
        lines.append(
            "| "
            + " | ".join(
                (
                    STRATEGY_LABELS[strategy],
                    str(item.get("runs", 0)),
                    _percent(item.get("final_public_pass_rate")),
                    _percent(item.get("final_hidden_pass_rate")),
                    _signed_percent(item.get("public_hidden_gap")),
                    _percent(item.get("hidden_improvement_rate")),
                    _format_number(item.get("tokens_per_success")),
                )
            )
            + " |"
        )
    return "\n".join(lines)


def _html_table(metrics: Mapping[str, Mapping[str, Any]]) -> str:
    rows = []
    for strategy in STRATEGY_ORDER:
        if strategy not in metrics:
            continue
        item = metrics[strategy]
        values = (
            STRATEGY_LABELS[strategy],
            str(item.get("runs", 0)),
            _percent(item.get("final_public_pass_rate")),
            _percent(item.get("final_hidden_pass_rate")),
            _signed_percent(item.get("public_hidden_gap")),
            _percent(item.get("hidden_improvement_rate")),
            _format_number(item.get("tokens_per_success")),
        )
        rows.append(
            "<tr>" + "".join(f"<td>{html.escape(value)}</td>" for value in values) + "</tr>"
        )
    headers = ("策略", "Runs", "最终公开", "最终隐藏", "公隐差距", "隐藏提升", "每成功 token")
    return (
        "<table><thead><tr>"
        + "".join(f"<th>{item}</th>" for item in headers)
        + "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table>"
    )


def _blend(start: str, end: str, fraction: float) -> str:
    fraction = min(1.0, max(0.0, fraction))
    first = tuple(int(start[index : index + 2], 16) for index in (1, 3, 5))
    second = tuple(int(end[index : index + 2], 16) for index in (1, 3, 5))
    mixed = tuple(round(a + (b - a) * fraction) for a, b in zip(first, second, strict=True))
    return "#" + "".join(f"{value:02X}" for value in mixed)


def _number(value: object, default: float | None = None) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return default


def _integer(value: object, default: int) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else default


def _percent(value: object) -> str:
    number = _number(value)
    return f"{number:.1%}" if number is not None else "N/A"


def _signed_percent(value: object) -> str:
    number = _number(value)
    return f"{number:+.1%}" if number is not None else "N/A"


def _format_number(value: object) -> str:
    number = _number(value)
    return f"{number:,.1f}" if number is not None else "N/A"


def _protocol_name(report: Mapping[str, Any]) -> str:
    design = report.get("design")
    if isinstance(design, Mapping):
        value = design.get("repair_protocol")
        if isinstance(value, str) and value:
            return value
    return "legacy-or-unspecified"
