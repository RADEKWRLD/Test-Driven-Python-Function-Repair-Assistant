import ast
from pathlib import Path

from repair_assistant.task import TaskSpec


def test_benchmark_contains_thirty_separated_test_functions() -> None:
    root = Path(__file__).resolve().parents[1] / "benchmarks/tasks"
    public_count = 0
    hidden_count = 0
    tasks = sorted(path.parent for path in root.glob("*/task.json"))

    for task_dir in tasks:
        task = TaskSpec.load(task_dir)
        assert not task.hidden_tests_dir.is_relative_to(task.source_dir)
        public_count += _count_tests(task.source_dir / "tests")
        hidden_count += _count_tests(task.hidden_tests_dir)

    assert len(tasks) == 3
    assert public_count == 15
    assert hidden_count == 15


def _count_tests(directory: Path) -> int:
    count = 0
    for path in directory.glob("test_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        count += sum(
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
            for node in tree.body
        )
    return count
