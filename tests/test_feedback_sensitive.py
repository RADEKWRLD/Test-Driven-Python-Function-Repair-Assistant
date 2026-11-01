"""Check dataset boundaries and frozen QA evidence without executing candidates."""

import ast
import hashlib
import json
from pathlib import Path

from repair_assistant.task import TaskSpec

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "benchmarks/feedback-sensitive"
NAMES = {
    "alternating-extreme-blocks",
    "serpentine-ragged",
    "round-robin-drain",
    "escaped-fields",
    "capped-runs",
    "interval-buckets",
    "sliding-window-modes",
    "bounded-subarray-sums",
    "stable-top-k",
    "rotate-slice",
    "multiset-intersection",
    "nested-token-split",
    "quoted-whitespace-tokens",
    "escaped-backspaces",
    "wildcard-match",
    "normalize-segments",
    "merge-intervals",
    "subtract-interval",
    "slice-runs",
    "deletion-index-map",
}


def test_feedback_sensitive_cases_have_separate_tests_and_oracles() -> None:
    manifests = sorted(DATASET.glob("*/task.json"))
    assert {path.parent.name for path in manifests} == NAMES
    ids = set()
    counts = {"public": 0, "hidden": 0}
    for manifest in manifests:
        task = TaskSpec.load(manifest.parent)
        ids.add(task.task_id)
        assert task.editable_paths == ("solution.py",)
        assert task.test_version == "feedback-sensitive-v1"
        assert not task.hidden_tests_dir.is_relative_to(task.source_dir)
        workspace_files = {
            path.relative_to(task.source_dir).as_posix()
            for path in task.source_dir.rglob("*")
            if path.is_file()
        }
        assert workspace_files == {"solution.py", "tests/test_public.py"}
        reference = (
            ROOT / "tools/fixtures/feedback_sensitive" / manifest.parent.name / "solution.py"
        )
        assert reference.is_file()
        assert not reference.is_relative_to(task.source_dir)
        for path in [reference, *manifest.parent.rglob("*.py")]:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for label, directory, minimum in (
            ("public", task.source_dir / "tests", 5),
            ("hidden", task.hidden_tests_dir, 8),
        ):
            names: list[str] = []
            for path in directory.glob("test_*.py"):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                names.extend(
                    node.name
                    for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
                )
            assert len(names) == len(set(names)) >= minimum
            counts[label] += len(names)
    assert len(ids) == len(NAMES)
    assert counts == {"public": 157, "hidden": 201}


def test_feedback_sensitive_preflight_matches_current_sources() -> None:
    report = json.loads((DATASET / "preflight.json").read_text(encoding="utf-8"))
    assert report["kind"] == "dataset-validation-not-model-results"
    assert report["model_calls"] == 0
    assert report["all_valid"] is True
    assert report["tasks"] == report["valid_tasks"] == len(NAMES)
    expected_ids = {TaskSpec.load(DATASET / name).task_id for name in NAMES}
    assert {row["task_id"] for row in report["results"]} == expected_ids
    for row in report["results"]:
        assert row["valid"] is True
        for relative, expected in row["sha256"].items():
            actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            assert actual == expected, f"Rerun tools/preflight_feedback_sensitive.py: {relative}"
        for suite in ("public", "hidden"):
            reference = row["verifications"][f"reference_{suite}"]
            buggy = row["verifications"][f"buggy_{suite}"]
            assert reference["passed"] is True
            assert set(reference["cases"].values()) == {"passed"}
            assert buggy["passed"] is False
            assert set(buggy["cases"].values()) == {"passed", "failed"}
