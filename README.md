# Multi-Agent Argumentation for Explainable Clinical Decision Support

> MSc AI/Data Science dissertation — Heriot-Watt University Dubai
> **Research prototype — not clinical advice.**

Three **modality-partitioned** LLM agents each see a *different clinical modality* of the same chest
study — the X-ray image, the radiology report, or the structured EHR — debate the likely chest
pathologies, and a **symbolic argumentation engine** (Dung's Abstract Argumentation Framework + Walton
schemes) resolves the cross-modal debate into an explainable, calibrated recommendation.

Authoritative spec: **`Dessertation Doc/Dissertation_Final_v6.pdf`** → distilled into
**[`IMPLEMENTATION_CONTEXT.md`](./IMPLEMENTATION_CONTEXT.md)** (full spec + build order).

## Status — Track 1: Surrogate Data First

MIMIC access is pending PhysioNet + CITI credentialing, so the pipeline is built and validated
end-to-end on **real, openly-licensed surrogate datasets that share MIMIC's formats** — NIH
ChestX-ray14 (images), OpenI Indiana (reports), MIMIC-IV Demo (EHR). When credentialing lands, the
data loaders are swapped for MIMIC — nothing else changes.

## Architecture

```
Multimodal study (subject_id / study_id)
  ├─ CXR image → Vision Agent:   BioViL embed → CLIP Image RAG (ChromaDB) → LLaVA-Med 7B
  ├─ report    → Report Agent:   section extract + scispaCy NER → Meditron-8B
  └─ EHR       → Clinical Agent: serialise labs/vitals (ref ranges, ↑/↓/✓) → Meditron-8B
       → text arguments (Walton-labelled) → Supervisor mediates [LangGraph, ≤5 rounds]
       → Dung's AAF → preferred extension → explanation + arg tree + confidence
```

| Agent | Sees | Model |
|-------|------|-------|
| Vision | CXR image only | LLaVA-Med 7B (4-bit) |
| Report | radiology report only | Meditron-8B (4-bit) |
| Clinical | structured EHR only | Meditron-8B (4-bit) |
| Supervisor | all agents' text arguments (no raw data) | Meditron-8B (4-bit) |

Targets: **CheXpert 14 labels** (focus 5: Cardiomegaly, Pleural Effusion, Pneumonia, Pneumothorax,
Atelectasis). Information partitioning by **modality** (OIDP) is the independent variable.

## Quickstart

```powershell
conda activate medargue
pip install -r requirements-dev.txt          # dev + core stack
pip install -r requirements-models.txt        # scispaCy clinical model (~1GB)
python -m playwright install chromium          # for E2E UI tests
ollama list                                    # meditron + llama3.1:8b local
cp .env.example .env                           # then fill keys / paths

pytest                                         # run tests
streamlit run ui/app.py                        # launch UI
```

## Tech stack

LangGraph · ChromaDB (CLIP Image RAG + vector) · Microsoft GraphRAG + Neo4j · Meditron-8B (Ollama) ·
LLaVA-Med 7B (VLM) · BioViL (image embeddings) · scispaCy · NetworkX (Dung's AAF) · GPT-4o (baseline) ·
Streamlit + Graphviz · MLflow. Local models 4-bit on 8 GB VRAM, loaded sequentially.

## Repository layout

See [`IMPLEMENTATION_CONTEXT.md` §3/§6](./IMPLEMENTATION_CONTEXT.md) and the card backlog at
[`docs/plans/cards.md`](./docs/plans/cards.md). Source under `src/`, UI under `ui/`, tests under
`tests/`, design + plan docs under `docs/`.

## Development

Follows [`engineering-methodology.md`](./engineering-methodology.md) via the `/mp-card` skill:
plan-first, TDD (RED→GREEN→REFACTOR), one card = one branch = one PR to `main`, green local CI before
push. Pre-commit hooks run ruff + mypy + bandit + detect-secrets.

## License

MIT (code). Track-1 surrogate datasets are open-licensed (CC0 / open access). No credentialed or real
patient data is stored in this repository.
