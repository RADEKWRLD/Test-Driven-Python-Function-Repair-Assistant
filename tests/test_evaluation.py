from repair_assistant.evaluation import aggregate_summaries


def test_aggregate_reports_hidden_improvement_regression_and_cost() -> None:
    report = aggregate_summaries(
        [
            {
                "strategy": "test-feedback",
                "first_public_passed": False,
                "final_public_passed": True,
                "first_hidden_passed": False,
                "final_hidden_passed": True,
                "timed_out": False,
                "hidden_regression": False,
                "protected_test_violation": False,
                "cost": {"model_calls": 2, "total_tokens": 100},
            },
            {
                "strategy": "test-feedback",
                "first_public_passed": False,
                "final_public_passed": True,
                "first_hidden_passed": True,
                "final_hidden_passed": False,
                "timed_out": True,
                "hidden_regression": True,
                "protected_test_violation": False,
                "cost": {"model_calls": 3, "total_tokens": 150},
            },
        ]
    )

    metrics = report["strategies"]["test-feedback"]
    assert metrics["first_hidden_pass_rate"] == 0.5
    assert metrics["final_hidden_pass_rate"] == 0.5
    assert metrics["hidden_regression_rate"] == 0.5
    assert metrics["timeout_rate"] == 0.5
    assert metrics["model_calls"] == 5
    assert metrics["total_tokens"] == 250
