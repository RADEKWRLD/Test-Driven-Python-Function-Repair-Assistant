"""Shared immutable result types."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CommandResult:
    command: str
    cwd: str
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: int
    timed_out: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class VerificationResult:
    passed: bool
    command_result: CommandResult
    protected_files_unchanged: bool = True
    workspace_policy_compliant: bool = True
    violations: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "command_result": self.command_result.to_dict(),
            "protected_files_unchanged": self.protected_files_unchanged,
            "workspace_policy_compliant": self.workspace_policy_compliant,
            "violations": list(self.violations),
        }
