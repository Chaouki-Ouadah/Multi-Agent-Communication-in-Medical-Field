# Knowledge Base — medargue

> Curated institutional knowledge. Every entry MUST cite provenance with `[Source: ...]`.
> Keep under 200 lines — curate stale entries before adding new ones.
> (Format enforced by .claude/hooks/completeness-gate.sh)

## Environment & tooling
- **Python env**: project runs in conda env `medargue` (3.12), not base 3.13 — torch, scispacy en_core_sci_lg, graphrag 3.0.2 do not reliably build on 3.13. [Source: empirical — workspace setup 2026-06-29]
- **jq PATH (Windows/git-bash)**: git-bash does NOT inherit winget's PATH; place `jq.exe` in `/c/Users/chawk/bin` (already on bash PATH) so hooks can find it. [Source: empirical — jq not found in hooks until copied, 2026-06-29]
- **Hook line endings**: Claude Code hooks run via git-bash and require LF line endings; CRLF causes carriage-return parse failures. Normalize hooks to LF after copying from Windows sources. [Source: empirical — file showed CRLF; hooks failed until normalized, 2026-06-29]
- **Local CI gate**: `ruff check .`, `ruff format --check .`, `mypy`, `pytest -m "not slow and not llm"` must pass before push. [Source: CLAUDE.md, engineering-methodology.md §7]

## Project architecture
- **Loader contract**: all data flows through `BaseDatasetLoader` (load, feature_domains, targets, variable_dictionary). Keep it stable so SurrogateLoader can be swapped for UCI/MIMIC with no pipeline changes. [Source: IMPLEMENTATION_CONTEXT.md §2]
- **Surrogate shape**: ~111 features (78 binary, 22 ordinal, 11 continuous), 12 complication targets, 10–15% missingness, seed=42 deterministic, mimics UCI #579. [Source: IMPLEMENTATION_CONTEXT.md §2]
- **Agent partition (independent variable)**: History&Risk (~37 feats), Diagnostic (~46), Treatment&Progression (~28), Supervisor (all 111). Agents disagree because they hold different data, not different tone. [Source: IMPLEMENTATION_CONTEXT.md §3]
- **Argumentation**: Dung's Abstract Argumentation Framework via NetworkX; preferred extensions resolve the debate; Walton schemes structure arguments. [Source: IMPLEMENTATION_CONTEXT.md §4, Appendix B]
- **Pipeline order**: row → vignette → partition → NER → KG retrieval → 3-agent debate (LangGraph) → AAF resolution → explanation → output. [Source: IMPLEMENTATION_CONTEXT.md §3]
- **Eval dimensions**: multi-label F1 (macro/micro), per-complication recall, explainability, process transparency, calibration (ECE), robustness, information fusion. [Source: IMPLEMENTATION_CONTEXT.md §8]

## Guardrails
- **Not clinical advice**: label every model output as a research-prototype, non-clinical result. [Source: IMPLEMENTATION_CONTEXT.md §10]
- **No real patient data** in the surrogate track; MIMIC/UCI only after PhysioNet + CITI credentialing. [Source: IMPLEMENTATION_CONTEXT.md §10]
- **Build discipline**: strict TDD (RED → GREEN → REFACTOR), one feature branch per §6 step, small PRs to main, tests green before merge. [Source: IMPLEMENTATION_CONTEXT.md §6, engineering-methodology.md §3]
