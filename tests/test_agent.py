import json
from collections.abc import Sequence
from pathlib import Path

import pytest

from repair_assistant.agent import MAX_ATTEMPTS, RepairStrategy, TestDrivenRepairAgent
from repair_assistant.event_log import EventLog
from repair_assistant.model import Message, ModelResponse, ToolCall, ToolDefinition
from repair_assistant.task import TaskSpec, capture_workspace_baseline
from repair_assistant.types import CommandResult


class FakeSandbox:
    def __init__(self, public_results: Sequence[CommandResult]) -> None:
        self.public_results = iter(public_results)
        self.commands: list[str] = []

    def start(self) -> None:
        pass

    def execute(self, command: str, *, cwd: str = ".", timeout_seconds: int = 120) -> CommandResult:
        del timeout_seconds
        self.commands.append(command)
        if command == "pytest-public":
            return next(self.public_results)
        return CommandResult(command, cwd, 0, "tool saw this\n", "", 1)

    def close(self) -> None:
        pass


class RecordingModel:
    def __init__(self, responses: Sequence[ModelResponse]) -> None:
        self.responses = iter(responses)
        self.requests: list[list[Message]] = []

    @property
    def name(self) -> str:
        return "recording-model"

    @property
    def provider(self) -> str:
        return "test"

    @property
    def sensitive_values(self) -> tuple[str, ...]:
        return ()

    def complete(
        self, messages: Sequence[Message], tools: Sequence[ToolDefinition]
    ) -> ModelResponse:
        del tools
        self.requests.append(list(messages))
        return next(self.responses)


def _result(code: int, output: str) -> CommandResult:
    return CommandResult("pytest-public", ".", code, output, "", 4)


def _build(
    tmp_path: Path,
    model: RecordingModel,
    sandbox: FakeSandbox,
    strategy: RepairStrategy,
) -> tuple[TestDrivenRepairAgent, TaskSpec, EventLog]:
    workspace = tmp_path / "workspace"
    tests = workspace / "tests"
    tests.mkdir(parents=True)
    (workspace / "solution.py").write_text("def f(): return 0\n", encoding="utf-8")
    (tests / "test_public.py").write_text("def test_x(): assert True\n", encoding="utf-8")
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    task = TaskSpec(
        "task-1",
        "Fix f",
        "Return one.",
        ("Do not edit tests",),
        "pytest-public",
        ("tests",),
        workspace,
        hidden,
        "pytest-hidden",
    )
    log = EventLog(tmp_path / "events.jsonl", run_id="run-1", task_id=task.task_id)
    agent = TestDrivenRepairAgent(
        model=model,
        sandbox=sandbox,
        event_log=log,
        workspace=workspace,
        workspace_baseline=capture_workspace_baseline(task, workspace),
        attempts_dir=tmp_path / "attempts",
        strategy=strategy,
    )
    return agent, task, log


def test_failed_pytest_feedback_updates_next_attempt_memory(tmp_path: Path) -> None:
    model = RecordingModel(
        [
            ModelResponse(content="first", usage={"total_tokens": 5}),
            ModelResponse(content="fixed", usage={"total_tokens": 7}),
        ]
    )
    sandbox = FakeSandbox([_result(1, "1 failed"), _result(0, "2 passed")])
    agent, task, log = _build(tmp_path, model, sandbox, RepairStrategy.TEST_FEEDBACK)

    result = agent.run(task)

    assert result.status == "public_tests_passed"
    assert len(result.attempts) == 2
    assert "1 failed" in json.dumps(model.requests[1])
    assert result.attempts[1].cost.total_tokens == 7
    assert sum(event["type"] == "feedback_added" for event in log.read()) == 1


def test_retry_without_feedback_has_fresh_memory(tmp_path: Path) -> None:
    model = RecordingModel([ModelResponse(content="first"), ModelResponse(content="second")])
    sandbox = FakeSandbox([_result(1, "private failure"), _result(0, "passed")])
    agent, task, _log = _build(tmp_path, model, sandbox, RepairStrategy.RETRY_WITHOUT_FEEDBACK)

    result = agent.run(task)

    assert len(result.attempts) == 2
    assert "private failure" not in json.dumps(model.requests[1])
    assert "first" not in json.dumps(model.requests[1])


def test_single_shot_forces_one_attempt(tmp_path: Path) -> None:
    model = RecordingModel([ModelResponse(content="done")])
    agent, task, _log = _build(
        tmp_path,
        model,
        FakeSandbox([_result(1, "failed")]),
        RepairStrategy.SINGLE_SHOT,
    )

    result = agent.run(task)

    assert result.status == "attempt_limit"
    assert len(result.attempts) == 1


def test_attempt_count_cannot_exceed_hard_limit(tmp_path: Path) -> None:
    model = RecordingModel([ModelResponse(content="done")])
    agent, _task, _log = _build(
        tmp_path,
        model,
        FakeSandbox([_result(1, "failed")]),
        RepairStrategy.TEST_FEEDBACK,
    )

    with pytest.raises(ValueError, match="max_attempts"):
        TestDrivenRepairAgent(
            model=agent.model,
            sandbox=agent.sandbox,
            event_log=agent.event_log,
            workspace=agent.workspace,
            workspace_baseline=agent.workspace_baseline,
            attempts_dir=agent.attempts_dir,
            strategy=RepairStrategy.TEST_FEEDBACK,
            max_attempts=MAX_ATTEMPTS + 1,
        )


def test_tool_result_is_returned_as_next_model_turn(tmp_path: Path) -> None:
    model = RecordingModel(
        [
            ModelResponse(
                content=None,
                tool_calls=(ToolCall("call-1", "shell", '{"command":"inspect"}'),),
                finish_reason="tool_calls",
            ),
            ModelResponse(content="done"),
        ]
    )
    sandbox = FakeSandbox([_result(0, "passed")])
    agent, task, _log = _build(tmp_path, model, sandbox, RepairStrategy.TEST_FEEDBACK)

    result = agent.run(task)

    tool_turn = next(message for message in model.requests[1] if message["role"] == "tool")
    assert "tool saw this" in tool_turn["content"]
    assert result.attempts[0].turns == 2
    assert (tmp_path / "attempts/attempt-1/solution.py").is_file()
