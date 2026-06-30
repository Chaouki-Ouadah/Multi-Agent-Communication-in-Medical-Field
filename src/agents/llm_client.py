"""Real Ollama text-LLM client (Meditron-8B) for the Report / Clinical / Supervisor agents.

A typed `LLMClient` Protocol + a real `OllamaLLMClient` (via `langchain_ollama.ChatOllama`). The
model handle is created lazily on first `generate()` so importing/constructing is cheap (keeps CI and
unit tests fast). Config comes from the environment — never hardcode model names in business logic.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class LLMConfig:
    model: str
    base_url: str
    temperature: float
    timeout: int


def llm_config() -> LLMConfig:
    """Read LLM settings from the environment (with dissertation defaults)."""
    return LLMConfig(
        model=os.environ.get("LLM_PRIMARY_MODEL", "meditron"),
        base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=float(os.environ.get("LLM_TEMPERATURE", "0.2")),
        timeout=int(os.environ.get("LLM_REQUEST_TIMEOUT", "120")),
    )


@runtime_checkable
class LLMClient(Protocol):
    """Text-in, text-out language model."""

    def generate(self, prompt: str, system: str | None = None) -> str: ...


class OllamaLLMClient:
    """Real text LLM served locally by Ollama (default model: Meditron-8B)."""

    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or llm_config()
        self._llm: Any = None  # lazy

    @property
    def is_loaded(self) -> bool:
        return self._llm is not None

    def _ensure(self) -> Any:
        if self._llm is None:
            from langchain_ollama import ChatOllama

            self._llm = ChatOllama(
                model=self.config.model,
                base_url=self.config.base_url,
                temperature=self.config.temperature,
            )
        return self._llm

    def generate(self, prompt: str, system: str | None = None) -> str:
        llm = self._ensure()
        messages: list[tuple[str, str]] = []
        if system:
            messages.append(("system", system))
        messages.append(("human", prompt))
        response = llm.invoke(messages)
        content = getattr(response, "content", response)
        return content if isinstance(content, str) else str(content)
