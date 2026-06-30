# Plan — Card 11: Evaluation metrics (6 dimensions)

## Context
The dissertation's evaluation framework (§4.6, Table 4.5) spans six dimensions; §4.6.2 formalises five
core metrics. Card 11 implements the computable metrics as **pure, deterministic functions** so the
SRQ1/SRQ2 sweeps (Cards 12+) can score any system condition. No models, no infra. Branch
`feature/eval`. Hand-implemented with numpy (no sklearn dependency) — tests check against
hand-computed fixtures, matching the card's RED requirement.

## Decisions
- **Hand-implement** F1/AUROC/ECE/κ (numpy only) — avoids a heavy sklearn pin and makes the
  fixtures exact. AUROC via the rank (Mann-Whitney U) identity with tie-aware average ranks.
- **Scope by dimension** (compute what is pure + formalised; flag what needs experiment runs):
  - **D1 Clinical:** `f1_macro`, `f1_micro` (eqs 4.1/4.2 over the 14 CheXpert labels), `per_pathology_auroc`
    (eq 4.3), `cooccurrence_accuracy`.
  - **D2 Explainability:** `explanation_completeness` (winners + evidence + disclaimer present),
    `argumentation_coverage` (fraction of winning claims surfaced in the narrative), `rouge_l` (pure LCS
    F-measure). BLEU + LLM-judged faithfulness deferred (needs refs/judge — note).
  - **D3 Process transparency:** `debate_depth`, `attack_rate`, `convergence_quality`,
    `argument_traceability` — computed from a `DebateState` (reuse Card-7 types).
  - **D4 Trust:** `expected_calibration_error` (eq 4.4, M-bin).
  - **D5 Robustness:** experiment-driven (missing-evidence dropout / paraphrase) → **Card 12** (note).
  - **D6 Cross-modal:** `cohen_kappa` (eq 4.5), `cross_modal_discovery_rate`, `unique_evidence_contribution`.
- Undefined cases return `nan` (e.g. AUROC for a single-class label) rather than raising; documented.

## State map
- `src/evaluation/metrics.py` — docstring-only stub → implement. `analysis.py`/`baselines.py` stay
  stubs (Card 12). `tests/test_eval.py` — does not exist (create).
- Reuse `DebateState`/`Argument`/`Attack` (pipeline/state.py, argumentation/framework.py) for D3.
- numpy present (1.26.4). No new deps.

## Approach (files)
- **`src/evaluation/metrics.py`** — the functions above; type-annotated; numpy arrays for the
  label/score metrics; `DebateState`/`Argument` inputs for D3/D2.
- **`tests/test_eval.py`** (RED→GREEN, pure): hand-computed fixtures for f1_macro/micro, AUROC
  (incl. ties + single-class→nan), ECE (perfect-calibration→0, known-gap value), Cohen's κ (perfect→1,
  chance→0), rouge_l (identical→1, disjoint→0), plus D3 transparency metrics on a small DebateState
  and explainability coverage/completeness. Edge cases: empty, all-zero, single-class.

## Out of scope (verbatim from cards.md Card 11 + this)
- Baselines B1–B5 + ablations A1–A7 (Card 12) — incl. robustness perturbation runs + Wilcoxon tests.
- BLEU + LLM-judged faithfulness (need reference corpora / a judge model).
- Wiring metrics into a runnable evaluation harness over real cases (Card 12); UI (Card 13).

## Verification matrix (AC → test)
- AC "macro/micro F1 correct" → `test_f1_macro_hand`, `test_f1_micro_hand` (vs hand math).
- AC "AUROC per label" → `test_auroc_per_label`, `test_auroc_ties`, `test_auroc_single_class_nan`.
- AC "ECE + κ within tolerance" → `test_ece_perfect_zero`, `test_ece_known_gap`, `test_kappa_perfect`,
  `test_kappa_chance`.
- Extra dims → `test_rouge_l`, `test_process_transparency_from_state`, `test_argumentation_coverage`,
  `test_cooccurrence_accuracy`, `test_cross_modal_discovery`.

## Risks + rollback
- AUROC tie handling is the classic gotcha → use average ranks; test a tie fixture. Rollback: revert.
- Float tolerances → assert with `pytest.approx` / explicit `abs(... ) < 1e-9`.

## Phase plan
- P0 branch `feature/eval`. P2 `metrics.py`. P5 tests (RED→GREEN, pure). P7 self-audit +
  `/security-review` (trivial — pure math, no I/O). P8 gate. P9 PR → STOP. Skip P1/P3/P4/P6/P10.

## Commit (one PR: `feature/eval`)
`feat(evaluation): six-dimension metrics (F1, AUROC, ECE, Cohen's κ, transparency, explainability)` —
hand-implemented numpy metrics + DebateState-based process/explainability measures; pure fixtures.
ruff/mypy/bandit/pip-audit green; /security-review run. STOP for merge.
