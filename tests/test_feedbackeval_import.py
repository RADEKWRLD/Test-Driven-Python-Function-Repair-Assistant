import json
from pathlib import Path

from repair_assistant.task import TaskSpec


def test_checked_in_feedbackeval_tasks_exclude_oracles_and_feedback() -> None:
    root = Path(__file__).resolve().parents[1] / "benchmarks/feedbackeval-humaneval"
    manifest = json.loads((root / "dataset-manifest.json").read_text(encoding="utf-8"))
    tasks = sorted(path.parent for path in root.glob("*/task.json"))

    assert manifest["selection"]["outcome_blind"] is True
    assert manifest["test_policy"]["correct_code_copied"] is False
    assert len(tasks) == len(manifest["tasks"]) == 50
    assert {item["candidate_source"] for item in manifest["tasks"]} <= {
        "existing",
        "llm-based",
        "rule_based",
    }
    for task_dir in tasks:
        task = TaskSpec.load(task_dir)
        assert task.editable_paths == ("solution.py",)
        assert not task.hidden_tests_dir.is_relative_to(task.source_dir)
        text = (task_dir / "task.json").read_text(encoding="utf-8")
        assert '"correct_code"' not in text
        assert "llm_expert_feedback" not in text
        assert "test_feedback" not in text

    preflight = json.loads((root / "preflight.json").read_text(encoding="utf-8"))
    assert preflight["tasks"] == preflight["initial_public_failures"] == 50
    assert preflight["timeouts"] == 0


def test_full_feedbackeval_humaneval_has_all_tasks_and_evalplus_hidden_tests() -> None:
    root = Path(__file__).resolve().parents[1] / "benchmarks/feedbackeval-humaneval-full"
    manifest = json.loads((root / "dataset-manifest.json").read_text(encoding="utf-8"))
    tasks = sorted(path.parent for path in root.glob("*/task.json"))

    assert manifest["count"] == len(manifest["tasks"]) == len(tasks) == 164
    assert manifest["selection"] == {"method": "complete-HumanEval", "outcome_blind": True}
    assert manifest["candidate_overrides"] == {"57": 2, "105": 0}
    assert manifest["oracle_invalid_inputs_removed"] == 7
    assert manifest["test_policy"]["correct_code_copied"] is False
    assert manifest["test_policy"]["precomputed_feedback_copied"] is False
    assert {item["source_task_id"] for item in manifest["tasks"]} == {
        f"HumanEval/{number}" for number in range(164)
    }
    for task_dir in tasks:
        task = TaskSpec.load(task_dir)
        assert task.test_version == "feedbackeval-base-evalplus-v0.1.10-hidden-v2"
        assert not task.hidden_tests_dir.is_relative_to(task.source_dir)
        manifest_text = (task_dir / "task.json").read_text(encoding="utf-8")
        assert '"correct_code"' not in manifest_text
        assert "llm_expert_feedback" not in manifest_text

    preflight = json.loads((root / "preflight.json").read_text(encoding="utf-8"))
    assert preflight["tasks"] == preflight["initial_public_failures"] == 164
    assert preflight["timeouts"] == 0

    hidden_preflight = json.loads(
        (root / "hidden-reference-preflight.json").read_text(encoding="utf-8")
    )
    assert hidden_preflight["tasks"] == hidden_preflight["reference_hidden_passes"] == 164
    assert hidden_preflight["timeouts"] == 0
