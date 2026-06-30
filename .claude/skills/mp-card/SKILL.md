---
name: mp-card
description: |
  Execute one medargue (Multi-Agent Argumentation Clinical Decision Support) card
  end-to-end using the 11-phase methodology. Triggers when the user pastes a card
  spec (Goal/Description + Scope + Files + Tests + Acceptance criteria), says
  "next card" / "let's work on this card" / "work on this", or invokes /mp-card.
  Read CLAUDE.md + .claude/memory.md + .claude/knowledge-base.md + the build plan
  (docs/plans/cards.md) before acting. PRs target main. Strict TDD (RED first).
  Project-scoped to c:/Projects/Dissertation - Copy.
metadata:
  scope: personal
  audience: Chaouki only — MSc dissertation, not team use
  project: medargue (Chaouki-Ouadah/Multi-Agent-Communication-in-Medical-Field)
  pr_base: main
  adapted_from: cylas-card (Laravel/Pest) → medargue (Python/pytest/LangGraph)
---

# mp-card

Execute one medargue "card" end-to-end. A card is shaped like:
**Goal/Description · Scope (must) · Files to create · code snippets · Verification ·
Out of scope · Acceptance tests (pytest) · Acceptance criteria**.

Rigid about process (plan-first, TDD RED→GREEN→REFACTOR, gates-before-push, PR→main),
flexible about implementation detail. Follow phases in order; skip a phase only when
the card genuinely has nothing for it.

---

## STACK (what this project is)

- **Language:** Python `>=3.10,<3.13`. Runs in conda env `medargue` (3.12) — `conda activate medargue`.
- **Orchestration:** LangGraph 1.0.9 (debate state machine).
- **Argumentation:** NetworkX (custom Dung's AAF + Walton schemes).
- **KG-RAG:** ChromaDB (Track 1) → Microsoft GraphRAG + Neo4j (later).
- **NER:** scispaCy `en_core_sci_lg`.
- **LLM (local, free):** Ollama — primary `meditron` (clinical) or `llama3.1:8b`; stronger `qwen2.5:14b`.
  Baseline GPT-4o (API) for comparison only. Base URL `http://localhost:11434`.
- **UI:** Streamlit + Graphviz (arg-tree viz). Design spec: `docs/design/ui-spec.md`.
- **Tests:** pytest (markers: `slow`, `e2e`, `llm`). E2E: Playwright vs Streamlit.
- **Tracking:** MLflow. **Data:** surrogate (Track 1) → UCI/MIMIC (after credentialing).

---

## LOCAL ENVIRONMENT (this machine — Windows)

- **conda env:** `conda activate medargue` (Python 3.12). Run tools via env, e.g.
  `conda run -n medargue pytest`.
- **Ollama:** installed + running on `http://localhost:11434`. `ollama list` to see models.
  Pull more with `ollama pull <model>`.
- **jq** (hooks dependency): lives at `/c/Users/chawk/bin/jq.exe` (git-bash PATH).
- **gh CLI:** installed; `gh auth login --web` once if `gh pr create` is needed (push works via
  Git Credential Manager).
- **Git:** base branch `main`; remote `origin` = the project repo.

---

## BEFORE ANYTHING — load context + hard rules

Read every card, before planning:
1. `CLAUDE.md` — standing instructions.
2. `.claude/memory.md` — current state.
3. `.claude/knowledge-base.md` — learned hard rules ([Source:]-cited).
4. `docs/plans/cards.md` + `docs/plans/build-order.md` — the card backlog + build order.
5. `IMPLEMENTATION_CONTEXT.md` — single source of truth for what to build.

### medargue hard rules (non-negotiable)
- **One card = one branch = one PR.** Do exactly ONE card at a time. Never batch multiple cards
  into a branch/PR, never split one card across PRs. Fresh `feature/<card>` from `main` → single PR
  to `main` → branch deleted after merge. Finish (merge) the current card before starting the next.
- **Research prototype, NOT clinical advice.** Every model-facing output (explanation,
  recommendation, UI panel) carries a "not clinical advice" label. [Source: IMPLEMENTATION_CONTEXT §10]
- **No real patient data** in the surrogate track. MIMIC/UCI only after PhysioNet + CITI. Never
  commit real patient data.
- **`BaseDatasetLoader` interface is stable.** Swap data sources (Surrogate→UCI→MIMIC) by
  implementing the same ABC — never change the pipeline to fit a loader.
- **Determinism:** every randomness path takes `seed=42`. Tests must be reproducible.
- **Information partitioning is the independent variable** — agents disagree because they hold
  different feature partitions, NOT because of tone/attitude prompts.
- **TDD RED first.** Write the failing test before implementation. RED → GREEN → REFACTOR.
- **All local gates green before push.** Never `--no-verify`. Small PRs to `main`.
- **Pin versions** (requirements*.txt). Keep modules small + pure where logic is testable.

---

## PLAN-FIRST (mandatory)

Do NOT touch code before an approved plan.

1. **Enter plan mode.**
2. **Re-grep every path / symbol / line the card cites.** Many cards cite net-new
   `src/<module>/...` files — confirm which exist vs which you create (Grep/Glob).
3. **Read each cited existing file.** Note where reality diverges from the card.
4. **Classify scope:** data/loader · utils · agent · pipeline · argumentation · knowledge/RAG ·
   evaluation · UI. Determines which phases run.
5. **Honor the card's "Out of scope" verbatim.**
6. **Reuse audit:** for each "Files to create", grep `src/` for an existing helper that already
   does it. Reuse the `BaseDatasetLoader`, partitioner, prompt templates, LLM client wrapper.
7. **AskUserQuestion** for genuine ambiguity (not free-text in plan mode).
8. **Write the plan** (use `superpowers:writing-plans`) to `docs/plans/<card-kebab>.md`:
   Context · State map (code now vs card claims) · Approach · Files to create/modify (full
   paths) · Out-of-scope (verbatim) · Verification matrix (AC# → test/check) · Risks + rollback ·
   Phase plan · Commit-message draft.
9. **ExitPlanMode** only after user approval.

### Plain-language brief (after approval, before code)
Post a 6–12 sentence chat-only brief for a junior/non-technical reader: **Problem** (what's
missing/why it matters) · **Fix** (high-level approach, one line on any trade-off). Skip only on
truly trivial cards.

---

## PHASES

### Phase 0 — Pre-flight (git + env)
```bash
git status -sb
git checkout main
git fetch origin
git pull origin main --ff-only          # FF only, never plain pull
git checkout -b feature/<kebab-card-title> origin/main
```
- `conda activate medargue`. If `requirements*.txt` changed in the pull: `pip install -r requirements-dev.txt`.
- Branch prefix: `feature/` | `fix/` | `chore/` | `refactor/` | `test/` (match the card type).
- If the card needs an LLM: confirm Ollama is up (`ollama list`) and the model is pulled.

### Phase 1 — Data / schema (skip if none)
- No SQL DB in Track 1. "Schema" here = the surrogate data contract + `BaseDatasetLoader`.
- Extending feature domains / targets / variable dictionary → update the loader + the surrogate
  generator together; keep `feature_domains()`/`targets()` consistent with the data.
- **Enum/domain coverage:** if you add a complication target or feature domain, grep every map
  that references it (partition masks, metric label lists, UI legends) and update all.

### Phase 2 — Core logic modules (skip if none)
- Pure, testable functions under `src/{data,utils,argumentation,evaluation,knowledge}/`.
- Extract logic OUT of agents/UI into libs so it can be unit-tested directly.
- Type-annotate public functions (mypy gate). Keep modules small.

### Phase 3 — Agents / pipeline (skip if none)
- Agents in `src/agents/<name>.py` see ONLY their feature partition; the supervisor sees all.
- LLM access goes through ONE mockable client wrapper (Ollama by default). Never call the LLM
  directly in business logic — inject it so tests run with a mock (no live model).
- LangGraph state in `src/pipeline/state.py` (`DebateState` TypedDict), graph wiring in
  `src/pipeline/graph.py`. Mark live-LLM tests with `@pytest.mark.llm`.
- Argumentation: build the AAF (`framework.py`), resolve via preferred extensions (`resolver.py`).

### Phase 4 — UI (skip if no UI)
- Streamlit in `ui/app.py`; Graphviz arg-tree. **Follow `docs/design/ui-spec.md`** (style tokens,
  colors, fonts, accessibility). Extract render logic to pure helpers for unit tests.
- **Every output panel shows the "research prototype — not clinical advice" disclaimer.**

### Phase 5 — Tests (TDD — RED first)
- pytest under `tests/`; mirror the card's acceptance tests verbatim, then make them green.
- Cover EVERY acceptance-criteria line. Test success AND failure AND edge cases (empty, missing
  features, all-missing, cross-partition leakage, degenerate AAF graphs).
- Use `seed=42` fixtures for determinism. Mock the LLM client (no live calls in unit tests).
- Markers: `slow` (long), `llm` (needs Ollama), `e2e` (Playwright). Default gate excludes these.

### Phase 6 — E2E (only if UI / flow)
- Playwright vs Streamlit, `tests/` marked `e2e`. ≥1 live (non-skipped) scenario: app loads,
  a case runs, recommendation + arg-tree + confidence + disclaimer visible. Use `page.route()`
  stubs for anything needing a live model.

### Phase 7 — Security & correctness self-audit (MANDATORY, before gates)
Green gates ≠ safe/correct code. Walk every new/changed module adversarially:
- **No real patient data** anywhere in code, tests, fixtures, or committed files.
- **No secrets in code** — API keys/tokens only in `.env` (gitignored). Reference by env var name.
- **Partition integrity:** an agent must never receive features outside its partition (test it).
- **Determinism:** no un-seeded randomness; no wall-clock dependence in logic that tests assert on.
- **Disclaimer present** on every recommendation/explanation output path.
- **Input bounds:** validate vignette/agent inputs; handle missing/NaN features explicitly.
- **MANDATORY: run the `/security-review` skill** on the branch diff; triage findings (fix real
  ones; note consciously-accepted ones in the PR body). Clean review is part of "done".

### Phase 8 — Local CI gate (ALL green before push) [mirror the CI jobs]
```bash
conda run -n medargue ruff check .              # ESLint-analog (Lint job)
conda run -n medargue ruff format --check .     # Pint/Prettier-analog (Format job)
conda run -n medargue mypy                       # PHPStan/TypeScript-analog (Types job)
conda run -n medargue pytest -m "not slow and not llm and not e2e"   # Pest-analog (Test job)
conda run -n medargue bandit -c pyproject.toml -r src   # part of Quality Gate
conda run -n medargue pip-audit -r requirements.txt     # part of Quality Gate
conda run -n medargue python -c "import src"            # Build-analog (import smoke)
# E2E only if UI changed:
conda run -n medargue pytest -m e2e
```
Fix anything you introduced before pushing. Pre-existing failures: report, don't absorb.

### Phase 9 — Commits + push + PR (to main)
- **Conventional commits**, grouped by concern (data → core → agents → ui → tests).
  Subject ≤72 chars; body = why + non-obvious what; footer `Card: <title>` +
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
- **Commit via `git commit -F <file>`** (a heredoc/file), never inline `-m` — conventional
  subjects contain parens `feat(data): …` which break unquoted bash.
- Sync with latest main before PR: `git fetch origin`; if behind, `git merge origin/main`,
  re-run Phase 8, then push.
- **Push + PR** (never the GitHub banner — it can default base wrong):
  ```bash
  gh auth status   # if not authed: gh auth login --web
  git push -u origin feature/<kebab>
  gh pr create --base main --head feature/<kebab> \
    --repo Chaouki-Ouadah/Multi-Agent-Communication-in-Medical-Field \
    --title "<conventional subject>" --body "$(cat <<'EOF'
## Card
<card title>
## Summary
- <bullet>
## Tests
- pytest — <N passed>
- ruff / ruff-format / mypy — <status>
- bandit / pip-audit — <status>
- playwright (e2e) — <status or N/A>
## Acceptance criteria
- [x] AC 1
## Out of scope (intentional)
- <thing>
## Rollback
- Revert this commit / branch.
EOF
)"
  ```
- **Post-PR block** + one-line `> **Shipped:** <plain-English>` recap.

### Phase 10 — Manual verify
Run the app: `conda run -n medargue streamlit run ui/app.py`. Walk the card's Verification list.
User clicks through; Claude waits + diagnoses failures.

### Phase 11 — Post-merge cleanup + close loop
```bash
git checkout main && git pull origin main --ff-only
git branch -d feature/<kebab>
git push origin --delete feature/<kebab>
git fetch --prune
```
Update `.claude/memory.md` + the daily note. New pattern/anti-pattern → add to this skill or
nominate in `.claude/knowledge-nominations.md`.

---

## medargue QUALITY-GATE CHECKLIST (run mentally each card)

| Gate | Trigger |
|---|---|
| Pulled main + `pip install` (if requirements changed) before starting | Phase 0 |
| RED test written before implementation | every code card |
| `BaseDatasetLoader` interface unchanged (new sources implement it) | data card |
| `seed=42` determinism; tests reproducible | any randomness |
| Agent sees ONLY its partition (tested) | agent card |
| LLM accessed via mockable client; unit tests don't hit live model | agent/pipeline card |
| Domain/target coverage: every map updated when a feature/target is added | enum/domain change |
| "Not clinical advice" disclaimer on every output path | any explanation/UI |
| No real patient data; no secrets in code | every card |
| Security self-audit + `/security-review` run on diff | every card, before push |
| ruff + ruff-format + mypy + pytest green locally | before push |
| ≥1 live Playwright E2E scenario | UI card, Phase 6 |
| Synced with latest origin/main before PR | Phase 9 |
| PR base = main; branch deleted after merge | Phase 9 / 11 |

---

## COMPOSE WITH (don't duplicate)
- `superpowers:writing-plans` — plan structure.
- `superpowers:test-driven-development` — Phase 5 RED→GREEN→REFACTOR.
- `superpowers:systematic-debugging` — when a test fails for an unknown reason.
- `superpowers:verification-before-completion` — before any "done" claim / Phase 8.
- `superpowers:finishing-a-development-branch` — Phase 9/11 options.
- `caveman-commit` — terse conventional commit messages.
- `ui-ux-pro-max` — Phase 4 UI design decisions (already distilled in docs/design/ui-spec.md).

## NOT IN SCOPE OF THIS SKILL
- Committing real patient data, or any secret/credential.
- Changing the `BaseDatasetLoader` contract to fit a specific dataset.
- Claiming clinical validity — this is a research prototype.
