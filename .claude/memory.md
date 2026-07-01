# Project Memory — medargue

> Working memory for cross-session continuity. Read on session start / after compaction.
> Durable facts live in the auto-memory store; this file is the active-work scratch.

## Now
Merged: Cards 1–10 (#8 loaders … #16 Walton, **#17 retrieval interface/Vector RAG**, **#18
GraphRAG+Neo4j**). Symbolic layer COMPLETE (AAF/resolver/schemes/explanation). **Retrieval COMPLETE
(SRQ2 A/B/C live):** `knowledge/retrieval.py` unified `Retriever` + `RetrievalConfig` A/B/C + real
ChromaDB `TextVectorRetriever` (A) + graph-ready `HybridRetriever` (C) + `build_retriever`. Card 10b:
`neo4j_client.py` (env creds) + `kg_schema.py` (PrimeKG ingest) + `graph_rag.py`
(`Neo4jGraphRetriever` Cypher entity-rel + `GraphRAGRetriever` subprocess→`.venv-graphrag`). Both live
paths PROVEN: Neo4j Docker `neo4j-medargue` (creds NEO4J_* in .env, dev pw medargue-dev-pw) + real MS
GraphRAG index/query (Ollama llama3.1:8b + nomic-embed-text, workspace `.graphrag`, both gitignored).
**Card 10 SPLIT done: 10a=#17, 10b=#18.**
ISOLATION RULE: graphrag lives ONLY in `.venv-graphrag` (numpy 2.5), invoked by subprocess; NEVER in
medargue (numpy 1.26.4) or requirements.txt. requirements-graphrag.txt = venv-only.
Still pure-module pattern: AAF/resolver/explanation + retrievers NOT yet wired into pipeline/graph.py
(DebateState.extension/explanation empty) — a future wiring card.
**Card 11 DONE (#19):** `evaluation/metrics.py` — 6-dim metrics (numpy-only, no sklearn): f1_macro/micro,
per_pathology_auroc (rank/tie-aware), expected_calibration_error, cohen_kappa (Vision-vs-Report),
rouge_l, explanation_completeness, argumentation_coverage, cooccurrence_accuracy,
cross_modal_discovery_rate, unique_evidence_contribution, + DebateState process-transparency
(debate_depth/attack_rate/convergence_quality/argument_traceability). `METRIC_REGISTRY` for Card 12.
DEFERRED to Card 12: D5 robustness (dropout/paraphrase runs) + BLEU + LLM-faithfulness.
**Card 12 DONE (#20):** `evaluation/baselines.py` (SystemConfig + BASELINES B1-B5 + ABLATIONS A1-A7 +
`run_condition` composing debate/AAF/explanation/retrieval per config — NOT via graph.py, eval-layer
only) + `analysis.py` (aggregate_results / wilcoxon_compare / ablation_delta). B1=Ollama qwen2.5:14b
(GPT-4o deferred — configurable llm_model); B4=external→NotImplementedError. Retrieval is harness-level
(per-agent injection = later). `_extract_labels`→FOCUS_5 negation-aware. Live B5 on Ollama passes.
NOTE: pipeline/graph.py STILL not wired with AAF/explanation/retrieval (DebateState.extension/
explanation empty) — eval layer composes them instead; Card 13 UI will likely call run_condition(B5).
Next: **Card 13 — Streamlit UI (CXR + 3 modality panels + debate/arg-tree + recommendation +
confidence + disclaimer)** + Playwright E2E. THE demo card (supervisor walkthrough). Make it
demo-oriented: bundled sample case (incl. a CXR image) for one-click end-to-end. Follow
docs/design/ui-spec.md. Disclaimer on every output panel.
Decisions locked: per-modality Cases; CheXpert policy configurable; OIDP frozen views; clients real
(no mocks); LLaVA-Med 4-bit via Ollama `rohithbojja/llava-med-v1.5`; BioViL via hi-ml-multimodal;
CLIP Image RAG = BioViL→ChromaDB (per-instance collection); shared `Argument` in
argumentation/framework.py; NIH slice via kagglehub (data/chestxray14, gitignored). env: numpy 2 +
CUDA torch cu128. PR discipline: raise PR + STOP, user merges (see [[pr-merge-discipline]]).

## Known follow-up
- **numpy split RESOLVED (Card 5):** env coheres on numpy 1.26.4 (scispaCy 0.6.2 / spaCy 3.7.5 /
  scipy 1.17.1 / transformers 5.x / torch cu128 all import; all 5 live tests pass). scispaCy model
  pins spaCy 3.7.5 — don't force 3.8.
- **graphrag (Card 10) deferred conflict:** wants spacy~=3.8 + numpy~=2.1 — unsatisfiable with the
  scispaCy set. Resolve when GraphRAG lands (likely isolate or drop the strict pin).

## Open threads
- Open implementation decisions flagged in cards.md (attack threshold, convergence def, confidence
  source, GraphRAG corpus) — resolve per card with the user.

## Recent decisions
- [2026-06-30] Dissertation_Final_v6.pdf is authoritative → realigned everything to MIMIC multimodal
  (Vision/Report/Clinical modality agents; CheXpert-14; CLIP image-RAG + GraphRAG; Dung's AAF + Walton 7).
- [2026-06-29] conda env `medargue` @ Python 3.12; main + feature branches; one card = one PR.
- [2026-06-29] Full Claudify skills library gitignored (local-only).

## Blockers
- (none) — real MIMIC blocked on PhysioNet+CITI+ethics (Track 2, parallel).

## Session handoff (2026-07-01 — pre-reboot checkpoint)
- **Cards 1–9 merged** (PRs #8–#16). Symbolic layer complete (AAF/resolver/schemes/explanation).
- **Card 10 SPLIT** (user): **10a** = retriever interface + Vector RAG (config A, ChromaDB) + hybrid
  fusion (graph-ready) — plan WRITTEN + APPROVED-pending at `docs/plans/card-10a-retrieval-interface.md`;
  branch will be `feature/retrieval-interface`; NO Docker needed; NOT started yet. **10b** = MS GraphRAG
  (isolated venv) + real Neo4j (Docker) + UMLS/SNOMED/ICD-10/PrimeKG — later, infra-gated.
- Decisions: KG corpus **external-only** (faithful, no leakage); **heavy-faithful path always**
  ([[heavy-faithful-path]]).
- **DOCKER FIX IN PROGRESS:** Docker Desktop failed ("virtualization not detected"). Root cause =
  Virtual Machine Platform feature was OFF + WSL2 had no distro. Ran elevated DISM enable of
  `Microsoft-Windows-Subsystem-Linux` + `VirtualMachinePlatform` (both succeeded). **PC reboot pending**
  to finish. HypervisorPresent=True (firmware VT-x already on). After reboot: start Docker Desktop →
  verify `docker run --rm hello-world` → stage Neo4j container for 10b.
- **RESUME AFTER REBOOT:** either build Card 10a (say "go 10a") or finish Docker verify first.
- Earlier realignment note (historical): after realign merged, Card 1 ran. Done.
