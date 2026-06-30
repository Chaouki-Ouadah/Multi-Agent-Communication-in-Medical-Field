# Project Memory — medargue

> Working memory for cross-session continuity. Read on session start / after compaction.
> Durable facts live in the auto-memory store; this file is the active-work scratch.

## Now
Merged: Cards 1–4 (#8 loaders, #9 partitioner, #10 model clients, **#11 Vision Agent**).
Next: **Card 5 — Report Agent (section extraction + scispaCy NER + Meditron)**.
Decisions locked: per-modality Cases; CheXpert policy configurable; OIDP frozen views; clients real
(no mocks); LLaVA-Med 4-bit via Ollama `rohithbojja/llava-med-v1.5`; BioViL via hi-ml-multimodal;
CLIP Image RAG = BioViL→ChromaDB (per-instance collection); shared `Argument` in
argumentation/framework.py; NIH slice via kagglehub (data/chestxray14, gitignored). env: numpy 2 +
CUDA torch cu128. PR discipline: raise PR + STOP, user merges (see [[pr-merge-discipline]]).

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
