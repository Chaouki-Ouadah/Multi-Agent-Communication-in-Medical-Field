# Multi-Agent Argumentation for Explainable Clinical Decision Support

> MSc AI/Data Science dissertation — Heriot-Watt University Dubai
> **Research prototype — not clinical advice.**

Three LLM "specialist" agents each see a **different partition** of a patient's clinical features,
debate likely complications, and a **symbolic argumentation engine** (Dung's Abstract Argumentation
Framework + Walton schemes) resolves the debate into an explainable recommendation.

## Status — Track 1: Surrogate Data First

MIMIC access is pending credentialing, so the pipeline is built and validated end-to-end on
**fully synthetic surrogate data** that structurally mimics the UCI #579 MI-Complications dataset.
When real-data access is granted, only the data loader is swapped — nothing else changes.

See **[`IMPLEMENTATION_CONTEXT.md`](./IMPLEMENTATION_CONTEXT.md)** for the full spec and build order.

## Architecture

```
Tabular patient row → Vignette Generator → Feature Partitioner (3 domain masks)
  → scispaCy NER → KG Retrieval (Vector / GraphRAG / Hybrid)
  → 3 LLM Agents debate [LangGraph] → Dung's AAF resolution
  → Explanation Generator → recommendation + explanation + arg tree + confidence
```

| Agent | Sees | Role |
|-------|------|------|
| History & Risk | demographics, prior MI, comorbidities, vitals | "Who is this patient?" |
| Diagnostic | ECG, MI location, labs, admission | "What's happening now?" |
| Treatment & Progression | meds, fibrinolytics, pain trends | "What was done, how responding?" |
| Supervisor | all features | moderator, convergence, gap detection |

## Quickstart

```powershell
conda activate medargue
pip install -r requirements-dev.txt          # dev + core stack
pip install -r requirements-models.txt        # scispaCy clinical model (~1GB)
python -m playwright install chromium          # for E2E UI tests
cp .env.example .env                           # then fill in keys

pytest                                         # run tests
streamlit run ui/app.py                        # launch UI
```

## Tech stack

LangGraph · GraphRAG + Neo4j + ChromaDB · Llama-3-Meditron-8B (Ollama) · GPT-4o (baseline) ·
BGE-large embeddings · scispaCy · NetworkX (Dung's AAF) · Streamlit + Graphviz · MLflow.

## Repository layout

See [`IMPLEMENTATION_CONTEXT.md` §5](./IMPLEMENTATION_CONTEXT.md). Source lives under `src/`,
UI under `ui/`, tests under `tests/`, experiment configs/results under `experiments/`.

## Development

This repo follows [`engineering-methodology.md`](./engineering-methodology.md): 11-phase card flow,
TDD (RED→GREEN→REFACTOR), small PRs to `main`, green local CI before push. Pre-commit hooks run
ruff + mypy + bandit + detect-secrets on staged files.

## License

MIT. Surrogate data is synthetic; no real patient data is stored in this repository.
