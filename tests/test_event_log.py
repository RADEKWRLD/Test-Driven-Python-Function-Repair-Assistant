import json
from pathlib import Path

import pytest

from repair_assistant.event_log import EventLog, EventLogReadError


def test_event_log_appends_plain_jsonl_and_can_be_reopened(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    EventLog(path, run_id="run-1", task_id="task-1").append("started", "controller", {"value": 1})
    log = EventLog(path, run_id="run-1", task_id="task-1")
    log.append("finished", "controller", {"value": 2})
    events = list(log.read())
    assert [event["sequence"] for event in events] == [1, 2]
    assert all("integrity" not in event for event in events)
    assert events[1]["payload"] == {"value": 2}
    # Ordinary logs deliberately make no tamper-proof claim.
    first = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    first["payload"]["value"] = 999
    path.write_text(json.dumps(first) + "\n", encoding="utf-8")
    assert next(log.read())["payload"]["value"] == 999


def test_event_log_reports_malformed_json_without_inventing_events(tmp_path: Path) -> None:
    path = tmp_path / "bad.jsonl"
    path.write_text("{broken\n", encoding="utf-8")
    with pytest.raises(EventLogReadError, match="line 1"):
        EventLog(path, run_id="run-1", task_id="task-1")
