"""Card 3 — real model clients (Ollama Meditron / LLaVA-Med / BioViL).

Pure tests (CI): config parsing, lazy loading, protocol conformance — no model loaded.
Live tests (`llm` + `slow`, local only; CI skips): exercise the REAL models / Ollama.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from src.agents.embeddings import BioViLEmbedder, ImageEmbedder
from src.agents.llm_client import LLMClient, LLMConfig, OllamaLLMClient, llm_config
from src.agents.vlm_client import LlavaMedClient, VLMClient


# ── PURE: config from env ────────────────────────────────────────────────────
def test_llm_config_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    for k in ("LLM_PRIMARY_MODEL", "OLLAMA_BASE_URL", "LLM_TEMPERATURE", "LLM_REQUEST_TIMEOUT"):
        monkeypatch.delenv(k, raising=False)
    cfg = llm_config()
    assert isinstance(cfg, LLMConfig)
    assert cfg.model == "meditron"
    assert cfg.base_url == "http://localhost:11434"
    assert cfg.temperature == 0.2


def test_llm_config_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PRIMARY_MODEL", "llama3.1:8b")
    monkeypatch.setenv("LLM_TEMPERATURE", "0.7")
    cfg = llm_config()
    assert cfg.model == "llama3.1:8b"
    assert cfg.temperature == 0.7


# ── PURE: construction does NOT load the model (lazy) ────────────────────────
def test_clients_lazy_load() -> None:
    assert OllamaLLMClient().is_loaded is False
    assert BioViLEmbedder().is_loaded is False
    assert LlavaMedClient().is_loaded is False


# ── PURE: protocol conformance ───────────────────────────────────────────────
def test_protocol_conformance() -> None:
    assert isinstance(OllamaLLMClient(), LLMClient)
    assert isinstance(BioViLEmbedder(), ImageEmbedder)
    assert isinstance(LlavaMedClient(), VLMClient)


# ── LIVE: real models (local only; CI skips llm/slow) ────────────────────────
@pytest.mark.llm
def test_ollama_generate_live() -> None:
    out = OllamaLLMClient().generate("List two chest X-ray signs of cardiomegaly.")
    assert isinstance(out, str) and out.strip()


@pytest.mark.llm
@pytest.mark.slow
def test_biovil_embed_live(sample_cxr: Path) -> None:
    emb = BioViLEmbedder()
    vec = emb.embed_image(sample_cxr)
    assert isinstance(vec, np.ndarray)
    assert vec.ndim == 1 and vec.shape[0] == emb.embed_dim


@pytest.mark.llm
@pytest.mark.slow
def test_llava_med_answer_live(sample_cxr: Path) -> None:
    out = LlavaMedClient().answer(sample_cxr, "Describe the chest X-ray findings.")
    assert isinstance(out, str) and out.strip()
