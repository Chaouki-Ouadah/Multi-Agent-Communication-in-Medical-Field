# Implementation Plan — medargue Track 1 (Surrogate Data First)

> Derived from `IMPLEMENTATION_CONTEXT.md` §6 build order. Each step is RED → GREEN → REFACTOR.
> One feature branch per step (`feature/<short>`), PR to `main`, tests green before merge.
> This plan is the contract; re-read it per session instead of re-deriving from the spec.

## Context
Build a multi-agent argumentation clinical-decision-support pipeline end-to-end on synthetic
surrogate data that structurally mimics UCI #579 (MI Complications). Prove the whole pipeline,
then swap the data loader for real data once MIMIC/UCI access is granted. No real patient data in
this track. Research prototype — every model output labeled "not clinical advice".

## State map (current vs spec)
- Repo skeleton, env, CI/CD: DONE (foundation only, all `src/` are stubs).
- `BaseDatasetLoader` interface: specified in §2; not yet coded.
- Everything in §6 steps 2–12: not started (this plan).

## Approach
Strict TDD per step. Keep modules small and pure where possible (extract logic out of UI/agents
into testable functions). Stub LLM and RAG behind interfaces so early steps run with zero external
services. Determinism via `seed=42` everywhere randomness appears.

## Out of scope (Track 1)
- Real datasets (MIMIC/UCI) — deferred to §6.12 after credentialing.
- GraphRAG/Neo4j may be stubbed with ChromaDB-only until §6.11.
- GPT-4o baseline calls — only after local Ollama path works.

---

## Step plan (TDD tasks)

### Step 2 — SurrogatePatientGenerator + SurrogateLoader  (`feature/surrogate`)
- RED: `tests/test_surrogate.py`
  - shape: N rows (default 1700), expected column count; binary/ordinal/continuous split.
  - missingness: ~10–15% per column (tolerance band), seed-deterministic.
  - labels: ground-truth target columns present; injected correlations hold statistically
    (e.g. anterior MI ↑ AV-block rate vs base rate).
  - reproducibility: same seed → identical frames.
  - `SurrogateLoader.load()/feature_domains()/targets()/variable_dictionary()` satisfy
    `BaseDatasetLoader` ABC.
- GREEN: implement `src/data/surrogate.py` (generator) + `src/data/loaders.py`
  (`BaseDatasetLoader` ABC + `SurrogateLoader`). Use Appendix A skeleton as starting point.
- REFACTOR: extract correlation rules to a config dict; document domains.
- Commit: `feat(data): surrogate generator + loader (Track 1)`

### Step 3 — FeaturePartitioner  (`feature/partition`)
- RED: `tests/test_partition.py` — 3 masks (history_risk / diagnostic / treatment) are
  pairwise disjoint; union covers all non-target feature columns; supervisor sees all.
- GREEN: `src/utils/feature_partitioner.py`.
- Commit: `feat(utils): feature partitioner (3 disjoint domain masks)`

### Step 4 — Vignette Generator  (`feature/vignette`)
- RED: deterministic template decode — given a row, output contains the expected feature phrases;
  no LLM in this step.
- GREEN: `src/utils/vignette_generator.py` (templates only). LLM glue later behind a flag.
- Commit: `feat(utils): template vignette generator`

### Step 5 — History&Risk agent stub  (`feature/agent-history`)
- RED: agent returns a structured argument object (claim + cited feature values + scheme tag)
  from ONLY its partition; raises/ignores features it cannot see.
- GREEN: `src/agents/history_risk.py` + a thin LLM client interface (mockable).
- Commit: `feat(agents): history&risk agent (structured args)`

### Step 6 — 3 agents in LangGraph  (`feature/debate-graph`)
- RED: graph runs 3 agents with a MOCK convergence; `DebateState` accumulates arguments/attacks;
  terminates deterministically.
- GREEN: `src/pipeline/state.py` (Appendix C) + `src/pipeline/graph.py`.
- Commit: `feat(pipeline): langgraph 3-agent debate (mock convergence)`

### Step 7 — Dung's AAF resolver  (`feature/aaf`)
- RED: `tests/test_argumentation.py` — preferred extensions on toy graphs (known answers):
  empty attacks, single attack, even/odd cycles, defended sets.
- GREEN: `src/argumentation/framework.py` + `src/argumentation/resolver.py`
  (Appendix B preferred-extensions; consider NetworkX).
- Commit: `feat(argumentation): dung AAF + preferred-extension resolver`

### Step 8 — Explanation generator  (`feature/explanation`)
- RED: given an extension + arg tree, output a narrative containing the winning claims +
  the "not clinical advice" label.
- GREEN: `src/argumentation/explanation.py` (+ schemes in `schemes.py`).
- Commit: `feat(argumentation): explanation generator`

### Step 9 — Evaluation metrics  (`feature/eval`)
- RED: multi-label F1 (macro/micro), per-complication recall, calibration (ECE) on synthetic
  predictions with known scores.
- GREEN: `src/evaluation/metrics.py` (+ baselines/analysis scaffolds).
- Commit: `feat(evaluation): multi-label metrics + ECE`

### Step 10 — Streamlit UI  (`feature/ui`)  [E2E with Playwright]
- RED: ≥1 live Playwright scenario (page.route stubs) — loads a case, shows recommendation +
  arg-tree + confidence + disclaimer.
- GREEN: `ui/app.py` (Graphviz arg-tree). Extract render logic to pure helpers for unit tests.
- Commit: `feat(ui): streamlit arg-tree viz` + `test(ui): e2e scenario`

### Step 11 — RAG  (`feature/rag`)
- RED: retriever returns top-k chunks for a query from a seeded ChromaDB; per-agent context split.
- GREEN: `src/knowledge/retriever.py` (ChromaDB) → later `graph_rag.py`/`neo4j_client.py`.
- Commit: `feat(knowledge): chromadb retriever` (GraphRAG follows)

### Step 12 — Swap loader → real data  (post-credentialing)
- Implement `UCILoader`/`MIMICLoader` against the same ABC; no pipeline changes.

---

## Verification matrix (AC → proof)
- Each step's RED tests above are its acceptance proof.
- Definition of Done (Appendix D): end-to-end surrogate run → 3 agents debate → AAF resolves →
  explanation + arg tree in Streamlit → metrics logged in MLflow → all tests green → pushed.

## Risks + rollback
- Risk: heavy LLM/RAG deps slow tests → keep them behind mockable interfaces; mark `llm`/`slow`.
- Risk: surrogate correlations too weak/strong for stable label tests → assert on rate bands, seed-fixed.
- Rollback: each step is one branch/PR; revert the commit to undo.

## Phase mapping (methodology 11-phase)
- Phases 1 (schema) mostly N/A (no DB; surrogate is in-memory/CSV).
- Phases 2–3 = agent/UI code; Phase 5 = unit tests (RED first); Phase 6 = E2E (step 10);
  Phase 7 local CI gate every step; Phase 8 commit/PR per step.
