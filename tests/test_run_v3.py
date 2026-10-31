import json
from pathlib import Path
from typing import Any

from repair_assistant.agent import RepairStrategy
from repair_assistant.event_log import EventLog
from repair_assistant.model import ModelResponse, ScriptedModel, ToolCall
from repair_assistant.run import RunService
from repair_assistant.task import TaskSpec
from repair_assistant.types import CommandResult


def test_v3_evaluates_baseline_first_final_without_executing_candidates(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    task_dir = tmp_path / "task"
    tests = task_dir / "workspace/tests"
    tests.mkdir(parents=True)
    hidden = task_dir / "hidden_tests"
    hidden.mkdir()
    (tests.parent / "solution.py").write_text("def f(): return 0\n", encoding="utf-8")
    for file in (tests / "test_public.py", hidden / "test_hidden.py"):
        file.write_text("def test_a(): pass\ndef test_b(): pass\n", encoding="utf-8")
    task = TaskSpec(
        "t",
        "title",
        "goal",
        (),
        "python -m pytest -q tests",
        ("tests",),
        tests.parent,
        hidden,
        "python -m pytest -q /hidden_tests",
    )

    class Sandbox:
        def __init__(self, **kwargs: Any) -> None:
            self.workspace = kwargs["workspace"]
            self.container_name = "fake"
            self.report = ""

        def start(self) -> None:
            pass

        def close(self) -> None:
            pass

        def execute(
            self, command: str, *, cwd: str = ".", timeout_seconds: int = 120
        ) -> CommandResult:
            if command.startswith("cat "):
                return CommandResult(command, cwd, 0, self.report, "", 0)
            # Read text markers only. No host eval/import/exec of the submitted code.
            code = (self.workspace / "solution.py").read_text(encoding="utf-8")
            outcomes = (
                [True, True]
                if "FINAL" in code
                else [False, True]
                if "FIRST" in code
                else [True, False]
            )
            module = "test_hidden" if "/hidden_tests" in command else "test_public"
            cases = "".join(
                f'<testcase classname="{module}" name="test_{name}">'
                + ("" if passed else "<failure/>")
                + "</testcase>"
                for name, passed in zip(("a", "b"), outcomes, strict=True)
            )
            self.report = f"<testsuites><testsuite>{cases}</testsuite></testsuites>"
            return CommandResult(
                command, cwd, 0 if all(outcomes) else 1, "public diagnostic", "", 2
            )

    monkeypatch.setattr("repair_assistant.run.DockerSandbox", Sandbox)
    model = ScriptedModel(
        [
            ModelResponse(
                None,
                (ToolCall("fix", "submit_solution", json.dumps({"content": code})),),
                usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            )
            for code in ("def f(): return 1 # FIRST\n", "def f(): return 2 # FINAL\n")
        ]
    )
    result = RunService(data_dir=tmp_path / "data").execute(
        task=task,
        model=model,
        strategy=RepairStrategy.TEST_FEEDBACK,
    )
    summary = json.loads((result.run_dir / "summary.json").read_text(encoding="utf-8"))
    assert (result.run_dir / "original_code/solution.py").is_file()
    assert (result.run_dir / "repair_attempts/01/solution.py").is_file()
    assert (result.run_dir / "repair_attempts/02/solution.py").is_file()
    assert summary["protocol"]["version"] == 3
    assert summary["case_changes"]["baseline_to_final"]["fixed"] == 1
    assert summary["case_changes"]["first_to_final"]["fixed"] == 1
    assert summary["test_runtime_ms"] == 14  # 2 repair checks + 5 final-stage evaluations
    assert summary["cost"]["total_tokens"] == 30
    events = list(
        EventLog(result.run_dir / "events.jsonl", run_id=result.run_id, task_id="t").read()
    )
    hidden_index = next(i for i, e in enumerate(events) if e["type"] == "hidden_verification")
    last_model_index = max(i for i, e in enumerate(events) if e["type"] == "model_request")
    assert hidden_index > last_model_index
