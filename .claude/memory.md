# Project Memory — medargue

> Working memory for cross-session continuity. Read on session start / after compaction.
> Durable facts live in the auto-memory store; this file is the active-work scratch.

## Now
**Project realigned to dissertation v6 (MIMIC multimodal)** — the UCI #579 synthetic-tabular spec was
the stale pre-pivot design. IMPLEMENTATION_CONTEXT, cards, build-order, README, docs, src stubs,
.env, knowledge-base all rewritten on branch `chore/align-dissertation-v6` (PR pending).
Next after merge: **Card 1 — multimodal loader + surrogate datasets** (NIH ChestX-ray14 / OpenI /
MIMIC-IV Demo), TDD RED first.

## Open threads
- Open implementation decisions flagged in cards.md (attack threshold, convergence def, confidence
  source, GraphRAG corpus) — resolve per card with the user.

## Recent decisions
- [2026-06-30] Dissertation_Final_v6.pdf is authoritative → realigned everything to MIMIC multimodal
  (Vision/Report/Clinical modality agents; CheXpert-14; CLIP image-RAG + GraphRAG; Dung's AAF + Walton 7).
- [2026-06-29] conda env `medargue` @ Python 3.12; main + feature branches; one card = one PR.
- [2026-06-29] Full Claudify skills library gitignored (local-only).

## Blockers
- (none) — real MIMIC blocked on PhysioNet+CITI+ethics (Track 2, parallel).

## Session handoff
- Realignment branch open. After it merges, run `/mp-card` on Card 1.
