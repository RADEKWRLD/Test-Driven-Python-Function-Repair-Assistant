"""Versioned, user-supplied prices; no built-in or online price guesses."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any, cast


def token_count(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


@dataclass(frozen=True)
class Pricing:
    provider: str
    model: str
    effective_date: str
    currency: str
    input_per_million: float
    output_per_million: float
    cached_input_per_million: float | None = None

    @classmethod
    def load(cls, path: Path) -> Pricing:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("pricing must be a JSON object")
        pricing = cls(**raw)
        if pricing.input_per_million is None or pricing.output_per_million is None:
            raise ValueError(
                "input and output prices are required; do not use the placeholder template"
            )
        date.fromisoformat(pricing.effective_date)
        if not all((pricing.provider, pricing.model, pricing.currency)):
            raise ValueError("pricing requires provider, model and currency")
        for value in (
            pricing.input_per_million,
            pricing.output_per_million,
            pricing.cached_input_per_million,
        ):
            if value is not None and (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or value < 0
            ):
                raise ValueError("prices must be finite non-negative numbers")
        return pricing

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def estimate(
        self, usages: Sequence[Mapping[str, Any]], *, model: str, provider: str
    ) -> float | None:
        if model != self.model or provider != self.provider or not usages:
            return None
        total = 0.0
        for usage in usages:
            prompt = token_count(usage.get("prompt_tokens"))
            completion = token_count(usage.get("completion_tokens"))
            if prompt is None or completion is None:
                return None
            hit = token_count(usage.get("prompt_cache_hit_tokens"))
            details = usage.get("prompt_tokens_details")
            if hit is None and isinstance(details, Mapping):
                hit = token_count(details.get("cached_tokens"))
            if self.cached_input_per_million is not None and hit is None:
                return None
            hit = hit or 0
            if hit > prompt:
                return None
            miss = token_count(usage.get("prompt_cache_miss_tokens"))
            if miss is not None and miss + hit != prompt:
                return None
            cached_price = (
                self.cached_input_per_million
                if self.cached_input_per_million is not None
                else self.input_per_million
            )
            total += (
                (prompt - hit) * self.input_per_million
                + hit * cached_price
                + completion * self.output_per_million
            ) / 1_000_000
        return total


def usage_totals(usages: Sequence[Mapping[str, Any]]) -> dict[str, int | None]:
    result: dict[str, int | None] = {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        values = [token_count(usage.get(key)) for usage in usages]
        result[key] = (
            sum(cast(int, value) for value in values)
            if usages and all(value is not None for value in values)
            else None
        )
    return result
