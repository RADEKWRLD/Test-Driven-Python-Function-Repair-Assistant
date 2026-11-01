from collections import Counter
from pathlib import Path

import pytest

from repair_assistant.cli import _benchmark_schedule, _events, _model_adapter, _parser
from repair_assistant.event_log import EventLog
from repair_assistant.model import DeepSeekAdapter


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


def test_cli_rejects_more_than_three_attempts() -> None:
    with pytest.raises(SystemExit):
        _parser().parse_args(["run", "task", "--max-attempts", "4"])


def test_v4_defaults_and_resume_options() -> None:
    args = _parser().parse_args(["benchmark", "--resume", "experiment"])
    assert args.max_attempts == 3
    assert args.tasks_dir == Path("benchmarks/feedbackeval-humaneval-full")
    assert args.resume == Path("experiment")
    assert args.repetitions == 1


def test_removed_multi_turn_option_is_rejected() -> None:
    with pytest.raises(SystemExit):
        _parser().parse_args(["run", "task", "--max-turns", "12"])


def test_report_command_accepts_an_existing_report_path() -> None:
    args = _parser().parse_args(["report", "benchmark.json", "--output-dir", "visuals"])

    assert args.command == "report"
    assert args.report_json == Path("benchmark.json")
    assert args.output_dir == Path("visuals")


def test_removed_dataset_import_and_advanced_retry_commands_are_rejected() -> None:
    for command in (["import-humanevalpack"], ["benchmark", "--retry-errors"]):
        with pytest.raises(SystemExit):
            _parser().parse_args(command)


def test_deepseek_model_limits_are_configurable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setenv("REPAIR_ASSISTANT_BASE_URL", "https://deepseek.example/v1")
    monkeypatch.setenv("REPAIR_ASSISTANT_MODEL_TIMEOUT_SECONDS", "321")
    monkeypatch.setenv("REPAIR_ASSISTANT_MAX_TOKENS", "1024")

    adapter = _model_adapter("deepseek-chat")

    assert isinstance(adapter, DeepSeekAdapter)
    assert adapter.base_url == "https://deepseek.example/v1"
    assert adapter.timeout_seconds == 321
    assert adapter.max_tokens == 1024


@pytest.mark.parametrize("group", ["", "group_c"])
def test_events_finds_legacy_and_grouped_logs(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], group: str
) -> None:
    path = tmp_path / "runs" / group / "20261031_001" / "events.jsonl"
    EventLog(path, run_id="20261031_001", task_id="task").append("test_event", "controller", {})
    args = _parser().parse_args(["events", "20261031_001", "--data-dir", str(tmp_path)])
    assert _events(args) == 0
    assert "test_event" in capsys.readouterr().out
