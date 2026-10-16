"""Deterministic public and hidden pytest verification; no LLM is involved."""

from __future__ import annotations

from pathlib import Path

from repair_assistant.sandbox import Sandbox
from repair_assistant.task import TaskSpec, snapshot_paths
from repair_assistant.types import VerificationResult


class PublicVerifier:
    def verify(
        self,
        *,
        task: TaskSpec,
        sandbox: Sandbox,
        workspace: Path,
        protected_baseline: dict[str, str],
        timeout_seconds: int = 120,
    ) -> VerificationResult:
        current = snapshot_paths(workspace, task.protected_paths)
        violations: list[str] = []
        if current != protected_baseline:
            violations.append("protected public tests were added, removed, or modified")
        result = sandbox.execute(task.public_command, timeout_seconds=timeout_seconds)
        return VerificationResult(
            result.exit_code == 0 and not violations,
            result,
            not violations,
            tuple(violations),
        )


class HiddenVerifier:
    """Run predeclared hidden tests in a sandbox where they are mounted read-only."""

    def verify(
        self,
        *,
        task: TaskSpec,
        sandbox: Sandbox,
        timeout_seconds: int = 120,
    ) -> VerificationResult:
        result = sandbox.execute(task.hidden_command, timeout_seconds=timeout_seconds)
        return VerificationResult(result.exit_code == 0, result)
