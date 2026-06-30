# Plan — Card 10b: Microsoft GraphRAG (isolated venv) + Neo4j KG (PrimeKG) — configs B/C live

## Context
Card 10a shipped the unified `Retriever` interface + config A (Vector RAG) + graph-ready
`HybridRetriever`; config B raised `NotImplementedError`. Card 10b makes **config B** real — the two
faithful halves of dissertation §4.5.2 + Table 4.4:
1. **Neo4j entity-relationship retrieval** over the **PrimeKG** ontology (open, Harvard/MIT).
2. **Microsoft GraphRAG** community-detection (local + global search) over a clinical-text corpus.
Then wires B + C live in `build_retriever`. Branch `feature/graphrag`. Heavy-faithful path
([[heavy-faithful-path]]).

## Hard isolation rule (why subprocess)
MS GraphRAG pins `numpy~=2.1`, incompatible with the `medargue` numpy<2 / scispaCy stack. So GraphRAG
lives in a **separate `.venv-graphrag`** and is invoked by **subprocess** — `medargue` code NEVER
imports `graphrag` (keeps CI import-smoke + the core env clean). Also: **uninstall the stray
`graphrag 3.0.2`** a prior session left in `medargue` (housekeeping; not in requirements, so CI is
already clean). Neo4j driver (`neo4j`, already pinned) imports fine in CI; live connection is
skip-marked.

## State map
- `knowledge/retrieval.py` (10a) — `Retriever`, `RetrievalQuery/Item`, `HybridRetriever`,
  `build_retriever` (B raises). EDIT: B/C build the real graph retriever when injected.
- `knowledge/graph_rag.py`, `neo4j_client.py`, `kg_schema.py` — stubs → implement.
- Neo4j Docker `neo4j-medargue` live + driver-verified (bolt://localhost:7687, creds via `.env`).
- `neo4j` driver 6.2.0 in env. `chromadb` present. No graphrag in `requirements.txt` (stays out).

## Approach (files)
- **`src/knowledge/neo4j_client.py`** — `Neo4jClient(uri, user, password)` (all from env: `NEO4J_URI`,
  `NEO4J_USER`, `NEO4J_PASSWORD`; **no hardcoded creds**). `verify()`, `run(cypher, params)`,
  `upsert_node`, `upsert_relationship`, `close`, `is_available()` (ping → False on failure, for
  skip-marking). Lazy driver.
- **`src/knowledge/kg_schema.py`** — PrimeKG node/relation type constants (disease, drug, gene/protein,
  phenotype/effect, pathway, anatomy…); `parse_primekg_row(row) -> (src_node, rel, dst_node)` (pure,
  unit-tested on a tiny fixture); `ingest_primekg(client, rows, batch=1000)` (batched MERGE; live).
- **`src/knowledge/graph_rag.py`**:
  - `Neo4jGraphRetriever(client)` — entity-relationship retrieval: extract query entities (reuse
    scispaCy NER from Card 5) → Cypher neighbourhood lookup → `RetrievedItem`s (modality="graph").
  - `GraphRAGRetriever(workspace, venv_python)` — **subprocess** to `.venv-graphrag` running
    `graphrag query` (local + global); parse output → `RetrievedItem`s. `is_available()` checks venv
    + indexed artifacts. Never imports graphrag in-process.
  - `CompositeGraphRetriever([...])` — config B = Neo4j entity-rel + GraphRAG community, merged.
- **`src/knowledge/retrieval.py`** (edit) — `build_retriever(B, graph_retriever=...)` returns the graph
  retriever (or raises a clear error if none injected); `C` already composes via `HybridRetriever`.
- **`scripts/setup_graphrag_venv.ps1` + `.sh`** — create `.venv-graphrag`, `pip install -r
  requirements-graphrag.txt`, `graphrag init` workspace, write `settings.yaml` pointed at **Ollama**
  (local LLM + embeddings — no OpenAI key).
- **`scripts/build_graphrag_corpus.py`** — assemble the indexing corpus from **PubMed abstracts**
  (focus-5 pathologies, via NCBI E-utilities) — open/permissible; **no copyrighted guideline text
  committed**. Small committed sample for dev/tests.
- **`scripts/ingest_primekg.py`** — download PrimeKG (Harvard Dataverse) → `ingest_primekg` into Neo4j
  (full, one-off). A tiny PrimeKG sample CSV committed for live-test ingest.
- **`requirements-graphrag.txt`** — pinned `graphrag` (isolated venv only; NOT in `requirements.txt`).
- **`.env.example`** — `NEO4J_URI/USER/PASSWORD` (real `.env` gitignored).
- **`docs/graphrag-neo4j-setup.md`** — full setup + run guide.
- **tests/`test_kg.py`** — pure: schema, `parse_primekg_row`, `Neo4jClient.run` (mock driver),
  `Neo4jGraphRetriever` mapping (mock client), `GraphRAGRetriever` parse (mock subprocess),
  `build_retriever` B/C wiring. Live (`slow`, skip if no server/venv): real PrimeKG-sample ingest +
  retrieve; real `graphrag query` on the sample corpus.

## What runs where
- **CI (pure):** everything mockable — schema, parsing, retriever result-mapping, build_retriever
  wiring. No Neo4j, no graphrag, no network.
- **Local live (skip-marked):** PrimeKG-sample ingest+retrieve against the running Neo4j; a real
  GraphRAG index+query on the small PubMed-abstract corpus in `.venv-graphrag` — proves the real path.
- **Scripted one-off (documented):** full PrimeKG ingest + full corpus index (multi-GB / long).

## Out of scope (verbatim from cards.md Card 10b + this)
- Wiring retrievers into the agents/pipeline; the SRQ2 evaluation sweep itself (Cards 11/12); UI.
- UMLS/SNOMED (licensed) — PrimeKG + ICD-10 only; UMLS a possible later top-up.
- Committing PrimeKG full data, copyrighted guidelines, or any patient text.

## Verification matrix (AC → test)
- AC "configs B/C live" → `test_build_retriever_b_with_graph` (B returns the graph retriever),
  `test_build_retriever_c_includes_graph` (hybrid contains graph modality).
- AC "Neo4j entity-relationship retrieval" → `test_neo4j_graph_retriever_maps_results` (mock client) +
  live `test_primekg_ingest_and_retrieve` (skip if no server).
- AC "MS GraphRAG isolated + community retrieval" → `test_graphrag_retriever_parses_output` (mock
  subprocess) + live `test_graphrag_query` (skip if no venv/artifacts).
- AC "PrimeKG schema" → `test_parse_primekg_row`, `test_kg_schema_types`.
- Security: `test_neo4j_client_creds_from_env` (no hardcoded password).

## Risks + rollback
- GraphRAG indexing needs an LLM + time; pointed at Ollama; live test on a tiny corpus only. Full
  index is scripted. Rollback: revert branch.
- PrimeKG full is large; live test uses a committed sample; full ingest scripted.
- Subprocess parsing of `graphrag query` output is brittle to version drift — pin graphrag in
  `requirements-graphrag.txt`; parse the structured (`--response-type`) output; tolerate empties.
- Corpus licensing: PubMed abstracts / open only; no copyrighted guideline text committed.
- Neo4j creds: env-only, `.env` gitignored, `.env.example` documents names.

## Phase plan
- P0 branch + uninstall stray graphrag from `medargue` + create `.venv-graphrag` (script).
  P2 `kg_schema.py`, `neo4j_client.py`. P3 `graph_rag.py` + `retrieval.py` wiring. P5 tests
  (RED→GREEN pure; live skip-marked; run live locally to prove). P7 self-audit + `/security-review`
  (focus: creds, subprocess injection). P8 gate. P9 PR → STOP. Skip P1/P4/P6/P10.

## Commit (one PR: `feature/graphrag`)
`feat(knowledge): GraphRAG (isolated venv) + Neo4j KG (PrimeKG) — SRQ2 configs B/C live` — Neo4jClient
(env creds), PrimeKG schema + ingest, Neo4jGraphRetriever (entity-relationship), GraphRAGRetriever
(subprocess to isolated venv, Ollama-backed), composite config B, B/C wired in build_retriever; setup
+ ingest scripts; pure tests (CI) + live (local). ruff/mypy/bandit/pip-audit green; /security-review.
STOP for merge.
