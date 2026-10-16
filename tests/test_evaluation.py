from repair_assistant.evaluation import aggregate_summaries


def test_aggregate_reports_hidden_improvement_regression_and_cost() -> None:
    report = aggregate_summaries(
        [
            {
                "outcome": "passed",
                "strategy": "test-feedback",
                "first_public_passed": False,
                "final_public_passed": True,
                "first_hidden_passed": False,
                "final_hidden_passed": True,
                "hidden_improvement": True,
                "timed_out": False,
                "hidden_regression": False,
                "protected_test_violation": False,
                "workspace_policy_violation": False,
                "cost": {"model_calls": 2, "total_tokens": 100},
            },
            {
                "outcome": "failed",
                "strategy": "test-feedback",
                "first_public_passed": False,
                "final_public_passed": True,
                "first_hidden_passed": True,
                "final_hidden_passed": False,
                "hidden_improvement": False,
                "timed_out": True,
                "hidden_regression": True,
                "protected_test_violation": False,
                "workspace_policy_violation": True,
                "cost": {"model_calls": 3, "total_tokens": 150},
            },
        ]
    )

    metrics = report["strategies"]["test-feedback"]
    assert metrics["first_hidden_pass_rate"] == 0.5
    assert metrics["final_hidden_pass_rate"] == 0.5
    assert metrics["public_hidden_gap"] == 0.5
    assert metrics["hidden_improvement_rate"] == 0.5
    assert metrics["hidden_regression_rate"] == 0.5
    assert metrics["timeout_rate"] == 0.5
    assert metrics["workspace_policy_violation_rate"] == 0.5
    assert metrics["successful_runs"] == 1
    assert metrics["model_calls"] == 5
    assert metrics["total_tokens"] == 250
    assert metrics["average_model_calls"] == 2.5
    assert metrics["average_total_tokens"] == 125
    assert metrics["tokens_per_success"] == 250
