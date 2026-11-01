"""Task pass rates, test-function regressions and measured request costs."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Any


def _rate(rows: list[dict[str, Any]], key: str) -> float | None:
    return sum(bool(row.get(key)) for row in rows) / len(rows) if rows else None


def _mean(rows: list[dict[str, Any]], key: str, *, cost: bool = False) -> float | None:
    values = [row.get("cost", {}).get(key) if cost else row.get(key) for row in rows]
    if not values or any(not isinstance(value, (int, float)) for value in values):
        return None
    return sum(float(value) for value in values if isinstance(value, (int, float))) / len(values)


def _cost_sum(rows: list[dict[str, Any]], key: str) -> float | int | None:
    values = [row.get("cost", {}).get(key) for row in rows]
    if not values or any(not isinstance(value, (int, float)) for value in values):
        return None
    return sum(value for value in values if isinstance(value, (int, float)))


def _public_pass_through(row: dict[str, Any], attempt: int) -> bool:
    values = row.get("public_pass_by_attempt")
    if isinstance(values, list):
        return any(value is True for value in values[:attempt])
    if attempt == 1:
        return bool(row.get("first_public_passed"))
    return bool(row.get("final_public_passed"))


def aggregate_summaries(summaries: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(summaries)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["strategy"])].append(row)
    metrics = {}
    for strategy, all_rows in sorted(grouped.items()):
        valid = [row for row in all_rows if row.get("outcome") in {"passed", "failed"}]
        regressions = []
        for row in valid:
            changes = row.get("case_changes", {})
            regressions.append(
                bool(row.get("hidden_regression"))
                or any(item.get("regressed", 0) > 0 for item in changes.values())
            )
        item = {
            "runs": len(valid),
            "attempted_runs": len(all_rows),
            "infrastructure_errors": len(all_rows) - len(valid),
            "successful_runs": sum(row.get("outcome") == "passed" for row in valid),
            **{
                f"{stage}_pass_rate": _rate(valid, f"{stage}_passed")
                for stage in ("first_public", "final_public", "first_hidden", "final_hidden")
            },
            "hidden_improvement_rate": _rate(valid, "hidden_improvement"),
            "hidden_regression_rate": _rate(valid, "hidden_regression"),
            "function_regression_rate": sum(regressions) / len(valid) if valid else None,
            "timeout_rate": _rate(valid, "timed_out"),
            "protected_test_violation_rate": _rate(valid, "protected_test_violation"),
            "workspace_policy_violation_rate": _rate(valid, "workspace_policy_violation"),
            **{
                f"public_cumulative_pass_rate_attempt_{attempt}": (
                    sum(_public_pass_through(row, attempt) for row in valid) / len(valid)
                    if valid
                    else None
                )
                for attempt in range(1, 4)
            },
            "average_duration_ms": _mean(valid, "duration_ms"),
            "average_test_runtime_ms": _mean(valid, "test_runtime_ms"),
            "average_model_calls": _mean(valid, "model_calls", cost=True),
            "average_total_tokens": _mean(valid, "total_tokens", cost=True),
            "average_model_latency_ms": _mean(valid, "model_latency_ms", cost=True),
            **{
                key: _cost_sum(all_rows, key)
                for key in (
                    "model_calls",
                    "prompt_tokens",
                    "completion_tokens",
                    "total_tokens",
                    "model_latency_ms",
                    "currency_cost",
                )
            },
        }
        public, hidden = item["final_public_pass_rate"], item["final_hidden_pass_rate"]
        item["public_hidden_gap"] = (
            public - hidden if public is not None and hidden is not None else None
        )
        currencies = {row.get("cost", {}).get("currency") for row in all_rows}
        item["currency"] = next(iter(currencies)) if len(currencies) == 1 else None
        if item["currency"] is None:
            item["currency_cost"] = None
        total_tokens = item["total_tokens"]
        successful_runs = item["successful_runs"]
        item["tokens_per_successful_run"] = (
            total_tokens / successful_runs
            if isinstance(total_tokens, (int, float)) and successful_runs > 0
            else None
        )
        metrics[strategy] = item
    paired: dict[tuple[str, int], dict[str, bool]] = defaultdict(dict)
    for row in rows:
        if row.get("outcome") in {"passed", "failed"}:
            paired[(str(row.get("task_id", "")), int(row.get("repetition", 1)))][
                row["strategy"]
            ] = bool(row.get("final_hidden_passed"))
    differences = [
        int(arms["test-feedback"]) - int(arms["retry-without-feedback"])
        for arms in paired.values()
        if {"test-feedback", "retry-without-feedback"} <= arms.keys()
    ]
    return {
        "schema_version": 2,
        "runs": len(rows),
        "strategies": metrics,
        "valid_runs": sum(item["runs"] for item in metrics.values()),
        "infrastructure_errors": sum(item["infrastructure_errors"] for item in metrics.values()),
        "feedback_comparison": {
            "paired_runs": len(differences),
            "hidden_pass_rate_difference": sum(differences) / len(differences)
            if differences
            else None,
        },
    }
