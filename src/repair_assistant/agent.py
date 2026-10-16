"""Bounded test-driven Agent loop."""

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

SYSTEM_PROMPT = """You are a test-driven Python function repair agent in an isolated workspace.
Solve only the supplied short pure-function task. Use the shell tool for every file
inspection, edit, and command. You may run the declared public pytest command. Never
modify tests or attempt to find hidden tests. Preserve behavior not contradicted by
the requirement or public tests. When your patch is ready, stop calling tools and
briefly report the change. A deterministic controller will independently run pytest.
"""

SHELL_TOOL: ToolDefinition = {
    "type": "function",
    "function": {
        "name": "shell",
        "description": "Run one Bash command inside the isolated task workspace.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "cwd": {"type": "string"},
                "timeout_seconds": {"type": "integer", "minimum": 1, "maximum": 300},
            },
            "required": ["command"],
            "additionalProperties": False,
        },
    },
}


class RepairStrategy(StrEnum):
    SINGLE_SHOT = "single-shot"
    RETRY_WITHOUT_FEEDBACK = "retry-without-feedback"
    TEST_FEEDBACK = "test-feedback"


MAX_ATTEMPTS = 3


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
    public_verification: VerificationResult
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
    """Submit a patch, verify it, and optionally add failure evidence to memory."""

    __test__ = False

    def __init__(
        self,
        *,
        model: ModelAdapter,
        sandbox: Sandbox,
        event_log: EventLog,
        workspace: Path,
        workspace_baseline: WorkspaceBaseline,
        attempts_dir: Path,
        strategy: RepairStrategy,
        max_attempts: int = 3,
        max_turns_per_attempt: int = 12,
        verifier: PublicVerifier | None = None,
    ) -> None:
        if not 1 <= max_attempts <= MAX_ATTEMPTS:
            raise ValueError(f"max_attempts must be from 1 to {MAX_ATTEMPTS}")
        if max_turns_per_attempt < 1:
            raise ValueError("attempt and turn limits must be positive")
        self.model = model
        self.sandbox = sandbox
        self.event_log = event_log
        self.workspace = workspace.resolve()
        self.workspace_baseline = workspace_baseline
        self.attempts_dir = attempts_dir.resolve()
        self.strategy = strategy
        self.max_attempts = 1 if strategy is RepairStrategy.SINGLE_SHOT else max_attempts
        self.max_turns = max_turns_per_attempt
        self.verifier = verifier or PublicVerifier()

    def run(self, task: TaskSpec) -> AgentResult:
        base_messages: list[Message] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task.prompt()},
        ]
        messages = list(base_messages)
        attempts: list[AttemptResult] = []
        self.event_log.append("user_message", "user", {"content": task.prompt()})

        for number in range(1, self.max_attempts + 1):
            if number > 1 and self.strategy is RepairStrategy.RETRY_WITHOUT_FEEDBACK:
                messages = [
                    *base_messages,
                    {
                        "role": "user",
                        "content": (
                            "Make another independent repair attempt in the current workspace. "
                            "The controller supplies no previous test output."
                        ),
                    },
                ]
            self.event_log.append(
                "attempt_started",
                "controller",
                {"attempt": number, "strategy": self.strategy.value},
            )
            status, turns, final_message, cost = self._model_attempt(messages, number)
            verification = self.verifier.verify(
                task=task,
                sandbox=self.sandbox,
                workspace=self.workspace,
                workspace_baseline=self.workspace_baseline,
            )
            snapshot = self._snapshot(number)
            self.event_log.append(
                "public_verification",
                "verifier",
                {"attempt": number, **verification.to_dict()},
            )
            self.event_log.append(
                "attempt_completed",
                "controller",
                {
                    "attempt": number,
                    "status": status,
                    "turns": turns,
                    "cost": cost.to_dict(),
                    "snapshot": str(snapshot.relative_to(self.attempts_dir.parent)),
                },
            )
            attempt = AttemptResult(
                number, status, turns, final_message, verification, cost, snapshot
            )
            attempts.append(attempt)
            if verification.passed:
                return AgentResult("public_tests_passed", self.strategy, tuple(attempts))
            if number < self.max_attempts and self.strategy is RepairStrategy.TEST_FEEDBACK:
                feedback = _feedback(verification, number)
                messages.append({"role": "user", "content": feedback})
                self.event_log.append(
                    "feedback_added", "controller", {"attempt": number, "content": feedback}
                )

        return AgentResult("attempt_limit", self.strategy, tuple(attempts))

    def _model_attempt(
        self, messages: list[Message], attempt: int
    ) -> tuple[str, int, str | None, AttemptCost]:
        calls = prompt = completion = total = latency = 0
        secrets = self.model.sensitive_values
        for turn in range(1, self.max_turns + 1):
            self.event_log.append(
                "model_request",
                "controller",
                {
                    "attempt": attempt,
                    "turn": turn,
                    "model": self.model.name,
                    "messages": redact(messages, secrets=secrets),
                    "tools": [SHELL_TOOL],
                    "redaction": {"applied": True, "marker": REDACTED},
                },
            )
            started = time.monotonic()
            response = self.model.complete(messages, [SHELL_TOOL])
            elapsed = round((time.monotonic() - started) * 1000)
            calls += 1
            latency += elapsed
            prompt += _usage(response.usage, "prompt_tokens")
            completion += _usage(response.usage, "completion_tokens")
            total += _usage(response.usage, "total_tokens")
            self.event_log.append(
                "model_response",
                "model",
                {
                    "attempt": attempt,
                    "turn": turn,
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
            messages.append(response.as_message())
            cost = AttemptCost(calls, prompt, completion, total, latency)
            if not response.tool_calls:
                status = (
                    "model_finished" if response.finish_reason == "stop" else "model_incomplete"
                )
                return status, turn, response.content, cost
            if response.finish_reason != "tool_calls":
                return "model_protocol_error", turn, response.content, cost
            for tool_call in response.tool_calls:
                content = self._execute_tool(
                    tool_call.name, tool_call.arguments_json, tool_call.call_id
                )
                messages.append(
                    {"role": "tool", "tool_call_id": tool_call.call_id, "content": content}
                )
        return (
            "turn_limit",
            self.max_turns,
            None,
            AttemptCost(calls, prompt, completion, total, latency),
        )

    def _execute_tool(self, name: str, arguments_json: str, call_id: str) -> str:
        self.event_log.append(
            "tool_call",
            "model",
            redact(
                {"call_id": call_id, "name": name, "arguments": arguments_json},
                secrets=self.model.sensitive_values,
            ),
        )
        try:
            arguments = cast(dict[str, Any], json.loads(arguments_json))
            if name != "shell":
                raise ValueError(f"unknown tool: {name}")
            command = arguments.get("command")
            cwd = arguments.get("cwd", ".")
            timeout = arguments.get("timeout_seconds", 120)
            if not isinstance(command, str) or not command.strip():
                raise ValueError("shell.command must be a non-empty string")
            if not isinstance(cwd, str):
                raise ValueError("shell.cwd must be a string")
            if not isinstance(timeout, int) or isinstance(timeout, bool) or not 1 <= timeout <= 300:
                raise ValueError("timeout_seconds must be an integer from 1 to 300")
        except (json.JSONDecodeError, ValueError) as exc:
            payload = {"call_id": call_id, "accepted": False, "error": str(exc)}
            self.event_log.append("tool_result", "tool", payload)
            return json.dumps(payload, ensure_ascii=False)
        result = self.sandbox.execute(command, cwd=cwd, timeout_seconds=timeout)
        payload = {"call_id": call_id, "accepted": True, **result.to_dict()}
        safe_payload = cast(dict[str, Any], redact(payload, secrets=self.model.sensitive_values))
        self.event_log.append("tool_result", "tool", safe_payload)
        return json.dumps(safe_payload, ensure_ascii=False)

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
        "Repair the implementation without modifying tests."
    )


def _usage(usage: dict[str, Any], key: str) -> int:
    value = usage.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) else 0
