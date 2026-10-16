"""Deterministic aggregation of raw per-run experiment summaries."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Any


def aggregate_summaries(summaries: Iterable[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for summary in summaries:
        grouped[str(summary["strategy"])].append(summary)

    strategies: dict[str, dict[str, Any]] = {}
    for strategy, rows in sorted(grouped.items()):
        count = len(rows)
        final_public_pass_rate = _rate(rows, "final_public_passed")
        final_hidden_pass_rate = _rate(rows, "final_hidden_passed")
        successful_runs = sum(row.get("outcome") == "passed" for row in rows)
        model_calls = sum(_cost(row, "model_calls") for row in rows)
        total_tokens = sum(_cost(row, "total_tokens") for row in rows)
        model_latency_ms = sum(_cost(row, "model_latency_ms") for row in rows)
        strategies[strategy] = {
            "runs": count,
            "first_public_pass_rate": _rate(rows, "first_public_passed"),
            "final_public_pass_rate": final_public_pass_rate,
            "first_hidden_pass_rate": _rate(rows, "first_hidden_passed"),
            "final_hidden_pass_rate": final_hidden_pass_rate,
            "public_hidden_gap": final_public_pass_rate - final_hidden_pass_rate,
            "hidden_improvement_rate": _rate(rows, "hidden_improvement"),
            "timeout_rate": _rate(rows, "timed_out"),
            "hidden_regression_rate": _rate(rows, "hidden_regression"),
            "protected_test_violation_rate": _rate(rows, "protected_test_violation"),
            "workspace_policy_violation_rate": _rate(rows, "workspace_policy_violation"),
            "successful_runs": successful_runs,
            "model_calls": model_calls,
            "prompt_tokens": sum(_cost(row, "prompt_tokens") for row in rows),
            "completion_tokens": sum(_cost(row, "completion_tokens") for row in rows),
            "total_tokens": total_tokens,
            "model_latency_ms": model_latency_ms,
            "average_model_calls": model_calls / count,
            "average_total_tokens": total_tokens / count,
            "average_model_latency_ms": model_latency_ms / count,
            "tokens_per_success": (total_tokens / successful_runs if successful_runs else None),
        }
    return {
        "schema_version": 1,
        "runs": sum(len(rows) for rows in grouped.values()),
        "strategies": strategies,
    }


def _rate(rows: list[dict[str, Any]], key: str) -> float:
    return sum(bool(row.get(key)) for row in rows) / len(rows)


def _cost(row: dict[str, Any], key: str) -> int:
    cost = row.get("cost", {})
    value = cost.get(key, 0) if isinstance(cost, dict) else 0
    return value if isinstance(value, int) and not isinstance(value, bool) else 0
