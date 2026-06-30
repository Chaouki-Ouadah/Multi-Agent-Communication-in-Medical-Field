"""Unified retrieval interface for the SRQ2 infrastructure sweep (configs A / B / C).

The dissertation (Table 4.4) compares three retrieval backends with everything else held constant:
**A** Vector RAG (ChromaDB text), **B** GraphRAG (Microsoft GraphRAG + Neo4j), **C** Multimodal Hybrid
(text vector + GraphRAG + CLIP Image RAG). This module gives all retrievers ONE interface so the agents
can be run unchanged across configs, and implements **A** (real ChromaDB text RAG) + **C** (hybrid
fusion). **B** lands in Card 10b (Microsoft GraphRAG in an isolated venv + a populated Neo4j); here
`build_retriever(GRAPH)` raises a clear `NotImplementedError`. The hybrid is graph-ready: it fans a
query out to any injected sub-retrievers, so the real GraphRAG retriever slots in with no interface
change.

Corpus is external-only (public ontologies + guidelines/PubMed) — no patient text → no train/test
leakage into SRQ2 (dissertation §4.5.2/4.5.4).
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from src.knowledge.retriever import ClipImageRetriever


class RetrievalConfig(Enum):
    """SRQ2 infrastructure-sweep conditions (dissertation Table 4.4)."""

    VECTOR = "A"  # text vector RAG (ChromaDB)
    GRAPH = "B"  # Microsoft GraphRAG + Neo4j (Card 10b)
    HYBRID = "C"  # text vector + graph + CLIP image


@dataclass(frozen=True)
class RetrievalQuery:
    """A retrieval request. Carries optional text and/or an image so one interface spans modalities."""

    text: str | None = None
    image_path: Path | None = None


@dataclass(frozen=True)
class RetrievedItem:
    """One retrieved piece of evidence, with its source retriever, modality and normalised score."""

    content: str
    source: str
    score: float
    modality: str
    metadata: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class Retriever(Protocol):
    """Every backend (vector / graph / image / hybrid) implements this single method."""

    def retrieve(self, query: RetrievalQuery, k: int = 5) -> list[RetrievedItem]: ...


class _TextEmbedder(Protocol):
    def embed_text(self, text: str) -> Any: ...


class TextVectorRetriever:
    """Config A — semantic text retrieval over a ChromaDB cosine collection (injected embedder)."""

    def __init__(
        self,
        embedder: _TextEmbedder,
        collection_name: str | None = None,
        client: Any = None,
        source: str = "text_vector",
    ) -> None:
        import chromadb

        self.embedder = embedder
        self.source = source
        self._client = client or chromadb.EphemeralClient()
        name = collection_name or f"text_{uuid.uuid4().hex}"
        self._collection = self._client.get_or_create_collection(
            name=name, metadata={"hnsw:space": "cosine"}
        )

    def build_index(self, items: Iterable[tuple[str, str, dict[str, Any]]]) -> int:
        """Index (id, text, metadata) triples. Returns the number indexed."""
        ids: list[str] = []
        embeddings: list[Any] = []
        documents: list[str] = []
        metadatas: list[Any] = []
        for item_id, text, metadata in items:
            ids.append(item_id)
            embeddings.append([float(x) for x in self.embedder.embed_text(text)])
            documents.append(text)
            metadatas.append(metadata or {"_": ""})
        if ids:
            self._collection.add(
                ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas
            )
        return len(ids)

    def retrieve(self, query: RetrievalQuery, k: int = 5) -> list[RetrievedItem]:
        if not query.text:
            return []
        vec: Any = [float(x) for x in self.embedder.embed_text(query.text)]
        res: Any = self._collection.query(query_embeddings=[vec], n_results=k)
        docs = res["documents"][0]
        dists = res["distances"][0]
        metas = res["metadatas"][0]
        out: list[RetrievedItem] = []
        for doc, dist, meta in zip(docs, dists, metas, strict=True):
            out.append(
                RetrievedItem(
                    content=doc,
                    source=self.source,
                    score=1.0 - float(dist),  # cosine distance → similarity
                    modality="text",
                    metadata=dict(meta) if meta else {},
                )
            )
        return out


class ClipImageRetrieverAdapter:
    """Adapts the Card-4 `ClipImageRetriever` (image → Precedent) to the unified `Retriever`."""

    def __init__(self, retriever: ClipImageRetriever, source: str = "image_clip") -> None:
        self.retriever = retriever
        self.source = source

    def retrieve(self, query: RetrievalQuery, k: int = 5) -> list[RetrievedItem]:
        if query.image_path is None:
            return []
        precedents = self.retriever.retrieve(query.image_path, k)
        out: list[RetrievedItem] = []
        for p in precedents:
            labels = ", ".join(p.labels) if p.labels else "no labels"
            out.append(
                RetrievedItem(
                    content=f"Visually similar prior CXR labelled: {labels}",
                    source=self.source,
                    score=1.0 - float(p.distance),
                    modality="image",
                    metadata={"id": p.id, "labels": p.labels},
                )
            )
        return out


def _minmax_normalise(items: list[RetrievedItem]) -> list[RetrievedItem]:
    """Rescale a single retriever's scores to [0, 1] so heterogeneous backends merge fairly."""
    if not items:
        return items
    scores = [it.score for it in items]
    lo, hi = min(scores), max(scores)
    if hi == lo:
        return [RetrievedItem(it.content, it.source, 1.0, it.modality, it.metadata) for it in items]
    span = hi - lo
    return [
        RetrievedItem(it.content, it.source, (it.score - lo) / span, it.modality, it.metadata)
        for it in items
    ]


class HybridRetriever:
    """Config C — fan a query out to N sub-retrievers, normalise, dedupe by content, return top-k.

    Graph-ready: pass the (Card-10b) GraphRAG retriever alongside the text + image retrievers and it
    is fused with no interface change.
    """

    def __init__(self, retrievers: list[Retriever]) -> None:
        self.retrievers = retrievers

    def retrieve(self, query: RetrievalQuery, k: int = 5) -> list[RetrievedItem]:
        merged: dict[str, RetrievedItem] = {}
        for retriever in self.retrievers:
            for item in _minmax_normalise(retriever.retrieve(query, k)):
                existing = merged.get(item.content)
                if existing is None or item.score > existing.score:
                    merged[item.content] = item  # dedupe by content, keep best score
        ranked = sorted(merged.values(), key=lambda it: it.score, reverse=True)
        return ranked[:k]


def build_retriever(
    config: RetrievalConfig,
    *,
    text_retriever: Retriever | None = None,
    image_retriever: Retriever | None = None,
    graph_retriever: Retriever | None = None,
) -> Retriever:
    """Build the retriever for an SRQ2 config. GRAPH (config B) lands in Card 10b."""
    if config is RetrievalConfig.VECTOR:
        if text_retriever is None:
            raise ValueError("config A (VECTOR) needs a text_retriever")
        return text_retriever
    if config is RetrievalConfig.GRAPH:
        if graph_retriever is None:
            raise ValueError("config B (GRAPH) needs a graph_retriever (Neo4j and/or GraphRAG)")
        return graph_retriever
    if config is RetrievalConfig.HYBRID:
        members = [r for r in (text_retriever, image_retriever, graph_retriever) if r is not None]
        if not members:
            raise ValueError("config C (HYBRID) needs at least one sub-retriever")
        return HybridRetriever(members)
    raise ValueError(f"unknown config: {config}")  # pragma: no cover
