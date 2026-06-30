# Knowledge Base — medargue

> Curated institutional knowledge. Every entry MUST cite provenance with `[Source: ...]`.
> Keep under 200 lines — curate stale entries before adding new ones.
> (Format enforced by .claude/hooks/completeness-gate.sh)

## Environment & tooling
- **Python env**: project runs in conda env `medargue` (3.12), not base 3.13 — torch, scispacy en_core_sci_lg, graphrag 3.0.2 do not reliably build on 3.13. [Source: empirical — workspace setup 2026-06-29]
- **jq PATH (Windows/git-bash)**: git-bash does NOT inherit winget's PATH; place `jq.exe` in `/c/Users/chawk/bin` (already on bash PATH) so hooks can find it. [Source: empirical — jq not found in hooks until copied, 2026-06-29]
- **Hook line endings**: Claude Code hooks run via git-bash and require LF line endings; CRLF causes carriage-return parse failures. Normalize hooks to LF after copying from Windows sources. [Source: empirical — file showed CRLF; hooks failed until normalized, 2026-06-29]
- **Local CI gate**: `ruff check .`, `ruff format --check .`, `mypy`, `pytest -m "not slow and not llm"` must pass before push. [Source: CLAUDE.md, engineering-methodology.md §7]
- **numpy 2 required**: transformers 5.x + scipy need numpy>=2; env upgraded to numpy 2.5 (scispaCy/thinc still want <2 — unresolved split, address when Card 5/scispaCy lands). [Source: empirical — scipy np.long crash on numpy 1.26, Card 3]
- **CUDA torch for RTX 5070 (Blackwell)**: `pip install --index-url https://download.pytorch.org/whl/cu128 torch torchvision` (cu128). Default PyPI torch is CPU-only on Windows. [Source: empirical — torch+cpu had cuda=False until cu128, Card 3]
- **LLaVA-Med via Ollama, NOT HF transformers**: the HF checkpoint is `LlavaMistralForCausalLM` (bespoke codebase, old-transformers) — incompatible with transformers 5.x. Use Ollama `rohithbojja/llava-med-v1.5` (Q4_K_M 4-bit, CLIP projector). [Source: empirical + user decision, Card 3]
- **BioViL-T via `hi-ml-multimodal`**: HF AutoImageProcessor unsupported; use `health_multimodal.image.get_image_inference(ImageModelType.BIOVIL_T).get_projected_global_embedding()`. [Source: empirical — AutoImageProcessor OSError, Card 3]
- **Model clients are real, never mocked in the pipeline**: live model tests marked `llm`/`slow` run locally; CI skips them. [Source: user rule — "nothing mocked, real things", Card 3]

## Project architecture (MIMIC multimodal — dissertation v6 is authoritative)
- **Data is MULTIMODAL, not tabular**: CXR image + radiology report + structured EHR, linked by subject_id/study_id; targets = CheXpert 14 labels (focus 5). NOT UCI #579. [Source: Dissertation_Final_v6.pdf pp.34-36]
- **Loader contract**: `BaseDatasetLoader` (cases, labels, modalities, variable_dictionary); a Case bundles the three modalities. Surrogate loaders -> MIMIC later, same interface. [Source: IMPLEMENTATION_CONTEXT.md §2]
- **Surrogate datasets are REAL open data** (no synthetic generation): NIH ChestX-ray14 (images), OpenI Indiana (reports), MIMIC-IV Demo (EHR); mirror MIMIC formats. [Source: Dissertation_Final_v6.pdf p.36]
- **Agents partition by MODALITY (independent variable, OIDP)**: Vision (CXR image, LLaVA-Med 7B), Report (report text, Meditron-8B), Clinical (EHR, Meditron-8B), Supervisor (text args only, Meditron-8B). [Source: Dissertation_Final_v6.pdf pp.36-38]
- **Argumentation**: Dung's AAF via NetworkX, preferred extensions; Walton's 7 clinically-relevant schemes label/weight arguments; text-domain, modality-agnostic. [Source: Dissertation_Final_v6.pdf pp.41-43]
- **Debate**: LangGraph state machine, <=5 rounds, converge when no new attacks; Supervisor never sees raw data. [Source: Dissertation_Final_v6.pdf p.39]
- **RAG (SRQ2)**: A=Vector (ChromaDB), B=GraphRAG (Microsoft+Neo4j, UMLS/SNOMED/ICD-10/PrimeKG), C=Hybrid (+CLIP Image RAG via BioViL). [Source: Dissertation_Final_v6.pdf pp.43-44]
- **Eval (6 dims)**: multi-label F1 macro/micro, per-pathology AUROC, explainability, process transparency, ECE, Cohen's kappa; baselines B1-B5, ablations A1-A7. [Source: Dissertation_Final_v6.pdf pp.45-48]

## Guardrails
- **Not clinical advice**: label every model output as a research-prototype, non-clinical result. [Source: IMPLEMENTATION_CONTEXT.md §10]
- **No credentialed/real patient data**; real MIMIC only after PhysioNet+CITI+ethics. Track-1 uses open surrogates. [Source: IMPLEMENTATION_CONTEXT.md §10]
- **Build discipline**: strict TDD (RED → GREEN → REFACTOR), one feature branch per §6 step, small PRs to main, tests green before merge. [Source: IMPLEMENTATION_CONTEXT.md §6, engineering-methodology.md §3]
