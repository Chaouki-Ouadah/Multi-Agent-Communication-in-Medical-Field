"""Card 10b — assemble the GraphRAG indexing corpus from PubMed abstracts (SRQ2 config B, half 2).

Per dissertation §4.5.2 the GraphRAG corpus is built from open clinical text (guidelines, textbook
excerpts, PubMed abstracts). To stay licence-clean we use **PubMed abstracts** (open, fetched via NCBI
E-utilities) for the focus-5 pathologies — NO copyrighted guideline text is committed. A small
hand-written sample lives in data/graphrag_corpus/sample/ for dev/tests.

    python scripts/build_graphrag_corpus.py --out .graphrag/input --per-term 20

Then index with the isolated venv (see docs/graphrag-neo4j-setup.md). Network required.
"""

from __future__ import annotations

import argparse
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

_EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
_TERMS = [
    "cardiomegaly chest radiograph",
    "pleural effusion chest x-ray",
    "pneumonia radiographic findings",
    "pneumothorax chest radiograph",
    "atelectasis chest imaging",
]


def _get(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def _pmids(term: str, n: int) -> list[str]:
    q = urllib.parse.urlencode({"db": "pubmed", "term": term, "retmax": n, "retmode": "json"})
    import json

    data = json.loads(_get(f"{_EUTILS}/esearch.fcgi?{q}"))
    return data.get("esearchresult", {}).get("idlist", [])


def _abstracts(pmids: list[str]) -> str:
    if not pmids:
        return ""
    q = urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(pmids), "rettype": "abstract", "retmode": "text"}
    )
    return _get(f"{_EUTILS}/efetch.fcgi?{q}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a PubMed-abstract corpus for GraphRAG.")
    parser.add_argument("--out", default=".graphrag/input", help="output directory")
    parser.add_argument("--per-term", type=int, default=20, help="abstracts per pathology term")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for term in _TERMS:
        pmids = _pmids(term, args.per_term)
        text = _abstracts(pmids)
        if text.strip():
            slug = term.split()[0]
            (out / f"pubmed_{slug}.txt").write_text(text, encoding="utf-8")
            print(f"{term}: {len(pmids)} abstracts")
        time.sleep(0.4)  # be polite to NCBI
    return 0


if __name__ == "__main__":
    sys.exit(main())
