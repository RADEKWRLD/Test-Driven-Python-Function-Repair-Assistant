"""Deterministic public and hidden pytest verification; no LLM is involved."""

from __future__ import annotations

from pathlib import Path

from repair_assistant.sandbox import Sandbox
from repair_assistant.task import (
    TaskSpec,
    WorkspaceBaseline,
    snapshot_paths,
    snapshot_workspace,
    unauthorized_workspace_changes,
)
from repair_assistant.types import VerificationResult


class PublicVerifier:
    def verify(
        self,
        *,
        task: TaskSpec,
        sandbox: Sandbox,
        workspace: Path,
        workspace_baseline: WorkspaceBaseline,
        timeout_seconds: int = 120,
    ) -> VerificationResult:
        before_protected = snapshot_paths(workspace, task.protected_paths)
        before_workspace = snapshot_workspace(workspace)
        before_policy_changes = unauthorized_workspace_changes(
            workspace_baseline.entries, before_workspace, task.editable_paths
        )
        result = sandbox.execute(task.public_command, timeout_seconds=timeout_seconds)
        after_protected = snapshot_paths(workspace, task.protected_paths)
        after_workspace = snapshot_workspace(workspace)
        after_policy_changes = unauthorized_workspace_changes(
            workspace_baseline.entries, after_workspace, task.editable_paths
        )

        violations: list[str] = []
        protected_unchanged = (
            before_protected == workspace_baseline.protected
            and after_protected == workspace_baseline.protected
        )
        if not protected_unchanged:
            violations.append("protected public tests were added, removed, or modified")
        policy_changes = tuple(dict.fromkeys((*before_policy_changes, *after_policy_changes)))
        violations.extend(policy_changes)
        policy_compliant = not policy_changes
        return VerificationResult(
            result.exit_code == 0 and not violations,
            result,
            protected_files_unchanged=protected_unchanged,
            workspace_policy_compliant=policy_compliant,
            violations=tuple(violations),
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
