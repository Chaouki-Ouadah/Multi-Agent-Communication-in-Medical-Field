# Model Setup — local models for the medargue agents

The debate runs on **local, free** models. Text agents (Report / Clinical / Supervisor) use
**Meditron-8B** via **Ollama**; the **Vision** agent uses **LLaVA-Med 7B** (VLM) + **BioViL** image
embeddings via Hugging Face Transformers. GPT-4o (API) is the B1 baseline only. All local models run
**4-bit on 8 GB VRAM**, loaded **sequentially** (not concurrently).

## Models & roles

| Env var | Model | Role | Serving |
|---------|-------|------|---------|
| `LLM_PRIMARY_MODEL` | `meditron` (EPFL clinical) | Report / Clinical / Supervisor text reasoning | Ollama |
| `VLM_MODEL` | `LLaVA-Med 7B` | Vision Agent VQA on CXR | HF Transformers (4-bit) |
| `EMBED_MODEL` | `BioViL` | CXR image embeddings (CLIP Image RAG) | HF / `health-multimodal` |
| `LLM_BASELINE_GENERAL` | `llama3.1:8b` | A5 ablation / general-LLM baseline | Ollama |
| `LLM_STRONG_MODEL` | `qwen2.5:14b` | stronger reasoning fallback | Ollama |
| `LLM_BASELINE_MODEL` | `gpt-4o` (API) | B1 zero-shot baseline only | OpenAI API |

Check Ollama models: `ollama list` (meditron, llama3.1:8b, qwen2.5:14b installed). LLaVA-Med + BioViL
weights are pulled from HF during the Vision/model-client cards (not committed).

## Verify Ollama works
```bash
curl -s http://localhost:11434/api/generate \
  -d '{"model":"meditron","prompt":"List two findings suggesting cardiomegaly on a chest X-ray.","stream":false}'
# → JSON with a clinical "response" field
```

## Wiring contract (implement during Card 3 — model clients)

- Every model call goes through **one mockable client** — never a direct call in business logic:
  `src/agents/llm_client.py` (Meditron via Ollama), `src/agents/vlm_client.py` (LLaVA-Med),
  `src/agents/embeddings.py` (BioViL). Unit tests inject fakes; only `@pytest.mark.llm` (and `slow`)
  tests hit live models.
- Ollama text via LangChain:
  ```python
  from langchain_ollama import ChatOllama
  llm = ChatOllama(
      model=os.environ.get("LLM_PRIMARY_MODEL", "meditron"),
      base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
      temperature=float(os.environ.get("LLM_TEMPERATURE", "0.2")),
  )
  ```
- **VRAM discipline:** load one heavy model at a time (Vision pass, then text agents); free between
  stages. **Determinism:** low temperature; log exact model + params to MLflow per run.
- **Config from `.env`** — never hardcode model names in modules.

## Notes
- `meditron` (Ollama) is the freely-available EPFL Meditron; the dissertation names "Meditron-8B" /
  "Llama-3-Meditron-8B" — swap via `LLM_PRIMARY_MODEL` if a better clinical build is pulled.
- The model-selection benchmark card (Card 14) empirically compares Meditron vs Llama-3.1, BioViL vs
  MedCLIP, LLaVA-Med vs LLaVA-1.5 on F1 / latency / VRAM — choices are justified, not assumed.
- Ollama must be running before any `llm`-marked test or UI run.
