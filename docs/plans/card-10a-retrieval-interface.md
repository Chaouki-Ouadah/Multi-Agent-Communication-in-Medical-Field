# Plan — Card 10a: Retrieval interface + Vector RAG (config A) + hybrid fusion

## Context
SRQ2 compares three retrieval backends with everything else held constant (dissertation Table 4.4):
**A** = Vector RAG (ChromaDB text), **B** = GraphRAG (Microsoft GraphRAG + Neo4j), **C** = Multimodal
Hybrid (text vector + GraphRAG + CLIP Image RAG). Card 10 is **split** (user decision): this card (10a)
delivers the **one unified retriever interface**, **config A** (real ChromaDB text RAG), and the
**hybrid fusion** mechanism (graph-ready) — all CI-green now. The heavy-faithful **config B** (Microsoft
GraphRAG isolated venv + real Neo4j Docker + UMLS/SNOMED/ICD-10/PrimeKG) becomes **Card 10b** once the
infra/licenses are stood up. Branch `feature/retrieval-interface`.

**Corpus = external-only** (faithful per §4.5.2/4.5.4): public ontologies + guidelines/textbook/PubMed.
No MIMIC patient text in the retrieval corpus → no train/test leakage into SRQ2.

## Decisions
- One **`Retriever` Protocol**: `retrieve(query: RetrievalQuery, k: int) -> list[RetrievedItem]`.
  `RetrievalQuery` carries optional `text` and `image_path` so a single interface spans text-only
  (A/B) and image (CLIP) retrievers; each retriever uses the parts it understands.
- **`RetrievalConfig` enum** A=VECTOR, B=GRAPH, C=HYBRID — `build_retriever(config, ...)` factory.
  B raises a clear `NotImplementedError("GraphRAG — Card 10b")` for now (config is enumerable/selectable;
  the live backend lands in 10b). A and C build fully.
- **`TextVectorRetriever`** (config A): real ChromaDB cosine collection; text embedder **injected**
  (Protocol) exactly like `ClipImageRetriever` (deterministic fake in tests; real sentence/BioViL-text
  embedder in production) → no surprise model downloads in CI.
- **`HybridRetriever`** (config C): fans a query out to N injected sub-retrievers (text + image now,
  graph slot ready), merges by normalised score, dedupes, returns top-k. Graph-readiness proven with a
  mock graph retriever in tests; real GraphRAG slots in at 10b with zero interface change.
- **`ClipImageRetrieverAdapter`**: wraps the existing Card-4 `ClipImageRetriever` (image → `Precedent`)
  into the unified `Retriever` (→ `RetrievedItem`), so hybrid can include image evidence.

## State map
- `knowledge/retriever.py` (Card 4) — `ClipImageRetriever`, `Precedent` (reuse, unchanged).
- `knowledge/graph_rag.py`, `neo4j_client.py`, `kg_schema.py` — stubs; stay stubs (point to Card 10b).
- `tests/test_rag.py` — does not exist (create).
- `chromadb` already a dependency; **no new deps** → no numpy clash, CI-safe. `graphrag` stays OUT of
  requirements (isolated env, Card 10b).

## Approach (files)
- **`src/knowledge/retrieval.py`** (NEW): `RetrievalConfig`, `RetrievalQuery`, `RetrievedItem`,
  `Retriever` Protocol, `TextVectorRetriever`, `ClipImageRetrieverAdapter`, `HybridRetriever`,
  `build_retriever`.
- **`tests/test_rag.py`** (NEW, pure): interface conformance; config enum has A/B/C; `build_retriever`
  A→TextVectorRetriever, C→HybridRetriever, B→NotImplementedError; TextVectorRetriever indexes +
  retrieves (fake embedder, deterministic); hybrid combines **text + image + (mock) graph**, dedupes,
  respects k; empty-query / empty-index edge cases.
- **`src/knowledge/graph_rag.py`** (edit docstring only): note config B lands in Card 10b + the isolated
  venv approach. No logic.
- **`docs/plans/cards.md`** (edit): split Card 10 → 10a (this) + 10b (GraphRAG/Neo4j, infra-gated).

## Out of scope (verbatim from cards.md Card 10 minus the split + this)
- Microsoft GraphRAG pipeline (local+global), `neo4j_client.py`, `kg_schema.py` ontology indexing,
  real Neo4j server, UMLS/SNOMED/ICD-10/PrimeKG ingestion → **Card 10b** (heavy faithful, infra-gated).
- Wiring retrievers into the agents/pipeline; the SRQ2 evaluation sweep itself (Card 11/12); UI.

## Verification matrix (AC → test)
- AC "all retrievers share one interface" → `test_retrievers_share_interface` (Text/Clip-adapter/Hybrid
  all satisfy `Retriever`, same `retrieve` signature).
- AC "A/B/C selectable" → `test_config_enum_has_abc` + `test_build_retriever_a_c` +
  `test_build_retriever_b_not_yet` (B raises NotImplementedError naming Card 10b).
- AC "hybrid combines image+text+graph" → `test_hybrid_combines_modalities` (mock text+image+graph
  sub-retrievers; result spans all three sources) + `test_hybrid_dedupes_and_topk`.
- Config A real → `test_text_vector_retriever_indexes_and_retrieves` (fake embedder, nearest-first).

## Risks + rollback
- Splitting the card risks "A/B/C selectable" looking incomplete (B not live). Mitigated: enum +
  factory make B *selectable*; the live backend is explicitly Card 10b; hybrid is graph-ready and
  tested with a mock graph retriever. Documented in cards.md + the PR body. Rollback: revert branch.
- Score-normalisation across heterogeneous retrievers (cosine vs graph relevance) is heuristic —
  min-max per sub-retriever before merge; documented; revisited when real GraphRAG scores exist (10b).

## Phase plan
- P0 branch `feature/retrieval-interface`. P2 `retrieval.py`. P5 tests (RED→GREEN, pure — no LLM/server).
  P7 self-audit + `/security-review`. P8 gate. P9 PR → STOP. Skip P1/P3/P4/P6/P10.

## Commit (one PR: `feature/retrieval-interface`)
`feat(knowledge): unified retriever interface + Vector RAG (config A) + hybrid fusion (SRQ2 A/C)` —
RetrievalConfig/Query/Item, Retriever Protocol, TextVectorRetriever (ChromaDB), ClipImageRetriever
adapter, graph-ready HybridRetriever, build_retriever; pure tests; Card 10 split (10b = GraphRAG/Neo4j).
ruff/mypy/bandit/pip-audit green; /security-review run. STOP for merge.
