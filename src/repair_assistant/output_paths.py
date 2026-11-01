"""Readable output directories, numbered per Beijing calendar date."""

from datetime import datetime, timedelta, timezone
from pathlib import Path

GROUP_DIRECTORIES = {
    "single-shot": "group_a",
    "retry-without-feedback": "group_b",
    "test-feedback": "group_c",
}


def create_output_directory(
    parent: Path, *, prefix: str | None = None, occupied_names: set[str] | None = None
) -> Path:
    parent.mkdir(parents=True, exist_ok=True)
    prefix = prefix or datetime.now(timezone(timedelta(hours=8))).strftime("%Y%m%d")
    number = 1
    while True:
        directory = parent / f"{prefix}_{number:03d}"
        if occupied_names and directory.name in occupied_names:
            number += 1
            continue
        try:
            directory.mkdir()
        except FileExistsError:
            number += 1
        else:
            return directory


def grouped_run_directory(data_dir: Path, strategy: str, run_id: str) -> Path:
    return data_dir / "runs" / GROUP_DIRECTORIES[strategy] / run_id


def create_run_directory(data_dir: Path, strategy: str, *, prefix: str | None = None) -> Path:
    root = data_dir / "runs"
    locations = [root, *(root / group for group in GROUP_DIRECTORIES.values())]
    occupied = {
        child.name for location in locations if location.is_dir() for child in location.iterdir()
    }
    return create_output_directory(
        root / GROUP_DIRECTORIES[strategy], prefix=prefix, occupied_names=occupied
    )


def resolve_run_directory(data_dir: Path, strategy: str, run_id: str) -> Path:
    grouped = grouped_run_directory(data_dir, strategy, run_id)
    return grouped if grouped.is_dir() else data_dir / "runs" / run_id
