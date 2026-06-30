"""CLIP Image RAG — retrieve similar precedent CXRs by BioViL embedding (ChromaDB).

The Vision Agent embeds a query CXR and retrieves the top-k most similar indexed cases (with their
CheXpert/NIH labels) as precedent evidence. The embedder is injected (real `BioViLEmbedder` in
production; a deterministic fake in unit tests) so retrieval logic is testable without the model.
"""

from __future__ import annotations

import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


class _Embedder(Protocol):
    def embed_image(self, image_path: Path) -> Any: ...


@dataclass(frozen=True)
class Precedent:
    """A retrieved similar case: its id, labels, and distance to the query (nearest first)."""

    id: str
    labels: list[str]
    distance: float


class ClipImageRetriever:
    """BioViL-embedding image retriever backed by a ChromaDB collection (cosine space)."""

    def __init__(
        self,
        embedder: _Embedder,
        collection_name: str | None = None,
        client: Any = None,
    ) -> None:
        import chromadb

        self.embedder = embedder
        self._client = client or chromadb.EphemeralClient()
        # Unique per instance by default — ChromaDB caches clients/collections by name within a
        # process, so a fixed name collides across instances (e.g. tests with different embed dims).
        # Pass an explicit name for a stable persistent index.
        name = collection_name or f"cxr_{uuid.uuid4().hex}"
        self._collection = self._client.get_or_create_collection(
            name=name, metadata={"hnsw:space": "cosine"}
        )

    def build_index(self, items: Iterable[tuple[str, Path, list[str]]]) -> int:
        """Index (id, image_path, labels) triples. Returns the number indexed."""
        ids: list[str] = []
        embeddings: list[Any] = []
        metadatas: list[Any] = []
        for item_id, image_path, labels in items:
            ids.append(item_id)
            embeddings.append([float(x) for x in self.embedder.embed_image(image_path)])
            metadatas.append({"labels": "|".join(labels)})
        if ids:
            self._collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
        return len(ids)

    def retrieve(self, image_path: Path, k: int = 3) -> list[Precedent]:
        query: Any = [float(x) for x in self.embedder.embed_image(image_path)]
        res: Any = self._collection.query(query_embeddings=[query], n_results=k)
        ids = res["ids"][0]
        dists = res["distances"][0]
        metas = res["metadatas"][0]
        out: list[Precedent] = []
        for item_id, dist, meta in zip(ids, dists, metas, strict=True):
            labels = [x for x in str(meta.get("labels", "")).split("|") if x]
            out.append(Precedent(id=item_id, labels=labels, distance=float(dist)))
        return out
