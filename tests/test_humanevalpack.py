import json
from pathlib import Path

import pytest

from repair_assistant.humanevalpack import DATASET_REVISION, import_records
from repair_assistant.task import TaskSpec


def _record(number: int) -> dict[str, str]:
    return {
        "task_id": f"Python/{number}",
        "prompt": 'def increment(value: int) -> int:\n    """Return value plus one."""\n',
        "canonical_solution": "    return value + 1\n",
        "buggy_solution": "    return value - 1\n",
        "bug_type": "operator misuse",
        "failure_symptoms": "incorrect output",
        "entry_point": "increment",
        "test": "def check(candidate):\n    assert candidate(-1) == 0\ncheck(increment)\n",
        "example_test": "def check(candidate):\n    assert candidate(1) == 2\ncheck(increment)\n",
        "instruction": "Repair increment so it returns value plus one.",
    }


def test_import_records_creates_isolated_tasks_without_canonical_solution(tmp_path: Path) -> None:
    output = tmp_path / "tasks"

    result = import_records([_record(0), _record(1)], output, limit=1, seed=7)

    assert result.imported == 1
    assert result.source_total == 2
    assert result.eligible_total == 2
    manifest = json.loads(result.manifest.read_text(encoding="utf-8"))
    assert manifest["revision"] == DATASET_REVISION
    assert manifest["canonical_solutions_stored"] is False
    task_dir = next(path.parent for path in output.glob("*/task.json"))
    task = TaskSpec.load(task_dir)
    assert task.editable_paths == ("solution.py",)
    assert not task.hidden_tests_dir.is_relative_to(task.source_dir)
    all_text = "\n".join(
        path.read_text(encoding="utf-8") for path in output.rglob("*") if path.is_file()
    )
    assert "return value + 1" not in all_text
    assert "return value - 1" in all_text


def test_import_records_refuses_to_overwrite_an_existing_directory(tmp_path: Path) -> None:
    output = tmp_path / "tasks"
    output.mkdir()

    with pytest.raises(FileExistsError):
        import_records([_record(0)], output, limit=1, seed=0)


def test_import_records_uses_seeded_selection(tmp_path: Path) -> None:
    records = [_record(number) for number in range(10)]
    first = import_records(records, tmp_path / "first", limit=4, seed=42)
    second = import_records(records, tmp_path / "second", limit=4, seed=42)

    first_manifest = json.loads(first.manifest.read_text(encoding="utf-8"))
    second_manifest = json.loads(second.manifest.read_text(encoding="utf-8"))
    assert first_manifest["tasks"] == second_manifest["tasks"]


def test_import_records_excludes_records_without_public_examples(tmp_path: Path) -> None:
    empty_public = _record(1)
    empty_public["example_test"] = ""

    result = import_records([_record(0), empty_public], tmp_path / "tasks", limit=1, seed=0)

    manifest = json.loads(result.manifest.read_text(encoding="utf-8"))
    assert result.source_total == 2
    assert result.eligible_total == 1
    assert manifest["excluded_empty_example_test"] == 1
    assert manifest["excluded_invalid_record"] == 0
    assert manifest["tasks"][0]["source_task_id"] == "Python/0"


def test_import_records_excludes_records_with_invalid_test_syntax(tmp_path: Path) -> None:
    invalid = _record(1)
    invalid["example_test"] = "return 1"

    result = import_records([_record(0), invalid], tmp_path / "tasks", limit=1, seed=0)

    manifest = json.loads(result.manifest.read_text(encoding="utf-8"))
    assert result.eligible_total == 1
    assert manifest["excluded_invalid_record"] == 1
