#!/usr/bin/env python3
"""Validate synthetic tasks and reference implementations exclusively in Docker.

This is dataset QA, not a model experiment. Never import a task's solution/tests
on the host, and never copy references into the checked-in task workspace.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from repair_assistant.sandbox import DockerSandbox
from repair_assistant.task import TaskSpec, capture_workspace_baseline
from repair_assistant.types import VerificationResult
from repair_assistant.verifier import HiddenVerifier, PublicVerifier

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "benchmarks/feedback-sensitive"
REFERENCES = ROOT / "tools/fixtures/feedback_sensitive"


def verify_candidate(
    task: TaskSpec, workspace: Path, *, image: str, hidden: bool
) -> VerificationResult:
    # Separate containers keep hidden tests out of even the QA public execution.
    mounts = ((task.hidden_tests_dir, "/hidden_tests"),) if hidden else ()
    with DockerSandbox(
        workspace=workspace,
        run_id=f"synthetic-qa-{uuid4().hex[:16]}",
        image=image,
        readonly_mounts=mounts,
        workspace_readonly=True,
    ) as sandbox:
        if hidden:
            return HiddenVerifier().verify(task=task, sandbox=sandbox, timeout_seconds=30)
        return PublicVerifier().verify(
            task=task,
            sandbox=sandbox,
            workspace=workspace,
            workspace_baseline=capture_workspace_baseline(task, workspace),
            collect_cases=True,
            timeout_seconds=30,
        )


def acceptable(result: VerificationResult, *, reference: bool) -> bool:
    statuses = set(result.cases.values())
    complete = (
        result.case_results_complete
        and not result.command_result.timed_out
        and result.workspace_policy_compliant
        and result.protected_files_unchanged
        and not result.violations
    )
    if reference:
        return complete and result.passed and statuses == {"passed"}
    # Defects must fail assertions, not collection/import errors; retain some
    # originally correct cases so functional regression can be measured.
    return (
        complete
        and not result.passed
        and result.command_result.exit_code == 1
        and statuses == {"passed", "failed"}
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", default="function-repair/sandbox-python:dev")
    parser.add_argument("--output", type=Path, default=DATASET / "preflight.json")
    args = parser.parse_args()
    paths = sorted(DATASET.glob("*/task.json"))
    if not paths:
        parser.error("no feedback-sensitive tasks found")
    rows = []
    all_valid = True
    temporary_parent = Path("/private/tmp") if Path("/private/tmp").is_dir() else None
    with tempfile.TemporaryDirectory(prefix="feedback-sensitive-qa-", dir=temporary_parent) as raw:
        temporary_root = Path(raw)
        for manifest in paths:
            task = TaskSpec.load(manifest.parent)
            reference_path = REFERENCES / manifest.parent.name / "solution.py"
            source_files = [
                manifest,
                *sorted(task.source_dir.rglob("*.py")),
                *sorted(task.hidden_tests_dir.rglob("*.py")),
                reference_path,
            ]
            fingerprints = {
                path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in source_files
            }
            verifications = {}
            valid = True
            for variant in ("buggy", "reference"):
                workspace = temporary_root / manifest.parent.name / variant
                shutil.copytree(task.source_dir, workspace)
                if variant == "reference":
                    shutil.copyfile(reference_path, workspace / "solution.py")
                for suite in ("public", "hidden"):
                    result = verify_candidate(
                        task, workspace, image=args.image, hidden=suite == "hidden"
                    )
                    valid &= acceptable(result, reference=variant == "reference")
                    verifications[f"{variant}_{suite}"] = result.to_dict()
            all_valid &= valid
            rows.append(
                {
                    "task_id": task.task_id,
                    "test_version": task.test_version,
                    "valid": valid,
                    "sha256": fingerprints,
                    "verifications": verifications,
                }
            )
            print(f"{task.task_id}: {'VALID' if valid else 'INVALID'}", flush=True)
    report = {
        "kind": "dataset-validation-not-model-results",
        "created_at": datetime.now(UTC).isoformat(),
        "image": args.image,
        "network": "none",
        "model_calls": 0,
        "reference_in_model_workspace": False,
        "tasks": len(rows),
        "valid_tasks": sum(row["valid"] for row in rows),
        "all_valid": all_valid,
        "results": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Dataset validation: {args.output}")
    return 0 if all_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
