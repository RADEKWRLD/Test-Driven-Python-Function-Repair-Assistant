import re
from pathlib import Path

from repair_assistant.output_paths import (
    create_output_directory,
    create_run_directory,
    resolve_run_directory,
)


def test_new_execution_uses_next_number_without_overwriting_previous_results(
    tmp_path: Path,
) -> None:
    parent = tmp_path / "experiments"
    first = create_output_directory(parent)
    result = first / "report.json"
    result.write_text("saved result", encoding="utf-8")
    second = create_output_directory(parent)

    assert re.fullmatch(r"\d{8}_001", first.name)
    assert second.name == f"{first.name[:8]}_002"
    assert result.read_text(encoding="utf-8") == "saved result"


def test_grouped_runs_keep_unique_ids_and_read_legacy_directories(tmp_path: Path) -> None:
    legacy = tmp_path / "runs/20261031_001_001"
    legacy.mkdir(parents=True)
    a = create_run_directory(tmp_path, "single-shot", prefix="20261031_001")
    b = create_run_directory(tmp_path, "retry-without-feedback", prefix="20261031_001")
    c = create_run_directory(tmp_path, "test-feedback", prefix="20261031_001")
    assert [path.parent.name for path in (a, b, c)] == ["group_a", "group_b", "group_c"]
    assert [path.name for path in (a, b, c)] == [
        "20261031_001_002",
        "20261031_001_003",
        "20261031_001_004",
    ]
    assert resolve_run_directory(tmp_path, "single-shot", a.name) == a
    assert resolve_run_directory(tmp_path, "single-shot", legacy.name) == legacy
