#!/usr/bin/env python3
"""Convert FeedbackEval HumanEval candidates into isolated course tasks.

The converter copies only the selected erroneous implementation. Public/hidden tests
and requirements come from an already frozen HumanEvalPack task set. It deliberately
does not copy FeedbackEval's correct_code or precomputed feedback fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

FEEDBACKEVAL_COMMIT = "bd8d8aefbc2319e9fdab5b1b85091b0665a48e50"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _source_id(value: str) -> str:
    return value.rsplit("/", 1)[-1].zfill(3)


def import_tasks(
    source: Path,
    base_root: Path,
    output_root: Path,
    *,
    candidate_pool: Path | None = None,
    overrides_path: Path | None = None,
) -> dict[str, Any]:
    if output_root == base_root or output_root.parent == output_root:
        raise ValueError("output must be a dedicated directory different from the base dataset")
    source_bytes = source.read_bytes()
    candidates: dict[str, tuple[dict[str, Any], str, int]] = {}
    for row in _read_jsonl(source):
        false_results = row.get("false_results")
        if not isinstance(false_results, list) or len(false_results) != 1:
            raise ValueError("feedback test data must contain exactly one candidate per task")
        candidate = false_results[0]
        code = candidate.get("generate_code")
        if not isinstance(code, str) or not code.strip():
            raise ValueError(f"missing candidate code for {row.get('_id')}")
        candidates[_source_id(str(row["_id"]))] = (candidate, source.name, 0)

    pool_rows: dict[str, list[dict[str, Any]]] = {}
    pool_sha256 = None
    if candidate_pool is not None:
        pool_sha256 = _sha256(candidate_pool.read_bytes())
        for row in _read_jsonl(candidate_pool):
            row_id = row.get("task_id") or row.get("_id")
            pool_rows[_source_id(str(row_id))] = list(row.get("false_results", []))
    overrides = json.loads(overrides_path.read_text(encoding="utf-8")) if overrides_path else {}
    for numeric_id, raw_index in overrides.items():
        index = int(raw_index)
        pool = pool_rows.get(_source_id(numeric_id), [])
        if not 0 <= index < len(pool):
            raise ValueError(f"invalid candidate override for HumanEval/{numeric_id}: {index}")
        assert candidate_pool is not None
        candidates[_source_id(numeric_id)] = (pool[index], candidate_pool.name, index)

    base_manifest = json.loads((base_root / "dataset-manifest.json").read_text(encoding="utf-8"))
    task_entries: list[dict[str, Any]] = []
    staging = output_root.with_name(f".{output_root.name}.staging")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    try:
        for entry in base_manifest["tasks"]:
            source_task_id = str(entry["source_task_id"])
            numeric_id = _source_id(source_task_id)
            selected = candidates.get(numeric_id)
            if selected is None:
                raise ValueError(f"FeedbackEval candidate missing for {source_task_id}")
            candidate, candidate_file, candidate_index = selected

            base_task_id = f"humanevalpack-python-{numeric_id}"
            base_task = base_root / base_task_id
            if not base_task.is_dir():
                raise ValueError(f"base task missing: {base_task}")

            task_id = f"feedbackeval-humaneval-{numeric_id}"
            destination = staging / task_id
            shutil.copytree(base_task, destination)
            code = str(candidate["generate_code"]).rstrip() + "\n"
            (destination / "workspace/solution.py").write_text(code, encoding="utf-8")

            manifest_path = destination / "task.json"
            task = json.loads(manifest_path.read_text(encoding="utf-8"))
            task["task_id"] = task_id
            task["title"] = f"FeedbackEval HumanEval repair: {task['title'].split(': ', 1)[-1]}"
            task["provenance"] = {
                "dataset": "FeedbackEval/HumanEval_feedback_test",
                "feedbackeval_commit": FEEDBACKEVAL_COMMIT,
                "source_file_sha256": _sha256(source_bytes),
                "source_task_id": f"HumanEval/{int(numeric_id)}",
                "candidate_source": str(candidate.get("source", "unknown")),
                "candidate_file": candidate_file,
                "candidate_index": candidate_index,
                "candidate_sha256": _sha256(code.encode()),
                "base_test_dataset": base_manifest["dataset"],
                "base_test_revision": base_manifest["revision"],
                "base_task_id": base_task_id,
                "correct_code_included": False,
                "precomputed_feedback_included": False,
            }
            manifest_path.write_text(
                json.dumps(task, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            task_entries.append(
                {
                    "task_id": task_id,
                    "source_task_id": task["provenance"]["source_task_id"],
                    "candidate_source": task["provenance"]["candidate_source"],
                    "candidate_file": candidate_file,
                    "candidate_index": candidate_index,
                    "candidate_sha256": task["provenance"]["candidate_sha256"],
                    "base_task_id": base_task_id,
                }
            )

        manifest = {
            "schema_version": 1,
            "dataset": "FeedbackEval/HumanEval_feedback_test",
            "feedbackeval_commit": FEEDBACKEVAL_COMMIT,
            "source_file_sha256": _sha256(source_bytes),
            "candidate_pool_sha256": pool_sha256,
            "selection_overrides": overrides,
            "selection": {
                "method": "inherit-frozen-humanevalpack-selection",
                "base_manifest_sha256": _sha256((base_root / "dataset-manifest.json").read_bytes()),
                "count": len(task_entries),
                "outcome_blind": True,
            },
            "test_policy": {
                "public_and_hidden_inherited_from": f"benchmarks/{base_root.name}",
                "public_hidden_disjoint": True,
                "feedbackeval_test_field_copied": False,
                "correct_code_copied": False,
                "precomputed_feedback_copied": False,
            },
            "tasks": task_entries,
        }
        (staging / "dataset-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        if output_root.exists():
            shutil.rmtree(output_root)
        staging.rename(output_root)
        return manifest
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--base", type=Path, default=Path("benchmarks/humanevalpack"))
    parser.add_argument("--candidate-pool", type=Path)
    parser.add_argument("--overrides", type=Path)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/feedbackeval-humaneval"))
    args = parser.parse_args()
    manifest = import_tasks(
        args.source.resolve(),
        args.base.resolve(),
        args.output.resolve(),
        candidate_pool=args.candidate_pool.resolve() if args.candidate_pool else None,
        overrides_path=args.overrides.resolve() if args.overrides else None,
    )
    print(f"Imported {len(manifest['tasks'])} tasks into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
