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


def test_removed_multi_turn_option_is_rejected() -> None:
    with pytest.raises(SystemExit):
        _parser().parse_args(["run", "task", "--max-turns", "12"])


def test_report_command_accepts_an_existing_report_path() -> None:
    args = _parser().parse_args(["report", "benchmark.json", "--output-dir", "visuals"])

    assert args.command == "report"
    assert args.report_json == Path("benchmark.json")
    assert args.output_dir == Path("visuals")
