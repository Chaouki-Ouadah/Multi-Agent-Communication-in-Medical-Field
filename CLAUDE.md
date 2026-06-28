# CLAUDE.md — Standing instructions for this repo

> Multi-Agent Argumentation for Explainable Clinical Decision Support.
> MSc AI/Data Science dissertation — Heriot-Watt University Dubai.
> Student: Chaouki Ouadah · Supervisor: Radu-Casian Mihailescu, Ph.D.

## Standing methodology

Before any task, read [`engineering-methodology.md`](./engineering-methodology.md) and
[`IMPLEMENTATION_CONTEXT.md`](./IMPLEMENTATION_CONTEXT.md). Apply the 11-phase card flow.
Use the kickoff prompt (methodology §1.6) on the first session of every chat.

`IMPLEMENTATION_CONTEXT.md` is the **single source of truth** for what to build and in what order
(see its §6 Build Order — strict TDD, RED→GREEN→REFACTOR per step).

## Project basics

| | |
|---|---|
| Language | Python `>=3.10,<3.13` |
| Environment | conda env `medargue` (Python 3.12) — `conda activate medargue` |
| Package manager | `pip` (`requirements*.txt`) |
| Base branch | `main` |
| Branch model | fresh `feature/` \| `fix/` \| `chore/` \| `refactor/` \| `test/` branch per card, cut from `main` |
| PR target | `main` on `Chaouki-Ouadah/Multi-Agent-Communication-in-Medical-Field` |
| Test runner | `pytest` |
| Lint | `ruff check .` (autofix: `ruff check --fix .` / format: `ruff format .`) |
| Type-check | `mypy` |
| Security | `bandit -r src`, `pip-audit`, `detect-secrets` |
| E2E | `pytest -m e2e` (Playwright against Streamlit) |

## Local CI gate (all must pass before push — methodology §7)

```bash
ruff check .          # lint, 0 errors
ruff format --check .  # format
mypy                  # type-check
pytest -m "not slow and not llm"   # unit
```

## Guardrails (IMPLEMENTATION_CONTEXT.md §10)

- Research prototype only — **not clinical advice**. Label every model output as such.
- **No real patient data** in the surrogate track. MIMIC/UCI only after PhysioNet+CITI credentialing.
- Pin versions. Keep the `BaseDatasetLoader` interface stable so the data source can be swapped.
- Commit often, small PRs, tests green before merge. Never `--no-verify`.

## Communication

Default to caveman full mode in chat (token-efficient). Code, commits, PR bodies, and security
warnings: write normal prose.
