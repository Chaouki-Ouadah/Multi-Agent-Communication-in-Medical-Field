"""Card 10a — unified retriever interface + Vector RAG (config A) + hybrid fusion. Pure (no LLM)."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.knowledge.retrieval import (
    HybridRetriever,
    RetrievalConfig,
    RetrievalQuery,
    RetrievedItem,
    TextVectorRetriever,
    build_retriever,
)

_VOCAB = [
    "cardiomegaly",
    "effusion",
    "pneumonia",
    "atelectasis",
    "pneumothorax",
    "normal",
    "bnp",
    "edema",
]


class FakeTextEmbedder:
    """Deterministic bag-of-words embedder over a fixed vocab (identical text → identical vector)."""

    def embed_text(self, text: str) -> list[float]:
        low = text.lower()
        vec = [float(low.count(word)) for word in _VOCAB]
        if not any(vec):
            vec[0] = 0.0
            vec.append(1.0)  # avoid all-zero (cosine undefined); keep deterministic
        return vec


class MockRetriever:
    """Returns a fixed list of RetrievedItem regardless of query (for hybrid tests)."""

    def __init__(self, items: list[RetrievedItem]) -> None:
        self._items = items
        self.queries: list[RetrievalQuery] = []

    def retrieve(self, query: RetrievalQuery, k: int = 5) -> list[RetrievedItem]:
        self.queries.append(query)
        return self._items[:k]


# ── config enum + factory ─────────────────────────────────────────────────────
def test_config_enum_has_abc() -> None:
    assert {c.name for c in RetrievalConfig} == {"VECTOR", "GRAPH", "HYBRID"}


def test_build_retriever_vector_and_hybrid() -> None:
    text = TextVectorRetriever(embedder=FakeTextEmbedder())
    built_a = build_retriever(RetrievalConfig.VECTOR, text_retriever=text)
    assert built_a is text
    built_c = build_retriever(
        RetrievalConfig.HYBRID, text_retriever=text, image_retriever=MockRetriever([])
    )
    assert isinstance(built_c, HybridRetriever)


def test_build_retriever_graph_requires_graph_retriever() -> None:
    # config B (GraphRAG) is implemented in Card 10b; build needs a graph_retriever injected
    with pytest.raises(ValueError, match="graph"):
        build_retriever(RetrievalConfig.GRAPH)


# ── shared interface ────────────────────────────────────────────────────────
def test_retrievers_share_interface() -> None:
    text = TextVectorRetriever(embedder=FakeTextEmbedder())
    hybrid = HybridRetriever([text])
    for r in (text, hybrid, MockRetriever([])):
        assert callable(r.retrieve)
        assert r.retrieve(RetrievalQuery(text="x"), k=1) is not None


# ── config A: real ChromaDB text vector RAG ─────────────────────────────────
def test_text_vector_retriever_indexes_and_retrieves() -> None:
    text = TextVectorRetriever(embedder=FakeTextEmbedder())
    n = text.build_index(
        [
            ("d1", "cardiomegaly with pleural effusion", {"src": "guideline"}),
            ("d2", "pneumonia consolidation", {}),
            ("d3", "pneumothorax left apex", {}),
        ]
    )
    assert n == 3
    hits = text.retrieve(RetrievalQuery(text="pneumonia"), k=1)
    assert len(hits) == 1
    assert isinstance(hits[0], RetrievedItem)
    assert "pneumonia" in hits[0].content.lower()
    assert hits[0].modality == "text"


def test_text_vector_empty_query_returns_empty() -> None:
    text = TextVectorRetriever(embedder=FakeTextEmbedder())
    text.build_index([("d1", "cardiomegaly", {})])
    assert text.retrieve(RetrievalQuery(text=None), k=3) == []


# ── config C: hybrid fusion (graph-ready) ────────────────────────────────────
def _item(content: str, source: str, modality: str, score: float) -> RetrievedItem:
    return RetrievedItem(content=content, source=source, score=score, modality=modality)


def test_hybrid_combines_modalities() -> None:
    text = MockRetriever([_item("text evidence", "text_vector", "text", 0.9)])
    image = MockRetriever([_item("similar CXR: Cardiomegaly", "image_clip", "image", 0.8)])
    graph = MockRetriever([_item("BNP -> heart failure", "graph", "graph", 0.7)])
    hybrid = HybridRetriever([text, image, graph])
    hits = hybrid.retrieve(RetrievalQuery(text="q", image_path=Path("x.png")), k=5)
    modalities = {h.modality for h in hits}
    assert modalities == {"text", "image", "graph"}
    # every sub-retriever was consulted
    assert text.queries and image.queries and graph.queries


def test_hybrid_dedupes_and_respects_k() -> None:
    a = MockRetriever([_item("same finding", "text_vector", "text", 0.9)])
    b = MockRetriever([_item("same finding", "graph", "graph", 0.5)])
    hybrid = HybridRetriever([a, b])
    hits = hybrid.retrieve(RetrievalQuery(text="q"), k=5)
    assert len(hits) == 1  # deduped by content
    hits_capped = HybridRetriever(
        [MockRetriever([_item(f"f{i}", "text_vector", "text", 0.5) for i in range(10)])]
    ).retrieve(RetrievalQuery(text="q"), k=3)
    assert len(hits_capped) == 3
