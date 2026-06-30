# Implementation Plan — medargue Track 1 (MIMIC multimodal, surrogate-data-first)

> Derived from `IMPLEMENTATION_CONTEXT.md` §6 (which derives from `Dissertation_Final_v6.pdf`).
> Each step = RED → GREEN → REFACTOR, one `feature/` branch → one PR to `main`. Full card detail in
> `docs/plans/cards.md`. This file is the at-a-glance TDD sequence.

## Context
Build/validate the whole multi-agent argumentation pipeline on real open **surrogate** datasets
(NIH ChestX-ray14 / OpenI / MIMIC-IV Demo) that mirror MIMIC's formats, then swap loaders for real
MIMIC once PhysioNet+CITI credentialing lands. Three modality-partitioned agents (Vision / Report /
Clinical) + Supervisor debate chest-pathology findings; Dung's AAF + Walton schemes resolve it.

## State map
- Workspace, env, CI/CD, Claude config: DONE. Spec realigned to dissertation v6 (this branch).
- All `src/` modules are stubs. Steps 1–15 below are not started.

## Approach
Strict TDD. Pure, testable libs; LLM/VLM/embedding access behind mockable clients (no live model in
unit tests; `@pytest.mark.llm` for live). Determinism via `seed=42`. Text-domain symbolic layer so
argumentation is modality-agnostic.

## Out of scope (Track 1)
Real MIMIC data (credentialing pending — Step 15). Heavy model weights downloaded only when their
card runs. GPT-4o baseline only after the local path works.

## Step sequence (TDD)
1. **Loaders** (`feature/loaders`) — `BaseDatasetLoader` + `Case` + CheXpert-14 + 3 surrogate loaders.
2. **Modality partitioner** (`feature/modality-partition`) — per-agent views; leakage tests.
3. **Model clients** (`feature/model-clients`) — Meditron (Ollama), LLaVA-Med, BioViL; mockable.
4. **Vision Agent** (`feature/agent-vision`) — BioViL → CLIP Image RAG → LLaVA-Med findings.
5. **Report Agent** (`feature/agent-report`) — sections + scispaCy NER → Meditron.
6. **Clinical Agent** (`feature/agent-clinical`) — EHR serialisation → Meditron.
7. **Debate graph** (`feature/debate-graph`) — LangGraph state machine + Supervisor, ≤5 rounds.
8. **AAF** (`feature/aaf`) — Dung's framework + preferred-extension resolver (toy-graph tests).
9. **Explanation** (`feature/explanation`) — Walton 7 schemes + attacks + narrative + disclaimer.
10. **GraphRAG** (`feature/graphrag`) — Microsoft GraphRAG + Neo4j KG; SRQ2 configs A/B/C.
11. **Metrics** (`feature/eval`) — 6 dimensions (F1 macro/micro, AUROC, ECE, Cohen's κ).
12. **Baselines/ablations** (`feature/baselines`) — B1–B5, A1–A7, paired Wilcoxon.
13. **UI** (`feature/ui`) — Streamlit CXR + 3 modality panels + arg-tree + confidence; E2E.
14. **Benchmark** (`feature/benchmark`) — model-selection harness (F1/latency/VRAM, MLflow).
15. **Real MIMIC** (`feature/mimic`) — `MimicLoader` swap, post-credentialing.

## Verification (per step)
`conda run -n medargue ruff check . && ruff format --check . && mypy && pytest -m "not slow and not llm and not e2e"` green before push. ≥1 live Playwright scenario at Step 13.

## Definition of Done (track)
End-to-end surrogate run → 3 agents debate → AAF resolves → explanation + arg tree in Streamlit →
6-dim metrics in MLflow → tests green → pushed. Then Step 15 swaps to real MIMIC.
