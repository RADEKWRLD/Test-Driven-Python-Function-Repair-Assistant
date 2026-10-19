"""Provider-independent model turns and a minimal DeepSeek adapter."""

from __future__ import annotations

import json
import re
import ssl
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol, cast
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import certifi

Message = dict[str, Any]
ToolDefinition = dict[str, Any]


class ModelAdapterError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ToolCall:
    call_id: str
    name: str
    arguments_json: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.call_id,
            "type": "function",
            "function": {"name": self.name, "arguments": self.arguments_json},
        }


@dataclass(frozen=True, slots=True)
class ModelResponse:
    content: str | None
    tool_calls: tuple[ToolCall, ...] = ()
    finish_reason: str = "stop"
    response_id: str | None = None
    model: str | None = None
    provider: str = "unknown"
    usage: dict[str, Any] = field(default_factory=dict)

    def as_message(self) -> Message:
        message: Message = {"role": "assistant", "content": self.content}
        if self.tool_calls:
            message["tool_calls"] = [call.to_dict() for call in self.tool_calls]
        return message


class ModelAdapter(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def provider(self) -> str: ...

    @property
    def sensitive_values(self) -> tuple[str, ...]: ...

    def complete(
        self, messages: Sequence[Message], tools: Sequence[ToolDefinition]
    ) -> ModelResponse: ...


class DeepSeekAdapter:
    def __init__(
        self,
        *,
        api_key: str,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com",
        timeout_seconds: int = 120,
        max_tokens: int = 8192,
        ca_bundle: str | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("DeepSeek API key is required")
        self.api_key = api_key
        self._name = model
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.max_tokens = max_tokens
        try:
            self.ssl_context = ssl.create_default_context(cafile=ca_bundle or certifi.where())
        except (OSError, ssl.SSLError) as exc:
            raise ValueError(f"invalid CA bundle: {ca_bundle}") from exc

    @property
    def name(self) -> str:
        return self._name

    @property
    def provider(self) -> str:
        return "deepseek"

    @property
    def sensitive_values(self) -> tuple[str, ...]:
        return (self.api_key,)

    def complete(
        self, messages: Sequence[Message], tools: Sequence[ToolDefinition]
    ) -> ModelResponse:
        tool_choice: str | dict[str, object] = "auto"
        function = tools[0].get("function") if len(tools) == 1 else None
        if isinstance(function, dict) and function.get("name") == "submit_solution":
            tool_choice = {
                "type": "function",
                "function": {"name": "submit_solution"},
            }
        payload = {
            "model": self._name,
            "messages": list(messages),
            "tools": list(tools),
            "tool_choice": tool_choice,
            "temperature": 0,
            "max_tokens": self.max_tokens,
            "stream": False,
        }
        request = Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload, ensure_ascii=False).encode(),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(
                request,
                timeout=self.timeout_seconds,
                context=self.ssl_context,
            ) as response:
                body = response.read().decode()
        except HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            raise ModelAdapterError(f"DeepSeek returned HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise ModelAdapterError(f"DeepSeek request failed: {exc.reason}") from exc
        try:
            data = cast(dict[str, Any], json.loads(body))
            choice = cast(dict[str, Any], data["choices"][0])
            message = cast(dict[str, Any], choice["message"])
            calls = tuple(self._parse_tool_call(item) for item in message.get("tool_calls", []))
            usage = dict(cast(Mapping[str, Any], data.get("usage", {})))
            return ModelResponse(
                content=cast(str | None, message.get("content")),
                tool_calls=calls,
                finish_reason=str(choice["finish_reason"]),
                response_id=cast(str | None, data.get("id")),
                model=cast(str | None, data.get("model")),
                provider=self.provider,
                usage=usage,
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ModelAdapterError("DeepSeek returned an invalid completion") from exc

    @staticmethod
    def _parse_tool_call(value: Any) -> ToolCall:
        item = cast(dict[str, Any], value)
        function = cast(dict[str, Any], item["function"])
        return ToolCall(str(item["id"]), str(function["name"]), str(function["arguments"]))


_CODE_BLOCK = re.compile(r"```(?:python|py)?[ \t]*\n(.*?)\n?```", re.IGNORECASE | re.DOTALL)
_LOCAL_SYSTEM_PROMPT = """You repair one short Python pure-function implementation.
You cannot inspect files, execute commands, or run tests. The controller gives you the
requirement, current solution.py, and public test source. Return exactly one complete
replacement for solution.py as raw Python source. Do not use Markdown fences, explain
the answer, include tests, or create any other file. Preserve behavior not contradicted
by the requirement or public tests. Hidden tests are unavailable.
"""


class MlxLocalAdapter(DeepSeekAdapter):
    """Use an MLX OpenAI-compatible endpoint without relying on model tool calling.

    The controller still exposes only ``submit_solution``. This adapter asks the model
    for plain source and converts that response into the same single non-executable tool
    call consumed by the repair protocol.
    """

    def __init__(
        self,
        *,
        model: str = "default_model",
        base_url: str = "http://127.0.0.1:8080/v1",
        timeout_seconds: int = 600,
        max_tokens: int = 2048,
    ) -> None:
        super().__init__(
            api_key="local",
            model=model,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_tokens=max_tokens,
        )

    @property
    def provider(self) -> str:
        return "mlx-local"

    @property
    def sensitive_values(self) -> tuple[str, ...]:
        return ()

    def complete(
        self, messages: Sequence[Message], tools: Sequence[ToolDefinition]
    ) -> ModelResponse:
        if not _is_submit_solution_only(tools):
            raise ModelAdapterError("MLX local adapter only supports submit_solution")

        local_messages = [dict(message) for message in messages]
        if local_messages and local_messages[0].get("role") == "system":
            local_messages[0] = {"role": "system", "content": _LOCAL_SYSTEM_PROMPT}
        else:
            local_messages.insert(0, {"role": "system", "content": _LOCAL_SYSTEM_PROMPT})

        payload = {
            "model": self._name,
            "messages": local_messages,
            "temperature": 0,
            "max_tokens": self.max_tokens,
            "stream": False,
        }
        request = Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload, ensure_ascii=False).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(
                request,
                timeout=self.timeout_seconds,
                context=self.ssl_context,
            ) as response:
                body = response.read().decode()
        except HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            raise ModelAdapterError(f"MLX returned HTTP {exc.code}: {detail}") from exc
        except TimeoutError as exc:
            raise ModelAdapterError(
                f"MLX request timed out after {self.timeout_seconds} seconds"
            ) from exc
        except URLError as exc:
            raise ModelAdapterError(f"MLX request failed: {exc.reason}") from exc

        try:
            data = cast(dict[str, Any], json.loads(body))
            choice = cast(dict[str, Any], data["choices"][0])
            message = cast(dict[str, Any], choice["message"])
            content = cast(str, message["content"])
            source = _extract_source(content)
            usage = dict(cast(Mapping[str, Any], data.get("usage", {})))
            submission = ToolCall(
                "mlx-local-submit",
                "submit_solution",
                json.dumps({"content": source}, ensure_ascii=False),
            )
            return ModelResponse(
                content=content,
                tool_calls=(submission,),
                finish_reason=str(choice.get("finish_reason", "stop")),
                response_id=cast(str | None, data.get("id")),
                model=cast(str | None, data.get("model")),
                provider=self.provider,
                usage=usage,
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ModelAdapterError("MLX returned an invalid completion") from exc


def _is_submit_solution_only(tools: Sequence[ToolDefinition]) -> bool:
    if len(tools) != 1:
        return False
    function = tools[0].get("function")
    return isinstance(function, dict) and function.get("name") == "submit_solution"


def _extract_source(content: str) -> str:
    stripped = content.strip()
    if not stripped:
        raise ValueError("MLX returned an empty solution")
    blocks = _CODE_BLOCK.findall(stripped)
    if blocks:
        if len(blocks) != 1:
            raise ValueError("MLX returned multiple code blocks")
        stripped = blocks[0].strip()
    elif "```" in stripped:
        raise ValueError("MLX returned an unsupported fenced response")
    if not stripped:
        raise ValueError("MLX returned an empty solution")
    return stripped.rstrip() + "\n"


class ScriptedModel:
    """Deterministic adapter for tests; it never accesses a network."""

    def __init__(self, responses: Sequence[ModelResponse]) -> None:
        self._responses = iter(responses)

    @property
    def name(self) -> str:
        return "scripted-model"

    @property
    def provider(self) -> str:
        return "scripted"

    @property
    def sensitive_values(self) -> tuple[str, ...]:
        return ()

    def complete(
        self, messages: Sequence[Message], tools: Sequence[ToolDefinition]
    ) -> ModelResponse:
        del messages, tools
        try:
            return next(self._responses)
        except StopIteration as exc:
            raise ModelAdapterError("scripted model has no response left") from exc
