# Roadmap Changelog — March 30, 2026

## Document: `dissertation_project_roadmap - Revised.md`

**Change Type:** Dataset Replacement (OIDP Single-Disease Pivot) + Architecture Alignment
**Trigger:** Adoption of the "One Issue, Different Perspectives" (OIDP) approach with single-disease datasets, replacing the original multi-disease/general-purpose datasets.

---

## Summary of Decisions Made

| Decision | Outcome | Rationale |
|----------|---------|-----------|
| **Agent count** | **3 + Supervisor** (not 6) | 6 agents produce 30 attack edges vs. 6 with 3 agents; ablation studies and evaluation become impractical within 25–50 page scope. Each agent absorbs 2 domain perspectives instead. 6-agent expansion documented as future work. |
| **Primary dataset** | **MI Complications (UCI #579)** replaces DDXPlus | Richest feature space (111 features, 17 domains), 12 complication targets, temporal structure, treatment data, genuine argumentation conflicts. Best fit for OIDP. |
| **Secondary datasets** | **CKD (UCI #336) + Heart Failure (UCI #519)** replace MedQA, PubMedQA, MedMCQA, MIMIC-IV, HealthSearchQA, LiveQA-Med | Old datasets were multi-disease QA tasks; new datasets are single-disease, tabular, anonymised — consistent OIDP framing across all three. |
| **Clinical Vignette Generator** | **Added** as new pipeline stage | All 3 new datasets are tabular. The NLP pipeline (scispaCy, GraphRAG, LLM agents) requires text input. Hybrid approach: deterministic templates + LLM narrative glue. |

---

## Changes by Section

### Section 3.1 — High-Level Data Flow
- **Added:** New `Clinical Vignette Generator` stage at the start of the pipeline (Tabular → Text), before Case Parser & Entity Extraction
- **Added:** Detailed subsection explaining the 3-component hybrid approach (Feature Decoder, Section Assembler, Narrative Smoother)
- **Added:** Example MI vignette conversion (raw CSV → clinical narrative)
- **Changed:** INPUT label from "Patient Case (symptoms, history, lab results)" to "Tabular Patient Record (CSV row from MI / CKD / HF dataset)"

### Section 3.2 — Agent Perspective Design
- **Changed:** Table from 4-column generic descriptions to 5-column MI-specific design with "MI-Specific Focus" and "Absorbed Domains" columns
- **Added:** Concrete MI-specific reasoning examples for each agent:
  - Conservative: temporal trajectory, missing prehospital BP, prior MI history
  - Aggressive: ECG QS-complex, fibrinolysis gaps, lidocaine/beta-blocker arguments
  - Evidence-Based: ESC 2023 STEMI guidelines, TIMI risk score, ZSN complication rates
- **Added:** "Design rationale — 3 agents + supervisor (not 6)" paragraph explaining why 6 was rejected and where it fits as future work

### Section 4 — Publicly Available Datasets (COMPLETE REWRITE)

#### 4.1 Primary Dataset
- **Removed:** Entire DDXPlus section (~45 lines) — dataset table, "Why DDXPlus is ideal" table, "How to use DDXPlus" numbered list
- **Added:** MI Complications (UCI #579) section with:
  - Full dataset attribute table (disease, source, DOI, citation, license, size, features, targets, temporal structure, treatment data, missing values, anonymisation)
  - 12-row target variables table with positive rates and argumentation relevance
  - "Why This Dataset Is Ideal for OIDP Argumentation" table (8 features)
  - "How to Use MI Complications for OIDP Argumentation" numbered list (5 steps, MI-specific)

#### 4.2 Secondary Datasets
- **Removed:** 6-row table of old datasets (MedQA, PubMedQA, MedMCQA, MIMIC-IV-Note, HealthSearchQA, LiveQA-Med)
- **Added:** 2-row table for CKD and Heart Failure with: disease, patients, features, target, license, source, DOI, purpose
- **Added:** Agent dynamics paragraphs for each secondary dataset (CKD: KDIGO guidelines, dietary vs. dialysis debate; HF: ejection fraction pivot, cardiorenal syndrome, ACC/AHA guidelines)

#### 4.3 Knowledge Sources for GraphRAG Indexing
- **Removed:** Generic sources (NICE, WHO, Wikidata Medical Subset)
- **Added:** Disease-specific guideline sources:
  - ESC 2023 STEMI/NSTEMI Guidelines (MI primary)
  - AHA MI Management Protocols (MI primary)
  - KDIGO Clinical Practice Guidelines (CKD secondary)
  - ACC/AHA/ESC Heart Failure Guidelines (HF secondary)
  - Golovenkin et al. (2020) original MI dataset paper
- **Kept:** PubMed Abstracts, DrugBank, PrimeKG
- **Added:** "Disease Relevance" column to table

#### 4.4 Dataset Ethics Compliance Summary
- **Removed:** DDXPlus / MedQA / PubMedQA / MIMIC-IV compliance table (with ⚠️ warnings for MIMIC-IV)
- **Added:** MI Complications / CKD / Heart Failure compliance table — all ✅ across all 7 requirements (publicly available, anonymised, open license, no human participants, no external approval, GDPR compliant, HWU Low Risk)

### Section 5.2 — Phase 1: Design, Step 1.6
- **Changed:** "Preprocessed DDXPlus + MedQA subsets" → "MI Complications preprocessed, Clinical Vignette Generator pipeline built, train/test split defined"

### Section 5.4 — Phase 3: Evaluate, Step 3.1
- **Changed:** "Quantitative evaluation on DDXPlus → Accuracy, F1, Explainability scores" → "Quantitative evaluation on MI Complications → Multi-label F1, Complication Recall, Explainability scores"

### Section 6.2 — Evaluation Metrics, Dimension 1
- **Renamed:** "Diagnostic Outcome Quality" → "Clinical Outcome Quality"
- **Removed:** Top-1 Accuracy, Top-3 Accuracy, DDx-Score, KL Divergence (all DDXPlus-specific ranked-list metrics)
- **Added:** 5 new MI-appropriate metrics:
  - Multi-label F1 (Macro) — average across 12 complications
  - Multi-label F1 (Micro) — global pooled
  - Per-Complication Recall — especially RAZRIV (100% fatal), LET_IS
  - Complication Co-occurrence Accuracy — multi-complication patients (17.4%)
  - Temporal Prediction Accuracy — F1 across T0/T1/T2/T3 prediction windows

### Section 6.3 — Evaluation Protocol
- **Changed:** Test set from "n=1,000 from DDXPlus" to "n=~340 held-out from MI Complications, stratified by complication profile"
- **Added:** Step 1: Clinical Vignette Generator conversion step
- **Added:** Step 6: Generalisability testing on CKD and Heart Failure
- **Added:** Qualitative note about highlighting protective-complication disagreement cases

### Section 7.1 — HWU Ethics Requirements
- **Changed:** Risk level description from "Using publicly available synthesized data only" → "Using publicly available anonymised clinical data (CC-BY 4.0) only"

### Section 7.2 — Ethics Form Strategy
- **Changed:** Argument #2 from DDXPlus-synthesized framing to "All three datasets are anonymised UCI ML Repository data with no patient identifiers, published under CC-BY 4.0"
- **Changed:** Argument #3 from MedQA/PubMedQA framing to "No new data is collected from human participants"

### Section 7.3 — Ethics Form Section Mapping
- **Changed:** Data Sources from "DDXPlus (CC-BY, synthesized), MedQA (open), PubMedQA (MIT)" → "MI Complications (CC-BY 4.0, UCI #579), CKD (CC-BY 4.0, UCI #336), Heart Failure (CC-BY 4.0, UCI #519) — all anonymised, pre-existing"

### Section 8 — SOTA Comparison Table
- **Changed:** Proposed System dataset column from "DDXPlus + MedQA" → "MI Complications + CKD + HF"

### Section 9 — Project Timeline, W9–10
- **Changed:** "DDXPlus preprocessed, 1000-case test set defined" → "MI Complications preprocessed, Clinical Vignette Generator built, train/test split defined"

### Section 11 — Risk Mitigation
- **Changed:** Scope creep row from "Fixed scope: DDXPlus primary, 3 agents, 5 metrics" → "Fixed scope: MI Complications primary, 3 agents + supervisor, 5 metric dimensions. CKD/Heart Failure for generalisability"

### Section 12 — References
- **Removed:** Tchango et al. (2022) — DDXPlus paper (reference #9)
- **Added:** Golovenkin et al. (2020) — MI Complications dataset paper (reference #9)
- **Added:** Chicco & Jurman (2020) — Heart Failure dataset paper (reference #10)
- **Renumbered:** Edge et al. (2024) is now reference #11

### Appendix B — System Prompt Templates
- **Changed:** All 3 agent prompts from generic medical to MI-specific:
  - Conservative: Now references temporal Day 1→2→3 trends, prior MI history, missing prehospital BP uncertainty, comorbidity burden
  - Aggressive: Now references ECG QS-complex interpretation, fibrinolysis/PCI escalation, lidocaine/beta-blockers, myocardial rupture urgency
  - Evidence-Based: Now references ESC 2023 STEMI guidelines, TIMI risk score, GDMT protocols, Level A/B evidence, ZSN complication statistics
- **Added:** "Perspective domains" line to each prompt clarifying which clinical domains are absorbed

### Appendix C — Project Directory Structure
- **Removed:** `data/ddxplus/` with 4 DDXPlus-specific files
- **Removed:** `data/medqa/`
- **Added:** `data/mi_complications/` with `raw/`, `processed/`, `vignettes/` subdirectories
- **Added:** `data/ckd/` and `data/heart_failure/`
- **Changed:** `knowledge/` comment from "Clinical guidelines PDFs" → "ESC/AHA/KDIGO guidelines PDFs"
- **Changed:** `data_loader.py` comment from "DDXPlus data loading" → "MI/CKD/HF dataset loading (ucimlrepo)"
- **Added:** `vignette_generator.py` — Clinical Vignette Generator module

### Footer
- **Changed:** "Last updated: February 2026" → "Last updated: March 30, 2026"
- **Added:** "dataset fitness report" to the "Based on" list

---

## Sections NOT Changed (confirmed reviewed, no dataset references)

| Section | Reason No Change Needed |
|---------|------------------------|
| 1. Research Questions | Already updated in prior revision (generic RQ, RAG-version SRQ2, removed SRQ5) |
| 2. SOTA Technology Stack | Technology choices are dataset-independent |
| 3.3 LangGraph State Machine | Code is dataset-agnostic |
| 5.1 Research Design | Design Science methodology unchanged |
| 5.3 Phase 2: Implement | Activities are component-based, not dataset-specific |
| 5.5 Experimental Design (Baselines & Ablations) | Baselines and ablations are methodology-level, not dataset-specific |
| 6.2 Dimensions 2–5 | Explainability, Process, Trust, Robustness metrics are dataset-independent |
| 10. Report Structure | Chapter outline unchanged |
| Appendix A items A1, A4–A18 | Not dataset-specific |

---

---

## Change Set 2: Agent Redesign — Direction 1 (Information Partitioning)

**Change Type:** Agent Architecture Redesign + Experimental Design Overhaul
**Trigger:** Supervisor feedback (Radu Mihailescu): *"We need to think deeper about the different agent roles based on a specific experimental setup."*
**Decision:** Direction 1 — Information Partitioning (clinical MDT model). Agents are defined by which subset of the 111 MI features they can see, not by attitudinal tone.

---

### Summary of Decisions Made

| Decision | Outcome | Rationale |
|----------|---------|-----------|
| **Agent differentiation mechanism** | **Information Partitioning** (not attitudinal prompts) | Each agent sees only its clinical domain's features. Like a real MDT: the cardiologist doesn't see the pharmacist's notes and vice versa. Creates genuine information asymmetry that drives meaningful debate. |
| **3 domain-specialist agents** | **History & Risk (~37 features), Diagnostic (~46 features), Treatment & Progression (~28 features)** | Maps to the 17 clinical domains in the dataset fitness report. Each agent has a coherent clinical scope. |
| **SRQ2 answering mechanism** | **Infrastructure Sweep** (same agents × 3 retrieval backends) | Swap Vector RAG / GraphRAG / Hybrid while keeping agents fixed. The unit of analysis is the whole system's collective output, not individual agents. Cleanly isolates the RAG variable. |
| **Ablation A3 redesign** | **"No Information Partitioning"** replaces "No Perspective Diversity (same prompt)" | Tests whether information asymmetry (the core architectural contribution) actually drives meaningful debate. Much more architecturally significant than the old "same prompt" test. |

---

### Changes by Section

#### Section 1 — Research Questions (SRQ3)
- **Changed:** SRQ3 wording from "different medical perspectives (e.g., conservative vs. aggressive treatment)" → "different medical domain perspectives (e.g., history vs. diagnostics vs. treatment), modelled as information-partitioned agents"

#### Section 2.1 — Architecture Pattern (ASCII Diagram)
- **Changed:** 3 agent labels from Conservative/Aggressive/Evidence-Based → History & Risk / Diagnostic / Treatment & Progression
- **Changed:** Agent descriptions from attitudinal (Perspective/Treatment/Based) → domain-based (History & Risk / Diagnostics / Treatment & Progression)

#### Section 2.6 — Complete Tech Stack Summary (Orchestration Layer)
- **Changed:** 3 agent labels and descriptions from attitudinal to domain-specialist:
  - "Conservative Agent (Risk-averse perspective)" → "History & Risk Agent (Patient history, comorbidities)"
  - "Aggressive Agent (Intervention-focused perspective)" → "Diagnostic Agent (ECG, labs, vitals)"
  - "Evidence-Based Agent (Guidelines-focused)" → "Treatment & Progression Agent (Medications, temporal trends)"

#### Section 3.1 — High-Level Data Flow
- **Added:** Feature Partitioner step between Clinical Vignette Generator and Case Parser
- **Changed:** Agent labels from (Cons.) / (Aggr.) / (Evid.) → (Hist.) / (Diag.) / (Treat.)
- **Changed:** Agent description from "Each with unique system prompt + perspective-specific KG context" → "Each sees only its feature partition + domain-specific KG context"

#### Section 3.2 — Agent Perspective Design (COMPLETE REWRITE)
- **Removed:** Entire 5-column attitudinal agent table (Conservative/Aggressive/Evidence-Based with "Absorbed Domains" column)
- **Removed:** "Design rationale — 3 agents + supervisor (not 6)" paragraph about absorbing domain perspectives
- **Added:** New "Information Partitioning" framing — agents defined by feature subsets, not attitudinal tone
- **Added:** 3-agent table with Domain, Feature Partition (17-domain mapping), # Features, Clinical Role, KG Retrieval Scope
- **Added:** Feature partition table mapping all 17 clinical domains to their assigned agent
- **Added:** "Design rationale — Information Partitioning (not attitudinal prompts)" paragraph explaining MDT analogy and why this is better
- **Added:** "Why 3 partitions (not 6)" paragraph preserving the tractability argument

#### Section 3.3 — LangGraph State Machine
- **Added:** `feature_partitions: dict` to `DebateState` TypedDict
- **Changed:** Node names from `agent_conservative/agent_aggressive/agent_evidence` → `agent_history_risk/agent_diagnostic/agent_treatment`
- **Changed:** Function names accordingly
- **Changed:** Conditional edge fallback target from `agent_conservative` → `agent_history_risk`

#### Section 4.1 — How to Use MI Complications for OIDP (Step 3)
- **Changed:** Agent perspective descriptions:
  - "Conservative Agent: Focuses on patient history, temporal trends, monitoring strategy" → "History & Risk Agent: Sees only demographics, prior MI history, arrhythmia/conduction history, comorbidities, vital signs (~37 features)"
  - "Aggressive Agent: Focuses on ECG abnormalities, pharmacological intervention gaps" → "Diagnostic Agent: Sees only ECG findings, MI location, admission status, lab results (~46 features)"
  - "Evidence-Based Agent: Applies ESC 2023 STEMI guidelines..." → "Treatment & Progression Agent: Sees only ICU medications, fibrinolytic therapy, pain/opioid/NSAID temporal trends (~28 features)"

#### Section 4.2 — Secondary Dataset Agent Dynamics
- **Changed:** CKD dynamics from attitudinal framing (Conservative/Aggressive/Evidence-Based) → domain-partitioned framing (History & Risk / Diagnostic / Treatment & Progression agents seeing different CKD feature subsets)
- **Changed:** Heart Failure dynamics similarly updated to domain-partitioned framing

#### Section 5.5 — Experimental Design (MAJOR REWRITE)
- **Added:** New "Infrastructure Sweep" section before Baselines — Run A (Vector RAG), Run B (GraphRAG), Run C (Hybrid). Same 3 domain agents, only retrieval backend changes. Directly answers SRQ2.
- **Changed:** Ablation A3 from "No Perspective Diversity — All agents have same system prompt — Multi-perspective contribution" → "No Information Partitioning — All agents see all 111 features (remove feature masks) — Information asymmetry contribution"

#### Section 6.2 — Evaluation Metrics
- **Added:** Dimension 6: Information Fusion Quality — new metric dimension testing whether agents with partial information produce better collective outcomes than agents with full information. Metrics: Cross-Domain Discovery Rate, Unique Evidence Contribution, Partition Complementarity.

#### Section 8 — Research Gaps Addressed
- **Changed:** Last gap from "Designed perspectives (conservative/aggressive/evidence-based)" → "Information-partitioned domain agents (history/diagnostics/treatment) mirroring clinical MDT structure"

#### Section 11 — Risk Mitigation (Scope Creep Row)
- **Changed:** From "3 agents + supervisor" → "3 information-partitioned domain agents + supervisor"

#### Appendix A — Implementation Checklist
- **Changed:** A7 from "Write system prompts for 3 agent perspectives + supervisor" → "Define feature partitions and write system prompts for 3 domain agents + supervisor"
- **Added:** A6b: "Implement Feature Partitioner module (feature masks per agent)"

#### Appendix B — System Prompt Templates (COMPLETE REWRITE)
- **Removed:** Conservative Agent, Aggressive Treatment Agent, Evidence-Based Agent (all 3 attitudinal prompts)
- **Added:** History & Risk-Factor Agent prompt — defines visible features (Patient History, Arrhythmia History, Conduction History, Comorbidities, Vital Signs), explicitly states which data is NOT visible
- **Added:** Diagnostic Agent prompt — defines visible features (Admission Status, ECG MI Location, ECG Rhythm, ECG Arrhythmia, ECG Conduction, Lab Results), explicitly states which data is NOT visible
- **Added:** Treatment & Progression Agent prompt — defines visible features (Fibrinolytic Therapy, Pre-hospital Treatment, ICU Treatment, Pain Recurrence, Opioids ICU, NSAIDs ICU), explicitly states which data is NOT visible

#### Appendix C — Project Directory Structure
- **Changed:** Agent filenames from `conservative.py / aggressive.py / evidence_based.py` → `history_risk.py / diagnostic.py / treatment_progression.py`
- **Changed:** File comments accordingly
- **Added:** `feature_partitioner.py` to `src/utils/` — Feature Partitioner module

#### Footer
- **Changed:** "Based on:" list — added "supervisor feedback on agent roles"

---

### Sections NOT Changed (confirmed reviewed)

| Section | Reason No Change Needed |
|---------|------------------------|
| 2.2–2.5 SOTA Technology Stack | Technology choices are agent-design-independent |
| 3.1 Clinical Vignette Generator subsection | Template/decoder approach unchanged |
| 4.3 Knowledge Sources | KG sources unchanged |
| 4.4 Dataset Ethics Compliance | Ethics status unchanged |
| 5.1–5.4 Methodology phases | Phase structure unchanged |
| 6.2 Dimensions 2–5 | Explainability/Process/Trust/Robustness metrics unchanged |
| 6.3 Evaluation Protocol | Protocol steps unchanged |
| 7. Ethics Compliance Plan | Ethics unchanged |
| 9. Timeline & Milestones | Schedule unchanged |
| 10. Report Structure | Chapter outline unchanged |
| 12. References | No new papers needed |

---

---

# Roadmap Changelog — April 6, 2026

## Document: `dissertation_project_roadmap - Revised- MIMIC.md` (NEW FILE)

**Change Type:** Full MIMIC Multimodal Pivot — new roadmap version, literature expansion, writing prompt update, supervisor presentation
**Trigger:** Supervisor (Dr Radu-Casian Mihailescu) recommended pivoting from MI Complications (UCI #579, tabular-only) to the MIMIC ecosystem (CXR images + radiology reports + structured EHR) to enable genuinely multimodal argumentation with Vision Language Models. User confirmed full pivot with Arrangement A (Modality-Based Partitioning).

---

## Files Created / Updated

| File | Action | Description |
|------|--------|-------------|
| `dissertation_project_roadmap - Revised- MIMIC.md` | **CREATED** (1,306 lines) | Complete MIMIC-updated project roadmap — all 12 sections + 3 appendices rewritten |
| `research_papers_literature_review.md` | **UPDATED** (1,799 lines) | Expanded from 35 → 53 papers, 10 → 14 categories, added C11/C12 coverage matrix columns |
| `best_practice_writing_prompt_MIMIC.md` | **CREATED** (584 lines) | AI writing assistant prompt updated for MIMIC context — all 8 sections revised |
| `Research_Paper/MIMIC_Feasibility_Study.md` | **CREATED prior** (997 lines) | Feasibility analysis — motivation, dataset comparison, hardware constraints, dual-track strategy |
| `Research_Paper/new_references_mimic_vlm.md` | **CREATED prior** (437 lines) | 19 new reference papers for MIMIC/VLM/multimodal categories |
| `MIMIC_Pivot_Supervisor_Update_April2026.pptx` | **CREATED** (28 slides) | 20-minute professional supervisor presentation covering the full MIMIC pivot |
| `MIMIC_Pivot_Supervisor_Update_April2026.pdf` | **CREATED** (PDF export) | PDF version of the supervisor presentation |

**Files preserved unchanged:** `dissertation_project_roadmap - Revised.md` (original MI version), `best_practice_writing_prompt.md` (original writing prompt)

---

## Summary of Decisions Made (April 6, 2026)

| Decision | Outcome | Rationale |
|----------|---------|-----------|
| **Dataset pivot** | **MIMIC ecosystem** replaces MI Complications (UCI #579) | MI dataset is tabular-only (single modality); MIMIC offers genuinely multimodal data — CXR images + radiology reports + structured EHR — enabling real information asymmetry between agents |
| **Architecture** | **Arrangement A: Modality-Based Partitioning** | Each agent processes a fundamentally different data modality (pixels / free text / structured tables). Mirrors real clinical MDT workflow. Stronger than feature masking |
| **Agent design** | **Vision / Report / Clinical + Supervisor** | Vision Agent (BioViL + LLaVA-Med) sees CXR images; Report Agent (Meditron-8B) sees radiology reports; Clinical Agent (Meditron-8B) sees structured EHR; Supervisor orchestrates debate |
| **VLM stack** | **BioViL** (image embeddings) + **LLaVA-Med 7B** (image interpretation) | BioViL replaces BiomedCLIP (ECCV 2022, CLIP-pretrained on CXR, ~400M params, ~2 GB VRAM). LLaVA-Med 7B for CXR-to-text (4-bit ~4–5 GB). CheXagent removed (too large, restricted license) |
| **Development strategy** | **Dual-track** (surrogates + PhysioNet credentialing in parallel) | Track 1 builds full pipeline on open surrogates (NIH CXR14, OpenI, MIMIC-IV Demo); Track 2 obtains credentials. Merge at ~Week 16. Project never blocked |
| **Subset strategy** | **2,000–3,000 frontal CXR studies** (~2–3 GB) | Filter metadata CSV → frontal views → 5–6 CheXpert pathologies → stratified sample → selective download. Full MIMIC-CXR (570 GB) not needed |
| **Evaluation** | **6 dimensions** expanded with Dimension 6 (Cross-Modal Agreement + VLM Faithfulness) | New metrics: cross-modal discovery rate, unique evidence contribution, modality complementarity, VLM faithfulness vs CheXpert ground truth |
| **Papers** | **53 papers total** (19 new, 1 removed) across **14 categories** | Added Cat 10 (MIMIC Datasets), Cat 11 (VLMs), Cat 12 (Multimodal Fusion), Cat 13 (Report Generation), Cat 14 (CLIP-Based Retrieval). Removed Golovenkin (MI dataset paper) |

---

## Changes by Section — Roadmap (`dissertation_project_roadmap - Revised- MIMIC.md`)

### Section 1 — Research Questions
- **Changed:** SRQ3 from feature-based partitioning to "How does modality-based information partitioning (images vs. reports vs. structured EHR) affect diagnostic outcomes compared to single-agent access to all modalities?"
- **Unchanged:** RQ, SRQ1, SRQ2, SRQ4 remain as previously revised

### Section 2 — SOTA Technology Stack (MAJOR REWRITE)
- **Added:** BioViL (ECCV 2022) — CLIP backbone for Image RAG (~400M params, ~2 GB VRAM)
- **Added:** LLaVA-Med 7B (NeurIPS 2023) — Primary VLM for Vision Agent (4-bit ~4–5 GB VRAM)
- **Added:** MedCLIP (EMNLP 2022) as backup VLM candidate
- **Removed:** BiomedCLIP (replaced by BioViL — better CXR-specific pretraining)
- **Removed:** CheXagent (14B params too large for 8 GB VRAM, restricted license)
- **Changed:** Meditron-7B → Meditron-8B (4-bit GGUF, ~5 GB VRAM) as primary text LLM
- **Added:** Complete tech stack architecture diagram (ASCII)
- **Added:** VRAM budget analysis showing sequential inference fits in 8 GB
- **Renumbered:** Papers from 21 → 19 total in stack table

### Section 3 — System Architecture (COMPLETE REWRITE)
- **Replaced:** Feature-based agent perspective table with modality-based design
- **Added:** 3 new complete agent pipeline descriptions:
  - Vision Agent: CXR JPG → BioViL embeddings → CLIP Image RAG → LLaVA-Med 7B → text arguments
  - Report Agent: Radiology report → section extraction → Meditron-8B → text arguments
  - Clinical Agent: MIMIC-IV structured data → deterministic serialisation → Meditron-8B → text arguments
- **Added:** 4 cross-modal conflict scenarios table (bilateral opacities, PE+HF, subtle PTX, isolated finding)
- **Added:** Key architectural insight: all agents produce text arguments; symbolic layer operates in text domain; images never enter debate directly
- **Updated:** LangGraph DebateState code to include `image_findings`, `report_findings`, `clinical_findings` typed fields

### Section 4 — Datasets (COMPLETE REWRITE)

#### 4.1 Primary Datasets
- **Removed:** MI Complications (UCI #579) — entire section
- **Added:** MIMIC-CXR-JPG v2.1.0 — 377,110 CXR JPGs, 14 CheXpert labels, 64,588 patients
- **Added:** MIMIC-IV-Note v2.2 — 2.3M radiology reports + 331K discharge summaries
- **Added:** MIMIC-IV v3.1 — structured EHR (labs, meds, diagnoses, vitals, procedures), 364K patients
- **Added:** Cross-dataset linkage description via `subject_id`
- **Added:** 7-step subset strategy pipeline (metadata filter → frontal views → pathology filter → stratified sample → selective download)

#### 4.2 Surrogate Datasets (NEW)
- **Added:** NIH ChestX-ray14 (112K CXRs, 14 labels, CC0) — Vision Agent surrogate
- **Added:** OpenI Indiana CXR (7,470 report/image pairs) — Report Agent surrogate
- **Added:** MIMIC-IV Demo (100 patients, ODbL) — Clinical Agent surrogate
- **Added:** PadChest (160K CXRs, Spanish) as optional alternative

#### 4.3 Knowledge Sources
- **Removed:** ESC STEMI/NSTEMI, AHA MI Management, KDIGO, ACC/AHA HF
- **Added:** ACR Appropriateness Criteria, Fleischner Society Guidelines, BTS Pleural Disease Guidelines, STR Thoracic Imaging Resources, CheXpert labelling paper

#### 4.4 Ethics Compliance
- **Changed:** All-green (✅) table to mixed: MIMIC datasets = ⚠️ (PhysioNet credential required); surrogates = ✅

### Section 5 — Methodology (MAJOR REWRITE)
- **Added:** Dual-track phasing: Track 1 (surrogates, immediate) + Track 2 (PhysioNet credentialing, parallel)
- **Changed:** Phase 1 to include CITI training + PhysioNet application
- **Changed:** Phase 2 to include surrogate pipeline first, then MIMIC swap
- **Changed:** Phase 3 evaluation to MIMIC-specific protocol
- **Added:** Infrastructure sweep answers SRQ2: Run A (Vector RAG), Run B (GraphRAG), Run C (Multimodal Hybrid — text + graph + CLIP image RAG)
- **Updated:** Baselines B1–B5 descriptions for multimodal context
- **Updated:** Ablations A1–A7 with new entries: A1 (No Image RAG), A6 (No Vision Agent), A7 (No Clinical Agent)

### Section 6 — Evaluation Framework (EXPANDED)
- **Changed:** Dimension 1 metrics from MI-specific (multi-label F1 for 12 complications) to CheXpert 14-label classification + cross-modal agreement (Cohen's κ)
- **Added:** Dimension 6 — Cross-Modal Agreement & VLM Faithfulness (new):
  - Cross-modal discovery rate (conflicts surfaced and resolved)
  - Unique evidence contribution per modality
  - Modality complementarity score
  - VLM faithfulness vs CheXpert ground truth (CXR-specific metric)
- **Changed:** Evaluation protocol from n ≈ 340 MI patients to n ≈ 400–600 MIMIC studies, stratified by pathology
- **Added:** 20 qualitative case studies for argumentation depth analysis

### Section 7 — Ethics Compliance Plan (REWRITE)
- **Changed:** Risk level from LOW to MEDIUM
- **Added:** PhysioNet Credentialed Health Data License 1.5.0 requirements (CITI training, signed DUA, no re-identification, aggregate reporting, local encrypted storage)
- **Added:** Two-phase ethics strategy: initial ethics for surrogates (low risk), then amendment for MIMIC DUA (medium risk)
- **Removed:** All-green UCI/CC-BY-4.0 framing

### Section 8 — SOTA Comparison Table
- **Changed:** Proposed System from "MI Complications + CKD + HF" to "MIMIC-CXR + MIMIC-IV-Note + MIMIC-IV"
- **Added:** VLM column (✅ BioViL + LLaVA-Med) — no other system has this
- **Updated:** Evaluation dimensions from 5 to 6

### Section 9 — Timeline (MAJOR REWRITE)
- **Replaced:** Linear single-track Gantt with dual-track Gantt chart
- **Added:** Track 1 milestones (surrogate builds) and Track 2 milestones (credentialing)
- **Added:** Merge point at ~Week 16 (June 2026)
- **Updated:** All 8 supervisor checkpoints (CP1–CP8) with MIMIC-specific focus areas
- **Added:** Fallback note: if credentials delayed beyond W16, evaluate fully on surrogates

### Section 10 — Report Structure
- **Changed:** Page estimate from 36–54 pages to reflect MIMIC content
- **Updated:** Chapter descriptions for MIMIC ecosystem context

### Section 11 — Risk Mitigation (EXPANDED)
- **Added:** PhysioNet credentialing delay as #1 risk (HIGH impact, medium likelihood) with dual-track mitigation
- **Added:** VLM VRAM overflow risk with 4-bit quantisation + sequential inference mitigation
- **Updated:** Scope creep to "Fixed scope: 3 agents, MIMIC subset, 6 metrics"

### Section 12 — References (UPDATED)
- **Removed:** Golovenkin et al. (2020) — MI dataset paper
- **Removed:** Chicco & Jurman (2020) — Heart Failure dataset paper
- **Added:** Johnson et al. (2019) — MIMIC-CXR paper
- **Added:** Johnson et al. (2024) — MIMIC-IV v3.1 paper
- **Added:** Boecking et al. (2022) — BioViL paper
- **Added:** Li et al. (2023) — LLaVA-Med paper
- **Renumbered:** All references (19 total)

### Appendix B — System Prompt Templates
- **Replaced:** MI-specific Conservative/Aggressive/Evidence-Based prompts with modality-specific prompts:
  - Vision Agent: CXR findings, spatial anatomy, radiodensity, comparison with priors
  - Report Agent: Radiology report interpretation, section-level evidence, hedging language
  - Clinical Agent: Structured EHR data, lab trends, medication context, comorbidities
  - Supervisor: Cross-modal integration, conflict resolution, argumentation orchestration

### Appendix C — Project Directory Structure
- **Replaced:** `data/mi_complications/`, `data/ckd/`, `data/heart_failure/` with:
  - `data/mimic_cxr/` with `raw/`, `processed/`, `embeddings/`
  - `data/mimic_iv_note/` with `raw/`, `processed/`
  - `data/mimic_iv/` with `raw/`, `processed/`
  - `data/surrogates/nih_cxr14/`, `data/surrogates/openi/`, `data/surrogates/mimic_iv_demo/`
- **Removed:** `vignette_generator.py` (no longer needed — MIMIC provides natural text)
- **Added:** `image_rag.py`, `vlm_pipeline.py`, `vision_agent.py`

---

## Changes to Literature Review (`research_papers_literature_review.md`)

### Papers Added (19 new → 53 total)
| # | Paper | Category |
|---|-------|----------|
| 35 | Johnson et al. (2019) — MIMIC-CXR | Cat 10: MIMIC Datasets |
| 36 | Johnson et al. (2023) — MIMIC-CXR-JPG | Cat 10 |
| 37 | Johnson et al. (2023) — MIMIC-IV | Cat 10 |
| 38 | Johnson et al. (2023) — MIMIC-IV-Note | Cat 10 |
| 39 | Irvin et al. (2019) — CheXpert | Cat 10 |
| 40 | Li et al. (2023) — LLaVA-Med | Cat 11: VLMs |
| 41 | Wang et al. (2022) — MedCLIP | Cat 11 |
| 42 | Moor et al. (2023) — Foundation Models for Healthcare | Cat 11 |
| 43 | Acosta et al. (2022) — Multimodal Biomedical AI | Cat 12: Multimodal Fusion |
| 44 | Kline et al. (2022) — Imaging + EHR Fusion | Cat 12 |
| 45 | Lipkova et al. (2022) — AI for Multimodal Data | Cat 12 |
| 46 | Chen et al. (2020) — R2Gen | Cat 13: Report Generation |
| 47 | Smit et al. (2020) — CheXbert | Cat 13 |
| 48 | Zhang et al. (2020) — Factual Completeness | Cat 13 |
| 49 | Radford et al. (2021) — CLIP | Cat 14: CLIP-Based Retrieval |
| 50 | Huang et al. (2021) — GLoRIA | Cat 14 |
| 51 | Tiu et al. (2022) — CheXzero | Cat 14 |
| 52 | Zhang et al. (2022) — ConVIRT | Cat 14 |
| 53 | Boecking et al. (2022) — BioViL | Cat 14 |

### Paper Removed (1)
- #35 Golovenkin et al. (2020) — MI Complications dataset paper (no longer relevant)

### Coverage Matrix Expanded
- **Added:** Component C11 (Vision Language Models) and C12 (Multimodal Data Fusion)
- **Updated:** Matrix from C1–C10 to C1–C12 for all 53 papers

---

## Changes to Writing Prompt (`best_practice_writing_prompt_MIMIC.md`)

- **Section 1 (Referencing):** Updated research paper filenames and roadmap file references
- **Section 2 (Roadmap Reference):** Changed filename to `dissertation_project_roadmap - Revised- MIMIC.md`
- **Section 3 (Lit Review Reference):** Changed to 53 papers, 14 categories, C1–C12 matrix
- **Section 4 (Chapter Guidance):** Updated all chapters (0–7) for MIMIC context — dataset descriptions, architecture, VLM stack, evaluation, ethics
- **Section 5 (Quality Checklist):** Updated dataset, architecture, model references
- **Section 6 (Project Facts):** Updated dataset, architecture, agent names, model stack, timeline dates
- **Section 7 (Glossary):** Added 12 new terms (MIMIC-CXR-JPG, MIMIC-IV-Note, BioViL, LLaVA-Med, CheXpert, PhysioNet DUA, CLIP, Image RAG, etc.)

---

## Supervisor Presentation Created

- **File:** `MIMIC_Pivot_Supervisor_Update_April2026.pptx` (28 slides, ~79 KB)
- **PDF:** `MIMIC_Pivot_Supervisor_Update_April2026.pdf` (~363 KB)
- **Duration:** ~20 minutes
- **Structure:** 8 sections with section dividers — Motivation, MIMIC Ecosystem, Architecture, Dual-Track Development, Evaluation, Literature & Ethics, Timeline, Next Steps
- **Design:** Navy/white/accent-blue professional theme, consistent headers, colour-coded tables, slide numbering
- **Includes:** 5 supervisor discussion questions, risk mitigation table, SOTA comparison, Gantt chart

---

## Sections NOT Changed (confirmed reviewed)

| Section | Reason No Change Needed |
|---------|------------------------|
| RQ, SRQ1, SRQ2, SRQ4 | Already updated in prior revisions; only SRQ3 changed for modality wording |
| 3.3 LangGraph State Machine | Code is dataset-agnostic (fields updated but structure unchanged) |
| 5.1 Research Design | Design Science methodology unchanged |
| 6.2 Dimensions 2–5 | Explainability, Process, Trust, Robustness metrics are dataset-independent |

---

---

# Roadmap Changelog — April 12, 2026

## Trigger: Supervisor Feedback on Model Selection

**Feedback (Dr Mihailescu, April 12):** *"On the VLM/LLM side, it would be worth experimenting with a small set of candidate models (e.g., 1–3) through some initial benchmarking before settling on the one to use for the final experiments."*

**Impact:** Minor — affects methodology wording & implementation sequencing, not research questions, architecture, or evaluation framework.

---

## Changes Made

### `dissertation_project_roadmap - Revised- MIMIC.md`

| Section | Change |
|---------|--------|
| **§2 Recommended Strategy** | Reframed from "Use Meditron/BioViL/LLaVA-Med as primary" to **"candidate set"** with explicit benchmarking caveat. Added bullet: "Evidence-based model selection (per supervisor recommendation)". Listed candidate pairs: Meditron-8B vs Llama-3.1-8B, BioViL vs MedCLIP, LLaVA-Med 7B vs LLaVA-v1.5-7B |
| **§2.4a BioViL justification** | Changed "BioViL is selected because…" to "BioViL is the leading candidate because…" with note that final selection depends on benchmark (§5.3, Step 2.1) |
| **§5.3 Phase 2, Track 1** | Inserted new **Step 2.1 — Model Selection Benchmark**: compare 1–3 candidates per role on ~100–200 surrogate studies, evaluate on F1/latency/VRAM, produce model selection report. All subsequent steps renumbered (2.2→2.3 through 2.8→2.9; Track 2 steps 2.9→2.10 through 2.12→2.13) |
| **§5.5 Experimental Design** | Added note after infrastructure sweep paragraph: "All infrastructure sweep runs use the models selected during the preliminary model selection benchmark (Step 2.1)" |
| **§9 Timeline** | Inserted **W9** milestone: "Model Selection Benchmark — Compare candidate LLMs/VLMs on ~100–200 surrogate studies; select winners". Surrogate data preparation shifted to start at W9 (overlapping) |

### `best_practice_writing_prompt_MIMIC.md`

| Section | Change |
|---------|--------|
| **§4 Chapter 4.3 (System Architecture)** | Added bullet: "Model Selection Benchmark (per supervisor recommendation): Preliminary benchmarking of 1–3 candidate models per role…" between agent description and modality rationale |
| **§4 Chapter 7 (Implementation)** | Inserted new item #2: "Model Selection Benchmark: Describe the preliminary benchmarking process — candidate models tested, surrogate dataset, metrics, results table, justification." Subsequent items renumbered (2→3 through 9→10) |

---

## Sections NOT Changed (confirmed reviewed)

| Section | Reason |
|---------|--------|
| Research Questions (RQ, SRQ1–4) | Model selection does not affect research questions |
| System Architecture (§3) | Architecture is model-agnostic — agents are defined by role, not by specific model |
| Datasets (§4) | No dataset changes |
| Evaluation Framework (§6) | Metrics are model-independent |
| Ethics (§7) | No impact |
| Literature Review | No new papers needed — candidates already cited |
| PPTX/PDF | Already sent to supervisor — not retroactively updated |

---

*Changelog updated: April 12, 2026*
*For: Chaouki Ouadah (H00498420) — MSc AI/Data Science, Heriot-Watt University Dubai*
