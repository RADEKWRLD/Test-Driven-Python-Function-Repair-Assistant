"""Append-only, hash-chained JSONL experiment log."""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Iterator, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


class EventLogIntegrityError(ValueError):
    pass


def _canonical(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


class EventLog:
    """One durable writer per run; historical lines are never rewritten."""

    def __init__(self, path: Path, *, run_id: str, task_id: str) -> None:
        self.path = path
        self.run_id = run_id
        self.task_id = task_id
        self.path.parent.mkdir(parents=True, exist_ok=True)
        existing = list(self.read()) if path.exists() else []
        self._sequence = int(existing[-1]["sequence"]) if existing else 0
        self._previous = existing[-1]["integrity"]["digest"] if existing else "0" * 64

    def append(self, event_type: str, actor: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        event: dict[str, Any] = {
            "schema_version": 1,
            "event_id": f"evt_{uuid4().hex}",
            "run_id": self.run_id,
            "task_id": self.task_id,
            "sequence": self._sequence + 1,
            "occurred_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "type": event_type,
            "actor": actor,
            "payload": dict(payload),
            "integrity": {"algorithm": "sha256", "previous_digest": self._previous},
        }
        digest = hashlib.sha256(_canonical(event)).hexdigest()
        event["integrity"]["digest"] = digest
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        self._sequence += 1
        self._previous = digest
        return event

    def read(self) -> Iterator[dict[str, Any]]:
        if not self.path.exists():
            return
        previous = "0" * 64
        sequence = 0
        with self.path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                try:
                    event = json.loads(line)
                    integrity = dict(event["integrity"])
                    supplied = str(integrity.pop("digest"))
                except (json.JSONDecodeError, KeyError, TypeError) as exc:
                    raise EventLogIntegrityError(f"invalid event at line {line_number}") from exc
                unsigned = dict(event)
                unsigned["integrity"] = integrity
                expected = hashlib.sha256(_canonical(unsigned)).hexdigest()
                if int(event["sequence"]) != sequence + 1:
                    raise EventLogIntegrityError(f"non-contiguous sequence at line {line_number}")
                if integrity.get("previous_digest") != previous or supplied != expected:
                    raise EventLogIntegrityError(f"digest mismatch at line {line_number}")
                event["integrity"]["digest"] = supplied
                previous = supplied
                sequence += 1
                yield event
