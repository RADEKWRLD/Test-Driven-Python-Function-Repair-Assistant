import json
from typing import Any
from urllib.request import Request

import pytest

import repair_assistant.model as model_module
from repair_assistant.model import DeepSeekAdapter, ModelResponse, ScriptedModel

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


def test_deepseek_submission_explicitly_disables_server_default_thinking(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_urlopen(request: Request, **_kwargs: object) -> FakeResponse:
        assert isinstance(request.data, bytes)
        captured.update(json.loads(request.data))
        return FakeResponse(
            {
                "model": "deepseek-flash",
                "choices": [
                    {
                        "finish_reason": "tool_calls",
                        "message": {
                            "content": None,
                            "tool_calls": [
                                {
                                    "id": "submission",
                                    "function": {
                                        "name": "submit_solution",
                                        "arguments": json.dumps({"content": "def f(): return 1\n"}),
                                    },
                                }
                            ],
                        },
                    }
                ],
                "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18},
            }
        )

    monkeypatch.setattr(model_module, "urlopen", fake_urlopen)
    response = DeepSeekAdapter(api_key="test-key", model="deepseek-flash").complete(
        [{"role": "user", "content": "repair f"}],
        [SUBMIT_TOOL],
    )
    assert captured["thinking"] == {"type": "disabled"}
    assert captured["tool_choice"]["function"]["name"] == "submit_solution"
    assert response.tool_calls[0].name == "submit_solution"
    assert response.usage["total_tokens"] == 18


def test_scripted_model_remains_an_offline_test_adapter() -> None:
    expected = ModelResponse(content="deterministic")

    response = ScriptedModel([expected]).complete(
        [{"role": "user", "content": "ignored"}],
        [SUBMIT_TOOL],
    )

    assert response is expected
    assert ScriptedModel([expected]).provider == "scripted"
