"""Best-effort secret removal for persisted model and tool observations."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

REDACTED = "[REDACTED]"
_SENSITIVE_KEY = re.compile(r"(api[_-]?key|authorization|password|secret|token)", re.I)
_BEARER = re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]+")


def redact(value: Any, *, secrets: Sequence[str] = ()) -> Any:
    if isinstance(value, str):
        result = _BEARER.sub(f"Bearer {REDACTED}", value)
        for secret in secrets:
            if secret:
                result = result.replace(secret, REDACTED)
        return result
    if isinstance(value, Mapping):
        return {
            str(key): REDACTED if _SENSITIVE_KEY.search(str(key)) else redact(item, secrets=secrets)
            for key, item in value.items()
        }
    if isinstance(value, tuple):
        return tuple(redact(item, secrets=secrets) for item in value)
    if isinstance(value, list):
        return [redact(item, secrets=secrets) for item in value]
    return value
