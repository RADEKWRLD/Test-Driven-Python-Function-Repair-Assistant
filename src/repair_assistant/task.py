"""Task manifests and run-workspace preparation."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, cast


@dataclass(frozen=True, slots=True)
class WorkspaceBaseline:
    protected: dict[str, str]
    entries: dict[str, str]


@dataclass(frozen=True, slots=True)
class TaskSpec:
    task_id: str
    title: str
    goal: str
    constraints: tuple[str, ...]
    public_command: str
    protected_paths: tuple[str, ...]
    source_dir: Path
    hidden_tests_dir: Path
    hidden_command: str
    editable_paths: tuple[str, ...] = ("solution.py",)

    @classmethod
    def load(cls, task_dir: Path) -> TaskSpec:
        root = task_dir.resolve()
        data = cast(dict[str, Any], json.loads((root / "task.json").read_text(encoding="utf-8")))
        public = cast(dict[str, Any], data["public_verification"])
        hidden = cast(dict[str, Any], data["hidden_verification"])
        source_dir = (root / str(data.get("workspace", "workspace"))).resolve()
        hidden_dir = (root / str(hidden.get("tests", "hidden_tests"))).resolve()
        if not source_dir.is_relative_to(root) or not hidden_dir.is_relative_to(root):
            raise ValueError("task paths must stay inside the task directory")
        if hidden_dir.is_relative_to(source_dir):
            raise ValueError("hidden tests must be physically outside the Agent workspace")
        if not source_dir.is_dir() or not hidden_dir.is_dir():
            raise ValueError("workspace and hidden test directories must exist")
        editable_paths = tuple(str(item) for item in data.get("editable_paths", ["solution.py"]))
        if not editable_paths:
            raise ValueError("at least one editable path is required")
        for raw in editable_paths:
            relative = _workspace_relative_path(raw, label="editable")
            target = source_dir.joinpath(*relative.parts)
            if not target.is_file() or target.is_symlink():
                raise ValueError(f"editable path must be an existing regular file: {raw}")
        return cls(
            task_id=str(data["task_id"]),
            title=str(data["title"]),
            goal=str(data["goal"]),
            constraints=tuple(str(item) for item in data.get("constraints", [])),
            public_command=str(public["command"]),
            protected_paths=tuple(str(item) for item in public.get("protected_paths", [])),
            source_dir=source_dir,
            hidden_tests_dir=hidden_dir,
            hidden_command=str(hidden["command"]),
            editable_paths=editable_paths,
        )

    def prompt(self) -> str:
        constraints = "\n".join(f"- {item}" for item in self.constraints)
        editable = "\n".join(f"- {item}" for item in self.editable_paths)
        return (
            f"Task: {self.title}\n\nRequirement:\n{self.goal}\n\n"
            f"Constraints:\n{constraints}\n\nEditable paths (all other workspace paths are "
            f"immutable):\n{editable}\n\nPublic verification: {self.public_command}"
        )


def prepare_workspace(task: TaskSpec, destination: Path) -> WorkspaceBaseline:
    if destination.exists():
        raise FileExistsError(f"run workspace already exists: {destination}")
    shutil.copytree(task.source_dir, destination, symlinks=True)
    return capture_workspace_baseline(task, destination)


def capture_workspace_baseline(task: TaskSpec, workspace: Path) -> WorkspaceBaseline:
    return WorkspaceBaseline(
        protected=snapshot_paths(workspace, task.protected_paths),
        entries=snapshot_workspace(workspace),
    )


def snapshot_workspace(workspace: Path) -> dict[str, str]:
    root = workspace.resolve()
    if not root.is_dir():
        raise ValueError(f"workspace does not exist: {root}")
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[relative] = f"symlink:{os.readlink(path)}"
        elif path.is_dir():
            result[relative] = "directory"
        elif path.is_file():
            result[relative] = f"file:{hashlib.sha256(path.read_bytes()).hexdigest()}"
        else:
            result[relative] = "special"
    return result


def snapshot_paths(workspace: Path, paths: tuple[str, ...]) -> dict[str, str]:
    entries = snapshot_workspace(workspace)
    result: dict[str, str] = {}
    for raw in paths:
        relative = _workspace_relative_path(raw, label="protected").as_posix()
        for path, fingerprint in entries.items():
            if path == relative or path.startswith(f"{relative}/"):
                result[path] = fingerprint
    return result


def unauthorized_workspace_changes(
    baseline: dict[str, str],
    current: dict[str, str],
    editable_paths: tuple[str, ...],
) -> tuple[str, ...]:
    editable = {
        _workspace_relative_path(raw, label="editable").as_posix() for raw in editable_paths
    }
    changes: list[str] = []
    for path in sorted(baseline.keys() | current.keys()):
        if path in editable or baseline.get(path) == current.get(path):
            continue
        if path not in baseline:
            action = "added"
        elif path not in current:
            action = "removed"
        else:
            action = "modified"
        changes.append(f"{action} non-editable workspace path: {path}")
    return tuple(changes)


def _workspace_relative_path(raw: str, *, label: str) -> PurePosixPath:
    relative = PurePosixPath(raw)
    if (
        not raw
        or relative.is_absolute()
        or ".." in relative.parts
        or relative == PurePosixPath(".")
    ):
        raise ValueError(f"{label} path must stay inside the workspace: {raw}")
    return relative
