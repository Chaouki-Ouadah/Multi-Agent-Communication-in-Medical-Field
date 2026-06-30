"""Graph retrieval for SRQ2 config B — Neo4j entity-relationship + Microsoft GraphRAG community search.

Two faithful halves of dissertation §4.5.2 / Table 4.4:
- `Neo4jGraphRetriever`: pulls a query's clinical entities, looks up their neighbourhood in the PrimeKG
  Neo4j graph (entity-relationship retrieval), returns them as `RetrievedItem`s.
- `GraphRAGRetriever`: calls Microsoft GraphRAG (local/global community search) in its **isolated
  `.venv-graphrag`** via **subprocess** — this module never imports `graphrag` (numpy~=2.1 clash with the
  core env). Mockable via an injected `runner` for unit tests.

`make_graph_retriever` composes whichever halves are available into one `Retriever` (config B); the
Card-10a `HybridRetriever` then folds B into config C with the text + image retrievers.
"""

from __future__ import annotations

import subprocess  # nosec B404 - fixed venv interpreter + list args, never shell; see _run
from collections.abc import Callable
from pathlib import Path
from typing import Any, Protocol

from src.knowledge.retrieval import HybridRetriever, RetrievalQuery, RetrievedItem, Retriever


class _Client(Protocol):
    def run(self, cypher: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]: ...


def _default_entities(text: str) -> list[str]:
    """Fallback entity extractor — distinct capitalised/long tokens (real use injects scispaCy NER)."""
    seen: list[str] = []
    for tok in text.replace(",", " ").split():
        t = tok.strip(".;:")
        if len(t) > 3 and t.lower() not in {"with", "from", "that", "this"} and t not in seen:
            seen.append(t)
    return seen


class Neo4jGraphRetriever:
    """Entity-relationship retrieval over the PrimeKG Neo4j graph (config B, half 1)."""

    def __init__(
        self,
        client: _Client,
        entities: Callable[[str], list[str]] | None = None,
        source: str = "neo4j_kg",
    ) -> None:
        self.client = client
        self.entities = entities or _default_entities
        self.source = source

    def retrieve(self, query: RetrievalQuery, k: int = 5) -> list[RetrievedItem]:
        if not query.text:
            return []
        items: list[RetrievedItem] = []
        for entity in self.entities(query.text):
            rows = self.client.run(
                "MATCH (a:Entity)-[r]-(b:Entity) WHERE toLower(a.name) = toLower($name) "
                "RETURN b.name AS neighbour, type(r) AS relation, b.type AS ntype LIMIT $k",
                {"name": entity, "k": k},
            )
            for row in rows:
                items.append(
                    RetrievedItem(
                        content=f"{entity} —{row.get('relation', 'related')}→ "
                        f"{row.get('neighbour', '?')} ({row.get('ntype', '')})",
                        source=self.source,
                        score=1.0,
                        modality="graph",
                        metadata=dict(row),
                    )
                )
        return items[:k]


class GraphRAGRetriever:
    """Microsoft GraphRAG community search via the isolated venv (config B, half 2; subprocess)."""

    def __init__(
        self,
        workspace: str,
        venv_python: str,
        runner: Callable[[str], str] | None = None,
        method: str = "local",
        source: str = "graphrag",
    ) -> None:
        self.workspace = workspace
        self.venv_python = venv_python
        self.method = method
        self.source = source
        self._runner = runner  # injected in tests; None → real subprocess

    def is_available(self) -> bool:
        """True only if the isolated venv python + an indexed workspace are both present."""
        if self._runner is not None:
            return True
        py = Path(self.venv_python)
        output = Path(self.workspace) / "output"
        return py.exists() and output.exists()

    def _run(self, question: str) -> str:
        if self._runner is not None:
            return self._runner(question)
        python = str(Path(self.venv_python).resolve())  # absolute + OS-native separators
        proc = subprocess.run(  # nosec B603 - fixed interpreter + literal argv, shell=False, no user shell
            [
                python,
                "-m",
                "graphrag",
                "query",
                "--root",
                self.workspace,
                "--method",
                self.method,
                question,  # positional QUERY arg
            ],
            capture_output=True,
            text=True,
            timeout=300,
            shell=False,
        )
        return proc.stdout

    def retrieve(self, query: RetrievalQuery, k: int = 5) -> list[RetrievedItem]:
        if not query.text:
            return []
        text = self._run(query.text).strip()
        if not text:
            return []
        return [
            RetrievedItem(
                content=text,
                source=self.source,
                score=1.0,
                modality="graph",
                metadata={"method": self.method},
            )
        ]


def make_graph_retriever(
    neo4j_graph: Retriever | None = None, graphrag: Retriever | None = None
) -> Retriever:
    """Compose the available graph halves into one config-B retriever."""
    members = [r for r in (neo4j_graph, graphrag) if r is not None]
    if not members:
        raise ValueError("config B needs a Neo4j and/or GraphRAG retriever")
    if len(members) == 1:
        return members[0]
    return HybridRetriever(members)
