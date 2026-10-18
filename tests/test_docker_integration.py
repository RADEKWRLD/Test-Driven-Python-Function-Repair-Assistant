import json
import subprocess
from pathlib import Path

import pytest

from repair_assistant.agent import RepairStrategy
from repair_assistant.model import ModelResponse, ScriptedModel, ToolCall
from repair_assistant.run import RunService
from repair_assistant.task import TaskSpec

IMAGE = "function-repair/sandbox-python:dev"


def _require_image() -> None:
    try:
        result = subprocess.run(
            ["docker", "image", "inspect", IMAGE],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        pytest.skip("Docker daemon timed out")
    if result.returncode != 0:
        pytest.skip(f"Docker daemon or image unavailable: {result.stderr.strip()}")


@pytest.mark.sandbox
def test_scripted_repair_and_hidden_verification_are_isolated(tmp_path: Path) -> None:
    _require_image()
    root = Path(__file__).resolve().parents[1]
    task = TaskSpec.load(root / "benchmarks/tasks/chunk-list")

    model = ScriptedModel(
        [
            ModelResponse(
                content=None,
                tool_calls=(
                    ToolCall(
                        "fix",
                        "submit_solution",
                        json.dumps(
                            {
                                "content": (
                                    "def chunk_list(items, size):\n"
                                    "    if size <= 0:\n"
                                    '        raise ValueError("size must be positive")\n'
                                    "    return [items[i:i + size] "
                                    "for i in range(0, len(items), size)]\n"
                                )
                            }
                        ),
                    ),
                ),
                finish_reason="tool_calls",
            ),
        ]
    )

    result = RunService(data_dir=tmp_path, image=IMAGE).execute(
        task=task,
        model=model,
        strategy=RepairStrategy.TEST_FEEDBACK,
    )

    assert result.outcome == "passed"
    assert result.first_public.passed is True
    assert result.first_hidden.passed is True
    assert result.agent.attempts[0].repair_verification is not None
    assert result.agent.attempts[0].repair_verification.passed is True
    assert not (result.run_dir / "workspace/hidden_tests").exists()
