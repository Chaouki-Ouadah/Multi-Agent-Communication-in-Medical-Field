"""Neo4j client wrapper — the medical knowledge graph backing SRQ2 config B.

Thin wrapper over the official `neo4j` driver. Credentials come from the environment
(`NEO4J_URI` / `NEO4J_USER` / `NEO4J_PASSWORD`) — never hardcoded; the real password lives in a
gitignored `.env` (see `.env.example`). A driver can be injected for unit tests (no live server).
"""

from __future__ import annotations

import os
from typing import Any

_DEFAULT_URI = "bolt://localhost:7687"
_DEFAULT_USER = "neo4j"


class Neo4jClient:
    """Connects to Neo4j and runs Cypher; raises if no password is configured (no hardcoded default)."""

    def __init__(
        self,
        uri: str | None = None,
        user: str | None = None,
        password: str | None = None,
        driver: Any = None,
    ) -> None:
        self.uri = uri or os.environ.get("NEO4J_URI", _DEFAULT_URI)
        self.user = user or os.environ.get("NEO4J_USER", _DEFAULT_USER)
        self.password = password or os.environ.get("NEO4J_PASSWORD")
        self._driver = driver

    def _ensure(self) -> Any:
        if self._driver is None:
            if not self.password:
                raise RuntimeError(
                    "NEO4J_PASSWORD not set — configure it in .env (no hardcoded credentials)"
                )
            from neo4j import GraphDatabase

            self._driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        return self._driver

    def is_available(self) -> bool:
        """True if the server is reachable (used to skip live tests when it isn't)."""
        try:
            self._ensure().verify_connectivity()
            return True
        except Exception:
            return False

    def run(self, cypher: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        with self._ensure().session() as session:
            return [record.data() for record in session.run(cypher, params or {})]

    def upsert_node(self, label: str, key: str, props: dict[str, Any]) -> None:
        self.run(
            f"MERGE (n:{label} {{id: $key}}) SET n += $props",
            {"key": key, "props": props},
        )

    def upsert_relationship(
        self, src_id: str, rel_type: str, dst_id: str, props: dict[str, Any] | None = None
    ) -> None:
        self.run(
            "MATCH (a {id: $src}), (b {id: $dst}) "
            f"MERGE (a)-[r:{rel_type}]->(b) SET r += $props",
            {"src": src_id, "dst": dst_id, "props": props or {}},
        )

    def close(self) -> None:
        if self._driver is not None:
            self._driver.close()
