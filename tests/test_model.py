import json
from typing import Any
from urllib.request import Request

import pytest

import repair_assistant.model as model_module
from repair_assistant.model import MlxLocalAdapter, ModelAdapterError

SUBMIT_TOOL = {
    "type": "function",
    "function": {
        "name": "submit_solution",
        "parameters": {
            "type": "object",
            "properties": {"content": {"type": "string"}},
            "required": ["content"],
        },
    },
}


class FakeResponse:
    def __init__(self, body: dict[str, Any]) -> None:
        self.body = body

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.body).encode()


def test_mlx_adapter_turns_plain_code_into_submission(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_urlopen(request: Request, **_kwargs: object) -> FakeResponse:
        request_data = request.data
        assert isinstance(request_data, bytes)
        captured.update(json.loads(request_data))
        return FakeResponse(
            {
                "id": "chatcmpl-local",
                "model": "default_model",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"content": "```python\ndef add(a, b):\n    return a + b\n```"},
                    }
                ],
                "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18},
            }
        )

    monkeypatch.setattr(model_module, "urlopen", fake_urlopen)
    adapter = MlxLocalAdapter()

    response = adapter.complete(
        [
            {"role": "system", "content": "call submit_solution"},
            {"role": "user", "content": "fix add"},
        ],
        [SUBMIT_TOOL],
    )

    assert "tools" not in captured
    assert "tool_choice" not in captured
    assert "raw Python source" in captured["messages"][0]["content"]
    assert response.provider == "mlx-local"
    assert response.usage["total_tokens"] == 18
    assert len(response.tool_calls) == 1
    assert response.tool_calls[0].name == "submit_solution"
    assert json.loads(response.tool_calls[0].arguments_json) == {
        "content": "def add(a, b):\n    return a + b\n"
    }


def test_mlx_adapter_rejects_multiple_code_blocks(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(_request: Request, **_kwargs: object) -> FakeResponse:
        return FakeResponse(
            {
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"content": "```python\na = 1\n```\n```python\nb = 2\n```"},
                    }
                ]
            }
        )

    monkeypatch.setattr(model_module, "urlopen", fake_urlopen)

    with pytest.raises(ModelAdapterError, match="invalid completion"):
        MlxLocalAdapter().complete([{"role": "user", "content": "fix"}], [SUBMIT_TOOL])


def test_mlx_adapter_reports_request_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(_request: Request, **_kwargs: object) -> FakeResponse:
        raise TimeoutError

    monkeypatch.setattr(model_module, "urlopen", fake_urlopen)

    with pytest.raises(ModelAdapterError, match="timed out after 7 seconds"):
        MlxLocalAdapter(timeout_seconds=7).complete(
            [{"role": "user", "content": "fix"}], [SUBMIT_TOOL]
        )
