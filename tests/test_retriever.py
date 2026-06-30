"""Card 4 — CLIP Image RAG retriever (BioViL embeddings in ChromaDB).

Pure tests use a deterministic fake embedder + an ephemeral ChromaDB so retrieval is reproducible
without loading BioViL or hitting the network.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from src.knowledge.retriever import ClipImageRetriever, Precedent


class FakeEmbedder:
    """Deterministic per-path vector (same path -> same vector) for reproducible retrieval."""

    embed_dim = 8

    def embed_image(self, image_path: Path) -> np.ndarray:
        h = int(hashlib.md5(Path(image_path).stem.encode()).hexdigest(), 16) % (2**32)
        return np.random.default_rng(h).random(self.embed_dim).astype(np.float32)


def _items() -> list[tuple[str, Path, list[str]]]:
    return [
        ("a", Path("a.png"), ["Cardiomegaly"]),
        ("b", Path("b.png"), ["Pneumonia", "Atelectasis"]),
        ("c", Path("c.png"), ["No Finding"]),
    ]


def test_retrieve_self_is_top1() -> None:
    r = ClipImageRetriever(embedder=FakeEmbedder())
    r.build_index(_items())
    top = r.retrieve(Path("b.png"), k=1)
    assert len(top) == 1
    assert isinstance(top[0], Precedent)
    assert top[0].id == "b"  # identical embedding -> nearest is itself
    assert "Pneumonia" in top[0].labels


def test_retrieve_topk_count_and_order() -> None:
    r = ClipImageRetriever(embedder=FakeEmbedder())
    r.build_index(_items())
    res = r.retrieve(Path("a.png"), k=3)
    assert next(p.id for p in res) == "a"  # self first
    assert len(res) == 3
    assert all(isinstance(p.distance, float) for p in res)
    # distances non-decreasing (nearest first)
    assert res == sorted(res, key=lambda p: p.distance)
