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
        raise AssertionError(f"unexpected command: {command}")

    def close(self) -> None:
        pass


class RecordingModel:
    def __init__(self, responses: Sequence[ModelResponse]) -> None:
        self.responses = iter(responses)
        self.requests: list[list[Message]] = []
        self.tools: list[list[ToolDefinition]] = []

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
        self.requests.append(list(messages))
        self.tools.append(list(tools))
        return next(self.responses)


def _result(code: int, output: str) -> CommandResult:
    return CommandResult("pytest-public", ".", code, output, "", 4)


def _submission(content: str, *, tokens: int = 0) -> ModelResponse:
    return ModelResponse(
        content=None,
        tool_calls=(
            ToolCall(
                "submission-1",
                "submit_solution",
                json.dumps({"content": content}),
            ),
        ),
        finish_reason="tool_calls",
        usage={"total_tokens": tokens},
    )


def _build(
    tmp_path: Path,
    model: RecordingModel,
    sandbox: FakeSandbox | None,
    strategy: RepairStrategy,
    *,
    max_attempts: int = 2,
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
        max_attempts=max_attempts,
    )
    return agent, task, log


def test_feedback_arm_runs_pytest_and_exposes_failure_next_attempt(tmp_path: Path) -> None:
    model = RecordingModel(
        [
            _submission("def f(): return 0\n", tokens=5),
            _submission("def f(): return 1\n", tokens=7),
        ]
    )
    sandbox = FakeSandbox([_result(1, "1 failed"), _result(0, "2 passed")])
    agent, task, log = _build(tmp_path, model, sandbox, RepairStrategy.TEST_FEEDBACK)

    result = agent.run(task)

    assert result.status == "public_tests_passed"
    assert len(result.attempts) == 2
    assert sandbox.commands == ["pytest-public", "pytest-public"]
    assert "1 failed" in json.dumps(model.requests[1])
    assert result.attempts[1].cost.total_tokens == 7
    assert sum(event["type"] == "feedback_added" for event in log.read()) == 1


def test_retry_arm_uses_pytest_to_stop_but_never_receives_diagnostics(tmp_path: Path) -> None:
    model = RecordingModel([_submission("def f(): return 0\n"), _submission("def f(): return 1\n")])
    sandbox = FakeSandbox([_result(1, "private failure"), _result(0, "passed")])
    agent, task, log = _build(tmp_path, model, sandbox, RepairStrategy.RETRY_WITHOUT_FEEDBACK)

    result = agent.run(task)

    assert result.status == "public_tests_passed"
    assert len(result.attempts) == 2
    assert sandbox.commands == ["pytest-public", "pytest-public"]
    assert "private failure" not in json.dumps(model.requests[1])
    assert "another repair attempt" in json.dumps(model.requests[1])
    assert not any(event["type"] == "feedback_added" for event in log.read())
    assert all(attempt.repair_verification is not None for attempt in result.attempts)
    assert "def f(): return 1" in (tmp_path / "workspace/solution.py").read_text()


def test_single_shot_submits_once_without_running_pytest(tmp_path: Path) -> None:
    model = RecordingModel([_submission("def f(): return 1\n")])
    sandbox = FakeSandbox([_result(1, "failed")])
    agent, task, _log = _build(tmp_path, model, sandbox, RepairStrategy.SINGLE_SHOT)

    result = agent.run(task)

    assert result.status == "single_submission_complete"
    assert len(result.attempts) == 1
    assert sandbox.commands == []
    assert result.attempts[0].turns == 1


def test_only_submit_solution_tool_is_available(tmp_path: Path) -> None:
    model = RecordingModel([_submission("def f(): return 1\n")])
    agent, task, _log = _build(tmp_path, model, None, RepairStrategy.SINGLE_SHOT)

    agent.run(task)

    assert [tool["function"]["name"] for tool in model.tools[0]] == ["submit_solution"]
    request = json.dumps(model.requests[0])
    assert "Current solution.py" in request
    assert "test_public.py" in request


def test_shell_submission_is_rejected_and_cannot_execute(tmp_path: Path) -> None:
    model = RecordingModel(
        [
            ModelResponse(
                content=None,
                tool_calls=(ToolCall("call-1", "shell", '{"command":"pytest"}'),),
                finish_reason="tool_calls",
            )
        ]
    )
    sandbox = FakeSandbox([])
    agent, task, _log = _build(tmp_path, model, sandbox, RepairStrategy.SINGLE_SHOT)

    result = agent.run(task)

    assert result.attempts[0].status == "model_protocol_error"
    assert sandbox.commands == []
    assert (tmp_path / "workspace/solution.py").read_text() == "def f(): return 0\n"


def test_attempt_count_cannot_exceed_hard_limit(tmp_path: Path) -> None:
    model = RecordingModel([_submission("def f(): return 1\n")])
    agent, _task, _log = _build(tmp_path, model, None, RepairStrategy.SINGLE_SHOT)

    with pytest.raises(ValueError, match="max_attempts"):
        TestDrivenRepairAgent(
            model=agent.model,
            sandbox=None,
            event_log=agent.event_log,
            workspace=agent.workspace,
            workspace_baseline=agent.workspace_baseline,
            attempts_dir=agent.attempts_dir,
            strategy=RepairStrategy.RETRY_WITHOUT_FEEDBACK,
            max_attempts=MAX_ATTEMPTS + 1,
        )
