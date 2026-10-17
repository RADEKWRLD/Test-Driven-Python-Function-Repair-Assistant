from collections import Counter
from pathlib import Path

import pytest

from repair_assistant.cli import _benchmark_schedule, _parser


def test_benchmark_schedule_repeats_every_pair_and_is_seeded() -> None:
    tasks = [Path("task-a"), Path("task-b")]
    strategies = ["single-shot", "retry-without-feedback", "test-feedback"]

    first = _benchmark_schedule(tasks, strategies, repetitions=2, seed=42)
    second = _benchmark_schedule(tasks, strategies, repetitions=2, seed=42)
    canonical = [
        (repetition, strategy, task)
        for repetition in (1, 2)
        for strategy in strategies
        for task in tasks
    ]

    assert first == second
    assert first != canonical
    assert Counter(first) == Counter(canonical)


def test_cli_rejects_more_than_five_attempts() -> None:
    with pytest.raises(SystemExit):
        _parser().parse_args(["run", "task", "--max-attempts", "6"])
