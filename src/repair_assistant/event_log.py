"""Append-only JSONL experiment log with timestamps and sequence numbers."""

from __future__ import annotations

import json
import os
from collections.abc import Iterator, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class EventLogReadError(ValueError):
    pass


class EventLog:
    """One durable writer per run; historical lines are never rewritten."""

    def __init__(self, path: Path, *, run_id: str, task_id: str) -> None:
        self.path = path
        self.run_id = run_id
        self.task_id = task_id
        self.path.parent.mkdir(parents=True, exist_ok=True)
        existing = list(self.read()) if path.exists() else []
        self._sequence = int(existing[-1]["sequence"]) if existing else 0

    def append(self, event_type: str, actor: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        event: dict[str, Any] = {
            "schema_version": 2,
            "run_id": self.run_id,
            "task_id": self.task_id,
            "sequence": self._sequence + 1,
            "occurred_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "type": event_type,
            "actor": actor,
            "payload": dict(payload),
        }
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        self._sequence += 1
        return event

    def read(self) -> Iterator[dict[str, Any]]:
        if not self.path.exists():
            return
        with self.path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                try:
                    event = json.loads(line)
                    if not isinstance(event, dict) or "type" not in event or "payload" not in event:
                        raise ValueError("event requires type and payload")
                except (ValueError, KeyError, TypeError) as exc:
                    raise EventLogReadError(f"invalid event at line {line_number}") from exc
                yield event
