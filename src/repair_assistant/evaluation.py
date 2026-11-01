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


def _nested_cost_sum(rows: list[dict[str, Any]], container: str, key: str) -> float | int | None:
    values = [row.get(container, {}).get(key) for row in rows]
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
            **{
                f"incremental_{key}": _nested_cost_sum(all_rows, "incremental_cost", key)
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
        shared_failures = [
            row
            for row in valid
            if row.get("shared_first_run_id") and row.get("first_public_passed") is False
        ]
        item["shared_first_failures"] = len(shared_failures)
        item["conditional_public_repair_rate"] = _rate(shared_failures, "final_public_passed")
        item["conditional_hidden_pass_rate"] = _rate(shared_failures, "final_hidden_passed")
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
    eligible_pairs: dict[tuple[str, int], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        if row.get("outcome") in {"passed", "failed"} and row.get("first_public_passed") is False:
            eligible_pairs[(str(row.get("task_id", "")), int(row.get("repetition", 1)))][
                str(row["strategy"])
            ] = row
    conditional_pairs = [
        arms
        for arms in eligible_pairs.values()
        if {"test-feedback", "retry-without-feedback"} <= arms.keys()
    ]
    physical_rows = []
    for row in rows:
        physical = (
            row.get("cost") if row.get("strategy") == "single-shot" else row.get("incremental_cost")
        )
        physical_rows.append({"cost": physical if isinstance(physical, dict) else {}})
    physical_cost = {
        key: _cost_sum(physical_rows, key)
        for key in (
            "model_calls",
            "prompt_tokens",
            "completion_tokens",
            "total_tokens",
            "model_latency_ms",
            "currency_cost",
        )
    }
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
            "shared_failure_pairs": len(conditional_pairs),
            "conditional_hidden_pass_rate_difference": (
                sum(
                    int(arms["test-feedback"].get("final_hidden_passed") is True)
                    - int(arms["retry-without-feedback"].get("final_hidden_passed") is True)
                    for arms in conditional_pairs
                )
                / len(conditional_pairs)
                if conditional_pairs
                else None
            ),
            "test_feedback_only_successes": sum(
                arms["test-feedback"].get("final_hidden_passed") is True
                and arms["retry-without-feedback"].get("final_hidden_passed") is False
                for arms in conditional_pairs
            ),
            "retry_only_successes": sum(
                arms["retry-without-feedback"].get("final_hidden_passed") is True
                and arms["test-feedback"].get("final_hidden_passed") is False
                for arms in conditional_pairs
            ),
        },
        "physical_cost": physical_cost,
    }
