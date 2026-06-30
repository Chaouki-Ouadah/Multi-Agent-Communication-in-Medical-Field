"""Card 10b — Neo4j KG (PrimeKG) + GraphRAG retrievers + configs B/C wiring.

Pure tests mock the Neo4j driver + the GraphRAG subprocess (no server, no venv, no network).
Live tests (`slow`) are skip-marked unless a Neo4j server / GraphRAG venv is actually present.
"""

from __future__ import annotations

import os

import pytest

from src.knowledge.graph_rag import GraphRAGRetriever, Neo4jGraphRetriever, make_graph_retriever
from src.knowledge.kg_schema import (
    NODE_TYPES,
    KGNode,
    KGRelation,
    ingest_primekg,
    parse_primekg_row,
)
from src.knowledge.neo4j_client import Neo4jClient
from src.knowledge.retrieval import (
    HybridRetriever,
    RetrievalConfig,
    RetrievalQuery,
    build_retriever,
)

# ── PrimeKG schema ───────────────────────────────────────────────────────────
_ROW = {
    "relation": "indication",
    "display_relation": "treats",
    "x_id": "DB001",
    "x_type": "drug",
    "x_name": "Furosemide",
    "x_source": "DrugBank",
    "y_id": "D010",
    "y_type": "disease",
    "y_name": "Heart failure",
    "y_source": "MONDO",
}


def test_kg_schema_types() -> None:
    assert {"disease", "drug", "gene/protein", "effect/phenotype"} <= NODE_TYPES


def test_parse_primekg_row() -> None:
    x, rel, y = parse_primekg_row(_ROW)
    assert isinstance(x, KGNode) and isinstance(y, KGNode) and isinstance(rel, KGRelation)
    assert x.id == "DB001" and x.type == "drug" and x.name == "Furosemide"
    assert y.id == "D010" and y.type == "disease"
    assert rel.source_id == "DB001" and rel.target_id == "D010" and rel.relation == "indication"


# ── Neo4j client (mock driver — no server) ───────────────────────────────────
class _FakeSession:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows

    def __enter__(self) -> _FakeSession:
        return self

    def __exit__(self, *a: object) -> None:
        return None

    def run(self, cypher: str, params: dict | None = None) -> list[_FakeRecord]:
        return [_FakeRecord(r) for r in self._rows]


class _FakeRecord:
    def __init__(self, data: dict) -> None:
        self._data = data

    def data(self) -> dict:
        return self._data


class _FakeDriver:
    def __init__(self, rows: list[dict]) -> None:
        self.rows = rows
        self.closed = False

    def session(self) -> _FakeSession:
        return _FakeSession(self.rows)

    def verify_connectivity(self) -> None:
        return None

    def close(self) -> None:
        self.closed = True


def test_neo4j_client_creds_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NEO4J_PASSWORD", raising=False)
    client = Neo4jClient(uri="bolt://x:7687", user="neo4j")
    # no password + no injected driver → refuses to connect (no hardcoded default)
    with pytest.raises(RuntimeError, match="NEO4J_PASSWORD"):
        client.run("RETURN 1")


def test_neo4j_client_run_with_mock_driver() -> None:
    driver = _FakeDriver([{"ok": 1}])
    client = Neo4jClient(driver=driver)
    assert client.run("RETURN 1 AS ok") == [{"ok": 1}]
    assert client.is_available() is True


class _RecordingClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def run(self, cypher: str, params: dict | None = None) -> list[dict]:
        self.calls.append((cypher, params or {}))
        return []


def test_ingest_primekg_counts_rows() -> None:
    client = _RecordingClient()
    n = ingest_primekg(client, [_ROW, dict(_ROW, x_id="DB002")], batch=1)
    assert n == 2
    assert client.calls  # issued cypher upserts


# ── graph retrievers ─────────────────────────────────────────────────────────
def test_neo4j_graph_retriever_maps_results() -> None:
    rows = [{"neighbour": "Heart failure", "relation": "treats", "ntype": "disease"}]
    client = Neo4jClient(driver=_FakeDriver(rows))
    retr = Neo4jGraphRetriever(client, entities=lambda t: ["Furosemide"])
    hits = retr.retrieve(RetrievalQuery(text="Furosemide for oedema"), k=5)
    assert hits and hits[0].modality == "graph"
    assert "Heart failure" in hits[0].content


def test_neo4j_graph_retriever_empty_query() -> None:
    client = Neo4jClient(driver=_FakeDriver([]))
    assert Neo4jGraphRetriever(client).retrieve(RetrievalQuery(text=None)) == []


def test_graphrag_retriever_parses_output() -> None:
    # inject a fake subprocess runner (no venv needed)
    retr = GraphRAGRetriever(
        workspace="ws",
        venv_python="py",
        runner=lambda q: "Bilateral opacities + high BNP suggest oedema.",
    )
    hits = retr.retrieve(RetrievalQuery(text="bilateral opacities high BNP"), k=3)
    assert hits and hits[0].modality == "graph"
    assert "oedema" in hits[0].content.lower()


def test_graphrag_retriever_unavailable_is_graceful() -> None:
    retr = GraphRAGRetriever(workspace="/nope", venv_python="/nope/python")
    assert retr.is_available() is False
    # empty query → empty, regardless of availability
    assert retr.retrieve(RetrievalQuery(text=None)) == []


# ── configs B / C wired live ─────────────────────────────────────────────────
def test_build_retriever_b_with_graph() -> None:
    client = Neo4jClient(
        driver=_FakeDriver([{"neighbour": "X", "relation": "r", "ntype": "disease"}])
    )
    graph = make_graph_retriever(neo4j_graph=Neo4jGraphRetriever(client, entities=lambda t: ["q"]))
    built = build_retriever(RetrievalConfig.GRAPH, graph_retriever=graph)
    assert built is graph


def test_build_retriever_b_requires_graph() -> None:
    with pytest.raises(ValueError, match="graph"):
        build_retriever(RetrievalConfig.GRAPH)


def test_build_retriever_c_includes_graph() -> None:
    client = Neo4jClient(
        driver=_FakeDriver([{"neighbour": "Pneumonia", "relation": "sign", "ntype": "disease"}])
    )
    graph = Neo4jGraphRetriever(client, entities=lambda t: ["q"])
    built = build_retriever(RetrievalConfig.HYBRID, graph_retriever=graph)
    assert isinstance(built, HybridRetriever)
    hits = built.retrieve(RetrievalQuery(text="q"), k=5)
    assert any(h.modality == "graph" for h in hits)


# ── live (skip-marked) ───────────────────────────────────────────────────────
@pytest.mark.slow
def test_primekg_ingest_and_retrieve_live() -> None:
    client = Neo4jClient()  # creds from env / .env
    if not client.is_available():
        pytest.skip("no Neo4j server reachable")
    ingest_primekg(client, [_ROW], batch=10)
    retr = Neo4jGraphRetriever(client, entities=lambda t: ["Furosemide"])
    hits = retr.retrieve(RetrievalQuery(text="Furosemide"), k=5)
    assert isinstance(hits, list)


@pytest.mark.slow
def test_graphrag_query_live() -> None:
    ws = os.environ.get("GRAPHRAG_WORKSPACE", ".graphrag")
    venv = os.environ.get("GRAPHRAG_VENV_PYTHON", ".venv-graphrag/Scripts/python.exe")
    retr = GraphRAGRetriever(workspace=ws, venv_python=venv)
    if not retr.is_available():
        pytest.skip("GraphRAG venv / workspace not present")
    hits = retr.retrieve(
        RetrievalQuery(text="differential for bilateral opacities with elevated BNP")
    )
    assert isinstance(hits, list)
