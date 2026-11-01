#!/usr/bin/env python3
"""Run initial benchmark solutions in the isolated Docker verifier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from repair_assistant.sandbox import DockerSandbox
from repair_assistant.task import TaskSpec, capture_workspace_baseline
from repair_assistant.verifier import PublicVerifier


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks_dir", type=Path)
    parser.add_argument("--image", default="function-repair/sandbox-python:dev")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = []
    task_paths = sorted(path.parent for path in args.tasks_dir.resolve().glob("*/task.json"))
    for index, task_path in enumerate(task_paths, start=1):
        task = TaskSpec.load(task_path)
        sandbox = DockerSandbox(
            workspace=task.source_dir,
            run_id=f"preflight-{index:03d}",
            image=args.image,
            workspace_readonly=True,
        )
        try:
            sandbox.start()
            result = PublicVerifier().verify(
                task=task,
                sandbox=sandbox,
                workspace=task.source_dir,
                workspace_baseline=capture_workspace_baseline(task, task.source_dir),
            )
        finally:
            sandbox.close()
        row = {
            "task_id": task.task_id,
            "initial_public_passed": result.passed,
            "timed_out": result.command_result.timed_out,
            "exit_code": result.command_result.exit_code,
        }
        rows.append(row)
        print(
            f"[{index:02d}/{len(task_paths):02d}] {task.task_id}: "
            f"{'PASS' if result.passed else 'FAIL'}",
            flush=True,
        )

    output = args.output or args.tasks_dir.resolve() / "preflight.json"
    summary = {
        "tasks": len(rows),
        "initial_public_failures": sum(not row["initial_public_passed"] for row in rows),
        "timeouts": sum(row["timed_out"] for row in rows),
        "results": rows,
    }
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Preflight: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
