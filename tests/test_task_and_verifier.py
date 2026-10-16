import json
from pathlib import Path

import pytest

from repair_assistant.task import TaskSpec, capture_workspace_baseline
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
    baseline = capture_workspace_baseline(task, task.source_dir)
    test_file.write_text("def test_x(): assert False\n", encoding="utf-8")

    result = PublicVerifier().verify(
        task=task,
        sandbox=PassingSandbox(),
        workspace=task.source_dir,
        workspace_baseline=baseline,
    )

    assert result.passed is False
    assert result.protected_files_unchanged is False


def test_public_verifier_allows_only_declared_editable_file(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    tests = workspace / "tests"
    tests.mkdir(parents=True)
    solution = workspace / "solution.py"
    solution.write_text("def f(): return 0\n", encoding="utf-8")
    (tests / "test_x.py").write_text("def test_x(): assert True\n", encoding="utf-8")
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    task = _task(workspace, hidden)
    baseline = capture_workspace_baseline(task, workspace)

    solution.write_text("def f(): return 1\n", encoding="utf-8")
    allowed = PublicVerifier().verify(
        task=task,
        sandbox=PassingSandbox(),
        workspace=workspace,
        workspace_baseline=baseline,
    )
    assert allowed.passed is True

    (workspace / "conftest.py").write_text("# pytest manipulation\n", encoding="utf-8")
    rejected = PublicVerifier().verify(
        task=task,
        sandbox=PassingSandbox(),
        workspace=workspace,
        workspace_baseline=baseline,
    )
    assert rejected.passed is False
    assert rejected.protected_files_unchanged is True
    assert rejected.workspace_policy_compliant is False
    assert "added non-editable workspace path: conftest.py" in rejected.violations


def test_public_verifier_checks_workspace_again_after_pytest(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    tests = workspace / "tests"
    tests.mkdir(parents=True)
    (workspace / "solution.py").write_text("def f(): return 0\n", encoding="utf-8")
    (tests / "test_x.py").write_text("def test_x(): assert True\n", encoding="utf-8")
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    task = _task(workspace, hidden)
    baseline = capture_workspace_baseline(task, workspace)

    class MutatingSandbox(PassingSandbox):
        def execute(
            self, command: str, *, cwd: str = ".", timeout_seconds: int = 120
        ) -> CommandResult:
            (workspace / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
            return super().execute(command, cwd=cwd, timeout_seconds=timeout_seconds)

    result = PublicVerifier().verify(
        task=task,
        sandbox=MutatingSandbox(),
        workspace=workspace,
        workspace_baseline=baseline,
    )

    assert result.passed is False
    assert "added non-editable workspace path: pytest.ini" in result.violations


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
