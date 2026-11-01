import ast
from pathlib import Path

from repair_assistant.cases import compare_cases, execute_cases, parse_junit
from repair_assistant.types import CommandResult


def test_junit_preserves_failure_error_and_unexecuted_states() -> None:
    result = parse_junit("""<testsuites><testsuite>
      <testcase classname="tests.test_x" name="test_a"/>
      <testcase classname="tests.test_x" name="test_b"><failure/></testcase>
      <testcase classname="tests.test_x" name="test_c"><error/></testcase>
      <testcase classname="tests.test_x" name="test_d"><skipped/></testcase>
    </testsuite></testsuites>""")
    assert result == {
        "test_x::test_a": "passed",
        "test_x::test_b": "failed",
        "test_x::test_c": "error",
        "test_x::test_d": "not_run",
    }


def test_missing_junit_never_turns_zero_exit_into_a_success() -> None:
    class Sandbox:
        def execute(
            self, command: str, *, cwd: str = ".", timeout_seconds: int = 120
        ) -> CommandResult:
            return CommandResult(command, cwd, 0, "", "", 1)

        def start(self) -> None:
            pass

        def close(self) -> None:
            pass

    _, cases, complete = execute_cases(
        Sandbox(),
        "python -m pytest -q tests",
        expected=("test_x::test_a",),
        timeout_seconds=1,
    )
    assert complete is False
    assert cases == {"test_x::test_a": "not_run"}


def test_timeout_does_not_become_an_assertion_regression() -> None:
    class Sandbox:
        def execute(
            self, command: str, *, cwd: str = ".", timeout_seconds: int = 120
        ) -> CommandResult:
            return CommandResult(command, cwd, 124, "", "", 1000, True)

        def start(self) -> None:
            pass

        def close(self) -> None:
            pass

    _, cases, complete = execute_cases(
        Sandbox(),
        "python -m pytest",
        expected=("test_x::test_a",),
        timeout_seconds=1,
    )
    assert not complete
    assert cases["test_x::test_a"] == "timeout"
    assert compare_cases({"test_x::test_a": "passed"}, cases)["regressed"] == 0


def test_regression_can_be_detected_with_unchanged_total_pass_count() -> None:
    result = compare_cases(
        {"a": "passed", "b": "failed", "c": "passed"},
        {"a": "failed", "b": "passed", "c": "timeout"},
    )
    assert result == {"fixed": 1, "regressed": 1, "net_improvement": 0, "unavailable": 1}


def test_all_frozen_assertions_have_independent_cases() -> None:
    root = Path(__file__).resolve().parents[1] / "benchmarks/humanevalpack"
    for path in root.glob("*/hidden_tests/test_hidden.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        assert len(functions) >= 5
        assert all(sum(isinstance(n, ast.Assert) for n in ast.walk(f)) == 1 for f in functions)
