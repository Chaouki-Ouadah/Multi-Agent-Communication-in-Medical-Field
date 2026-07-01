# Plan — Card 13: Streamlit UI (demo) + Playwright E2E

## Context
The system has no visual surface. Card 13 is **the demo card** — a Streamlit dashboard that shows the
whole pipeline for a case: CXR panel, the 3 modality-agent panels (Vision/Report/Clinical), the
Graphviz argument tree (accepted vs attacked), the resolved recommendation + calibrated confidence, the
per-pathology table, and the always-visible not-clinical-advice disclaimer. Per `docs/design/ui-spec.md`
(the ui-ux-pro-max distillation = the contract). Branch `feature/ui`. Demo-oriented: a bundled sample
case renders the full flow offline/instantly so it is one-click demoable to the supervisor, with a
sidebar toggle to run live on Ollama.

## Decisions
- **Demo vs Live mode.** Default = **demo** (a precomputed, deterministic `ConditionOutput` from a
  bundled sample case) → the UI renders fully with no model/Neo4j, which also lets the **Playwright
  E2E run in CI** (no Ollama). Sidebar toggle → **live** calls `run_condition(B5)` (Card 12) with real
  agents on Ollama. The bundled case has a deliberate cross-modal conflict so the arg-graph shows an
  attack + a preferred extension.
- **Pure render helpers** in `ui/components/render.py` (no Streamlit import) so every panel is
  unit-testable; `ui/app.py` only wires sidebar/state → helpers → Streamlit widgets. Matches ui-spec §8.
- **Status→color is a static literal map** (ui-spec §2/§4): accepted green `#15803D`, attack red
  `#DC2626`, undecided amber `#D97706`. Color never the only signal (accepted also bold + green border).
- **a11y** (ui-spec §7): graph has a text/table fallback (pathology table + explanation), the ⚠ glyph
  is the one allowed emoji, wide responsive layout.
- No real patient data: bundled sample case is synthetic (report + EHR); image optional (the committed
  demo runs without a CXR — Vision panel shows it abstained; live mode can point at a local CXR).

## State map
- `ui/app.py` stub; `ui/components/` does not exist. `.streamlit/config.toml` does not exist.
- Reuse: `run_condition`/`BASELINES` (Card 12), `ConditionOutput`, `Argument`/`Attack`, `CHEXPERT_LABELS`
  + `FOCUS_5`, the agents/supervisor/`OllamaLLMClient` (live mode). `tests/conftest.py` has `seed` +
  `sample_cxr`. streamlit 1.58 / graphviz / playwright / pytest-playwright all installed; `e2e` marker
  + CI e2e job exist.

## Approach (files)
- **`.streamlit/config.toml`** — `[theme]` tokens (primary `#1E40AF`, bg `#F8FAFC`, font) per ui-spec §2/§3.
- **`ui/components/render.py`** (pure): `DISCLAIMER`, `STATUS_COLORS`, `disclaimer_text()`,
  `kpi_cards(output)`, `modality_panel(agent, args, blind_to)`, `build_argument_graph(args, attacks,
  extension_claims) -> graphviz.Digraph`, `pathology_rows(predicted, all14=CHEXPERT_LABELS,
  focus=FOCUS_5)`, `blind_modalities(agent)` (OIDP story).
- **`ui/sample_data.py`**: `demo_case() -> Case`; `demo_output() -> ConditionOutput` (3 agents'
  arguments, one cross-modal attack, a winning extension, explanation ending in the disclaimer,
  predicted FOCUS_5 labels, confidence).
- **`ui/app.py`**: `st.set_page_config(wide)`, sticky disclaimer banner, sidebar (case pick, RAG config
  A/B/C, model, demo/live toggle, Run), main rows per ui-spec §4 (KPI cards · CXR + 3 panels · arg
  graph · explanation · pathology table). Live → `run_condition`; demo → `demo_output()`.
- **`tests/test_ui.py`** (pure, CI): kpi_cards values; argument_graph nodes/edges + accepted=green /
  attack=red; pathology_rows marks focus-5 + predicted; disclaimer present; modality_panel lists
  evidence + blind modalities; demo_output well-formed (has attack + winning args + disclaimer).
- **`tests/test_ui_e2e.py`** (`e2e`, non-skipped): launch `streamlit run ui/app.py` (demo mode) via a
  fixture on a free port; Playwright asserts disclaimer banner, recommendation KPI, 3 modality panel
  headers, the argument graph element, and the pathology table all render.
- **`tests/conftest.py`**: add a `streamlit_app` fixture (spawn demo-mode server, wait for ready, yield
  URL, teardown).

## Out of scope (verbatim from cards.md Card 13 + this)
- Wiring AAF/explanation into `pipeline/graph.py` (the UI calls the Card-12 `run_condition`); the
  large experiment run; real MIMIC (Card 15); the model-selection benchmark (Card 14).
- Authentication, multi-user, deployment/hosting (local `streamlit run` only).

## Verification matrix (AC -> test)
- AC "launches" -> e2e `test_app_loads` (page title + disclaimer banner visible).
- AC "CXR + 3 panels + arg-tree + recommendation render" -> e2e asserts the 3 panel headers +
  graph element + recommendation KPI; unit `test_kpi_cards`, `test_argument_graph`, `test_modality_panel`.
- AC "disclaimer present" -> unit `test_disclaimer` + e2e banner assertion.
- AC ">=1 non-skipped Playwright scenario" -> `test_ui_e2e.py::test_app_loads` (demo mode, runs in CI).
- AC "a11y checklist" -> unit `test_pathology_table_is_graph_fallback` + static color map test; checklist
  ticked in PR body.

## Risks + rollback
- E2E flakiness (server boot timing) -> fixture polls the port until ready with a timeout; demo mode =
  no model latency. Rollback: revert branch.
- Graphviz `dot` binary may be absent on a runner -> `st.graphviz_chart` uses the JS renderer for
  display; the unit test asserts the `graphviz.Digraph` source string (no `dot` needed). Note in PR.
- Streamlit DOM selectors drift -> assert on visible text (disclaimer, panel headers, recommendation),
  not brittle CSS.

## Phase plan
- P0 branch `feature/ui`. P2 `render.py` + `sample_data.py` (pure). P4 `app.py` + `config.toml`.
  P5 unit tests (RED->GREEN). P6 Playwright e2e (1 live scenario, demo mode). P7 self-audit +
  `/security-review`. P8 gate (+ `pytest -m e2e`). P9 PR -> STOP.

## Commit (one PR: `feature/ui`)
`feat(ui): Streamlit explainability dashboard + Playwright E2E (demo + live)` - pure render helpers
(KPI/modality panels/arg-graph/pathology table), bundled sample case + precomputed demo output, app
wiring, theme; unit tests + 1 non-skipped Playwright scenario. Follows docs/design/ui-spec.md +
disclaimer on every panel. ruff/mypy/bandit/pip-audit green; /security-review run. STOP for merge.
