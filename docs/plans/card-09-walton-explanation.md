# Plan — Card 9: Walton 7 schemes + attack-formation + explanation

## Context
The agents already tag each `Argument` with a free-text scheme label ("Argument from Expert
Opinion", "…Sign", "…Analogy", "…Evidence to Hypothesis"); Card 8 gave us the AAF + preferred
extensions. Card 9 closes the explainability loop (SRQ1): formalise Walton's **7 clinical schemes**
(+ their critical questions), add a **deterministic symbolic attack-former** over agent claims, and a
**narrative explanation** generator that turns the winning extension + arg tree into clinician-readable
prose ending in the not-clinical-advice disclaimer. Per IMPLEMENTATION_CONTEXT §4 (pp.41-43). Branch
`feature/explanation`.

## Decisions
- **Attack threshold = negation/lexical** (user-chosen). Two claims from *different* agents contradict
  when they share a significant clinical content token AND exactly one carries a negation/uncertainty
  cue ("no", "without", "absent", "unlikely", "negative for", "rule out", "no evidence of"). Mutual →
  emit both directions (a↔b) so the AAF forms a 2-cycle → resolver yields the two competing extensions
  (matches the dissertation Pneumonia-vs-normal-WBC example). Deterministic, no model calls.
- **7 Walton schemes as an `Enum`** with canonical `.label` matching the strings agents already emit;
  `scheme_from_label()` maps label→enum. Agents are NOT changed (no scope creep; non-breaking).
- **`CRITICAL_QUESTIONS`** dict: a short list of Walton critical questions per scheme (explainability).
- **Explanation is pure**: `generate_explanation(aaf, extension, attacks=None) -> str` — resolves the
  extension's claim-ids back to `Argument`s via the AAF, lists each winner (agent · scheme · claim) and
  cites its evidence, summarises conflicts resolved, and ALWAYS ends with the disclaimer. Handles the
  empty extension.

## State map
- `schemes.py`, `explanation.py` — docstring-only stubs. `tests/test_explanation.py` — does not exist.
- `framework.py` (Card 8) — `Argument`, `Attack`, `AAF`. `resolver.py` — `preferred_extensions`.
- Agent scheme strings in use: Expert Opinion, Sign, Analogy, Evidence to Hypothesis.
- `DebateState.extension`/`explanation` exist but stay empty (pipeline wiring is out of scope).

## Approach (files)
- **`src/argumentation/schemes.py`**:
  - `WaltonScheme(Enum)` — EXPERT_OPINION, EVIDENCE_TO_HYPOTHESIS, ANALOGY, CAUSE_TO_EFFECT,
    CONSEQUENCES, ESTABLISHED_RULE, SIGN; each `.label` = "Argument from …".
  - `scheme_from_label(label) -> WaltonScheme | None`.
  - `CRITICAL_QUESTIONS: dict[WaltonScheme, list[str]]`.
  - `form_attacks(arguments) -> list[Attack]` — negation/lexical contradiction former (cross-agent,
    bidirectional on mutual conflict). Documented heuristic + cue/stopword sets.
- **`src/argumentation/explanation.py`**:
  - `DISCLAIMER` constant (matches the agents' wording).
  - `generate_explanation(aaf, extension, attacks=None) -> str`.
- **`tests/test_explanation.py`** (RED→GREEN, pure): 7 schemes enumerable + each has label & critical
  questions; `scheme_from_label` round-trips the 4 in-use labels; `form_attacks` — dissertation
  contradiction example forms a 2-cycle, agreement forms none, same-agent forms none; end-to-end
  args→form_attacks→AAF→preferred_extensions→`generate_explanation`; narrative lists winners + cites
  evidence + **ends with disclaimer**; empty-extension narrative still carries the disclaimer.

Reuse: `Argument`/`Attack`/`AAF` (framework.py), `preferred_extensions` (resolver.py).

## Out of scope (verbatim from cards.md Card 9 + this)
- GraphRAG + Neo4j KG / SRQ2 configs (Card 10). UI arg-tree rendering (Card 13).
- Wiring `form_attacks`/`generate_explanation` into `pipeline/graph.py` or populating
  `DebateState.extension`/`explanation` (later card). Changing the agents' scheme emission.
- Calibrated confidence scoring (separate concern; explanation states winners, not a probability).

## Verification matrix (AC → test)
- AC "7 schemes" → `test_seven_schemes_enumerable` (`len(WaltonScheme)==7`, labels unique,
  critical questions non-empty) + `test_scheme_from_label`.
- AC "attacks formed correctly" → `test_form_attacks_contradiction` (2-cycle), `test_no_attack_on_agreement`,
  `test_no_self_attack_same_agent`.
- AC "disclaimer on every explanation" → `test_explanation_ends_with_disclaimer`,
  `test_empty_extension_has_disclaimer`.
- Integration → `test_end_to_end_extension_to_narrative` (winners listed + evidence cited).

## Risks + rollback
- Lexical heuristic = false negatives on paraphrase / false positives on shared-but-unrelated terms.
  Accepted for the prototype (deterministic + explainable); the LLM Supervisor (Card 7) catches
  semantic conflicts the lexical former misses. Documented. Rollback: revert branch.
- Negation scoping is claim-level (not span-level) — simple; adequate for short clinical claims.

## Phase plan
- P0 branch `feature/explanation`. P2 `schemes.py` + `explanation.py`. P5 tests (RED→GREEN, all
  pure — no LLM). P7 self-audit + `/security-review`. P8 gate. P9 PR → STOP. Skip P1/P3/P4/P6/P10.

## Commit (one PR: `feature/explanation`)
`feat(argumentation): Walton 7 schemes + lexical attack-former + explanation narrative` — WaltonScheme
enum + critical questions, negation/lexical `form_attacks`, `generate_explanation` (winners + evidence
+ disclaimer); pure tests incl. end-to-end extension→narrative. ruff/mypy/bandit/pip-audit green;
/security-review run. STOP for merge.
