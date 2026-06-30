"""Knowledge-graph schema + PrimeKG ingestion for the Neo4j medical KG (SRQ2 config B).

PrimeKG (Chandak et al., Harvard/MIT-licensed) is an open precision-medicine knowledge graph that
harmonises ~20 sources (DrugBank, MONDO, HPO, Reactome, …). Its `kg.csv` is an edge list with columns
`relation, display_relation, x_id, x_type, x_name, x_source, y_id, y_type, y_name, y_source`. This
module defines the node/relation records, parses a row into them, and ingests rows into Neo4j via the
`Neo4jClient`. UMLS/SNOMED (licensed) are out of scope — PrimeKG + ICD-10 only.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Protocol

# PrimeKG node types (x_type / y_type values).
NODE_TYPES: frozenset[str] = frozenset(
    {
        "disease",
        "drug",
        "gene/protein",
        "effect/phenotype",
        "biological_process",
        "molecular_function",
        "cellular_component",
        "pathway",
        "anatomy",
        "exposure",
    }
)


@dataclass(frozen=True)
class KGNode:
    """A PrimeKG entity."""

    id: str
    type: str
    name: str
    source: str = ""


@dataclass(frozen=True)
class KGRelation:
    """A directed PrimeKG edge between two entities (`relation` = canonical, `display` = readable)."""

    source_id: str
    relation: str
    target_id: str
    display: str = ""


class _Client(Protocol):
    def run(self, cypher: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]: ...


def parse_primekg_row(row: dict[str, Any]) -> tuple[KGNode, KGRelation, KGNode]:
    """Parse one PrimeKG `kg.csv` row into (source node, relation, target node)."""
    x = KGNode(
        id=str(row["x_id"]), type=row["x_type"], name=row["x_name"], source=row.get("x_source", "")
    )
    y = KGNode(
        id=str(row["y_id"]), type=row["y_type"], name=row["y_name"], source=row.get("y_source", "")
    )
    rel = KGRelation(
        source_id=x.id,
        relation=row["relation"],
        target_id=y.id,
        display=row.get("display_relation", ""),
    )
    return x, rel, y


def _safe_rel_type(relation: str) -> str:
    """Neo4j relationship types must be alphanumeric/underscore; normalise the PrimeKG label."""
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in relation).strip("_").upper()
    return cleaned or "RELATED"


def ingest_primekg(client: _Client, rows: Iterable[dict[str, Any]], batch: int = 1000) -> int:
    """Ingest PrimeKG rows into Neo4j (MERGE nodes + relationship). Returns the number of edges ingested."""
    count = 0
    for row in rows:
        x, rel, y = parse_primekg_row(row)
        client.run(
            "MERGE (a:Entity {id: $xid}) SET a.name=$xname, a.type=$xtype, a.source=$xsrc "
            "MERGE (b:Entity {id: $yid}) SET b.name=$yname, b.type=$ytype, b.source=$ysrc "
            f"MERGE (a)-[r:{_safe_rel_type(rel.relation)}]->(b) SET r.display=$display",
            {
                "xid": x.id,
                "xname": x.name,
                "xtype": x.type,
                "xsrc": x.source,
                "yid": y.id,
                "yname": y.name,
                "ytype": y.type,
                "ysrc": y.source,
                "display": rel.display,
            },
        )
        count += 1
    return count
