# Project Memory — medargue

> Working memory for cross-session continuity. Read on session start / after compaction.
> Durable facts live in the auto-memory store; this file is the active-work scratch.

## Now
Merged: Cards 1–9 (#8 loaders … #14 debate, **#15 AAF**, **#16 Walton/explanation**).
Symbolic layer COMPLETE: `argumentation/framework.py` AAF (NetworkX ⟨A,R⟩, claim-keyed nodes) +
`resolver.py` Dung `preferred_extensions` (controversial-subgraph enumeration) + `schemes.py`
`WaltonScheme` (7) + `CRITICAL_QUESTIONS` + `form_attacks` (negation/lexical, cross-agent,
bidirectional→2-cycle) + `explanation.py` `generate_explanation` (winners+evidence, disclaimer-ended).
All pure, CI-green. Agents still emit free-text scheme strings (enum interprets via scheme_from_label).
DONE: pip-audit ignore PYSEC-2026-311 in ci.yml+security.yml+requirements (merged with #15).
Next: **Card 10 — GraphRAG + Neo4j KG (SRQ2 configs A/B/C)** — HEAVY. BLOCKER to resolve first:
graphrag wants numpy~=2.1 + spacy~=3.8, unsatisfiable with the scispaCy numpy<2 set → isolate
(separate env/optional-extra) or drop strict pin or pick alt. Also still pure-module pattern: AAF/
resolver/explanation NOT yet wired into pipeline/graph.py (DebateState.extension/explanation empty) —
a future wiring card.
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

## Session handoff (2026-07-01 — pre-reboot checkpoint)
- **Cards 1–9 merged** (PRs #8–#16). Symbolic layer complete (AAF/resolver/schemes/explanation).
- **Card 10 SPLIT** (user): **10a** = retriever interface + Vector RAG (config A, ChromaDB) + hybrid
  fusion (graph-ready) — plan WRITTEN + APPROVED-pending at `docs/plans/card-10a-retrieval-interface.md`;
  branch will be `feature/retrieval-interface`; NO Docker needed; NOT started yet. **10b** = MS GraphRAG
  (isolated venv) + real Neo4j (Docker) + UMLS/SNOMED/ICD-10/PrimeKG — later, infra-gated.
- Decisions: KG corpus **external-only** (faithful, no leakage); **heavy-faithful path always**
  ([[heavy-faithful-path]]).
- **DOCKER FIX IN PROGRESS:** Docker Desktop failed ("virtualization not detected"). Root cause =
  Virtual Machine Platform feature was OFF + WSL2 had no distro. Ran elevated DISM enable of
  `Microsoft-Windows-Subsystem-Linux` + `VirtualMachinePlatform` (both succeeded). **PC reboot pending**
  to finish. HypervisorPresent=True (firmware VT-x already on). After reboot: start Docker Desktop →
  verify `docker run --rm hello-world` → stage Neo4j container for 10b.
- **RESUME AFTER REBOOT:** either build Card 10a (say "go 10a") or finish Docker verify first.
- Earlier realignment note (historical): after realign merged, Card 1 ran. Done.
