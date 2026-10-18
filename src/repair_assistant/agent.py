"""Bounded repair protocol with a single, non-executable submission tool."""

from __future__ import annotations

import json
import shutil
import time
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, cast

from repair_assistant.event_log import EventLog
from repair_assistant.model import Message, ModelAdapter, ToolDefinition
from repair_assistant.redaction import REDACTED, redact
from repair_assistant.sandbox import Sandbox
from repair_assistant.task import TaskSpec, WorkspaceBaseline, snapshot_workspace
from repair_assistant.types import VerificationResult
from repair_assistant.verifier import PublicVerifier

SYSTEM_PROMPT = """You repair one short Python pure-function implementation.
You cannot inspect files, execute commands, or run tests. The controller gives you the
requirement, current solution.py, and public test source. Submit exactly one complete
replacement for solution.py by calling submit_solution once. Do not include tests or
create any other file. Preserve behavior not contradicted by the requirement or public
tests. Hidden tests are unavailable.
"""

SUBMIT_SOLUTION_TOOL: ToolDefinition = {
    "type": "function",
    "function": {
        "name": "submit_solution",
        "description": "Submit the complete replacement content of solution.py.",
        "parameters": {
            "type": "object",
            "properties": {"content": {"type": "string"}},
            "required": ["content"],
            "additionalProperties": False,
        },
    },
}


class RepairStrategy(StrEnum):
    SINGLE_SHOT = "single-shot"
    RETRY_WITHOUT_FEEDBACK = "retry-without-feedback"
    TEST_FEEDBACK = "test-feedback"


MAX_ATTEMPTS = 5
MAX_SOLUTION_BYTES = 64 * 1024


@dataclass(frozen=True, slots=True)
class AttemptCost:
    model_calls: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_ms: int

    def to_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AttemptResult:
    number: int
    status: str
    turns: int
    final_message: str | None
    repair_verification: VerificationResult | None
    cost: AttemptCost
    snapshot: Path


@dataclass(frozen=True, slots=True)
class AgentResult:
    status: str
    strategy: RepairStrategy
    attempts: tuple[AttemptResult, ...]

    @property
    def final_attempt(self) -> AttemptResult:
        return self.attempts[-1]


class TestDrivenRepairAgent:
    """Collect bounded submissions while exposing diagnostics only to the feedback arm."""

    __test__ = False

    def __init__(
        self,
        *,
        model: ModelAdapter,
        sandbox: Sandbox | None,
        event_log: EventLog,
        workspace: Path,
        workspace_baseline: WorkspaceBaseline,
        attempts_dir: Path,
        strategy: RepairStrategy,
        max_attempts: int = MAX_ATTEMPTS,
        verifier: PublicVerifier | None = None,
    ) -> None:
        if not 1 <= max_attempts <= MAX_ATTEMPTS:
            raise ValueError(f"max_attempts must be from 1 to {MAX_ATTEMPTS}")
        if strategy is not RepairStrategy.SINGLE_SHOT and sandbox is None:
            raise ValueError("multi-attempt strategies require a public-test sandbox")
        self.model = model
        self.sandbox = sandbox
        self.event_log = event_log
        self.workspace = workspace.resolve()
        self.workspace_baseline = workspace_baseline
        self.attempts_dir = attempts_dir.resolve()
        self.strategy = strategy
        self.max_attempts = 1 if strategy is RepairStrategy.SINGLE_SHOT else max_attempts
        self.verifier = verifier or PublicVerifier()

    def run(self, task: TaskSpec) -> AgentResult:
        if task.editable_paths != ("solution.py",):
            raise ValueError("the repair protocol requires editable_paths to be only solution.py")

        attempts: list[AttemptResult] = []
        previous_feedback: str | None = None
        self.event_log.append("user_message", "user", {"content": task.prompt()})

        for number in range(1, self.max_attempts + 1):
            messages: list[Message] = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": self._attempt_prompt(task, number, previous_feedback),
                },
            ]
            self.event_log.append(
                "attempt_started",
                "controller",
                {"attempt": number, "strategy": self.strategy.value},
            )
            status, final_message, cost = self._model_submission(messages, number)

            verification: VerificationResult | None = None
            if self.strategy is not RepairStrategy.SINGLE_SHOT:
                assert self.sandbox is not None
                verification = self.verifier.verify(
                    task=task,
                    sandbox=self.sandbox,
                    workspace=self.workspace,
                    workspace_baseline=self.workspace_baseline,
                )
                self.event_log.append(
                    "repair_public_verification",
                    "verifier",
                    {"attempt": number, **verification.to_dict()},
                )

            snapshot = self._snapshot(number)
            self.event_log.append(
                "attempt_completed",
                "controller",
                {
                    "attempt": number,
                    "status": status,
                    "turns": 1,
                    "cost": cost.to_dict(),
                    "repair_public_test_run": verification is not None,
                    "detailed_feedback_enabled": self.strategy is RepairStrategy.TEST_FEEDBACK,
                    "snapshot": str(snapshot.relative_to(self.attempts_dir.parent)),
                },
            )
            attempts.append(
                AttemptResult(number, status, 1, final_message, verification, cost, snapshot)
            )

            if verification is not None and verification.passed:
                return AgentResult("public_tests_passed", self.strategy, tuple(attempts))
            if (
                verification is not None
                and number < self.max_attempts
                and self.strategy is RepairStrategy.TEST_FEEDBACK
            ):
                previous_feedback = _feedback(verification, number)
                self.event_log.append(
                    "feedback_added",
                    "controller",
                    {"attempt": number, "content": previous_feedback},
                )

        status = "attempt_limit"
        if self.strategy is RepairStrategy.SINGLE_SHOT:
            status = "single_submission_complete"
        elif self.strategy is RepairStrategy.RETRY_WITHOUT_FEEDBACK:
            status = "retry_budget_complete"
        return AgentResult(status, self.strategy, tuple(attempts))

    def _model_submission(
        self, messages: list[Message], attempt: int
    ) -> tuple[str, str | None, AttemptCost]:
        secrets = self.model.sensitive_values
        self.event_log.append(
            "model_request",
            "controller",
            {
                "attempt": attempt,
                "turn": 1,
                "model": self.model.name,
                "messages": redact(messages, secrets=secrets),
                "tools": [SUBMIT_SOLUTION_TOOL],
                "redaction": {"applied": True, "marker": REDACTED},
            },
        )
        started = time.monotonic()
        response = self.model.complete(messages, [SUBMIT_SOLUTION_TOOL])
        elapsed = round((time.monotonic() - started) * 1000)
        cost = AttemptCost(
            1,
            _usage(response.usage, "prompt_tokens"),
            _usage(response.usage, "completion_tokens"),
            _usage(response.usage, "total_tokens"),
            elapsed,
        )
        self.event_log.append(
            "model_response",
            "model",
            {
                "attempt": attempt,
                "turn": 1,
                "provider": response.provider,
                "requested_model": self.model.name,
                "resolved_model": response.model,
                "response_id": response.response_id,
                "finish_reason": response.finish_reason,
                "latency_ms": elapsed,
                "content": redact(response.content, secrets=secrets),
                "tool_calls": redact(
                    [tool_call.to_dict() for tool_call in response.tool_calls], secrets=secrets
                ),
                "usage": response.usage,
            },
        )

        if len(response.tool_calls) != 1:
            return "model_protocol_error", response.content, cost
        tool_call = response.tool_calls[0]
        self.event_log.append(
            "tool_call",
            "model",
            redact(tool_call.to_dict(), secrets=secrets),
        )
        try:
            if tool_call.name != "submit_solution":
                raise ValueError(f"unknown tool: {tool_call.name}")
            arguments = cast(dict[str, Any], json.loads(tool_call.arguments_json))
            if set(arguments) != {"content"} or not isinstance(arguments["content"], str):
                raise ValueError("submit_solution requires only a string content field")
            content = arguments["content"]
            if len(content.encode("utf-8")) > MAX_SOLUTION_BYTES:
                raise ValueError(f"solution.py exceeds {MAX_SOLUTION_BYTES} bytes")
            target = self.workspace / "solution.py"
            if not target.is_file() or target.is_symlink():
                raise ValueError("solution.py must remain an existing regular file")
            target.write_text(content, encoding="utf-8")
        except (json.JSONDecodeError, UnicodeError, ValueError) as exc:
            self.event_log.append(
                "submission_rejected",
                "controller",
                {"attempt": attempt, "error": str(exc)},
            )
            return "model_protocol_error", response.content, cost
        self.event_log.append(
            "submission_accepted",
            "controller",
            {"attempt": attempt, "path": "solution.py", "bytes": len(content.encode("utf-8"))},
        )
        return "solution_submitted", response.content, cost

    def _attempt_prompt(self, task: TaskSpec, attempt: int, previous_feedback: str | None) -> str:
        current = (self.workspace / "solution.py").read_text(encoding="utf-8")
        public_sources = _public_test_sources(task, self.workspace)
        retry_note = ""
        if attempt > 1:
            retry_note = (
                "\nThis is another repair attempt. Reconsider the current implementation "
                "and submit a complete replacement.\n"
            )
        feedback = f"\n{previous_feedback}\n" if previous_feedback is not None else ""
        return (
            f"{task.prompt()}\n{retry_note}"
            f"\nCurrent solution.py:\n```python\n{current}\n```\n"
            f"\nPublic test source (read-only):\n{public_sources}\n"
            f"{feedback}"
        )

    def _snapshot(self, attempt: int) -> Path:
        destination = self.attempts_dir / f"attempt-{attempt}"
        if destination.exists():
            raise FileExistsError(f"attempt snapshot already exists: {destination}")
        shutil.copytree(
            self.workspace,
            destination,
            symlinks=True,
            ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc"),
        )
        manifest = snapshot_workspace(destination)
        self.event_log.append(
            "snapshot_created", "controller", {"attempt": attempt, "files": manifest}
        )
        return destination


def _public_test_sources(task: TaskSpec, workspace: Path) -> str:
    sections: list[str] = []
    for raw in task.protected_paths:
        target = workspace / raw
        paths = [target] if target.is_file() else sorted(target.rglob("*.py"))
        for path in paths:
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(workspace).as_posix()
            sections.append(f"### {relative}\n```python\n{path.read_text(encoding='utf-8')}\n```")
    return "\n\n".join(sections) or "(no public test source declared)"


def _feedback(result: VerificationResult, attempt: int) -> str:
    command = result.command_result
    violations = "\n".join(f"- {item}" for item in result.violations) or "- none"
    return (
        f"Deterministic public pytest feedback for attempt {attempt}:\n"
        f"exit_code={command.exit_code}\n"
        f"timed_out={command.timed_out}\n"
        f"protected_files_unchanged={result.protected_files_unchanged}\n"
        f"workspace_policy_compliant={result.workspace_policy_compliant}\n"
        f"violations:\n{violations}\nstdout:\n{command.stdout}\nstderr:\n{command.stderr}\n"
        "Repair solution.py without changing tests."
    )


def _usage(usage: dict[str, Any], key: str) -> int:
    value = usage.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) else 0
