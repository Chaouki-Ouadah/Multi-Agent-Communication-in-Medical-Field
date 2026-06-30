# Project Memory — medargue

> Working memory for cross-session continuity. Read on session start / after compaction.
> Durable facts live in the auto-memory store; this file is the active-work scratch.

## Now
Realigned to dissertation v6 (MIMIC multimodal) — merged (PR #7). **Card 1 (multimodal loader +
Case + CheXpert-14 + 3 surrogate loaders) done** — PR #8 open, auto-merge armed (TDD: 12 tests
RED→GREEN, gate green, /security-review clean). Next: **Card 2 — modality partitioner + Case views**.
Key decisions locked: per-modality Cases (tri-modal linkage waits for real MIMIC); CheXpert label
policy configurable, default = CheXpert-paper per-pathology.

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
