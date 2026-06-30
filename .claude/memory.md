# Project Memory — medargue

> Working memory for cross-session continuity. Read on session start / after compaction.
> Durable facts live in the auto-memory store; this file is the active-work scratch.

## Now
Realigned to dissertation v6 (#7). Merged: Card 1 loaders (#8), Card 2 modality partitioner (#9),
**Card 3 real model clients (#10)**. Next: **Card 4 — Vision Agent (BioViL + CLIP Image RAG + LLaVA-Med)**.
Decisions locked: per-modality Cases; CheXpert policy configurable (CheXpert-paper default); OIDP via
frozen views; **clients real (no mocks); LLaVA-Med 4-bit via Ollama (rohithbojja/llava-med-v1.5),
BioViL via hi-ml-multimodal; env on numpy 2 + CUDA torch cu128.** PR discipline: raise PR + STOP,
user merges (see [[pr-merge-discipline]]).

## Known follow-up
- **numpy 1↔2 split**: scispaCy/thinc want <2; transformers/scipy want ≥2 (env on 2.5). Card 5
  (Report Agent / scispaCy) must upgrade spaCy/thinc to numpy-2 versions first.

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
