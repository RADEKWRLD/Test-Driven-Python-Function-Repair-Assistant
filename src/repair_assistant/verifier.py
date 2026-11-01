"""Deterministic public and hidden pytest verification; no LLM is involved."""

from __future__ import annotations

from pathlib import Path

from repair_assistant.cases import declared_cases, execute_cases
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
        collect_cases: bool = False,
    ) -> VerificationResult:
        before_protected = snapshot_paths(workspace, task.protected_paths)
        before_workspace = snapshot_workspace(workspace)
        before_policy_changes = unauthorized_workspace_changes(
            workspace_baseline.entries, before_workspace, task.editable_paths
        )
        cases: dict[str, str] = {}
        complete = False
        if collect_cases:
            result, cases, complete = execute_cases(
                sandbox,
                task.public_command,
                expected=declared_cases(workspace / "tests"),
                timeout_seconds=timeout_seconds,
            )
        else:
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
            result.exit_code == 0
            and not result.timed_out
            and not violations
            and (not collect_cases or (complete and all(v == "passed" for v in cases.values()))),
            result,
            protected_files_unchanged=protected_unchanged,
            workspace_policy_compliant=policy_compliant,
            violations=tuple(violations),
            cases=cases,
            case_results_complete=complete,
        )


class HiddenVerifier:
    """Run predeclared hidden tests in a sandbox where they are mounted read-only."""

    def verify(
        self,
        *,
        task: TaskSpec,
        sandbox: Sandbox,
        timeout_seconds: int = 120,
        collect_cases: bool = True,
    ) -> VerificationResult:
        if not collect_cases:
            result = sandbox.execute(task.hidden_command, timeout_seconds=timeout_seconds)
            return VerificationResult(result.exit_code == 0 and not result.timed_out, result)
        result, cases, complete = execute_cases(
            sandbox,
            task.hidden_command,
            expected=declared_cases(task.hidden_tests_dir),
            timeout_seconds=timeout_seconds,
        )
        return VerificationResult(
            result.exit_code == 0 and complete and all(v == "passed" for v in cases.values()),
            result,
            cases=cases,
            case_results_complete=complete,
        )
