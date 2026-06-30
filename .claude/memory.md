# Project Memory — medargue

> Working memory for cross-session continuity. Read on session start / after compaction.
> Durable facts live in the auto-memory store; this file is the active-work scratch.

## Now
Merged: Cards 1–6 (#8 loaders, #9 partitioner, #10 clients, #11 Vision, #12 Report, **#13 Clinical**).
All 3 modality agents done (Vision/Report/Clinical, real + GPU-verified). 2-agent live demo ran OK.
Next: **Card 7 — LangGraph debate + Supervisor (≤5 rounds)** — also folds in the Report/Clinical
prompt-echo output-parse fix (Meditron echoes prompt → junk Sign args; see cards.md Card 7).
Decisions locked: per-modality Cases; CheXpert policy configurable; OIDP frozen views; clients real
(no mocks); LLaVA-Med 4-bit via Ollama `rohithbojja/llava-med-v1.5`; BioViL via hi-ml-multimodal;
CLIP Image RAG = BioViL→ChromaDB (per-instance collection); shared `Argument` in
argumentation/framework.py; NIH slice via kagglehub (data/chestxray14, gitignored). env: numpy 2 +
CUDA torch cu128. PR discipline: raise PR + STOP, user merges (see [[pr-merge-discipline]]).

## Known follow-up
- **numpy split RESOLVED (Card 5):** env coheres on numpy 1.26.4 (scispaCy 0.6.2 / spaCy 3.7.5 /
  scipy 1.17.1 / transformers 5.x / torch cu128 all import; all 5 live tests pass). scispaCy model
  pins spaCy 3.7.5 — don't force 3.8.
- **graphrag (Card 10) deferred conflict:** wants spacy~=3.8 + numpy~=2.1 — unsatisfiable with the
  scispaCy set. Resolve when GraphRAG lands (likely isolate or drop the strict pin).

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
