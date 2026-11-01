#!/usr/bin/env python3
"""Verify frozen HumanEval+ hidden tests against references without storing references."""

from __future__ import annotations

import argparse
import gzip
import json
import shutil
import tempfile
from pathlib import Path

from repair_assistant.sandbox import DockerSandbox
from repair_assistant.task import TaskSpec
from repair_assistant.verifier import HiddenVerifier


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks_dir", type=Path)
    parser.add_argument("evalplus_jsonl", type=Path)
    parser.add_argument("--image", default="function-repair/sandbox-python:dev")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--task-id", action="append")
    args = parser.parse_args()

    with gzip.open(args.evalplus_jsonl.resolve(), "rt", encoding="utf-8") as source:
        references = {
            str(row["task_id"]): row
            for line in source
            if line.strip()
            for row in [json.loads(line)]
        }
    task_paths = sorted(path.parent for path in args.tasks_dir.resolve().glob("*/task.json"))
    if args.task_id:
        selected = set(args.task_id)
        task_paths = [path for path in task_paths if path.name in selected]
    rows = []
    temporary_parent = Path("/private/tmp") if Path("/private/tmp").is_dir() else None
    with tempfile.TemporaryDirectory(prefix="evalplus-reference-", dir=temporary_parent) as raw:
        root = Path(raw)
        for index, task_path in enumerate(task_paths, start=1):
            task = TaskSpec.load(task_path)
            number = int(task.task_id.rsplit("-", 1)[-1])
            reference = references[f"HumanEval/{number}"]
            workspace = root / f"workspace-{number:03d}"
            shutil.copytree(task.source_dir, workspace)
            prompt = str(reference["prompt"])
            separator = "" if prompt.endswith("\n") else "\n"
            solution = f"{prompt}{separator}{str(reference['canonical_solution']).rstrip()}\n"
            (workspace / "solution.py").write_text(solution, encoding="utf-8")
            sandbox = DockerSandbox(
                workspace=workspace,
                run_id=f"evalplus-reference-{number:03d}",
                image=args.image,
                readonly_mounts=((task.hidden_tests_dir, "/hidden_tests"),),
                workspace_readonly=True,
            )
            try:
                sandbox.start()
                result = HiddenVerifier().verify(task=task, sandbox=sandbox)
            finally:
                sandbox.close()
            rows.append(
                {
                    "task_id": task.task_id,
                    "reference_hidden_passed": result.passed,
                    "timed_out": result.command_result.timed_out,
                    "exit_code": result.command_result.exit_code,
                }
            )
            print(
                f"[{index:03d}/{len(task_paths):03d}] {task.task_id}: "
                f"{'PASS' if result.passed else 'FAIL'}",
                flush=True,
            )
            if not result.passed:
                stdout = result.command_result.stdout
                stderr = result.command_result.stderr
                print(stdout[-4000:], flush=True)
                print(stderr[-4000:], flush=True)

    output = args.output or args.tasks_dir.resolve() / "hidden-reference-preflight.json"
    summary = {
        "tasks": len(rows),
        "reference_hidden_passes": sum(row["reference_hidden_passed"] for row in rows),
        "timeouts": sum(row["timed_out"] for row in rows),
        "correct_code_stored": False,
        "results": rows,
    }
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Reference hidden preflight: {output}")
    return 0 if summary["reference_hidden_passes"] == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
