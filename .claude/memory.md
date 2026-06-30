# Project Memory — medargue

> Working memory for cross-session continuity. Read on session start / after compaction.
> Durable facts live in the auto-memory store; this file is the active-work scratch.

## Now
Workspace + Claude Code tooling fully set up, pushed to `main`. Hooks/agents/commands/MCP/skills
+ superpowers plugin all active. Pre-implementation prep done: §6 plan at
`docs/plans/build-order.md`, knowledge-base enriched, Task Board + Scratchpad scaffolded.
**Awaiting greenlight** to implement — next: SurrogatePatientGenerator (§6.2, TDD RED first).

## Open threads
- gh CLI not authed → user must run `gh auth login --web` before first push/PR.
- Optional `/plugin install superpowers@superpowers-dev` (full plugin) — user to run; skills already work.

## Recent decisions
- [2026-06-29] conda env `medargue` @ Python 3.12 (not base 3.13 — ML stack lags 3.13).
- [2026-06-29] Branch model: `main` + feature branches; PRs target main.
- [2026-06-29] Full Claudify skills library gitignored (local-only) to keep academic repo lean.

## Blockers
- (none)

## Session handoff
- Setup phase done. Resume by confirming greenlight, then `/card`-style TDD on SurrogatePatientGenerator.
