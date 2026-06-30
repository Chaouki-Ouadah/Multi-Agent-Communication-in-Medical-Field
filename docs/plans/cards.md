# medargue — Card Backlog (Track 1: Surrogate Data First)

> The build, decomposed into **cards**. Each card = one `feature/` branch → one PR to `main`,
> executed with `/mp-card` (plan-first, TDD RED→GREEN→REFACTOR, gates green, PR).
> Source of truth for *what* to build: `IMPLEMENTATION_CONTEXT.md`. Order: `docs/plans/build-order.md`.
>
> **How to run a card:** paste its block (or say "work on Card N") → `/mp-card` enters plan mode →
> writes a plan → you approve → it implements + tests + PRs.

## Status

| # | Card | Type | Depends on | Status |
|---|------|------|-----------|--------|
| 0 | Workspace + tooling + CI/CD + Claude config | chore | — | ✅ done |
| 1 | Surrogate generator + loader | feature | 0 | ⬜ ready |
| 2 | Feature partitioner | feature | 1 | ⬜ |
| 3 | Vignette generator (templates) | feature | 1 | ⬜ |
| 4 | LLM client + History&Risk agent | feature | 2,3 | ⬜ |
| 5 | 3 agents in LangGraph (mock convergence) | feature | 4 | ⬜ |
| 6 | Dung's AAF + resolver | feature | — | ⬜ |
| 7 | Walton schemes + explanation generator | feature | 5,6 | ⬜ |
| 8 | Evaluation metrics | feature | 1 | ⬜ |
| 9 | Streamlit UI + arg-tree (E2E) | feature | 6,7 | ⬜ |
| 10 | ChromaDB RAG retriever | feature | 3 | ⬜ |
| 11 | GraphRAG / Neo4j (optional) | feature | 10 | ⬜ |
| 12 | Real-data loader swap | feature | 1 + credentialing | ⬜ blocked |

Definition of Done (whole track, Appendix D): end-to-end surrogate run → 3 agents debate → AAF
resolves → explanation + arg tree in Streamlit → metrics logged in MLflow → all tests green → pushed.

---

## Card 1 — Surrogate generator + loader
- **Type / branch:** feature / `feature/surrogate`
- **Goal:** Produce synthetic patients structurally matching UCI #579 (MI Complications) and expose
  them through the stable `BaseDatasetLoader` interface, so the whole pipeline can be built/tested
  with zero data-access risk and the source can later be swapped.
- **Scope (must):**
  - `BaseDatasetLoader` ABC: `load() -> pd.DataFrame`, `feature_domains() -> dict[str,list[str]]`,
    `targets() -> list[str]`, `variable_dictionary() -> dict[str,dict]`.
  - `SurrogatePatientGenerator`: N patients (default 1700), ~78 binary / 22 ordinal / 11 continuous
    features, 12 complication targets, 10–15% per-column missingness, injected clinical correlations
    (e.g. anterior MI ↑ AV-block; prior HF ↑ heart-failure target), `seed=42` deterministic.
    Start from Appendix A skeleton.
  - `SurrogateLoader(BaseDatasetLoader)` returning generated frame + domains + targets + dictionary.
- **Files:** `src/data/loaders.py`, `src/data/surrogate.py`, `tests/test_surrogate.py`.
- **Tests (RED first):** shape/column-type counts; missingness within 10–15% band; targets present;
  injected correlation rate > base rate; same seed → identical frames; loader satisfies the ABC.
- **Acceptance criteria:**
  - [ ] `SurrogateLoader().load()` returns a DataFrame with the documented feature + target columns.
  - [ ] Missingness per column is 10–15% and seed-reproducible.
  - [ ] At least two injected correlations are statistically present (rate vs base, fixed seed).
  - [ ] `feature_domains()` keys cover history_risk / diagnostic / treatment; values are real columns.
  - [ ] All four ABC methods implemented; calling them raises nothing.
- **Out of scope:** real datasets; partitioning logic (Card 2).
- **Estimate:** ~half day.

## Card 2 — Feature partitioner
- **Type / branch:** feature / `feature/partition`
- **Goal:** Split the ~111 features into the 3 agent partitions (history_risk / diagnostic /
  treatment); supervisor sees all. Partitioning is the independent variable.
- **Scope:** pure function mapping loader `feature_domains()` → 3 disjoint column masks; helper to
  project a patient row to a given agent's visible features.
- **Files:** `src/utils/feature_partitioner.py`, `tests/test_partition.py`.
- **Tests (RED):** masks pairwise disjoint; union covers all non-target features; supervisor mask =
  all; projecting a row hides out-of-partition columns.
- **Acceptance criteria:**
  - [ ] 3 masks are pairwise disjoint (no feature in two partitions).
  - [ ] Union of the 3 masks == all non-target feature columns.
  - [ ] Supervisor view == all features.
  - [ ] Row projection for an agent excludes every out-of-partition column.
- **Out of scope:** agents consuming the partition (Card 4).
- **Estimate:** ~2–3 h.

## Card 3 — Vignette generator (templates)
- **Type / branch:** feature / `feature/vignette`
- **Goal:** Turn a tabular patient row into clinical English (templates now; optional LLM glue later).
- **Scope:** deterministic template decode using the variable dictionary; handles missing values
  gracefully; per-partition vignette option (for agent prompts).
- **Files:** `src/utils/vignette_generator.py`, `tests/test_vignette.py`.
- **Tests (RED):** given a fixed row, output contains expected feature phrases; missing features
  omitted/flagged; deterministic (no LLM in this card).
- **Acceptance criteria:**
  - [ ] Output text includes the human-readable phrase for each present feature.
  - [ ] Missing features handled without error (omitted or explicitly "unknown").
  - [ ] Same row → identical text (deterministic).
- **Out of scope:** LLM-polished prose (later, behind a flag).
- **Estimate:** ~half day.

## Card 4 — LLM client + History&Risk agent
- **Type / branch:** feature / `feature/agent-history`
- **Goal:** A mockable Ollama-backed LLM client, plus the first agent returning structured arguments
  from ONLY its partition.
- **Scope:** `llm_client.py` wrapping `ChatOllama` (model/base-url/temp from env, see
  `docs/llm-setup.md`), injectable + mockable; `history_risk.py` producing structured args
  (claim + cited feature values + Walton-scheme tag) from its partition only.
- **Files:** `src/agents/llm_client.py`, `src/agents/history_risk.py`, `tests/test_agent_history.py`.
- **Tests (RED):** with a **mock** LLM, agent returns the structured arg object; cites only visible
  features; never references out-of-partition features. One `@pytest.mark.llm` smoke test hits live
  meditron.
- **Acceptance criteria:**
  - [ ] Unit tests pass with a mocked client (no live model).
  - [ ] Agent output is a typed structured object (claim, cited features, scheme).
  - [ ] Agent never cites a feature outside its partition (asserted).
  - [ ] `@pytest.mark.llm` test returns a non-empty response from local Ollama.
- **Out of scope:** the other agents + graph (Card 5).
- **Estimate:** ~1 day.

## Card 5 — 3 agents in LangGraph (mock convergence)
- **Type / branch:** feature / `feature/debate-graph`
- **Goal:** Wire History&Risk + Diagnostic + Treatment into a LangGraph debate with deterministic
  mock convergence; `DebateState` accumulates arguments + attacks.
- **Scope:** `state.py` (`DebateState` TypedDict, Appendix C); `graph.py` (nodes + edges + round
  control + convergence stub); Diagnostic + Treatment agents (mirror Card 4).
- **Files:** `src/pipeline/state.py`, `src/pipeline/graph.py`, `src/agents/diagnostic.py`,
  `src/agents/treatment.py`, `tests/test_pipeline.py` (graph portion).
- **Tests (RED):** graph runs to termination with mock LLMs; state accumulates args/attacks;
  terminates deterministically within max rounds; each agent constrained to its partition.
- **Acceptance criteria:**
  - [ ] `graph.run(case)` terminates deterministically with mocked agents.
  - [ ] `DebateState.arguments` / `.attacks` populated by all 3 agents.
  - [ ] Round cap respected; `converged` flag set by the stub rule.
- **Out of scope:** real convergence semantics, AAF resolution (Card 6), supervisor logic depth.
- **Estimate:** ~1–1.5 days.

## Card 6 — Dung's AAF + resolver
- **Type / branch:** feature / `feature/aaf`
- **Goal:** Symbolic resolution — build the abstract argumentation framework and compute preferred
  extensions over (arguments, attacks).
- **Scope:** `framework.py` (AAF graph, NetworkX); `resolver.py` (conflict-free, admissible,
  preferred extensions — Appendix B). Independent of agents (pure graph).
- **Files:** `src/argumentation/framework.py`, `src/argumentation/resolver.py`,
  `tests/test_argumentation.py`.
- **Tests (RED):** preferred extensions on toy graphs with known answers — no attacks, single
  attack, 2-cycle, 3-cycle, defended set; empty framework edge case.
- **Acceptance criteria:**
  - [ ] Empty attacks → the single extension is all arguments.
  - [ ] 2-cycle (a↔b) → two preferred extensions {a},{b}.
  - [ ] Defended argument is included; unattacked-by-defenders excluded.
  - [ ] Resolver returns maximal admissible sets (no extension is a subset of another).
- **Out of scope:** mapping LLM args→AAF nodes (Card 7), explanation prose.
- **Estimate:** ~1 day.

## Card 7 — Walton schemes + explanation generator
- **Type / branch:** feature / `feature/explanation`
- **Goal:** Tag arguments with Walton schemes + critical questions, and turn the resolved extension
  + arg tree into a clinical narrative (with the mandatory disclaimer).
- **Scope:** `schemes.py` (scheme catalogue + critical questions); `explanation.py` (extension +
  graph → narrative citing feature values; appends "not clinical advice").
- **Files:** `src/argumentation/schemes.py`, `src/argumentation/explanation.py`,
  `tests/test_explanation.py`.
- **Tests (RED):** narrative contains the winning claims; cites feature values; always ends with the
  disclaimer; deterministic given a fixed extension (mock any LLM polish).
- **Acceptance criteria:**
  - [ ] Explanation lists the accepted (winning) arguments.
  - [ ] Each cited claim references concrete feature values.
  - [ ] Output always includes the research-prototype / not-clinical-advice disclaimer.
- **Out of scope:** UI rendering (Card 9).
- **Estimate:** ~1 day.

## Card 8 — Evaluation metrics
- **Type / branch:** feature / `feature/eval`
- **Goal:** Multi-dimensional evaluation on surrogate predictions.
- **Scope:** `metrics.py` — multi-label F1 (macro/micro), per-complication recall, calibration (ECE);
  scaffolds for `baselines.py` (B1–B5) + `analysis.py`. MLflow logging hook.
- **Files:** `src/evaluation/metrics.py`, `src/evaluation/baselines.py`, `src/evaluation/analysis.py`,
  `tests/test_eval.py`.
- **Tests (RED):** F1/recall against hand-computed small cases; ECE on known-calibrated scores; edge
  cases (all-zero preds, perfect preds).
- **Acceptance criteria:**
  - [ ] Macro/micro F1 match hand-computed values on a 3-sample fixture.
  - [ ] Per-complication recall correct for a fixture.
  - [ ] ECE within tolerance on a known-calibration fixture.
- **Out of scope:** running full experiments; the baselines' internals.
- **Estimate:** ~1 day.

## Card 9 — Streamlit UI + arg-tree (E2E)
- **Type / branch:** feature / `feature/ui`
- **Goal:** Streamlit dashboard per `docs/design/ui-spec.md` — case selection, 3 agent panels,
  Graphviz arg-tree, recommendation + confidence, explanation, risk table, sticky disclaimer.
- **Scope:** `ui/app.py` + pure render helpers in `ui/components/`; theme via `.streamlit/config.toml`;
  ≥1 live Playwright E2E scenario.
- **Files:** `ui/app.py`, `ui/components/*.py`, `tests/` (e2e-marked + unit for helpers).
- **Tests (RED):** unit-test pure render helpers; Playwright: app loads, run a case, recommendation +
  arg-tree + confidence + disclaimer visible (page.route stubs for live model).
- **Acceptance criteria:**
  - [ ] App launches with `streamlit run ui/app.py`.
  - [ ] All three agent panels + arg-tree + recommendation + risk table render.
  - [ ] Disclaimer is present and non-dismissible on the main screen.
  - [ ] ≥1 non-skipped Playwright scenario passes.
  - [ ] Accessibility checklist (ui-spec §7) satisfied.
- **Out of scope:** RAG context display (Card 10+).
- **Estimate:** ~1.5 days.

## Card 10 — ChromaDB RAG retriever
- **Type / branch:** feature / `feature/rag`
- **Goal:** Per-agent knowledge retrieval from a seeded ChromaDB vector store.
- **Scope:** `retriever.py` — embed + top-k retrieval over guideline chunks; per-agent context split;
  BGE embeddings (configurable).
- **Files:** `src/knowledge/retriever.py`, `tests/test_rag.py`, seed fixture.
- **Tests (RED):** retriever returns top-k relevant chunks for a query from a seeded store;
  per-agent context differs by partition; deterministic given fixed embeddings.
- **Acceptance criteria:**
  - [ ] Seeding + querying a small store returns the expected top-k chunk(s).
  - [ ] Per-agent retrieval scopes context to that agent's domain.
- **Out of scope:** GraphRAG/Neo4j (Card 11).
- **Estimate:** ~1 day.

## Card 11 — GraphRAG / Neo4j (optional, SRQ2)
- **Type / branch:** feature / `feature/graphrag`
- **Goal:** Knowledge-graph RAG (Microsoft GraphRAG + Neo4j) behind the same retriever interface, to
  compare Vector vs GraphRAG vs Hybrid (SRQ2).
- **Scope:** `graph_rag.py`, `neo4j_client.py` implementing the retriever interface; Neo4j optional
  (skip-marked tests if no server).
- **Acceptance criteria:**
  - [ ] GraphRAG retriever satisfies the same interface as the ChromaDB retriever.
  - [ ] A Vector-vs-Graph comparison harness can call both.
- **Out of scope:** production graph tuning.
- **Estimate:** ~2 days (research-heavy).

## Card 12 — Real-data loader swap (blocked on credentialing)
- **Type / branch:** feature / `feature/real-data`
- **Goal:** Implement `UCILoader` / `MIMICLoader` against `BaseDatasetLoader`; run the pipeline on
  real data with NO pipeline changes.
- **Blocked by:** PhysioNet + CITI credentialing.
- **Acceptance criteria:**
  - [ ] New loader passes the same interface tests as `SurrogateLoader`.
  - [ ] End-to-end run on real data with zero changes outside `src/data/`.
- **Out of scope:** everything else (pipeline is frozen by this point).
- **Estimate:** ~1 day once data access lands.
