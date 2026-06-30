# medargue — Card Backlog (Track 1: Surrogate Data First, MIMIC multimodal)

> The build, decomposed into **cards**. Each card = one `feature/` branch → one PR to `main`,
> executed with `/mp-card` (plan-first, TDD RED→GREEN→REFACTOR, gates green, PR). One card at a time.
> Source of truth: `IMPLEMENTATION_CONTEXT.md` (derived from `Dessertation Doc/Dissertation_Final_v6.pdf`).

## Status

| # | Card | Type | Depends on | Status |
|---|------|------|-----------|--------|
| 0 | Workspace + tooling + CI/CD + Claude config | chore | — | ✅ done |
| R0 | Realign spec to dissertation v6 (MIMIC multimodal) | chore | 0 | ✅ this PR |
| 1 | Multimodal loader + surrogate datasets | feature | R0 | ⬜ ready |
| 2 | Modality partitioner + Case object | feature | 1 | ⬜ |
| 3 | Model clients (Meditron / LLaVA-Med / BioViL) | feature | R0 | ⬜ |
| 4 | Vision Agent (BioViL + CLIP Image RAG + LLaVA-Med) | feature | 2,3 | ⬜ |
| 5 | Report Agent (sections + scispaCy NER + Meditron) | feature | 2,3 | ⬜ |
| 6 | Clinical Agent (EHR serialisation + Meditron) | feature | 2,3 | ⬜ |
| 7 | LangGraph debate + Supervisor (≤5 rounds) | feature | 4,5,6 | ⬜ |
| 8 | Dung's AAF + preferred-extension resolver | feature | — | ⬜ |
| 9 | Walton 7 schemes + attacks + explanation | feature | 7,8 | ⬜ |
| 10 | GraphRAG + Neo4j KG; SRQ2 configs A/B/C | feature | 4,5,6 | ⬜ |
| 11 | Evaluation metrics (6 dimensions) | feature | 1 | ⬜ |
| 12 | Baselines B1–B5 + ablations A1–A7 | feature | 7,9,11 | ⬜ |
| 13 | Streamlit UI (CXR + modality panels + arg tree) | feature | 9 | ⬜ |
| 14 | Model-selection benchmark harness | feature | 3 | ⬜ |
| 15 | Swap surrogate → real MIMIC | feature | 1 + credentialing | ⬜ blocked |

DoD (whole track, dissertation p.55 CP4/CP6): end-to-end run on surrogate data → 3 modality agents
debate → AAF resolves → explanation + arg tree in Streamlit → 6-dim metrics logged in MLflow → tests
green → pushed. Then swap loaders for real MIMIC.

---

## Card 1 — Multimodal loader + surrogate datasets
- **Branch:** `feature/loaders`
- **Goal:** Expose multimodal patient studies through the stable `BaseDatasetLoader` so the pipeline
  is built/tested with zero credentialing risk; swap to MIMIC later with no pipeline change.
- **Scope:** `BaseDatasetLoader` ABC (`cases()`, `labels()`, `modalities()`, `variable_dictionary()`);
  a `Case` dataclass (`subject_id`, `study_id`, `image_path`, `report_text`, `ehr_record`, `labels`);
  CheXpert-14 label parsing (focus 5); surrogate loaders: `ChestXray14Loader` (images+labels),
  `OpenILoader` (report text), `MimicDemoLoader` (EHR). A small bundled fixture sample per source.
- **Files:** `src/data/loaders.py`, `src/data/chestxray14.py`, `src/data/openi.py`,
  `src/data/mimic_demo.py`, `tests/test_loaders.py`.
- **Tests (RED):** each loader yields `Case`s with the expected fields; CheXpert-14 labels parsed
  (incl. uncertain/blank handling); `labels()` == 14; a Case links image+report+EHR by id; loaders
  satisfy the ABC; deterministic ordering with `seed=42`.
- **AC:** [ ] all 3 surrogate loaders implement `BaseDatasetLoader`; [ ] a Case carries all 3
  modalities + labels; [ ] CheXpert-14 parsed with the focus-5 identifiable; [ ] no real/credentialed
  data committed (only open-licensed fixtures).
- **Out of scope:** embeddings, agents, real MIMIC.
- **Open decisions:** CheXpert uncertain-label policy (treat -1 as positive/negative/ignore) — flag.

## Card 2 — Modality partitioner + Case views
- **Branch:** `feature/modality-partition`
- **Goal:** Project a `Case` into per-agent modality views enforcing information asymmetry (OIDP).
- **Scope:** `modality_partitioner.py` — `vision_view(case)` → image only; `report_view` → text only;
  `clinical_view` → EHR only; `supervisor_view` → arguments only (no raw data).
- **Files:** `src/utils/modality_partitioner.py`, `tests/test_modality_partition.py`.
- **Tests (RED):** each view exposes ONLY its modality; vision view has no report/EHR; supervisor view
  exposes no raw modality; views are disjoint over raw data.
- **AC:** [ ] 3 raw-data views pairwise disjoint; [ ] supervisor sees no raw data; [ ] leakage test
  (an agent view never carries another modality) passes.

## Card 3 — Model clients (Meditron / LLaVA-Med / BioViL)
- **Branch:** `feature/model-clients`
- **Goal:** One mockable client per model so business logic never calls a model directly.
- **Scope:** `llm_client.py` (Ollama Meditron-8B, config from env), `vlm_client.py` (LLaVA-Med 7B VQA),
  `embeddings.py` (BioViL image embedding). Each injectable + mockable; a protocol/interface each.
- **Files:** `src/agents/llm_client.py`, `src/agents/vlm_client.py`, `src/agents/embeddings.py`,
  `tests/test_clients.py`.
- **Tests (RED):** unit tests pass with mocks (no live model); one `@pytest.mark.llm` smoke per client
  (Meditron via Ollama returns text; LLaVA-Med/BioViL marked `llm`+`slow`, skippable if weights absent).
- **AC:** [ ] all clients mockable; [ ] env-driven model selection; [ ] live Meditron smoke returns
  non-empty; [ ] no model call in non-`llm` tests.
- **Open decisions:** LLaVA-Med + BioViL serving (HF Transformers 4-bit vs other) — confirm in-card.

## Card 4 — Vision Agent
- **Branch:** `feature/agent-vision`
- **Goal:** CXR image → textual pathology findings as scheme-labelled arguments, image-only.
- **Scope:** BioViL embed → CLIP Image RAG (ChromaDB top-k similar cases + their labels) → LLaVA-Med
  VQA → structured findings; emits arguments (claim + evidence + Walton scheme). Mock VLM/embed in unit.
- **Files:** `src/agents/vision.py`, `src/knowledge/retriever.py` (CLIP Image RAG part),
  `tests/test_agent_vision.py`.
- **Tests (RED):** with mocks, agent returns structured args from image view only; cites retrieved
  precedent; never reads report/EHR.
- **AC:** [ ] image-only (asserted); [ ] returns scheme-labelled args; [ ] uses CLIP Image RAG context.

## Card 5 — Report Agent
- **Branch:** `feature/agent-report`
- **Scope:** section extraction (Findings/Impression) + scispaCy NER → Meditron → scheme-labelled
  findings, report-only. **Files:** `src/agents/report.py`, `src/utils/report_sections.py`,
  `tests/test_agent_report.py`.
- **AC:** [ ] report-only; [ ] NER entities feed the argument; [ ] scheme-labelled args.

## Card 6 — Clinical Agent
- **Branch:** `feature/agent-clinical`
- **Scope:** EHR serialisation (labs/vitals + reference ranges + ↑/↓/✓ flags) → Meditron →
  scheme-labelled findings, EHR-only. **Files:** `src/agents/clinical.py`,
  `src/utils/ehr_serializer.py`, `tests/test_agent_clinical.py`.
- **AC:** [ ] EHR-only; [ ] reference-range flags correct; [ ] scheme-labelled args.

## Card 7 — LangGraph debate + Supervisor
- **Branch:** `feature/debate-graph`
- **Goal:** Orchestrate the multi-round debate; Supervisor mediates over text args only; ≤5 rounds.
- **Scope:** `state.py` (`DebateState`: arguments, attacks, round, converged, extension); `graph.py`
  (nodes/edges, round control, convergence = no new attacks OR round==5); `supervisor.py` (conflict
  detection over arguments). Mock agents.
- **Files:** `src/pipeline/state.py`, `src/pipeline/graph.py`, `src/agents/supervisor.py`,
  `tests/test_pipeline.py`.
- **Tests (RED):** runs to termination with mock agents; round cap = 5 enforced; converges when no new
  attacks; supervisor sees only arguments (no raw data).
- **AC:** [ ] ≤5 rounds; [ ] convergence rule; [ ] state accumulates args+attacks; [ ] supervisor
  raw-data-blind.
- **Open decisions:** convergence definition + agent ordering — flag.

## Card 8 — Dung's AAF + resolver
- **Branch:** `feature/aaf`
- **Scope:** `framework.py` (AAF ⟨A,R⟩, NetworkX) + `resolver.py` (conflict-free, admissible,
  preferred extensions). **Files:** `src/argumentation/framework.py`,
  `src/argumentation/resolver.py`, `tests/test_argumentation.py`.
- **Tests (RED):** preferred extensions on toy graphs — no attacks, single attack, 2-cycle, 3-cycle,
  defended set, empty.
- **AC:** [ ] empty attacks → all args; [ ] 2-cycle → two extensions; [ ] defended arg included;
  [ ] returns maximal admissible sets.

## Card 9 — Walton schemes + attacks + explanation
- **Branch:** `feature/explanation`
- **Scope:** `schemes.py` (the 7 schemes + critical questions); attack-formation from agent args;
  `explanation.py` (extension + arg tree → narrative + disclaimer). **Files:**
  `src/argumentation/schemes.py`, `src/argumentation/explanation.py`, `tests/test_explanation.py`.
- **Tests (RED):** 7 schemes enumerable; attack formed on contradictory claims; narrative lists winning
  args + cites evidence + always ends with the not-clinical-advice disclaimer.
- **AC:** [ ] 7 schemes; [ ] attacks formed correctly; [ ] disclaimer on every explanation.
- **Open decisions:** attack threshold (negation vs probabilistic) — flag.

## Card 10 — GraphRAG + Neo4j KG (SRQ2)
- **Branch:** `feature/graphrag`
- **Scope:** `graph_rag.py` (Microsoft GraphRAG local+global), `neo4j_client.py`, `kg_schema.py`
  (UMLS/SNOMED-CT/ICD-10/PrimeKG + guideline indexing); retriever interface supports configs
  A (vector), B (graph), C (hybrid). Neo4j optional (skip-marked if no server).
- **Files:** `src/knowledge/graph_rag.py`, `src/knowledge/neo4j_client.py`,
  `src/knowledge/kg_schema.py`, `tests/test_rag.py`.
- **AC:** [ ] all retrievers share one interface; [ ] A/B/C selectable; [ ] hybrid combines image+text+graph.
- **Open decisions:** GraphRAG corpus (external-only vs +MIMIC text leakage) — flag.

## Card 11 — Evaluation metrics (6 dimensions)
- **Branch:** `feature/eval`
- **Scope:** `metrics.py` — multi-label F1 (macro/micro over 14), per-pathology AUROC, ECE,
  Cohen's κ (cross-modal), explainability + process-transparency measures. **Files:**
  `src/evaluation/metrics.py`, `tests/test_eval.py`.
- **Tests (RED):** F1/AUROC/ECE/κ against hand-computed fixtures; edge cases.
- **AC:** [ ] macro/micro F1 correct; [ ] AUROC per label; [ ] ECE + κ within tolerance.

## Card 12 — Baselines + ablations
- **Branch:** `feature/baselines`
- **Scope:** `baselines.py` (B1 GPT-4o zero-shot, B2 single+vector-RAG, B3 multi-agent-no-AAF, B4
  existing, B5 full); `analysis.py` (A1–A7 toggles + paired Wilcoxon). **Files:**
  `src/evaluation/baselines.py`, `src/evaluation/analysis.py`, `tests/test_baselines.py`.
- **AC:** [ ] B1–B5 runnable via config toggles; [ ] A1–A7 each disable one component; [ ] Wilcoxon harness.

## Card 13 — Streamlit UI (E2E)
- **Branch:** `feature/ui`
- **Scope:** `ui/app.py` + `ui/components/*` per `docs/design/ui-spec.md` — CXR image panel, 3 modality
  argument panels (Vision/Report/Clinical), Graphviz arg-tree (accepted/rejected), recommendation +
  calibrated confidence, sticky disclaimer; ≥1 live Playwright scenario.
- **AC:** [ ] launches; [ ] CXR + 3 panels + arg-tree + recommendation render; [ ] disclaimer present;
  [ ] ≥1 non-skipped Playwright scenario; [ ] a11y checklist (ui-spec §7).

## Card 14 — Model-selection benchmark harness
- **Branch:** `feature/benchmark`
- **Scope:** compare Meditron-8B vs Llama-3.1-8B (text), BioViL vs MedCLIP (embed), LLaVA-Med vs
  LLaVA-1.5 (VLM) on multi-label F1 + latency + VRAM over 100–200 surrogate studies; log to MLflow.
- **AC:** [ ] harness runs each candidate; [ ] reports F1/latency/VRAM; [ ] MLflow-logged.

## Card 15 — Swap surrogate → real MIMIC (blocked: credentialing)
- **Branch:** `feature/mimic`
- **Scope:** `MimicLoader` (CXR-JPG + IV-Note + IV) implementing `BaseDatasetLoader`; no pipeline change.
- **AC:** [ ] passes the same loader interface tests; [ ] end-to-end on real MIMIC with zero changes
  outside `src/data/`.
