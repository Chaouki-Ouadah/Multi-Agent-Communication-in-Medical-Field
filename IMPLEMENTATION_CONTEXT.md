# IMPLEMENTATION CONTEXT — Multi-Agent Argumentation Clinical Decision Support

> **Single source of truth for implementing this project. Derived from the authoritative dissertation
> `Dessertation Doc/Dissertation_Final_v6.pdf` (page refs throughout).** Read it fully before coding.
> Where this file and the dissertation diverge, the dissertation wins — reconcile and flag.

---

## 0. TL;DR — What We Are Building

A **multi-agent argumentation system** for explainable clinical decision support on **chest imaging**.
Three **modality-partitioned** LLM agents each see a *different clinical modality* of the same patient
study, debate the likely chest pathologies, and a **symbolic argumentation engine** (Dung's AAF +
Walton schemes) resolves the cross-modal debate into an explainable, calibrated recommendation.

**START HERE → Track 1 (Surrogate Data First):** PhysioNet + CITI credentialing for the primary MIMIC
data is pending. So we build and validate the entire pipeline NOW on **real, openly-available
surrogate datasets that share MIMIC's formats** (no credentialing). When MIMIC access is granted, we
swap the data loaders — nothing else changes.

**Repository:** https://github.com/Chaouki-Ouadah/Multi-Agent-Communication-in-Medical-Field
**Degree:** MSc AI/Data Science — Heriot-Watt University Dubai · **Student:** Chaouki Ouadah ·
**Supervisor:** Radu-Casian Mihailescu, Ph.D.

---

## 1. Research Questions (dissertation pp.4–5)

**Primary RQ:** How can multi-agent argumentation frameworks, augmented by LLMs and RAG, improve the
explainability and trustworthiness of clinical decision support systems?

| ID | Sub-Question | Targets |
|----|-------------|---------|
| SRQ1 | How can Walton's schemes integrate with LLM debate to produce clinically meaningful explanations? | symbolic layer |
| SRQ2 | How do different RAG approaches affect factual grounding/consistency of multi-agent reasoning? | retrieval (Vector / Graph / Hybrid) |
| SRQ3 | How do clinical data **modalities** (CXR image, report, structured EHR) as modality-partitioned agents affect outcomes? | agent architecture |
| SRQ4 | What metrics beyond accuracy (explainability, process, trust) best assess argumentation-based CDSS? | evaluation |

**Novel contribution:** combining **CLIP image-RAG + KG-RAG + multi-agent argumentation + symbolic
Dung's AAF resolution + modality partitioning**, with six-dimensional evaluation (the Multimodal
Hybrid retrieval config, Run C, is the most novel — no published system combines all three).

---

## 2. The Surrogate-Data-First Strategy (Track 1)  (dissertation p.36)

### Why surrogate data
MIMIC credentialing (PhysioNet + CITI "Data or Specimens Only Research") is pending; we must not block
implementation. The dissertation's surrogates are **real, open datasets that mirror MIMIC's structure**
— NOT synthetically generated data.

### Surrogate datasets (use now, no credentialing)
| Modality | Surrogate (Track 1) | Real (Track 2, after credentialing) |
|----------|---------------------|-------------------------------------|
| CXR image | **NIH ChestX-ray14** (112,120 images, CC0) | MIMIC-CXR-JPG v2.1.0 |
| Radiology report | **OpenI Indiana University** (7,470 CXR-report pairs) | MIMIC-IV-Note v2.2 |
| Structured EHR | **MIMIC-IV Demo** (100 patients, open access) | MIMIC-IV v3.1 |

### Design rule: dataset-agnostic, multimodal loader
All data flows through one interface `BaseDatasetLoader`. A **case** = `{image_path, report_text,
ehr_record}` linked by `subject_id` / `study_id`, plus CheXpert labels. Surrogate loaders implement it
first; `MIMICLoader` implements the same interface later → **no pipeline changes** to swap.

```python
class BaseDatasetLoader(ABC):
    @abstractmethod
    def cases(self) -> Iterable[Case]: ...          # multimodal case stream
    @abstractmethod
    def labels(self) -> list[str]: ...              # CheXpert-14 label set
    @abstractmethod
    def modalities(self) -> dict[str, str]: ...     # modality -> source description
    @abstractmethod
    def variable_dictionary(self) -> dict[str, dict]: ...  # EHR code -> human meaning + ref range
```

---

## 3. System Architecture (Data Flow)  (dissertation pp.26–27, 39–44)

```
Multimodal patient study (linked by subject_id / study_id)
   ├─ CXR image  → Vision Agent:   BioViL embed → CLIP Image RAG (ChromaDB) → LLaVA-Med 7B VQA → findings
   ├─ report     → Report Agent:   section extract (Findings/Impression) + scispaCy NER → Meditron-8B → findings
   └─ EHR        → Clinical Agent: prompt serialisation (ref ranges, ↑/↓/✓) → Meditron-8B → findings
        → all agents emit TEXT arguments (Walton-scheme labelled)
        → Supervisor (Meditron-8B): sees only the text arguments, detects cross-modal conflict, mediates
        → Multi-round debate [LangGraph state machine, ≤5 rounds, converge when no new attacks]
        → Symbolic resolution: Dung's AAF ⟨A,R⟩ → preferred extension (winning arguments)
        → Explanation generator: narrative + argumentation tree + calibrated confidence
   → OUTPUT: pathology recommendation + explanation + arg tree + confidence
```

### The 3 agents + supervisor (dissertation pp.36–38, Table 4.2)
| Agent | Sees | Cannot see | Model | Processing |
|-------|------|-----------|-------|-----------|
| **Vision** | CXR image only | report, EHR | LLaVA-Med 7B (4-bit) | BioViL embed → CLIP Image RAG → VQA |
| **Report** | report text only | image, EHR | Meditron-8B (4-bit) | Findings/Impression extract + scispaCy NER |
| **Clinical** | structured EHR only | image, report | Meditron-8B (4-bit) | serialise labs/vitals + reference ranges + ↑/↓/✓ |
| **Supervisor** | all agents' text args | raw data | Meditron-8B (4-bit) | mediate, detect conflict, convergence (≤5 rounds) |

**OIDP (One Issue, Different Perspectives):** modality partitioning creates genuine information
asymmetry that drives meaningful argumentation — agents disagree because they hold different modalities,
NOT because of tone/attitude prompts. All agents emit **text** arguments → the symbolic layer is
modality-agnostic and extensible (add a modality = add an agent, no symbolic-layer change).

---

## 4. Argumentation Engine  (dissertation pp.41–43)

- **Dung's AAF** ⟨A, R⟩: A = arguments, R ⊆ A×A = attacks. Compute **preferred extensions** (maximal
  admissible sets) → the winning arguments that survive cross-modal debate → formal justification.
- **Walton's schemes** — 7 clinically-relevant (Expert Opinion, Evidence→Hypothesis, Analogy,
  Cause→Effect, Consequences, Established Rule, Sign). Agents label each argument with its scheme;
  the Supervisor weights by scheme during mediation; labels drive explainability (the arg tree shows
  *why* each argument was made).
- Attack example: Vision "Pneumonia likely" vs Clinical "Normal WBC → pneumonia unlikely" → register
  an attack; preferred extension decides the survivor.

---

## 5. Tech Stack (dissertation pp.38–44)

| Layer | Tool | Notes |
|-------|------|------|
| Orchestration | LangGraph v1.0+ | debate state machine, ≤5 rounds |
| Text LLM | **Meditron-8B** (4-bit, Ollama) | Report / Clinical / Supervisor; baseline Llama-3.1-8B |
| VLM | **LLaVA-Med 7B** (4-bit) | Vision Agent VQA |
| Image embeddings | **BioViL** | CXR-specific; CLIP Image RAG |
| NER | scispaCy `en_core_sci_lg` | report findings |
| Vector store | ChromaDB | CLIP Image RAG + text vector RAG |
| Graph RAG | Microsoft GraphRAG + Neo4j | UMLS / SNOMED-CT / ICD-10 / PrimeKG + guidelines |
| Argumentation | NetworkX (custom Dung's AAF) | preferred extensions |
| Baseline (API) | GPT-4o | B1 only |
| UI | Streamlit + Graphviz | arg-tree + CXR + modality panels |
| Tracking | MLflow | experiments |
| Hardware | RTX 5070, 8 GB VRAM | 4-bit, models loaded sequentially |

---

## 6. Build Order (Track 1, TDD — write test first each step)

See `docs/plans/cards.md` for full card detail (goal/scope/files/tests/AC). Summary order:
1. Multimodal `BaseDatasetLoader` + surrogate loaders (NIH CXR14 / OpenI / MIMIC-IV Demo) + CheXpert-14.
2. Modality partitioner + `Case` object (image/report/EHR views) — partition integrity.
3. Model clients: Ollama Meditron `llm_client`, LLaVA-Med `vlm_client`, BioViL `embeddings` (mockable).
4. Vision Agent (BioViL → CLIP Image RAG → LLaVA-Med).
5. Report Agent (section extract + scispaCy NER → Meditron).
6. Clinical Agent (EHR serialisation → Meditron).
7. LangGraph debate + Supervisor + ≤5-round convergence (mock agents).
8. Dung's AAF + preferred-extension resolver.
9. Walton 7 schemes + attack formation + explanation generator.
10. GraphRAG + Neo4j KG; SRQ2 retrieval configs A/B/C.
11. Evaluation: 6-dim metrics (F1 macro/micro, AUROC, ECE, Cohen's κ).
12. Baselines B1–B5 + ablations A1–A7 + paired Wilcoxon.
13. Streamlit UI (CXR + 3 modality panels + arg tree + confidence + disclaimer).
14. Model-selection benchmark harness.
15. Swap loaders → real MIMIC (after credentialing).

Each step: RED (failing test) → GREEN (impl) → REFACTOR. Modules small; LLM/VLM access mockable.

---

## 7. Setup Commands

```powershell
conda activate medargue                 # Python 3.12
pip install -r requirements-dev.txt      # core + dev tooling
python -m playwright install chromium     # E2E
# Local models via Ollama: meditron (installed), llama3.1:8b; LLaVA-Med + BioViL via HF (data/model cards)
ollama list
cp .env.example .env                     # fill keys / paths
```

---

## 8. Evaluation — Six Dimensions (dissertation pp.45–48)
1. **Clinical outcome** — multi-label F1 (macro/micro over 14 CheXpert labels), per-pathology AUROC.
2. **Explainability** — completeness, argumentation coverage, faithfulness (BLEU/ROUGE-L vs reference).
3. **Process transparency** — debate depth, attack rate, convergence quality, traceability.
4. **Trust** — Expected Calibration Error (ECE), uncertainty indication.
5. **Robustness** — evidence dropout (10/20/30%), paraphrase consistency.
6. **Cross-modal agreement** — discovery rate, unique-evidence contribution, Cohen's κ (Vision↔Report).

**Baselines B1–B5** (additive): B1 single LLM zero-shot (GPT-4o); B2 single LLM + vector RAG; B3
multi-agent no-argumentation; B4 existing system; B5 full system. **Ablations A1–A7**: no image RAG,
no symbolic layer, no modality partitioning, single agent, general LLM (Llama-3.1), no Vision, no
Clinical. Test set 400–600 MIMIC studies (stratified); paired Wilcoxon; qualitative 20-case study.

---

## 9. Datasets (focus = 5 of 14 CheXpert labels)
- **CheXpert 14 labels**; focus 5: Cardiomegaly, Pleural Effusion, Pneumonia, Pneumothorax, Atelectasis.
- Track 1 surrogates: NIH ChestX-ray14, OpenI Indiana, MIMIC-IV Demo (all open).
- Track 2 primary: MIMIC-CXR-JPG / MIMIC-IV-Note / MIMIC-IV (PhysioNet + CITI).

---

## 10. Guardrails
- Research prototype only, **not clinical advice** — label every model output.
- **No credentialed/real patient data** until PhysioNet + CITI + HW ethics approved; never commit PHI.
  Track-1 surrogates are open-licensed.
- Pin versions. Keep `BaseDatasetLoader` interface stable. Commit often, small PRs, tests green, one
  card = one PR.

---

## 11. Open implementation decisions (dissertation leaves these to the build — resolve per card, flag)
- Attack threshold: logical negation vs probabilistic disagreement.
- Convergence: argument-set equality vs stable attack relations.
- Confidence source: model softmax vs textual statement vs AAF voting.
- Agent ordering within a round; Walton labelling during vs post generation.
- GraphRAG corpus: external-only (guidelines + ontologies) vs +de-identified MIMIC text (leakage risk).
