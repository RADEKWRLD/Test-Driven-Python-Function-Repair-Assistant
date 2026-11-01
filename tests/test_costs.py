from repair_assistant.costs import Pricing, usage_totals


def test_cached_pricing_and_unknown_usage() -> None:
    prices = Pricing("test", "model", "2026-10-21", "CNY", 2.0, 4.0, 0.5)
    usage = {
        "prompt_tokens": 1_000_000,
        "completion_tokens": 500_000,
        "prompt_cache_hit_tokens": 400_000,
        "prompt_cache_miss_tokens": 600_000,
    }
    assert prices.estimate([usage], model="model", provider="test") == 3.4
    assert prices.estimate([{}], model="model", provider="test") is None
    assert prices.estimate([usage], model="other", provider="test") is None
    missing_cache = {"prompt_tokens": 100, "completion_tokens": 10}
    assert prices.estimate([missing_cache], model="model", provider="test") is None
    assert usage_totals([{"prompt_tokens": 0}, {}])["prompt_tokens"] is None
    assert usage_totals([])["total_tokens"] is None
