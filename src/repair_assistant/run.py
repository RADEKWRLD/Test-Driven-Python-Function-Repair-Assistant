"""End-to-end orchestration for one controlled repair experiment."""

from __future__ import annotations

import json
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from repair_assistant.agent import (
    MAX_ATTEMPTS,
    PROTOCOL_NAME,
    PROTOCOL_VERSION,
    AgentResult,
    RepairStrategy,
    TestDrivenRepairAgent,
)
from repair_assistant.cases import compare_cases
from repair_assistant.costs import Pricing, usage_totals
from repair_assistant.event_log import EventLog
from repair_assistant.model import ModelAdapter, ModelAdapterError
from repair_assistant.output_paths import create_run_directory, grouped_run_directory
from repair_assistant.redaction import redact
from repair_assistant.sandbox import DockerSandbox, DockerSandboxError
from repair_assistant.task import TaskSpec, WorkspaceBaseline, prepare_workspace
from repair_assistant.types import VerificationResult
from repair_assistant.verifier import HiddenVerifier, PublicVerifier


@dataclass(frozen=True, slots=True)
class RunResult:
    run_id: str
    run_dir: Path
    outcome: str
    agent: AgentResult
    first_public: VerificationResult
    final_public: VerificationResult
    first_hidden: VerificationResult
    final_hidden: VerificationResult
    baseline_hidden: VerificationResult


class RunExecutionError(RuntimeError):
    def __init__(self, summary: dict[str, object]) -> None:
        super().__init__(str(summary.get("error_message", "run failed")))
        self.summary = summary


class RunService:
    def __init__(
        self,
        *,
        data_dir: Path,
        image: str = "function-repair/sandbox-python:dev",
        pricing: Pricing | None = None,
    ) -> None:
        self.data_dir = data_dir.resolve()
        self.image = image
        self.pricing = pricing

    def execute(
        self,
        *,
        task: TaskSpec,
        model: ModelAdapter,
        strategy: RepairStrategy = RepairStrategy.TEST_FEEDBACK,
        max_attempts: int = MAX_ATTEMPTS,
        run_id: str | None = None,
    ) -> RunResult:
        if not 1 <= max_attempts <= MAX_ATTEMPTS:
            raise ValueError(f"max_attempts must be from 1 to {MAX_ATTEMPTS}")
        run_id = run_id or create_run_directory(self.data_dir, strategy.value).name
        run_dir = grouped_run_directory(self.data_dir, strategy.value, run_id)
        started = time.monotonic()
        try:
            return self._execute(
                task=task,
                model=model,
                strategy=strategy,
                max_attempts=max_attempts,
                run_id=run_id,
                started=started,
            )
        except (Exception, KeyboardInterrupt) as exc:
            status = (
                "interrupted"
                if isinstance(exc, KeyboardInterrupt)
                else (
                    "sandbox_error"
                    if isinstance(exc, DockerSandboxError)
                    else "model_error"
                    if isinstance(exc, ModelAdapterError)
                    else "timeout"
                    if isinstance(exc, TimeoutError)
                    else "execution_error"
                )
            )
            log = EventLog(run_dir / "events.jsonl", run_id=run_id, task_id=task.task_id)
            events = list(log.read()) if log.path.exists() else []
            summary: dict[str, object] = {
                "schema_version": 3,
                "run_id": run_id,
                "task_id": task.task_id,
                "outcome": "error",
                "status": status,
                "strategy": strategy.value,
                "model": model.name,
                "provider": model.provider,
                "protocol": {"version": PROTOCOL_VERSION, "name": PROTOCOL_NAME},
                "error_type": type(exc).__name__,
                "error_message": redact(str(exc), secrets=model.sensitive_values),
                "failure_stage": events[-1]["type"] if events else "prepare_workspace",
                "duration_ms": round((time.monotonic() - started) * 1000),
                "cost": _event_cost(events, model, self.pricing),
            }
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "summary.json").write_text(
                json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            log.append("run_error", "controller", summary)
            if isinstance(exc, KeyboardInterrupt):
                raise
            raise RunExecutionError(summary) from exc

    def _execute(
        self,
        *,
        task: TaskSpec,
        model: ModelAdapter,
        strategy: RepairStrategy,
        max_attempts: int,
        run_id: str,
        started: float,
    ) -> RunResult:
        run_dir = grouped_run_directory(self.data_dir, strategy.value, run_id)
        workspace = run_dir / "workspace"
        workspace_baseline = prepare_workspace(task, workspace)
        baseline_snapshot = run_dir / "original_code"
        shutil.copytree(workspace, baseline_snapshot, symlinks=True)
        log = EventLog(run_dir / "events.jsonl", run_id=run_id, task_id=task.task_id)
        log.append(
            "run_started",
            "controller",
            {
                "protocol_version": PROTOCOL_VERSION,
                "strategy": strategy.value,
                "model": model.name,
                "provider": model.provider,
                "image": self.image,
                "thinking_mode": "disabled"
                if model.provider == "deepseek"
                else "server-controlled",
                "network": "none",
                "max_attempts": 1 if strategy is RepairStrategy.SINGLE_SHOT else max_attempts,
                "model_calls_per_attempt": 1,
                "repair_pytest_enabled": strategy is not RepairStrategy.SINGLE_SHOT,
                "detailed_test_feedback_enabled": strategy is RepairStrategy.TEST_FEEDBACK,
            },
        )
        repair_sandbox = None
        if strategy is not RepairStrategy.SINGLE_SHOT:
            repair_sandbox = DockerSandbox(
                workspace=workspace,
                run_id=f"{run_id}-repair-public",
                image=self.image,
                workspace_readonly=True,
            )
        try:
            if repair_sandbox is not None:
                repair_sandbox.start()
                log.append(
                    "sandbox_started",
                    "controller",
                    {
                        "purpose": "repair-public-stopping",
                        "container": repair_sandbox.container_name,
                        "mounted": ["run workspace"],
                        "hidden_tests_mounted": False,
                    },
                )
            agent = TestDrivenRepairAgent(
                model=model,
                sandbox=repair_sandbox,
                event_log=log,
                workspace=workspace,
                workspace_baseline=workspace_baseline,
                attempts_dir=run_dir / "repair_attempts",
                strategy=strategy,
                max_attempts=max_attempts,
            ).run(task)
        except Exception as exc:
            log.append(
                "run_failed",
                "controller",
                {
                    "error_type": type(exc).__name__,
                    "error": redact(str(exc), secrets=model.sensitive_values),
                },
            )
            raise
        finally:
            if repair_sandbox is not None:
                repair_sandbox.close()

        baseline_hidden = self._hidden_verify(
            task=task,
            workspace=baseline_snapshot,
            run_id=f"{run_id}-hidden-baseline",
            log=log,
            label="baseline",
        )
        first_public = self._public_verify(
            task=task,
            workspace=agent.attempts[0].snapshot,
            workspace_baseline=workspace_baseline,
            run_id=f"{run_id}-public-first",
            log=log,
            label="first",
        )
        if len(agent.attempts) == 1:
            final_public = first_public
        else:
            final_public = self._public_verify(
                task=task,
                workspace=agent.final_attempt.snapshot,
                workspace_baseline=workspace_baseline,
                run_id=f"{run_id}-public-final",
                log=log,
                label="final",
            )

        first_hidden = self._hidden_verify(
            task=task,
            workspace=agent.attempts[0].snapshot,
            run_id=f"{run_id}-hidden-first",
            log=log,
            label="first",
        )
        if len(agent.attempts) == 1:
            final_hidden = first_hidden
        else:
            final_hidden = self._hidden_verify(
                task=task,
                workspace=agent.final_attempt.snapshot,
                run_id=f"{run_id}-hidden-final",
                log=log,
                label="final",
            )

        outcome = "passed" if final_public.passed and final_hidden.passed else "failed"
        result = RunResult(
            run_id,
            run_dir,
            outcome,
            agent,
            first_public,
            final_public,
            first_hidden,
            final_hidden,
            baseline_hidden,
        )
        summary = _summary(result, model)
        summary["status"] = (
            "timeout"
            if summary["timed_out"]
            else "success"
            if outcome == "passed"
            else "repair_failed"
        )
        summary["task_id"] = task.task_id
        summary["max_attempts"] = 1 if strategy is RepairStrategy.SINGLE_SHOT else max_attempts
        summary["test_version"] = task.test_version
        summary["duration_ms"] = round((time.monotonic() - started) * 1000)
        events = list(log.read())
        summary["cost"] = _event_cost(events, model, self.pricing)
        summary["test_runtime_ms"] = sum(
            event["payload"]["command_result"]["duration_ms"]
            for event in events
            if event["type"]
            in {"repair_public_verification", "public_verification", "hidden_verification"}
        )
        (run_dir / "summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        log.append("run_completed", "controller", summary)
        return result

    def _public_verify(
        self,
        *,
        task: TaskSpec,
        workspace: Path,
        workspace_baseline: WorkspaceBaseline,
        run_id: str,
        log: EventLog,
        label: str,
    ) -> VerificationResult:
        sandbox = DockerSandbox(
            workspace=workspace,
            run_id=run_id,
            image=self.image,
            workspace_readonly=True,
        )
        try:
            sandbox.start()
            result = PublicVerifier().verify(
                task=task,
                sandbox=sandbox,
                workspace=workspace,
                workspace_baseline=workspace_baseline,
                collect_cases=True,
            )
        finally:
            sandbox.close()
        log.append("public_verification", "verifier", {"stage": label, **result.to_dict()})
        return result

    def _hidden_verify(
        self,
        *,
        task: TaskSpec,
        workspace: Path,
        run_id: str,
        log: EventLog,
        label: str,
    ) -> VerificationResult:
        sandbox = DockerSandbox(
            workspace=workspace,
            run_id=run_id,
            image=self.image,
            readonly_mounts=((task.hidden_tests_dir, "/hidden_tests"),),
            workspace_readonly=True,
        )
        try:
            sandbox.start()
            result = HiddenVerifier().verify(task=task, sandbox=sandbox)
        finally:
            sandbox.close()
        log.append(
            "hidden_verification",
            "verifier",
            {"stage": label, **result.to_dict()},
        )
        return result


def _summary(result: RunResult, model: ModelAdapter) -> dict[str, object]:
    attempts = result.agent.attempts
    if result.agent.strategy is RepairStrategy.SINGLE_SHOT:
        public_pass_by_attempt = [result.first_public.passed]
    else:
        public_pass_by_attempt = [
            bool(attempt.repair_verification and attempt.repair_verification.passed)
            for attempt in attempts
        ]
    first_success_attempt = next(
        (index for index, passed in enumerate(public_pass_by_attempt, start=1) if passed),
        None,
    )
    return {
        "schema_version": 3,
        "run_id": result.run_id,
        "outcome": result.outcome,
        "strategy": result.agent.strategy.value,
        "model": model.name,
        "provider": model.provider,
        "attempts": len(attempts),
        "public_pass_by_attempt": public_pass_by_attempt,
        "first_success_attempt": first_success_attempt,
        "protocol": {
            "version": PROTOCOL_VERSION,
            "name": PROTOCOL_NAME,
            "editable_paths": ["solution.py"],
            "model_calls_per_attempt": 1,
            "repair_pytest_enabled": result.agent.strategy is not RepairStrategy.SINGLE_SHOT,
            "detailed_test_feedback_enabled": result.agent.strategy is RepairStrategy.TEST_FEEDBACK,
            "repair_public_test_runs": sum(
                item.repair_verification is not None for item in attempts
            ),
        },
        "first_public_passed": result.first_public.passed,
        "final_public_passed": result.final_public.passed,
        "first_hidden_passed": result.first_hidden.passed,
        "final_hidden_passed": result.final_hidden.passed,
        "hidden_improvement": not result.first_hidden.passed and result.final_hidden.passed,
        "hidden_regression": result.first_hidden.passed and not result.final_hidden.passed,
        "hidden_cases": {
            "baseline": result.baseline_hidden.cases,
            "first": result.first_hidden.cases,
            "final": result.final_hidden.cases,
        },
        "public_cases": {
            "first": result.first_public.cases,
            "final": result.final_public.cases,
        },
        "case_results_complete": all(
            v.case_results_complete
            for v in (
                result.baseline_hidden,
                result.first_hidden,
                result.final_hidden,
            )
        ),
        "case_changes": {
            "baseline_to_final": compare_cases(
                result.baseline_hidden.cases, result.final_hidden.cases
            ),
            "first_to_final": compare_cases(result.first_hidden.cases, result.final_hidden.cases),
        },
        "timed_out": result.first_public.command_result.timed_out
        or result.final_public.command_result.timed_out
        or any(
            item.repair_verification is not None
            and item.repair_verification.command_result.timed_out
            for item in attempts
        )
        or result.first_hidden.command_result.timed_out
        or result.final_hidden.command_result.timed_out,
        "protected_test_violation": any(
            not verification.protected_files_unchanged
            for verification in (result.first_public, result.final_public)
        ),
        "workspace_policy_violation": any(
            not verification.workspace_policy_compliant
            for verification in (result.first_public, result.final_public)
        ),
    }


def _event_cost(
    events: list[dict[str, Any]],
    model: ModelAdapter,
    pricing: Pricing | None,
) -> dict[str, object]:
    responses = [e["payload"] for e in events if e["type"] == "model_response"]
    usages = [r.get("usage", {}) for r in responses]
    calls = sum(e["type"] == "model_request" for e in events)
    failed = [e["payload"] for e in events if e["type"] == "model_call_failed"]
    totals = (
        usage_totals(usages)
        if len(responses) == calls
        else dict.fromkeys(("prompt_tokens", "completion_tokens", "total_tokens"), None)
    )
    return {
        "model_calls": calls,
        **totals,
        "model_latency_ms": sum(r.get("latency_ms", 0) for r in [*responses, *failed]),
        "raw_usage": usages,
        "currency_cost": (
            pricing.estimate(usages, model=model.name, provider=model.provider)
            if pricing and len(responses) == calls
            else None
        ),
        "pricing": pricing.to_dict() if pricing else None,
        "currency": pricing.currency if pricing else None,
    }
