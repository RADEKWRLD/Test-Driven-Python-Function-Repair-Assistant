import json
from pathlib import Path

import pytest

from repair_assistant.event_log import EventLog, EventLogIntegrityError


def test_event_log_detects_history_changes(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    log = EventLog(path, run_id="run-1", task_id="task-1")
    log.append("started", "controller", {"value": 1})
    log.append("finished", "controller", {"value": 2})
    lines = path.read_text(encoding="utf-8").splitlines()
    first = json.loads(lines[0])
    first["payload"]["value"] = 999
    lines[0] = json.dumps(first)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(EventLogIntegrityError):
        list(EventLog(path, run_id="run-1", task_id="task-1").read())
