"""Import HumanEvalPack Python repair tasks into the local benchmark format."""

from __future__ import annotations

import ast
import hashlib
import json
import random
import tempfile
import textwrap
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from repair_assistant.sandbox import DockerSandbox

DATASET_NAME = "bigcode/humanevalpack"
DATASET_CONFIG = "python"
DATASET_SPLIT = "test"
DATASET_REVISION = "9a41762f73a8cb23bb5811b73d5aab164efcf378"

_REQUIRED_FIELDS = (
    "task_id",
    "prompt",
    "buggy_solution",
    "bug_type",
    "failure_symptoms",
    "entry_point",
    "test",
    "example_test",
    "instruction",
)


@dataclass(frozen=True, slots=True)
class ImportResult:
    output_dir: Path
    imported: int
    source_total: int
    eligible_total: int
    manifest: Path


@dataclass(frozen=True, slots=True)
class UsefulSelection:
    source_task_ids: tuple[str, ...]
    scores: dict[str, int]
    structurally_eligible: int
    public_failure_eligible: int


def import_records(
    records: Iterable[Mapping[str, Any]],
    output_dir: Path,
    *,
    limit: int,
    seed: int,
    revision: str = DATASET_REVISION,
    selected_task_ids: tuple[str, ...] | None = None,
    selection_method: str = "seeded-random",
    selection_scores: Mapping[str, int] | None = None,
    selection_details: Mapping[str, object] | None = None,
) -> ImportResult:
    """Select records deterministically and write isolated benchmark task directories."""
    if limit < 1:
        raise ValueError("limit must be positive")
    destination = output_dir.resolve()
    if destination.exists():
        raise FileExistsError(f"output directory already exists: {destination}")

    source_records = list(records)
    normalized, exclusion_counts = _normalize_records(source_records)
    if not normalized:
        raise ValueError("HumanEvalPack returned no Python records with non-empty example tests")
    if limit > len(normalized):
        raise ValueError(f"limit {limit} exceeds the {len(normalized)} available records")

    if selected_task_ids is None:
        selected = list(normalized)
        random.Random(seed).shuffle(selected)
        selected = selected[:limit]
    else:
        if len(selected_task_ids) != limit or len(set(selected_task_ids)) != limit:
            raise ValueError("selected_task_ids must contain exactly limit unique IDs")
        by_id = {record["task_id"]: record for record in normalized}
        missing = [task_id for task_id in selected_task_ids if task_id not in by_id]
        if missing:
            raise ValueError(f"selected HumanEvalPack task IDs are unavailable: {missing}")
        selected = [by_id[task_id] for task_id in selected_task_ids]
    destination.mkdir(parents=True)

    manifest_tasks: list[dict[str, object]] = []
    for record in selected:
        slug = _task_slug(record["task_id"])
        task_dir = destination / slug
        _write_task(task_dir, record, revision=revision)
        task_entry: dict[str, object] = {
            "task_id": slug,
            "source_task_id": record["task_id"],
            "bug_type": record["bug_type"],
            "failure_symptoms": record["failure_symptoms"],
        }
        if selection_scores is not None and record["task_id"] in selection_scores:
            task_entry["difficulty_proxy_score"] = selection_scores[record["task_id"]]
        manifest_tasks.append(task_entry)

    selection_manifest: dict[str, object] = {
        "method": selection_method,
        "seed": seed,
        "limit": limit,
    }
    if selection_details is not None:
        selection_manifest.update(selection_details)
    manifest = destination / "dataset-manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "dataset": DATASET_NAME,
                "config": DATASET_CONFIG,
                "split": DATASET_SPLIT,
                "revision": revision,
                "selection": selection_manifest,
                "source_total": len(source_records),
                "eligible_total": len(normalized),
                **exclusion_counts,
                "tasks": manifest_tasks,
                "canonical_solutions_stored": False,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return ImportResult(destination, len(selected), len(source_records), len(normalized), manifest)


def select_useful_records(
    records: Iterable[Mapping[str, Any]],
    *,
    limit: int,
    seed: int,
    image: str,
) -> UsefulSelection:
    """Select tasks whose buggy implementation reliably activates public-test feedback."""
    normalized, _ = _normalize_records(list(records))
    structural = [record for record in normalized if _has_useful_test_split(record)]
    if len(structural) < limit:
        raise ValueError(
            f"only {len(structural)} records have at least two public assertions and "
            "a larger hidden suite"
        )
    public_results = _validate_buggy_public_tests(structural, image=image)
    failing = [record for record in structural if public_results.get(record["task_id"]) == 1]
    if len(failing) < limit:
        raise ValueError(
            f"only {len(failing)} records fail public pytest cleanly; cannot select {limit}"
        )
    scores = {record["task_id"]: _difficulty_proxy(record) for record in failing}
    selected = _stratified_ranked_selection(failing, scores=scores, limit=limit, seed=seed)
    return UsefulSelection(
        tuple(record["task_id"] for record in selected),
        scores,
        len(structural),
        len(failing),
    )


def _normalize_records(
    source_records: list[Mapping[str, Any]],
) -> tuple[list[dict[str, str]], dict[str, int]]:
    normalized: list[dict[str, str]] = []
    excluded_empty_example_test = 0
    excluded_invalid_record = 0
    for record in source_records:
        if not isinstance(record.get("example_test"), str) or not record["example_test"].strip():
            excluded_empty_example_test += 1
            continue
        try:
            normalized.append(_normalize_record(record))
        except (SyntaxError, ValueError):
            excluded_invalid_record += 1
    return normalized, {
        "excluded_empty_example_test": excluded_empty_example_test,
        "excluded_invalid_record": excluded_invalid_record,
    }


def _has_useful_test_split(record: Mapping[str, str]) -> bool:
    public_asserts = _assert_count(record["example_test"])
    hidden_asserts = _assert_count(record["test"])
    return public_asserts >= 2 and hidden_asserts >= 5 and hidden_asserts > public_asserts


def _assert_count(source: str) -> int:
    tree = ast.parse(textwrap.dedent(source))
    return sum(isinstance(node, ast.Assert) for node in ast.walk(tree))


def _difficulty_proxy(record: Mapping[str, str]) -> int:
    tree = ast.parse(_solution_source(record))
    control_nodes = sum(
        isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.BoolOp, ast.Compare))
        for node in ast.walk(tree)
    )
    return sum(1 for _ in ast.walk(tree)) + 5 * control_nodes + 2 * _assert_count(record["test"])


def _stratified_ranked_selection(
    records: list[dict[str, str]],
    *,
    scores: Mapping[str, int],
    limit: int,
    seed: int,
) -> list[dict[str, str]]:
    rng = random.Random(seed)
    groups: dict[str, list[tuple[int, float, dict[str, str]]]] = defaultdict(list)
    for record in records:
        groups[record["bug_type"]].append((scores[record["task_id"]], rng.random(), record))
    for group in groups.values():
        group.sort(key=lambda item: (item[0], item[1]), reverse=True)

    bug_types = sorted(groups)
    rng.shuffle(bug_types)
    selected: list[dict[str, str]] = []
    while len(selected) < limit:
        made_progress = False
        for bug_type in bug_types:
            if groups[bug_type] and len(selected) < limit:
                selected.append(groups[bug_type].pop(0)[2])
                made_progress = True
        if not made_progress:
            break
    if len(selected) != limit:
        raise ValueError(f"could select only {len(selected)} of {limit} requested records")
    return selected


def _validate_buggy_public_tests(
    records: list[dict[str, str]], *, image: str
) -> dict[str, int | str]:
    temporary_parent = Path("/private/tmp") if Path("/private/tmp").is_dir() else None
    with tempfile.TemporaryDirectory(
        prefix="humanevalpack-selection-", dir=temporary_parent
    ) as temporary:
        root = Path(temporary)
        for record in records:
            _write_task(root / _task_slug(record["task_id"]), record, revision=DATASET_REVISION)
        (root / "_validate_public.py").write_text(_PUBLIC_VALIDATOR_SOURCE, encoding="utf-8")
        sandbox = DockerSandbox(
            workspace=root,
            run_id="humanevalpack-selection",
            image=image,
            workspace_readonly=True,
        )
        try:
            sandbox.start()
            command = sandbox.execute(
                "python _validate_public.py",
                timeout_seconds=max(120, len(records) * 6 + 30),
            )
        finally:
            sandbox.close()
    if command.exit_code != 0 or command.timed_out:
        detail = command.stderr.strip() or command.stdout.strip()
        raise RuntimeError(f"HumanEvalPack public-test preflight failed: {detail}")
    parsed = json.loads(command.stdout)
    if not isinstance(parsed, dict):
        raise RuntimeError("HumanEvalPack public-test preflight returned invalid JSON")
    return {
        str(task_id): value
        for task_id, value in parsed.items()
        if isinstance(value, (int, str)) and not isinstance(value, bool)
    }


_PUBLIC_VALIDATOR_SOURCE = r"""import json
import os
import subprocess
import sys
from pathlib import Path

environment = dict(os.environ)
environment["PYTHONDONTWRITEBYTECODE"] = "1"
environment["PYTEST_ADDOPTS"] = "-p no:cacheprovider"
results = {}
for workspace in sorted(Path(".").glob("humanevalpack-python-*/workspace")):
    source_id = "Python/" + workspace.parent.name.rsplit("-", 1)[1].lstrip("0")
    if source_id == "Python/":
        source_id = "Python/0"
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "tests"],
            cwd=workspace,
            env=environment,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        results[source_id] = completed.returncode
    except subprocess.TimeoutExpired:
        results[source_id] = "timeout"
print(json.dumps(results, sort_keys=True))
"""


def _normalize_record(record: Mapping[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for field in _REQUIRED_FIELDS:
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"HumanEvalPack record has an invalid {field!r} field")
        result[field] = value

    solution = _solution_source(result)
    compile(solution, filename=f"{result['task_id']}/solution.py", mode="exec")
    compile(
        textwrap.dedent(result["example_test"]),
        filename=f"{result['task_id']}/source_example_test.py",
        mode="exec",
    )
    compile(
        textwrap.dedent(result["test"]),
        filename=f"{result['task_id']}/source_hidden_test.py",
        mode="exec",
    )
    compile(
        _pytest_source(result["example_test"], "test_public_examples"),
        filename=f"{result['task_id']}/test_public.py",
        mode="exec",
    )
    compile(
        _pytest_source(result["test"], "test_hidden_suite"),
        filename=f"{result['task_id']}/test_hidden.py",
        mode="exec",
    )
    return result


def _write_task(task_dir: Path, record: Mapping[str, str], *, revision: str) -> None:
    workspace = task_dir / "workspace"
    public_tests = workspace / "tests"
    hidden_tests = task_dir / "hidden_tests"
    public_tests.mkdir(parents=True)
    hidden_tests.mkdir()

    solution = _solution_source(record)
    public_source = _pytest_source(record["example_test"], "test_public_examples")
    hidden_source = _pytest_source(record["test"], "test_hidden_suite")
    (workspace / "solution.py").write_text(solution, encoding="utf-8")
    (public_tests / "test_public.py").write_text(public_source, encoding="utf-8")
    (hidden_tests / "test_hidden.py").write_text(hidden_source, encoding="utf-8")

    slug = _task_slug(record["task_id"])
    task_manifest = {
        "schema_version": 1,
        "task_id": slug,
        "title": f"HumanEvalPack repair: {record['entry_point']}",
        "goal": record["instruction"],
        "constraints": [
            "Only edit solution.py.",
            "Do not add dependencies or modify tests.",
            f"Keep the public function {record['entry_point']} and its signature unchanged.",
        ],
        "editable_paths": ["solution.py"],
        "public_verification": {
            "command": "python -m pytest -q tests",
            "protected_paths": ["tests"],
        },
        "hidden_verification": {
            "tests": "hidden_tests",
            "command": "python -m pytest -q /hidden_tests",
        },
        "provenance": {
            "dataset": DATASET_NAME,
            "config": DATASET_CONFIG,
            "split": DATASET_SPLIT,
            "revision": revision,
            "source_task_id": record["task_id"],
            "bug_type": record["bug_type"],
            "failure_symptoms": record["failure_symptoms"],
            "initial_solution_sha256": hashlib.sha256(solution.encode()).hexdigest(),
            "canonical_solution_included": False,
        },
    }
    (task_dir / "task.json").write_text(
        json.dumps(task_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _solution_source(record: Mapping[str, str]) -> str:
    prompt = record["prompt"]
    separator = "" if prompt.endswith("\n") else "\n"
    return f"{prompt}{separator}{record['buggy_solution'].rstrip()}\n"


def _pytest_source(test_source: str, test_name: str) -> str:
    body = textwrap.indent(textwrap.dedent(test_source).strip(), "    ")
    return f"from solution import *  # noqa: F403\n\n\ndef {test_name}():\n{body}\n"


def _task_slug(source_task_id: str) -> str:
    language, separator, number = source_task_id.partition("/")
    if separator != "/" or language.lower() != "python" or not number.isdigit():
        raise ValueError(f"unexpected Python HumanEvalPack task_id: {source_task_id!r}")
    return f"humanevalpack-python-{int(number):03d}"
