# LLM Setup — Local Ollama for the medargue agents

The multi-agent debate runs on **local, free** models served by **Ollama** (`http://localhost:11434`).
GPT-4o (API) is used only as a comparison baseline.

## Installed models (verified on this machine)

| Env var | Model | Role |
|---------|-------|------|
| `LLM_PRIMARY_MODEL` | `meditron` (3.8 GB, EPFL clinical LLM) | primary agent reasoning |
| `LLM_STRONG_MODEL` | `qwen2.5:14b` (9.0 GB) | stronger reasoning / harder cases |
| `LLM_FALLBACK_MODEL` | `llama3.1:8b` (4.9 GB) | general fallback |
| `LLM_BASELINE_MODEL` | `gpt-4o` (API) | baseline comparison only |

Check: `ollama list`. Pull more: `ollama pull <model>`.

## Verify it works
```bash
curl -s http://localhost:11434/api/generate \
  -d '{"model":"meditron","prompt":"Define anterior MI in one sentence.","stream":false}'
# → JSON with a clinical "response" field
```

## How agents connect (the wiring contract — implement during agent cards)

- All LLM access goes through **one mockable client wrapper** (e.g. `src/agents/llm_client.py`),
  never a direct call in business logic. Unit tests inject a fake; only `@pytest.mark.llm` tests hit
  a live model.
- Use LangChain's Ollama integration inside LangGraph nodes:
  ```python
  from langchain_ollama import ChatOllama  # or langchain_community.chat_models.ChatOllama
  llm = ChatOllama(
      model=os.environ.get("LLM_PRIMARY_MODEL", "meditron"),
      base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
      temperature=float(os.environ.get("LLM_TEMPERATURE", "0.2")),
  )
  ```
- **Determinism:** fix `temperature` low and pass a seed where the backend supports it; record the
  exact model + params in MLflow for each run so experiments are reproducible.
- **Config source:** values come from `.env` (copy from `.env.example`). Never hardcode model names
  in modules — read the env vars so the model can be swapped without code changes.

## Notes
- `meditron` is Llama-2-based (EPFL Meditron-7B). The dissertation spec named "Llama-3-Meditron-8B";
  `meditron` is the freely-available Ollama equivalent. Swap via `LLM_PRIMARY_MODEL` if a better
  clinical model is pulled later.
- Ollama must be running (`ollama serve` / the desktop app) before any `llm`-marked test or a UI run.
