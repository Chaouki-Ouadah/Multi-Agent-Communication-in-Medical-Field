# Plan — Card 12: Baselines B1–B5 + ablations A1–A7

## Context
The dissertation isolates each component's contribution via five baselines (Table 4.6, §4.6.3) and
seven ablations (Table 4.7, §4.6.4), scored with the Card-11 metrics and compared with a paired
Wilcoxon signed-rank test (§4.6.5). Card 12 makes every condition **runnable via config toggles** and
provides the comparison harness. Branch `feature/baselines`. Heavy-faithful path.

## Decisions
- **Compose conditions in the evaluation layer**, not by editing `pipeline/graph.py`. Each condition is
  a `SystemConfig` → a configured `run_condition(case, config, components)` that reuses the existing
  pure pieces (`run_debate`, `form_attacks`, `AAF`, `preferred_extensions`, `generate_explanation`,
  the retrievers). Keeps the debate graph focused; no wiring debt incurred here.
- **B1 uses Ollama, not GPT-4o** (user decision) — `qwen2.5:14b` as the strong single-LLM stand-in
  (configurable via `SystemConfig.llm_model`; documented deviation, swap to GPT-4o when an API key
  lands). All model access is injected → unit tests use mocks (no live calls).
- **B4 (existing SOTA system)** is an external system that cannot be run here. It is a registered
  config slot that raises a clear `NotImplementedError` (documented); comparison against B4 is a
  manual literature step. Not a blocker for the AC ("B1–B5 runnable via config toggles" — B4's slot
  exists + is selectable).
- **Wilcoxon** via `scipy.stats.wilcoxon` (scipy present); zero-difference / too-few-samples handled.

## Condition → config map (faithful to Tables 4.6/4.7)
- B1 single LLM zero-shot: `single_agent`, no partitioning, no retrieval, no AAF.
- B2 single LLM + vector RAG: `single_agent`, retrieval=`vector` (config A), no AAF.
- B3 multi-agent, no argumentation: 3 agents, partitioning, debate, `use_argumentation=False`.
- B4 existing system: `external=True` → NotImplementedError (manual).
- B5 full: 3 agents, partitioning, retrieval=`hybrid` (config C), `use_argumentation=True`, explanation.
- A1 no image RAG: B5 with retrieval=`vector` (text-only). A2 no symbolic layer: B5 with
  `use_argumentation=False`. A3 no partitioning: B5 with `partitioning=False` (agents see all). A4
  single agent: `single_agent` + retrieval=`hybrid` + AAF. A5 general LLM: B5 with
  `llm_model=llama3.1:8b`. A6 no vision: B5 with agents={report,clinical}. A7 no clinical: B5 with
  agents={vision,report}.

## State map
- `evaluation/baselines.py`, `analysis.py` — stubs → implement. `metrics.py` (Card 11) reused.
- `run_debate`/`build_debate_graph` (Card 7), `form_attacks` (Card 9), `AAF`/`preferred_extensions`
  (Card 8), `generate_explanation` (Card 9), retrievers (Cards 10a/b), `FOCUS_5` (chexpert.py) — reuse.
- scipy 1.17.1 present. No new deps.

## Approach (files)
- **`src/evaluation/baselines.py`**:
  - `SystemConfig` dataclass (agents:set, partitioning:bool, retrieval:None|"vector"|"hybrid",
    use_argumentation:bool, single_agent:bool, llm_model:str, external:bool).
  - `BASELINES: dict[str, SystemConfig]` (B1–B5) + `ABLATIONS: dict[str, SystemConfig]` (A1–A7).
  - `ConditionOutput` (predicted_labels:set[str], explanation:str, winning_args:list, debate_state,
    confidence).
  - `run_condition(case, config, *, agents, supervisor, llm, retriever=None) -> ConditionOutput` —
    dispatch: single-agent path (one LLM call, optional retrieval) vs multi-agent debate; if
    `use_argumentation` → form_attacks→AAF→preferred_extensions→generate_explanation, else aggregate
    claims. `_extract_labels(text/args)` maps to `FOCUS_5` by keyword.
- **`src/evaluation/analysis.py`**:
  - `aggregate_results(condition -> list[float]) -> {mean,std,n}`.
  - `wilcoxon_compare(scores_a, scores_b) -> {statistic,pvalue}` (paired; guards equal/short input).
  - `ablation_delta(full_scores, ablated_scores) -> float` (mean drop = component contribution).
- **`tests/test_baselines.py`** (RED→GREEN, pure, mocks): config presets toggle the right components
  (B1 no agents/AAF; B3 agents on, AAF off; B5 all on; each A* disables exactly one vs B5);
  `run_condition` dispatch (mock agents/LLM record calls → B1 calls LLM once + no debate; B5 runs
  debate + resolver + explanation; B4 raises); `_extract_labels` finds FOCUS_5; Wilcoxon on fixtures
  (identical→p≈1/handled, clear difference→small p); `ablation_delta`. Live (`llm`+`slow`): one real
  B5 run on a case → produces labels + disclaimer-ended explanation.

## Out of scope (verbatim from cards.md Card 12 + this)
- The actual large-scale experimental run / results tables (a run script, not this card's logic);
  real GPT-4o B1 + real external B4 system; UI (Card 13); real MIMIC (Card 15).
- Modifying `pipeline/graph.py` (conditions compose in the eval layer).

## Verification matrix (AC → test)
- AC "B1–B5 runnable via config toggles" → `test_baseline_presets`, `test_run_condition_b1_single`,
  `test_run_condition_b5_full`, `test_b4_external_raises`.
- AC "A1–A7 each disable one component" → `test_ablations_disable_one_vs_b5` (diff B5 by exactly one
  field per A*).
- AC "Wilcoxon harness" → `test_wilcoxon_identical`, `test_wilcoxon_difference`, `test_aggregate_results`.

## Risks + rollback
- Label extraction from free text is heuristic (keyword vs FOCUS_5) — documented; deterministic +
  tested. Rollback: revert branch.
- B1 model swap (Ollama vs GPT-4o) is a flagged deviation — config-driven, reversible.
- Live B5 is slow (3 models + rounds) → `llm`+`slow`; pure tests are the CI gate.

## Phase plan
- P0 branch `feature/baselines`. P2 `baselines.py` + `analysis.py`. P5 tests (RED→GREEN pure; live).
  P7 self-audit + `/security-review`. P8 gate. P9 PR → STOP. Skip P1/P4/P6/P10.

## Commit (one PR: `feature/baselines`)
`feat(evaluation): baselines B1–B5 + ablations A1–A7 + Wilcoxon harness (config-toggled conditions)` —
SystemConfig presets, run_condition composing the existing pipeline pieces, analysis (aggregate +
paired Wilcoxon + ablation delta); pure tests (CI) + live B5. B1=Ollama (GPT-4o deferred), B4=external
slot. ruff/mypy/bandit/pip-audit green; /security-review run. STOP for merge.
