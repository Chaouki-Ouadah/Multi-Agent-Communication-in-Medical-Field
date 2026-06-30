"""Card 10b — ingest PrimeKG into Neo4j (SRQ2 config B, half 1).

PrimeKG (Chandak et al., Harvard Dataverse, MIT-licensed) is an open precision-medicine KG. Download
`kg.csv` from https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IXA7BM and run:

    python scripts/ingest_primekg.py path/to/kg.csv            # full ingest
    python scripts/ingest_primekg.py path/to/kg.csv --limit 5000   # subset for dev

Credentials come from the environment (NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD) — see .env.example.
The full graph is large (~8M edges); ingestion is batched and idempotent (MERGE).
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections.abc import Iterator
from typing import Any

from src.knowledge.kg_schema import ingest_primekg
from src.knowledge.neo4j_client import Neo4jClient


def _rows(path: str, limit: int | None) -> Iterator[dict[str, Any]]:
    with open(path, newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f)):
            if limit is not None and i >= limit:
                return
            yield row


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest PrimeKG kg.csv into Neo4j.")
    parser.add_argument("csv_path", help="path to PrimeKG kg.csv")
    parser.add_argument("--limit", type=int, default=None, help="ingest only the first N edges")
    args = parser.parse_args()

    client = Neo4jClient()  # creds from env / .env
    if not client.is_available():
        print("ERROR: Neo4j not reachable (check NEO4J_* env / that the container is running).")
        return 1
    n = ingest_primekg(client, _rows(args.csv_path, args.limit))
    client.close()
    print(f"ingested {n} edges from {args.csv_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
