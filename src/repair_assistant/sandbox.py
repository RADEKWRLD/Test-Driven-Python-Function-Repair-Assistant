"""Resource-limited Docker execution with explicit mount boundaries."""

from __future__ import annotations

import contextlib
import os
import re
import subprocess
import time
from pathlib import Path, PurePosixPath
from typing import Protocol

from repair_assistant.types import CommandResult


class Sandbox(Protocol):
    def start(self) -> None: ...

    def execute(
        self, command: str, *, cwd: str = ".", timeout_seconds: int = 120
    ) -> CommandResult: ...

    def close(self) -> None: ...


class DockerSandboxError(RuntimeError):
    pass


class DockerSandbox:
    def __init__(
        self,
        *,
        workspace: Path,
        run_id: str,
        image: str = "function-repair/sandbox-python:dev",
        readonly_mounts: tuple[tuple[Path, str], ...] = (),
        cpus: float = 1.0,
        memory: str = "512m",
        pids_limit: int = 128,
        workspace_readonly: bool = False,
    ) -> None:
        self.workspace = workspace.resolve()
        self.container_name = "function-repair-" + re.sub(r"[^a-zA-Z0-9_.-]", "-", run_id)[:48]
        self.image = image
        self.readonly_mounts = readonly_mounts
        self.cpus = cpus
        self.memory = memory
        self.pids_limit = pids_limit
        self.workspace_readonly = workspace_readonly
        self._started = False

    def start(self) -> None:
        if self._started:
            return
        if not self.workspace.is_dir():
            raise DockerSandboxError(f"workspace does not exist: {self.workspace}")
        command = [
            "docker",
            "run",
            "--detach",
            "--name",
            self.container_name,
            "--network",
            "none",
            "--read-only",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,size=64m",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--pids-limit",
            str(self.pids_limit),
            "--memory",
            self.memory,
            "--cpus",
            str(self.cpus),
            "--user",
            f"{os.getuid()}:{os.getgid()}",
            "--env",
            "HOME=/tmp",
            "--env",
            "PYTHONDONTWRITEBYTECODE=1",
            "--env",
            "PYTHONUNBUFFERED=1",
            "--env",
            "PYTEST_ADDOPTS=-p no:cacheprovider",
        ]
        workspace_mount = f"type=bind,src={self.workspace},dst=/workspace"
        if self.workspace_readonly:
            workspace_mount += ",readonly"
        command.extend(["--mount", workspace_mount])
        for source, target in self.readonly_mounts:
            source = source.resolve()
            if not source.is_dir():
                raise DockerSandboxError(f"read-only mount does not exist: {source}")
            target_path = PurePosixPath(target)
            workspace_target = PurePosixPath("/workspace")
            if not target_path.is_absolute() or target_path.is_relative_to(workspace_target):
                raise DockerSandboxError("read-only mount target must be absolute and separate")
            command.extend(["--mount", f"type=bind,src={source},dst={target_path},readonly"])
        command.extend(["--workdir", "/workspace", self.image, "sleep", "infinity"])
        try:
            result = subprocess.run(
                command, capture_output=True, text=True, check=False, timeout=30
            )
        except subprocess.TimeoutExpired as exc:
            raise DockerSandboxError("Docker daemon timed out while starting sandbox") from exc
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise DockerSandboxError(f"failed to start Docker sandbox: {detail}")
        self._started = True

    def execute(self, command: str, *, cwd: str = ".", timeout_seconds: int = 120) -> CommandResult:
        if not self._started:
            raise DockerSandboxError("sandbox has not been started")
        relative = PurePosixPath(cwd)
        if relative.is_absolute() or ".." in relative.parts:
            raise DockerSandboxError("cwd must stay inside /workspace")
        docker_command = [
            "docker",
            "exec",
            "--workdir",
            str(PurePosixPath("/workspace") / relative),
            self.container_name,
            "timeout",
            "--signal=KILL",
            f"{timeout_seconds}s",
            "bash",
            "-lc",
            command,
        ]
        started = time.monotonic()
        try:
            result = subprocess.run(
                docker_command,
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout_seconds + 5,
            )
            return CommandResult(
                command,
                cwd,
                result.returncode,
                result.stdout,
                result.stderr,
                round((time.monotonic() - started) * 1000),
                result.returncode == 124,
            )
        except subprocess.TimeoutExpired as exc:
            return CommandResult(
                command,
                cwd,
                124,
                _timeout_text(exc.stdout),
                _timeout_text(exc.stderr),
                round((time.monotonic() - started) * 1000),
                True,
            )

    def close(self) -> None:
        if self._started:
            with contextlib.suppress(subprocess.TimeoutExpired):
                subprocess.run(
                    ["docker", "rm", "--force", self.container_name],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=10,
                )
            self._started = False

    def __enter__(self) -> DockerSandbox:
        self.start()
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()


def _timeout_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    return value.decode(errors="replace") if isinstance(value, bytes) else value
