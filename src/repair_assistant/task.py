"""Task manifests and run-workspace preparation."""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast


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
        )

    def prompt(self) -> str:
        constraints = "\n".join(f"- {item}" for item in self.constraints)
        return (
            f"Task: {self.title}\n\nRequirement:\n{self.goal}\n\n"
            f"Constraints:\n{constraints}\n\nPublic verification: {self.public_command}"
        )


def prepare_workspace(task: TaskSpec, destination: Path) -> dict[str, str]:
    if destination.exists():
        raise FileExistsError(f"run workspace already exists: {destination}")
    shutil.copytree(task.source_dir, destination)
    return snapshot_paths(destination, task.protected_paths)


def snapshot_paths(workspace: Path, paths: tuple[str, ...]) -> dict[str, str]:
    workspace = workspace.resolve()
    result: dict[str, str] = {}
    for raw in paths:
        target = (workspace / raw).resolve()
        if not target.is_relative_to(workspace):
            raise ValueError(f"protected path escapes workspace: {raw}")
        candidates = sorted(target.rglob("*")) if target.is_dir() else [target]
        for candidate in candidates:
            if candidate.is_file():
                result[candidate.relative_to(workspace).as_posix()] = hashlib.sha256(
                    candidate.read_bytes()
                ).hexdigest()
    return result
