"""End-to-end orchestration for one controlled repair experiment."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from repair_assistant.agent import AgentResult, RepairStrategy, TestDrivenRepairAgent
from repair_assistant.event_log import EventLog
from repair_assistant.model import ModelAdapter
from repair_assistant.sandbox import DockerSandbox
from repair_assistant.task import TaskSpec, prepare_workspace
from repair_assistant.types import VerificationResult
from repair_assistant.verifier import HiddenVerifier


@dataclass(frozen=True, slots=True)
class RunResult:
    run_id: str
    run_dir: Path
    outcome: str
    agent: AgentResult
    first_hidden: VerificationResult
    final_hidden: VerificationResult


class RunService:
    def __init__(
        self,
        *,
        data_dir: Path,
        image: str = "function-repair/sandbox-python:dev",
    ) -> None:
        self.data_dir = data_dir.resolve()
        self.image = image

    def execute(
        self,
        *,
        task: TaskSpec,
        model: ModelAdapter,
        strategy: RepairStrategy = RepairStrategy.TEST_FEEDBACK,
        max_attempts: int = 3,
        max_turns_per_attempt: int = 12,
    ) -> RunResult:
        run_id = f"run_{uuid4().hex[:12]}"
        run_dir = self.data_dir / "runs" / run_id
        workspace = run_dir / "workspace"
        baseline = prepare_workspace(task, workspace)
        log = EventLog(run_dir / "events.jsonl", run_id=run_id, task_id=task.task_id)
        log.append(
            "run_started",
            "controller",
            {
                "strategy": strategy.value,
                "model": model.name,
                "provider": model.provider,
                "image": self.image,
                "network": "none",
                "max_attempts": 1 if strategy is RepairStrategy.SINGLE_SHOT else max_attempts,
                "max_turns_per_attempt": max_turns_per_attempt,
            },
        )
        agent_sandbox = DockerSandbox(
            workspace=workspace,
            run_id=f"{run_id}-agent",
            image=self.image,
        )
        try:
            agent_sandbox.start()
            log.append(
                "sandbox_started",
                "controller",
                {
                    "purpose": "agent",
                    "container": agent_sandbox.container_name,
                    "mounted": ["run workspace"],
                    "hidden_tests_mounted": False,
                },
            )
            agent = TestDrivenRepairAgent(
                model=model,
                sandbox=agent_sandbox,
                event_log=log,
                workspace=workspace,
                protected_baseline=baseline,
                attempts_dir=run_dir / "attempts",
                strategy=strategy,
                max_attempts=max_attempts,
                max_turns_per_attempt=max_turns_per_attempt,
            ).run(task)
        except Exception as exc:
            log.append(
                "run_failed",
                "controller",
                {"error_type": type(exc).__name__, "error": str(exc)},
            )
            raise
        finally:
            agent_sandbox.close()

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

        public_passed = agent.final_attempt.public_verification.passed
        outcome = "passed" if public_passed and final_hidden.passed else "failed"
        result = RunResult(run_id, run_dir, outcome, agent, first_hidden, final_hidden)
        summary = _summary(result, model)
        (run_dir / "summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        log.append("run_completed", "controller", summary)
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
    calls = sum(item.cost.model_calls for item in attempts)
    prompt = sum(item.cost.prompt_tokens for item in attempts)
    completion = sum(item.cost.completion_tokens for item in attempts)
    total = sum(item.cost.total_tokens for item in attempts)
    latency = sum(item.cost.latency_ms for item in attempts)
    return {
        "schema_version": 1,
        "run_id": result.run_id,
        "outcome": result.outcome,
        "strategy": result.agent.strategy.value,
        "model": model.name,
        "provider": model.provider,
        "attempts": len(attempts),
        "first_public_passed": attempts[0].public_verification.passed,
        "final_public_passed": attempts[-1].public_verification.passed,
        "first_hidden_passed": result.first_hidden.passed,
        "final_hidden_passed": result.final_hidden.passed,
        "hidden_regression": result.first_hidden.passed and not result.final_hidden.passed,
        "timed_out": any(item.public_verification.command_result.timed_out for item in attempts)
        or result.first_hidden.command_result.timed_out
        or result.final_hidden.command_result.timed_out,
        "protected_test_violation": any(
            not item.public_verification.protected_files_unchanged for item in attempts
        ),
        "cost": {
            "model_calls": calls,
            "prompt_tokens": prompt,
            "completion_tokens": completion,
            "total_tokens": total,
            "model_latency_ms": latency,
            "currency_cost": None,
        },
    }
