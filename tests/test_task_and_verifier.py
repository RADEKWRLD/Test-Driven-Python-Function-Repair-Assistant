import json
from pathlib import Path

import pytest

from repair_assistant.task import TaskSpec, snapshot_paths
from repair_assistant.types import CommandResult
from repair_assistant.verifier import PublicVerifier


class PassingSandbox:
    def start(self) -> None:
        pass

    def execute(self, command: str, *, cwd: str = ".", timeout_seconds: int = 120) -> CommandResult:
        del timeout_seconds
        return CommandResult(command, cwd, 0, "5 passed\n", "", 2)

    def close(self) -> None:
        pass


def _task(workspace: Path, hidden: Path) -> TaskSpec:
    return TaskSpec(
        "t",
        "title",
        "goal",
        (),
        "pytest -q",
        ("tests",),
        workspace,
        hidden,
        "pytest -q /hidden_tests",
    )


def test_public_verifier_rejects_test_modification(tmp_path: Path) -> None:
    tests = tmp_path / "workspace/tests"
    tests.mkdir(parents=True)
    test_file = tests / "test_x.py"
    test_file.write_text("def test_x(): assert True\n", encoding="utf-8")
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    task = _task(tmp_path / "workspace", hidden)
    baseline = snapshot_paths(task.source_dir, task.protected_paths)
    test_file.write_text("def test_x(): assert False\n", encoding="utf-8")

    result = PublicVerifier().verify(
        task=task,
        sandbox=PassingSandbox(),
        workspace=task.source_dir,
        protected_baseline=baseline,
    )

    assert result.passed is False
    assert result.protected_files_unchanged is False


def test_task_loader_rejects_hidden_tests_inside_workspace(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    (workspace / "hidden_tests").mkdir(parents=True)
    manifest = {
        "task_id": "unsafe",
        "title": "unsafe",
        "goal": "unsafe",
        "workspace": "workspace",
        "public_verification": {"command": "pytest", "protected_paths": []},
        "hidden_verification": {
            "tests": "workspace/hidden_tests",
            "command": "pytest /hidden_tests",
        },
    }
    (tmp_path / "task.json").write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(ValueError, match="physically outside"):
        TaskSpec.load(tmp_path)
