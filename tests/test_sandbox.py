from pathlib import Path
from typing import Any

from repair_assistant.sandbox import DockerSandbox


def test_docker_start_uses_required_isolation_flags(monkeypatch: Any, tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    recorded: list[list[str]] = []

    class Result:
        returncode = 0
        stdout = "container-id"
        stderr = ""

    def fake_run(command: list[str], **_kwargs: object) -> Result:
        recorded.append(command)
        return Result()

    monkeypatch.setattr("repair_assistant.sandbox.subprocess.run", fake_run)
    sandbox = DockerSandbox(workspace=workspace, run_id="run-1")

    sandbox.start()

    command = recorded[0]
    assert command[command.index("--network") + 1] == "none"
    assert "--read-only" in command
    assert command[command.index("--cap-drop") + 1] == "ALL"
    assert "DEEPSEEK_API_KEY" not in " ".join(command)
    mount = command[command.index("--mount") + 1]
    assert str(workspace) in mount


def test_hidden_verifier_can_mount_workspace_readonly(monkeypatch: Any, tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    recorded: list[list[str]] = []

    class Result:
        returncode = 0
        stdout = "container-id"
        stderr = ""

    def fake_run(command: list[str], **_kwargs: object) -> Result:
        recorded.append(command)
        return Result()

    monkeypatch.setattr("repair_assistant.sandbox.subprocess.run", fake_run)

    DockerSandbox(workspace=workspace, run_id="hidden", workspace_readonly=True).start()

    command = recorded[0]
    mount = command[command.index("--mount") + 1]
    assert mount.endswith(",readonly")
