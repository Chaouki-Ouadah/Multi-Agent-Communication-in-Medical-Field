"""Real LLaVA-Med vision-language client (Vision Agent VQA on chest X-rays).

LLaVA-Med v1.5 (mistral-7b) is served locally by **Ollama** (`z-uo/llava-med-v1.5-mistral-7b_q8_0`),
the same serving path as the text LLM — GPU-accelerated, no bespoke `LlavaMistralForCausalLM`
codebase / transformers-version conflict. The client connects lazily on first `answer()`.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class VLMClient(Protocol):
    """Image + question in, text answer out."""

    def answer(self, image_path: Path, prompt: str) -> str: ...


class LlavaMedClient:
    """Real LLaVA-Med 7B VQA via Ollama (vision model with image input)."""

    def __init__(self, model_name: str | None = None, base_url: str | None = None) -> None:
        self.model_name = model_name or os.environ.get("VLM_MODEL", "rohithbojja/llava-med-v1.5")
        self.base_url = base_url or os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        self._client: Any = None  # lazy

    @property
    def is_loaded(self) -> bool:
        return self._client is not None

    def _ensure(self) -> Any:
        if self._client is None:
            import ollama

            self._client = ollama.Client(host=self.base_url)
        return self._client

    def answer(self, image_path: Path, prompt: str) -> str:
        client = self._ensure()
        response = client.generate(
            model=self.model_name,
            prompt=prompt,
            images=[str(image_path)],
            stream=False,
        )
        text = response["response"]
        return text.strip() if isinstance(text, str) else str(text)
