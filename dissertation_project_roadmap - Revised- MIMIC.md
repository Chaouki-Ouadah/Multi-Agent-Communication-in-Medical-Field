# Complete Dissertation Project Roadmap (MIMIC Pivot)

## Multi-Agent Argumentation Frameworks with LLM-Augmented Reasoning in Healthcare Systems

**Degree:** MSc in AI/Data Science — Heriot-Watt University
**Supervisor:** Radu-Casian Mihailescu
**Deliverables:** 25–50 page report + Python-based prototype
**Timeline:** February 2026 – August 2026
**Dataset:** MIMIC Ecosystem (MIMIC-CXR-JPG + MIMIC-IV-Note + MIMIC-IV)
**Architecture:** Modality-Based Information Partitioning (Vision / Report / Clinical / Supervisor)

---

## Table of Contents

1. [Research Questions](#1-research-questions)
2. [State-of-the-Art Technology Stack](#2-state-of-the-art-technology-stack)
3. [System Architecture](#3-system-architecture)
4. [Publicly Available Datasets](#4-publicly-available-datasets)
5. [Methodology](#5-methodology)
6. [Evaluation Framework](#6-evaluation-framework)
7. [Ethics Compliance Plan](#7-ethics-compliance-plan)
8. [SOTA Comparison Table](#8-sota-comparison-table)
9. [Project Timeline & Milestones](#9-project-timeline--milestones)
10. [Report Structure](#10-report-structure)
11. [Risk Mitigation](#11-risk-mitigation)
12. [References & Resources](#12-references--resources)

---

## 1. Research Questions

### Primary Research Question (RQ)

> **How can multi-agent argumentation frameworks, augmented by Large Language Models and Retrieval-Augmented Generation, improve the explainability and trustworthiness of clinical decision support systems?**

### Sub-Research Questions

| ID | Sub-Question | Maps To Components |
|----|-------------|-------------------|
| **SRQ1** | How can formal argumentation schemes (e.g., Walton's schemes) be integrated with LLM-driven agent debate to produce clinically meaningful explanations? | C4, C5, C6 |
| **SRQ2** | How do different Retrieval-Augmented Generation approaches affect the factual grounding and consistency of multi-agent clinical reasoning? | C8, C2, C3 |
| **SRQ3** | How do different clinical data modalities (chest X-ray images, radiology reports, structured EHR), modelled as modality-partitioned agents, affect diagnostic differential outcomes? | C1, C3, C7 |
| **SRQ4** | What evaluation metrics beyond accuracy (explainability, process transparency, trust) are most effective for assessing argumentation-based clinical decision support? | C6, C9, C7 |

---

## 2. State-of-the-Art Technology Stack

### 2.1 Multi-Agent Orchestration Framework

#### Primary: LangGraph (v1.0+)

| Attribute | Details |
|-----------|---------|
| **Repository** | [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) — 24.9k stars, 466 releases |
| **Version** | v1.0.9 (latest stable, July 2025) |
| **Why SOTA** | Low-level graph-based orchestration with durable execution, native HITL interrupts, persistent memory, LangSmith debugging |
| **Key Features** | Stateful agents as graph nodes, conditional edges for argumentation flow, checkpoint/resume, streaming support |
| **Install** | `pip install -U langgraph` |
| **License** | MIT |

**Why LangGraph over alternatives:**

| Framework | Stars | Strengths | Weakness for This Project |
|-----------|-------|-----------|--------------------------|
| **LangGraph** ✅ | 24.9k | Graph-based control flow, HITL native, durable execution, fine-grained state | Requires more code than higher-level frameworks |
| AutoGen (Microsoft) | 40k+ | Easy multi-agent conversations | Less control over argumentation flow, opaque turn-taking |
| CrewAI | 27k+ | Simple role-based agents | Too high-level for structured argumentation, no graph control |
| Swarm (OpenAI) | 20k+ | Lightweight handoffs | Experimental, no persistence, limited state management |
| CAMEL | 6k+ | Role-playing agents | Research-focused, less production-ready |

**LangGraph is optimal** because argumentation frameworks require explicit control over:
- Which agent speaks when (graph edges)
- How arguments are attacked/supported (conditional routing)
- When the debate terminates (convergence detection)
- Preserving the full argumentation tree (checkpointed state)

#### Architecture Pattern: Supervisor + Modality-Specialised Agents

```
                    ┌─────────────────────┐
                    │   Supervisor Agent   │
                    │  (Debate Moderator)  │
                    │  Sees: ALL arguments │
                    │  LLM: Meditron-8B   │
                    └────────┬────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼──────┐ ┌────▼────────┐ ┌───▼──────────┐
     │  VISION       │ │  REPORT     │ │  CLINICAL    │
     │  AGENT        │ │  AGENT      │ │  AGENT       │
     │  BioViL /     │ │  Meditron   │ │  Meditron    │
     │  LLaVA-Med 7B │ │  -8B        │ │  -8B         │
     └───────────────┘ └─────────────┘ └──────────────┘
              │              │              │
         [CXR JPG     ] [Radiology   ] [Structured   ]
         [Images      ] [Reports     ] [EHR: labs,   ]
         [MIMIC-CXR   ] [MIMIC-IV    ] [meds, dx...  ]
         [             ] [-Note       ] [MIMIC-IV     ]
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────────┐
                    │  Argumentation      │
                    │  Resolution Engine  │
                    │  (Dung's AAF +      │
                    │   Walton Schemes)   │
                    └─────────────────────┘
```

---

### 2.2 Knowledge Graph RAG

#### Primary: Microsoft GraphRAG (v3.0+)

| Attribute | Details |
|-----------|---------|
| **Repository** | [github.com/microsoft/graphrag](https://github.com/microsoft/graphrag) — 31k stars |
| **Version** | v3.0.2 (latest, July 2025) |
| **What it does** | Extracts entities & relationships from unstructured text → builds a knowledge graph → enables community-aware retrieval |
| **Why SOTA** | Graph community detection enables "global" queries (vs. naive RAG which only does local semantic search) |
| **Paper** | [From Local to Global: A Graph RAG Approach (arXiv:2404.16130)](https://arxiv.org/pdf/2404.16130) |
| **Install** | `pip install graphrag` |
| **License** | MIT |

**Why GraphRAG over standard RAG:**

| Approach | Retrieval Type | Strengths | Weakness |
|----------|---------------|-----------|----------|
| **Naive/Vector RAG** | Local similarity | Fast, simple | Misses global patterns, no relationship reasoning |
| **Microsoft GraphRAG** ✅ | Graph community + local | Global reasoning, entity relationships, community summaries | Higher indexing cost, requires LLM for extraction |
| **LightRAG** | Dual-level graph | Lightweight graph RAG | Less mature, smaller community |
| **HippoRAG** | Neurobiologically inspired | Memory-like retrieval | Research-prototype only |

**Integration with medical knowledge:**
- Index clinical guidelines (e.g., NICE, WHO) into a knowledge graph
- Each agent retrieves from different graph communities based on their perspective
- The argumentation engine can trace which knowledge nodes support/attack each argument

#### Complementary: Neo4j + LangChain Integration

| Component | Purpose |
|-----------|---------|
| **Neo4j Community Edition** | Graph database for storing the medical knowledge graph |
| **LangChain Neo4j integration** | `langchain-neo4j` package for graph-aware retrieval chains |
| **Medical Ontologies** | SNOMED-CT, ICD-10, UMLS (all freely available for research) |

**Medical Knowledge Graph sources (all publicly available):**

| Source | Description | License |
|--------|-------------|---------|
| **UMLS Metathesaurus** | Unified medical language system, 200+ vocabularies | Free for research (NLM license) |
| **SNOMED-CT** | Clinical terminology with hierarchical relationships | Free for research via UMLS |
| **DrugBank** | Drug interactions, mechanisms, targets | CC BY-NC 4.0 |
| **Disease Ontology (DO)** | Disease classifications and relationships | CC0 |
| **PrimeKG** | Precision Medicine Knowledge Graph (Harvard) | MIT |

---

### 2.3 Medical LLMs (Open-Source / API-Based)

#### Tier 1: Recommended Open-Source Medical LLMs

| Model | Base | Parameters | Key Strength | HuggingFace |
|-------|------|-----------|--------------|-------------|
| **Llama-3-Meditron** | Llama-3.1 | 8B / 70B | State-of-the-art open medical LLM (EPFL, 2025), clinical reasoning | `epfl-llm/meditron-v2.1-llama-3.1-8B` |
| **BioMistral** | Mistral-7B | 7B | Strong biomedical domain adaptation (ACL 2024, Cited 541x) | `BioMistral/BioMistral-7B` |
| **OpenBioLLM** | Llama-3 | 8B / 70B | Medical QA, clinical notes understanding | `aaditya/OpenBioLLM-Llama3-8B` |
| **MedAlpaca** | LLaMA | 7B / 13B | Instruction-tuned on medical dialogues | `medalpaca/medalpaca-13b` |

#### Tier 2: API-Based (for comparison/baselines)

| Model | Provider | Key Feature |
|-------|----------|-------------|
| **GPT-4o** | OpenAI | Best overall reasoning, medical benchmarks |
| **Claude 4.6 Sonnet** | Anthropic | Strong reasoning, long context |
| **Gemini 1.5 Pro** | Google | Multimodal, long context medical documents |

#### Recommended Strategy

The following models form the **candidate set** for each role. Final selection will be determined by a preliminary model selection benchmark (see §5.3, Step 2.1) on ~100–200 surrogate studies, evaluated on F1, latency, and VRAM footprint:

- **Text LLM candidates:** Llama-3-Meditron-8B (medical-specialised), Llama-3.1-8B (general-purpose baseline)
- **Image embedding candidates:** BioViL (CXR-specific CLIP), MedCLIP (general medical CLIP)
- **VLM candidates:** LLaVA-Med 7B (biomedical instruction-tuned), LLaVA-v1.5-7B (general-purpose baseline)
- **Comparison baseline:** GPT-4o (commercial SOTA, API-based)

The leading candidates are Meditron-8B + BioViL + LLaVA-Med 7B based on literature evidence, but final selection is contingent on empirical benchmarking results. This gives:
- Full reproducibility (open weights)
- Medical domain specialization
- Cost-free inference on local hardware (RTX 5070, 8 GB VRAM)
- Publishable comparison with commercial SOTA
- Multimodal processing within a single-GPU budget
- Evidence-based model selection (per supervisor recommendation)

---

### 2.4a Vision Language Models (VLMs) — New for MIMIC Pivot

| Model | Base | Parameters | VRAM (4-bit) | Key Strength | Role in System |
|-------|------|-----------|-------------|--------------|----------------|
| **BioViL** | ResNet-50 + CXR-BERT | ~400M | ~2 GB | CXR-specific vision-language pre-training, phrase grounding (ECCV 2022) | Image embedding backbone for CLIP-based Image RAG |
| **LLaVA-Med 7B** | LLaVA + biomedical fine-tuning | ~7B | ~4–5 GB | Biomedical visual instruction tuning, open-ended CXR QA (NeurIPS 2023) | Vision Agent — interprets CXR images into textual findings |
| **MedCLIP** | CLIP + medical adaptation | ~150M | ~1 GB | Decoupled contrastive learning from unpaired data (EMNLP 2022) | Alternative CLIP backbone (comparison) |

**Why BioViL over other CLIP variants:**

| Model | CXR-Specific? | Peer-Reviewed? | Phrase Grounding? | License |
|-------|:---:|:---:|:---:|--------|
| **BioViL** ✅ | ✅ Yes | ✅ ECCV 2022 | ✅ Yes | MIT |
| CLIP (Radford et al.) | ❌ General | ✅ ICML 2021 | ❌ No | MIT |
| GLoRIA | ✅ CXR | ✅ ICCV 2021 | ✅ Region-level | Research |
| CheXzero | ✅ CXR | ✅ Nature BME 2022 | ❌ No | Research |
| MedCLIP | ✅ Medical | ✅ EMNLP 2022 | ❌ No | MIT |

BioViL is the leading candidate because it is (1) CXR-specific, (2) peer-reviewed at a top CV venue, (3) supports phrase-level grounding useful for argument traceability, and (4) MIT-licensed. Final selection will be confirmed by the model selection benchmark (§5.3, Step 2.1) comparing BioViL against MedCLIP on the surrogate dataset.

---

### 2.4b Symbolic Reasoning & Argumentation Engine

#### Argumentation Framework: Dung's Abstract Argumentation + Walton's Schemes

| Component | Implementation |
|-----------|---------------|
| **Formal Framework** | Dung's Abstract Argumentation Framework (AAF) — arguments + attack relations |
| **Argumentation Schemes** | Walton's 60 argumentation schemes (filtered to ~10 clinically relevant ones) |
| **Preferred Semantics** | Compute preferred extensions to determine "winning" arguments |
| **Python Libraries** | Custom implementation using NetworkX for argument graphs |

**Clinically Relevant Argumentation Schemes (Walton):**

| Scheme | Clinical Application |
|--------|---------------------|
| Argument from Expert Opinion | "Dr. X (specialist) recommends treatment Y" |
| Argument from Evidence to Hypothesis | "Blood test shows X, therefore condition Y is likely" |
| Argument from Analogy | "Similar patient responded well to treatment Z" |
| Argument from Cause to Effect | "Medication A causes side effect B in patients with condition C" |
| Argument from Consequences | "If we delay treatment, the risk of X increases" |
| Argument from Established Rule | "Clinical guidelines recommend X for patients meeting criteria Y" |
| Argument from Sign | "Symptom X is a sign of condition Y" |

#### Symbolic Layer Implementation

```python
# Conceptual architecture
class ArgumentNode:
    """Represents a single argument in the framework"""
    id: str
    claim: str                    # Natural language claim
    scheme: WaltonScheme          # Which argumentation scheme
    evidence: List[KGTriple]      # Knowledge graph triples supporting this
    confidence: float             # Agent's confidence in this argument

class ArgumentationFramework:
    """Dung's AAF with extensions"""
    arguments: Dict[str, ArgumentNode]
    attacks: List[Tuple[str, str]]   # (attacker, attacked)
    supports: List[Tuple[str, str]]  # (supporter, supported)

    def compute_preferred_extensions(self) -> List[Set[str]]:
        """Compute winning argument sets"""
        ...

    def get_explanation_trace(self) -> ExplanationTree:
        """Generate human-readable explanation of the resolution"""
        ...
```

---

### 2.5 Additional SOTA Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Vector Store** | ChromaDB or FAISS | Embedding-based retrieval for text RAG + image RAG |
| **Text Embeddings** | `BAAI/bge-large-en-v1.5` or `nomic-ai/nomic-embed-text-v1.5` | Text embeddings for semantic search |
| **Image Embeddings** | BioViL vision encoder | CXR image embeddings for CLIP-based Image RAG |
| **Medical NER** | `en_core_sci_lg` (scispaCy) | Extract medical entities from radiology reports |
| **Report Section Extractor** | Rule-based (regex for FINDINGS/IMPRESSION headers) | Parse MIMIC-IV-Note radiology reports into structured sections |
| **VLM Inference** | LLaVA-Med 7B (4-bit GGUF via Ollama) | Vision Agent image interpretation |
| **Visualization** | Streamlit + Graphviz | Interactive argumentation tree visualization |
| **Experiment Tracking** | MLflow or Weights & Biases | Track experiments, metrics, model versions |
| **LLM Serving** | Ollama or vLLM | Local inference for open-source text + vision models |

---

### 2.6 Complete Tech Stack Summary

```
┌──────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
│  Streamlit UI / Gradio  │  Argumentation Tree Viz (Graphviz)    │
├──────────────────────────────────────────────────────────────────┤
│                   ORCHESTRATION LAYER                            │
│  LangGraph (Multi-Agent Graph Orchestration)                    │
│  ├── Supervisor Agent (Debate Moderator — sees all arguments)   │
│  ├── Vision Agent (CXR images via BioViL + LLaVA-Med 7B)       │
│  ├── Report Agent (Radiology reports via Meditron-8B)           │
│  └── Clinical Agent (Structured EHR via Meditron-8B)            │
├──────────────────────────────────────────────────────────────────┤
│                   REASONING LAYER                                │
│  Symbolic Argumentation Engine                                   │
│  ├── Dung's AAF (attack/support relations)                      │
│  ├── Walton's Schemes (argument classification)                 │
│  └── Preferred Extension Solver (winner determination)          │
├──────────────────────────────────────────────────────────────────┤
│                   KNOWLEDGE LAYER                                │
│  Microsoft GraphRAG          │  Neo4j Knowledge Graph            │
│  ├── Community Detection     │  ├── Medical Ontologies           │
│  ├── Global Search           │  │   (UMLS, SNOMED-CT, ICD-10)   │
│  └── Local Search            │  └── Clinical Guidelines          │
│  ChromaDB (Text Vectors)     │  ChromaDB (BioViL Image Vectors) │
│  PrimeKG (Drug-Disease-Gene) │  MIMIC-CXR Training Set (Image   │
│                               │   RAG Retrieval Corpus)          │
├──────────────────────────────────────────────────────────────────┤
│                     LLM / VLM LAYER                              │
│  Text LLM: Llama-3-Meditron-8B (via Ollama, 4-bit, ~5 GB)      │
│  Vision LLM: LLaVA-Med 7B (via Ollama, 4-bit, ~4–5 GB)         │
│  Image Embeddings: BioViL (~400M, ~2 GB)                        │
│  Text Embeddings: BGE-large-en-v1.5                              │
│  Baseline: GPT-4o (via API)                                      │
├──────────────────────────────────────────────────────────────────┤
│                  EVALUATION LAYER                                │
│  MLflow / W&B  │  Custom Metrics Engine  │  Human Eval Forms    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. System Architecture

### 3.1 High-Level Data Flow

```
INPUT: Multimodal Patient Case (linked by subject_id from MIMIC ecosystem)
         │
         ├──────────────────────┬─────────────────────┐
         │                      │                     │
         ▼                      ▼                     ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ CXR JPG Image  │  │ Radiology Report│  │ Structured EHR │
│ (MIMIC-CXR-JPG)│  │ (MIMIC-IV-Note) │  │ (MIMIC-IV)     │
└───────┬────────┘  └───────┬────────┘  └───────┬────────┘
        │                  │                  │
        ▼                  ▼                  ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ VISION AGENT   │  │ REPORT AGENT   │  │ CLINICAL AGENT │
│ BioViL +       │  │ Meditron-8B    │  │ EHR-to-Text +  │
│ LLaVA-Med 7B   │  │ Section Extrac.│  │ Meditron-8B    │
└───────┬────────┘  └───────┬────────┘  └───────┬────────┘
        │                  │                  │
        ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────┐
│ TEXT ARGUMENTS (all agents produce NL arguments) │
└────────────────────────┬────────────────────────────┘
                        │
        ┌───────────────▼───────────────────┐
        │ Knowledge Graph Retrieval       │
        │ (Per-Agent: Text RAG / GraphRAG │
        │  + CLIP-based Image RAG)        │
        └───────────────┬───────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │  Multi-Round Debate              │
        │  (LangGraph + Supervisor Agent)  │
        │  Structured argumentation rounds  │
        │  Max N rounds or convergence      │
        └───────────────┬───────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │  Argumentation Resolution Engine  │
        │  (Dung's AAF + Walton's Schemes) │
        │  Compute preferred extensions     │
        └───────────────┬───────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────┐
        │  Explanation Generator            │
        │  (LLM + Arg Tree → narrative)    │
        └───────────────┬───────────────────┘
                        │
                        ▼
OUTPUT: Recommendation + Explanation + Argumentation Tree + Confidence
```

#### Multimodal Input Processing Pipelines

**Vision Agent pipeline:**
```
CXR JPG → BioViL (embedding) + LLaVA-Med 7B (interpretation)
    → Structured visual findings text
    → "Findings: bilateral lower lobe opacities, cardiomegaly present,
       no pneumothorax, support devices: endotracheal tube in situ"
    → LLM (Meditron-8B) → Arguments with Walton scheme labels
```

**Report Agent pipeline:**
```
Radiology report CSV → Section extractor (rule-based, identifies FINDINGS
    and IMPRESSION headers) → Extracted text
    → "FINDINGS: Heart size enlarged. Bilateral pleural effusions.
       IMPRESSION: Cardiomegaly. Bilateral pleural effusions."
    → LLM (Meditron-8B) → Arguments with Walton scheme labels
```

**Clinical Agent pipeline (two options under consideration):**

*Option A — Structured Prompt Serialisation (preferred):*
```
MIMIC-IV tables (filtered by subject_id) → SQL/pandas query → itemid lookup
    table join → Structured markdown block with headers, units, and reference
    ranges (no intermediate LLM call)
    → ## Patient Demographics
       - Age: 72 | Sex: Male | Admission Type: Emergency
       ## Laboratory Results
       - Troponin I: 2.4 ng/mL [ref: <0.04] ↑
       - WBC: 8.2 K/uL [ref: 4.5–11.0] ✓
       ## Active Medications
       - Heparin drip 18 units/kg/hr
    → LLM (Meditron-8B) → Arguments with Walton scheme labels
```

*Option B — Clinical Vignette Generator:*
```
MIMIC-IV tables → Clinical Vignette Generator (lookup rules + template
    assembly + LLM smoothing) → Fluent clinical prose
    → LLM (Meditron-8B) → Arguments with Walton scheme labels
```

**Decision:** To be finalised after supervisor review. Both options feed text into Meditron-8B for argument generation.

**Critical insight:** All three agents ultimately produce **text arguments**. The argumentation layer (Dung's AAF, attack/support relations, Walton schemes, preferred extensions) operates entirely in the text domain. The image never enters the debate directly — only the VLM's textual interpretation does. This means the symbolic argumentation infrastructure is **unchanged** from the original design.

### 3.2 Agent Design: Modality-Based Information Partitioning

Following the supervisor's OIDP guidance ("One Issue, Different Perspectives") and the MIMIC pivot, the system uses **modality-based information partitioning** to differentiate agents. Each agent sees only one clinical data modality from the MIMIC ecosystem, mirroring a real clinical Multidisciplinary Team (MDT) where the radiologist reads the image, the clinician reviews labs and history, and the NLP system processes clinical notes.

#### Agent Specifications

| Agent | Data Source | Input Processing | Model | Sees | Does Not See |
|-------|-----------|------------------|-------|------|---------|
| **Vision Agent** | MIMIC-CXR-JPG images | VLM converts image to visual findings text | BioViL / LLaVA-Med 7B | CXR image only | Report text, EHR data |
| **Report Agent** | MIMIC-IV-Note radiology reports | NER + section extraction (Findings/Impression) | Meditron-8B | Radiologist's report only | CXR image, EHR data |
| **Clinical Agent** | MIMIC-IV (hosp + icu tables) | Structured Prompt Serialisation or Clinical Vignette Generator | Meditron-8B | Structured EHR data only | CXR image, report text |
| **Supervisor** | Aggregated arguments from all agents | Argument consolidation | Meditron-8B | All arguments (text) | Raw images/data |

#### How Modality-Based Partitioning Creates Argumentation

| Scenario | Vision Agent Sees | Report Agent Sees | Clinical Agent Sees | Debate |
|----------|-------------------|-------------------|--------------------|---------|
| Bilateral opacities on CXR | "Bilateral lower lobe opacities — suggests pneumonia" | Radiologist's impression: "Cardiomegaly without acute infiltrate" | "WBC normal, no fever" | Genuine cross-modal conflict: image vs. report vs. labs |
| Pleural effusion + heart failure | "Large bilateral pleural effusions" | "Bilateral pleural effusions, cardiomegaly" | "BNP elevated, history of CHF, on furosemide" | Convergence: all modalities agree, argumentation strengthens confidence |
| Subtle pneumothorax | "Small right apical lucency — ?pneumothorax" | Report does not mention pneumothorax | "Chest tube insertion noted in procedures" | Clinical Agent resolves ambiguity from the other two |
| Missed finding | Sees nothing abnormal | "Small left pleural effusion" noted by radiologist | "Albumin low, fluid overload risk" | Only Report Agent flags what the VLM missed |

**Design rationale — Modality-Based Partitioning (not feature masking):**

The original design used feature-mask partitioning on a single CSV, where all agents operated on the same data type (tabular integers). Modality-based partitioning is a **stronger** form of information asymmetry because: (a) agents process fundamentally different data representations (image pixels vs. free text vs. structured tables); (b) agents cannot simply infer each other's information from the same source; (c) it mirrors real clinical workflows where the radiologist reads the image, the clinician reviews labs/history, and they then confer.

**Why 3 modality agents (not more):**

The MIMIC ecosystem provides exactly three linked data types: images (MIMIC-CXR-JPG), reports (MIMIC-IV-Note), and structured EHR (MIMIC-IV). Each maps to one agent. The 3-agent design produces up to 6 directed attack edges per round — manageable for evaluation within a 25–50 page dissertation. Sub-dividing (e.g., splitting EHR into labs agent + medications agent) is documented as future work.

### 3.3 LangGraph State Machine

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator

class DebateState(TypedDict):
    patient_case: dict                           # Input patient data (subject_id + linked records)
    cxr_image_path: str                          # Path to CXR JPG image
    report_text: str                             # Radiology report text
    ehr_data: dict                               # Structured EHR data from MIMIC-IV
    vlm_findings: str                            # VLM-generated image description
    kg_context: dict                             # Retrieved knowledge per agent
    arguments: Annotated[list, operator.add]     # Accumulated arguments
    attack_relations: list                       # Attack edges
    support_relations: list                      # Support edges
    round_number: int                            # Current debate round
    converged: bool                              # Whether agents agree
    preferred_extension: list                    # Winning argument set
    final_recommendation: str                    # Output recommendation
    explanation_trace: str                       # Human-readable reasoning

graph = StateGraph(DebateState)

# Nodes
graph.add_node("parse_case", parse_patient_case)
graph.add_node("route_modalities", route_to_modality_pipelines)
graph.add_node("process_cxr", vision_agent_process_image)
graph.add_node("process_report", report_agent_extract_sections)
graph.add_node("process_ehr", clinical_agent_serialize_ehr)
graph.add_node("retrieve_knowledge", retrieve_from_kg)
graph.add_node("agent_vision", vision_agent_argue)
graph.add_node("agent_report", report_agent_argue)
graph.add_node("agent_clinical", clinical_agent_argue)
graph.add_node("evaluate_arguments", symbolic_argumentation_resolution)
graph.add_node("check_convergence", check_debate_convergence)
graph.add_node("generate_explanation", generate_final_explanation)

# Edges
graph.add_edge(START, "parse_case")
graph.add_edge("parse_case", "route_modalities")
graph.add_edge("route_modalities", "process_cxr")
graph.add_edge("route_modalities", "process_report")
graph.add_edge("route_modalities", "process_ehr")
graph.add_edge("process_cxr", "retrieve_knowledge")
graph.add_edge("process_report", "retrieve_knowledge")
graph.add_edge("process_ehr", "retrieve_knowledge")
graph.add_edge("retrieve_knowledge", "agent_vision")
graph.add_edge("retrieve_knowledge", "agent_report")
graph.add_edge("retrieve_knowledge", "agent_clinical")
graph.add_edge("agent_vision", "evaluate_arguments")
graph.add_edge("agent_report", "evaluate_arguments")
graph.add_edge("agent_clinical", "evaluate_arguments")
graph.add_edge("evaluate_arguments", "check_convergence")

# Conditional: continue debate or resolve
graph.add_conditional_edges(
    "check_convergence",
    lambda state: "generate_explanation" if state["converged"] or state["round_number"] >= 5
    else "agent_vision"
)
graph.add_edge("generate_explanation", END)

app = graph.compile()
```

---

## 4. Datasets

All primary datasets are from the **MIMIC ecosystem** (MIT Laboratory for Computational Physiology, PhysioNet). Development surrogates are openly available and require no credentialing. The system uses the OIDP (One Issue, Different Perspectives) approach where each modality-specialised agent processes a different data type from the same patient.

### 4.1 Primary Datasets: MIMIC Ecosystem

| Dataset | Content | Size | Patients | License | Access |
|---------|---------|------|----------|---------|--------|
| **MIMIC-CXR-JPG v2.1.0** | 377,110 JPG chest radiographs with 14 CheXpert labels | ~570 GB (full); ~2 GB (subset) | 64,588 | PhysioNet Credentialed 1.5.0 | Credentialed |
| **MIMIC-IV-Note v2.2** | 331,794 discharge summaries + 2,321,355 radiology reports | ~3 GB | 237,427 (reports) | PhysioNet Credentialed 1.5.0 | Credentialed |
| **MIMIC-IV v3.1** | Structured EHR: labs, meds, diagnoses, vitals, procedures | ~7 GB | 364,627 | PhysioNet Credentialed 1.5.0 | Credentialed |

**Cross-dataset linkage:** All three datasets link via `subject_id`. MIMIC-CXR patients are a subset of MIMIC-IV (2011–2016, ED-admitted patients).

**The 14 CheXpert pathology labels (evaluation targets):**
Atelectasis, Cardiomegaly, Consolidation, Edema, Enlarged Cardiomediastinum, Fracture, Lung Lesion, Lung Opacity, Pleural Effusion, Pneumonia, Pneumothorax, Pleural Other, Support Devices, No Finding.

#### Subset Strategy

The project uses a **2,000–3,000 study subset** (~2–3 GB total), not the full 570 GB dataset:

| Step | Action | Result |
|------|--------|--------|
| 1 | Download CSV metadata files only (~10 MB) | `mimic-cxr-2.0.0-chexpert.csv.gz`, `mimic-cxr-2.0.0-metadata.csv.gz` |
| 2 | Filter to **frontal views only** (PA and AP) | Reduces image count by ~40% |
| 3 | Filter to studies with **positive CheXpert labels** for 5–6 target pathologies | Cardiomegaly, Pleural Effusion, Pneumonia, Pneumothorax, Atelectasis |
| 4 | Stratified random sample of **2,000–3,000 studies** | Balanced across pathologies + ~25% "No Finding" control |
| 5 | Download only matching JPGs via selective `wget` | ~1–2 GB images |
| 6 | Download linked MIMIC-IV-Note radiology reports | ~50 MB |
| 7 | Download linked MIMIC-IV structured EHR data | ~100–200 MB |

#### Why This Dataset Suite Is Ideal for OIDP Argumentation

| Feature | Relevance |
|---------|----------|
| **Genuinely multimodal** | Images + reports + structured EHR = three fundamentally different data types |
| **Natural modality-based partitioning** | Each agent sees a different data modality — stronger information asymmetry than feature masking |
| **Established benchmark** | MIMIC-CXR is one of the most widely cited medical imaging datasets |
| **14 CheXpert pathology labels** | Multi-hypothesis argumentation — agents debate which pathologies are present |
| **Genuine cross-modal conflicts** | Vision Agent sees "bilateral opacities" (pneumonia?), Report Agent reads "cardiomegaly without infiltrate", Clinical Agent notes "WBC normal" — Dung's AAF must resolve |
| **Radiologist-annotated test set** | Gold-standard evaluation against human expert performance |
| **Linked ecosystem** | All modules share `subject_id` — seamless cross-dataset joining |

### 4.2 Development Surrogate Datasets (Available Now — No Credentialing)

| Component | Surrogate Dataset | Access | Size | Purpose |
|-----------|------------------|--------|------|---------|
| Clinical Agent | **MIMIC-IV Demo** (100 patients, Open Access) | Download now | 15.5 MB | Build and test EHR-to-text pipeline against real MIMIC-IV schema |
| Vision Agent | **NIH ChestX-ray14** (112,120 images, CC0) | Download now | ~42 GB | Develop and test VLM pipeline, BioViL embeddings |
| Report Agent | **OpenI / Indiana CXR** (7,470 images + English reports) | Download now | ~1 GB | Develop and test report section extraction and NER |
| Argumentation Layer | Any text input | N/A | — | Framework is data-agnostic — can develop with synthetic examples |

### 4.3 Knowledge Sources for GraphRAG Indexing

| Source | Content | Clinical Relevance | Access |
|--------|---------|-------------------|--------|
| **ACR Appropriateness Criteria** | Imaging guidelines for clinical scenarios | CXR interpretation context | Free download |
| **Fleischner Society Guidelines** | Pulmonary nodule management | Lung pathology management | Free download |
| **ESC 2023 Guidelines** | Cardiovascular disease management | Cardiac pathologies (cardiomegaly, effusions) | Free download |
| **PubMed Abstracts** | 35M+ biomedical abstracts | All pathologies | Free API |
| **PrimeKG** | 29,085 diseases, 4,050,249 relationships | Drug-disease-gene links | MIT, Harvard |
| **MIMIC-CXR-JPG training set** | Non-test CXR images as CLIP retrieval corpus | Image RAG evidence base | Part of subset |

### 4.4 Dataset Ethics Compliance Summary

| Requirement (HWU) | MIMIC-CXR-JPG | MIMIC-IV-Note | MIMIC-IV | MIMIC-IV Demo | NIH CXR14 | OpenI |
|-------------------|:---:|:---:|:---:|:---:|:---:|:---:|
| Publicly available | ✅ PhysioNet | ✅ PhysioNet | ✅ PhysioNet | ✅ PhysioNet | ✅ NIH | ✅ NLM |
| Anonymised at source | ✅ HIPAA Safe Harbor | ✅ HIPAA | ✅ HIPAA | ✅ HIPAA | ✅ | ✅ |
| License | PhysioNet 1.5.0 | PhysioNet 1.5.0 | PhysioNet 1.5.0 | ODbL (Open) | CC0 | Open |
| Access level | Credentialed | Credentialed | Credentialed | **Open** | **Open** | **Open** |
| Ethics impact | DUA-bound — may require HWU ethics update | Same | Same | Low-risk | Low-risk | Low-risk |

---

## 5. Methodology

### 5.1 Research Design

**Type:** Design Science Research + Experimental Evaluation

The project follows a **three-phase methodology**:

```
Phase 1: DESIGN → Phase 2: IMPLEMENT → Phase 3: EVALUATE
```

### 5.2 Phase 1: Design (February – April 2026)

| Step | Activity | Deliverable |
|------|----------|-------------|
| 1.1 | Literature review of 15+ papers + 19 new MIMIC/VLM papers | Lit review chapter, SOTA comparison table |
| 1.2 | Define argumentation framework formalism | Formal specification of argument structure |
| 1.3 | Design modality-based agent specifications & prompts | System prompt templates for Vision, Report, Clinical agents |
| 1.4 | Design Knowledge Graph schema | Entity types, relationship types, ontology mapping |
| 1.5 | Design evaluation framework | Metrics specification document |
| 1.6a | Download surrogate datasets (MIMIC-IV Demo, NIH CXR14, OpenI) | Development data available |
| 1.6b | Initiate PhysioNet credentialing (CITI training, application) | Credentialing process started |
| 1.6c | Design modality input pipelines (CXR, report, EHR) | Pipeline design document |

### 5.3 Phase 2: Implement (April – July 2026) — Two-Track Development

**Track 1: Build Everything (using surrogates — starts immediately)**

| Step | Activity | Deliverable |
|------|----------|-------------|
| 2.1 | **Model Selection Benchmark:** Compare 1–3 candidate models per role (text LLM, image embeddings, VLM) on ~100–200 surrogate studies. Evaluate on F1, latency, VRAM. Select winners for full experiments | Model selection report with benchmark results |
| 2.2 | Set up LangGraph multi-agent graph | Working agent orchestration pipeline |
| 2.3 | Build Knowledge Graph from clinical guidelines | Neo4j database with indexed medical knowledge |
| 2.4 | Implement GraphRAG indexing pipeline | GraphRAG index over clinical guidelines |
| 2.5 | Implement symbolic argumentation engine | Dung's AAF + Walton scheme classifier |
| 2.6 | Build Vision Agent pipeline (benchmark-selected VLM) using NIH CXR14 | Working VLM inference pipeline |
| 2.7 | Build Report Agent pipeline using OpenI Indiana CXR reports | Working report section extraction + NER |
| 2.8 | Build Clinical Agent pipeline using MIMIC-IV Demo | Working EHR-to-text serialiser |
| 2.9 | Build Streamlit UI for visualization | Interactive argumentation tree viewer |

**Track 2: Get the Data (parallel credentialing process)**

| Step | Activity | Deliverable |
|------|----------|-------------|
| 2.10 | Complete CITI training + submit PhysioNet application | Credentialing submitted |
| 2.11 | Submit HWU ethics amendment (post-proposal) | Ethics update submitted |
| 2.12 | Download MIMIC subset upon credential approval | Real MIMIC data available |
| 2.13 | Integrate real MIMIC data into pipelines built in Track 1 | End-to-end system on real data |

### 5.4 Phase 3: Evaluate (July – August 2026)

| Step | Activity | Deliverable |
|------|----------|-------------|
| 3.1 | Quantitative evaluation on MIMIC subset | Multi-label F1 (14 CheXpert), per-pathology AUROC, explainability scores |
| 3.2 | Comparative evaluation vs. baselines | SOTA comparison results |
| 3.3 | Qualitative analysis of explanations | Example case studies with argumentation traces |
| 3.4 | Ablation studies (7 ablations) | Impact of each component and modality |
| 3.5 | Surrogate comparison analysis | Demo vs. full MIMIC performance |
| 3.6 | Write-up and finalize report | Complete dissertation document |

### 5.5 Experimental Design

#### Infrastructure Sweep (answers SRQ2)

To isolate the effect of different RAG approaches on multi-agent clinical reasoning, the same 3 modality-partitioned agents are run through multiple retrieval backends with everything else held constant:

| Run | Retrieval Backend | What Changes | What Stays Fixed |
|-----|-------------------|-------------|------------------|
| **Run A** | Vector RAG (ChromaDB, text) | Semantic similarity retrieval only | Same 3 agents, same modality partitions, same prompts, same symbolic layer |
| **Run B** | GraphRAG (Microsoft GraphRAG + Neo4j) | Graph community detection + entity-relationship retrieval | Same 3 agents, same modality partitions, same prompts, same symbolic layer |
| **Run C** | **Multimodal Hybrid** (Text Vector RAG + GraphRAG + CLIP-based Image RAG) | All retrieval methods combined, including BioViL image embeddings for visual evidence retrieval | Same 3 agents, same modality partitions, same prompts, same symbolic layer |

Run C is the most novel — no published argumentation system combines CLIP-based image retrieval with knowledge-graph-grounded text retrieval for formal argumentation.

> **Note:** All infrastructure sweep runs use the models selected during the preliminary model selection benchmark (Step 2.1). This ensures results reflect optimised model choices rather than arbitrary defaults.

The unit of analysis is the **whole system's collective output** (argumentation quality, pathology prediction, explanation completeness) — not individual agents. This directly answers SRQ2: "How do different RAG approaches affect multi-agent clinical reasoning?"

#### Baselines to Compare Against

| # | Baseline | Description | Purpose |
|---|----------|-------------|---------|
| B1 | **Single LLM (Zero-Shot)** | GPT-4o / Meditron with direct multimodal prompting | Shows value of multi-agent debate |
| B2 | **Single LLM + RAG** | Single LLM with standard vector RAG (text only) | Shows value of multimodal + KG-RAG |
| B3 | **Multi-Agent No Argumentation** | Three modality agents without Dung's AAF resolution | Shows value of symbolic layer |
| B4 | **Existing System Comparison** | Adapt closest published radiology MAS or argumentation system | Direct comparison with SOTA |
| B5 | **Full System (Proposed)** | All components — modality partitioning + AAF + best RAG | Cumulative improvement |

#### Ablation Studies

| Ablation | What's Removed | Tests |
|----------|---------------|-------|
| A1: No Image RAG | Replace CLIP-based image retrieval with text-only RAG | Visual retrieval contribution |
| A2: No Symbolic Layer | Remove Dung's AAF; keep LLM debate only | Symbolic reasoning contribution |
| A3: No Modality Partitioning | All agents see all modalities | Modality-based asymmetry contribution |
| A4: Single Agent + All Components | One agent with all data + KG-RAG + AAF | Multi-agent contribution |
| A5: General LLM | Replace Meditron with Llama-3.1-8B (general-purpose) | Domain specialisation contribution |
| A6: No Vision Agent | Remove CXR image modality entirely | Image modality contribution |
| A7: No Clinical Agent | Remove structured EHR data entirely | Tabular data contribution |

---

## 6. Evaluation Framework

### 6.1 Evaluation Principles (from Supervisor Guidance)

> "What metrics — NOT usual like accuracy → may: explainability, process, outcome, trust"

### 6.2 Multi-Dimensional Evaluation Metrics

#### Dimension 1: Clinical Outcome Quality

| Metric | Description | Computation |
|--------|-------------|-------------|
| **Multi-label F1 (Macro)** | Average F1 across all 14 CheXpert pathology labels, treating each equally | $F1_{macro} = \frac{1}{K} \sum_{k=1}^{K} F1_k$ |
| **Multi-label F1 (Micro)** | Global F1 pooling predictions across all pathology labels | Aggregate TP, FP, FN across all 14 labels |
| **Per-Pathology AUROC** | Discrimination for each individual pathology (especially Cardiomegaly, Pleural Effusion, Pneumothorax) | $AUROC_k$ per CheXpert label |
| **Pathology Co-occurrence Accuracy** | Can the system correctly identify multi-pathology studies? | Exact match ratio for studies with ≥2 positive labels |
| **Cross-Modal Agreement** | Do findings from different modalities converge on the same diagnoses? | Cohen's κ between Vision Agent labels and Report Agent labels |

#### Dimension 2: Explainability

| Metric | Description | How Measured |
|--------|-------------|-------------|
| **Explanation Completeness** | Does the explanation cover all relevant factors? | % of ground-truth evidences mentioned in explanation |
| **Argumentation Coverage** | How many relevant Walton schemes were invoked? | Count of applicable schemes used / total applicable |
| **Logical Consistency** | Are the arguments internally consistent (no self-contradictions)? | Automated check: no argument both attacks and supports same claim |
| **Faithfulness** | Does the explanation match the actual reasoning process? | Compare explanation trace to actual graph execution path |
| **BLEU/ROUGE-L** | Quality of natural language explanations | Against expert-written reference explanations |

#### Dimension 3: Process Transparency

| Metric | Description | How Measured |
|--------|-------------|-------------|
| **Debate Depth** | How many rounds of argumentation occurred? | Average rounds before convergence |
| **Attack Rate** | What percentage of arguments were challenged? | #attacks / #arguments |
| **Convergence Quality** | How quickly and cleanly did agents converge? | Rounds to convergence + final disagreement level |
| **Argument Traceability** | Can each conclusion be traced to evidence? | % of conclusions with complete evidence chains |

#### Dimension 4: Trust

| Metric | Description | How Measured |
|--------|-------------|-------------|
| **Confidence Calibration** | Does higher system confidence correlate with correct answers? | Expected Calibration Error (ECE) |
| **Uncertainty Indication** | Does the system indicate when it's uncertain? | Correlation between agent disagreement and case difficulty |
| **Reasoning Transparency Score** | Can a human follow the reasoning chain? | Proxy: explanation length, structure, jargon ratio |

#### Dimension 5: Robustness

| Metric | Description | How Measured |
|--------|-------------|-------------|
| **Sensitivity Analysis** | How does performance change with missing evidence? | Randomly drop 10/20/30% of patient evidence |
| **Consistency** | Same patient with reworded symptoms → same diagnosis? | Paraphrase patient cases, measure output stability |

#### Dimension 6: Information Fusion Quality

| Metric | Description | How Measured |
|--------|-------------|-------------|
| **Cross-Modal Discovery Rate** | How often does the debate surface insights that require information from multiple modalities (CXR + report + EHR)? | % of final arguments citing evidence from ≥2 agents' modalities |
| **Unique Evidence Contribution** | Does each agent contribute non-redundant information? | Count of unique evidence items per agent that appear in final resolution |
| **Modality Complementarity** | Do agents with different modalities collectively outperform agents with all modalities? | Compare full system vs. ablation A3 (no modality partitioning) on all Dimension 1 metrics |
| **VLM Faithfulness** | Are Vision Agent findings grounded in actual image content? | % of VLM-generated findings confirmed by CheXpert ground-truth labels |

### 6.3 Evaluation Protocol

```
For each study in test set (n=~400-600 held-out MIMIC studies, stratified by pathology profile):
  1. Load CXR image + radiology report + structured EHR for the study
  2. Run through full system → record: pathology predictions, explanation, arg tree
  3. Run through each baseline → record same outputs
  4. Compute all metrics for each system (6 dimensions)
  5. Statistical significance testing (paired t-test or Wilcoxon)
  6. Surrogate comparison: compare results on MIMIC-IV Demo vs. full MIMIC subset

Qualitative Analysis (20 MIMIC cases):
  - Select 10 correct + 10 incorrect cases
  - Analyze argumentation trees manually
  - Document reasoning patterns and failure modes
  - Highlight cases where modalities disagree (e.g., CXR shows opacity but report is equivocal)
  - Examine VLM grounding: are BioViL embeddings retrieving genuinely similar reference images?
```

---

## 7. Ethics Compliance Plan

### 7.1 HWU Ethics Requirements

| Requirement | Status | Action |
|-------------|--------|--------|
| Infonetica ethics form submission | Pending | Submit by **Week 7 (Feb 27, 2026)** |
| Ethics approval | Pending | Target approval by **April 2, 2026** |
| Risk level | **Medium** | MIMIC data requires PhysioNet DUA; de-identified but regulated |
| Data Protection (GDPR) | ✅ Compliant | All MIMIC data is de-identified per HIPAA Safe Harbor; no re-identification attempted |
| PhysioNet Credentialing | **Required** | CITI training + signed DUA per PhysioNet 1.5.0 |
| External ethics approval (NHS, etc.) | **NOT Required** | No human participants, no real-time patient data |

### 7.2 Ethics Form Strategy

**Category:** Medium-risk research using de-identified but regulated clinical datasets

**Key arguments for the ethics form:**

1. **No human participants** — all evaluation is automated against existing datasets
2. **All MIMIC datasets are de-identified per HIPAA Safe Harbor** — no direct patient identifiers, no free-text names/dates (dates shifted, ages capped at 89)
3. **Data access is governed by PhysioNet Credentialed Health Data License 1.5.0** — requires CITI "Data or Specimens Only Research" training, institutional sign-off, and agreement not to re-identify patients
4. **No new data is collected from human participants** — the project re-uses existing, regulated clinical records
5. **No real clinical deployment** — prototype for academic research only
6. **System is a decision support tool, not a standalone decision-maker** — always human-in-the-loop
7. **All models (BioViL, LLaVA-Med, Meditron) are open-source with permissive licenses**
8. **Surrogate datasets (MIMIC-IV Demo, NIH CXR14, OpenI) are fully public** — used for development before MIMIC access granted

### 7.3 Ethics Form Section Mapping

| Section | Content |
|---------|---------|
| **Project Title** | Multi-Agent Argumentation Frameworks with LLM-Augmented Reasoning in Healthcare Systems |
| **Project Description** | Developing a prototype system where multiple AI agents debate clinical cases from different data modalities (chest X-ray, radiology report, structured EHR), using formal argumentation frameworks |
| **Data Sources** | MIMIC-CXR-JPG v2.1.0 (PhysioNet 1.5.0), MIMIC-IV-Note v2.2 (PhysioNet 1.5.0), MIMIC-IV v3.1 (PhysioNet 1.5.0) — all de-identified under HIPAA Safe Harbor. Surrogates: MIMIC-IV Demo (open), NIH CXR14 (CC0), OpenI (public domain) |
| **Participants** | None — no human participants in the study |
| **Risk Level** | Medium — de-identified clinical data under DUA; no clinical deployment |
| **Data Storage** | Local machine only (encrypted SSD), no cloud upload; MIMIC data stored per DUA requirements |
| **Potential Harms** | Low — system is not deployed clinically; de-identified data; clear disclaimers that outputs are for research purposes only |
| **PhysioNet Compliance** | CITI training certificate, signed DUA, data not redistributed, results reported in aggregate only |

---

## 8. SOTA Comparison Table

### Existing Approaches vs. Proposed System

| Approach | Agents | LLM | Argumentation | KG-RAG | Explainability | Symbolic | Dataset | Metrics |
|----------|--------|-----|---------------|--------|---------------|----------|---------|---------|
| **ArgMed-Agents** (Hong 2024) | ✅ Multi | ✅ GPT-4 | ✅ Walton Schemes | ❌ None | ✅ Schemes | ✅ Partial | MedQA | Accuracy |
| **MedGen** (Liu 2024) | ✅ Multi | ✅ LLM | ✅ Debate | ❌ Standard RAG | ✅ Fusion | ❌ | Clinical cases | Accuracy, F1 |
| **MedAgent-Zero** (Mao 2024) | ✅ Multi | ✅ GPT-4 | ❌ Collaboration | ❌ None | ⚠️ Limited | ❌ | MedQA, PubMedQA | Accuracy |
| **MDAgents** (Kim 2024) | ✅ Multi | ✅ GPT-4 | ❌ Voting/Consensus | ❌ None | ⚠️ Limited | ❌ | MedQA, MMLU | Accuracy |
| **MedRAG** (Zhao 2025) | ❌ Single | ✅ LLM | ❌ None | ✅ KG-RAG | ⚠️ Retrieval-based | ❌ | Medical QA | Accuracy, F1 |
| **XLR-KGDD** (Bedi 2025) | ❌ Single | ✅ LLM | ❌ None | ✅ KG+RAG | ✅ KG-based | ❌ | Multimodal clinical | Accuracy |
| **Proposed System** | ✅ Multi | ✅ Meditron + LLaVA-Med + BioViL | ✅ Dung's AAF + Walton | ✅ GraphRAG + Neo4j + CLIP Image RAG | ✅ Full trace | ✅ Full | MIMIC-CXR + MIMIC-IV | Multi-dimensional |

### Research Gaps Addressed

| Gap | How Proposed System Addresses It |
|-----|----------------------------------|
| **No existing system combines KG-RAG with multi-agent argumentation** | First to integrate Microsoft GraphRAG with structured agent debate |
| **Existing argumentation systems don't use Knowledge Graphs** | GraphRAG provides entity-relationship grounding for each argument |
| **No argumentation system uses multimodal clinical data** | Three modality-specialised agents (CXR image, radiology report, structured EHR) debating via formal argumentation |
| **No system combines CLIP image retrieval with KG-grounded text RAG for argumentation** | BioViL-based image RAG + GraphRAG text RAG in a single argumentation pipeline |
| **Evaluation is accuracy-only** | Multi-dimensional metrics: explainability, process, trust, cross-modal agreement |
| **Most systems use closed-source LLMs only** | Open-source Meditron + LLaVA-Med as primary, with GPT-4o comparison |
| **No symbolic resolution of agent debates** | Dung's AAF computes preferred extensions formally |
| **Limited perspective diversity in existing multi-agent systems** | Modality-partitioned agents (Vision/Report/Clinical) mirroring clinical data integration |

---

## 9. Project Timeline & Milestones

### Gantt Chart (Text Format) — Dual-Track Development

```
Feb 2026  ──────────────────────────────────────────── Aug 2026
│ W1-2 │ W3-4 │ W5-8 │ W9-12│W13-16│W17-20│W21-24│W25-26│
│ Feb  │ Mar  │ Apr  │ May  │ Jun  │ Jul  │ Aug  │ Aug  │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│██████│      │      │      │      │      │      │      │ PPT + Ethics
│██████│██████│██████│      │      │      │      │      │ Literature Review
│      │██████│██████│      │      │      │      │      │ Formal Design
│      │      │      │      │      │      │      │      │
│ TRACK 1 (Surrogates — starts immediately)                │
│      │      │██████│██████│      │      │      │      │ Surrogate Data Prep (Demo/NIH/OpenI)
│      │      │      │██████│██████│      │      │      │ Core Implementation (agents, VLM, RAG)
│      │      │      │      │██████│██████│      │      │ KG-RAG + CLIP Image RAG Pipeline
│      │      │      │      │      │██████│      │      │ Surrogate Experiments
│      │      │      │      │      │      │      │      │
│ TRACK 2 (PhysioNet Credentialing — parallel)             │
│██████│██████│      │      │      │      │      │      │ CITI Training + PhysioNet Application
│      │      │██████│██████│      │      │      │      │ Credential Review (waiting)
│      │      │      │      │██████│      │      │      │ Download MIMIC Subset (upon approval)
│      │      │      │      │██████│██████│      │      │ Integrate Real MIMIC + Re-run Experiments
│      │      │      │      │      │      │      │      │
│      │      │      │      │      │      │██████│██████│ Write-up
```

### Detailed Milestone Schedule

| Week | Date | Milestone | Deliverable |
|------|------|-----------|-------------|
| **W1** | Feb 23–28 | ✅ PPT Presentation | PowerPoint slides for supervisor |
| **W1** | Feb 27 | ✅ Ethics Form Submission | Infonetica form submitted |
| **W1–2** | Feb 23 – Mar 7 | CITI Training Complete | Certificate for PhysioNet |
| **W2–4** | Mar 1–21 | Literature Review Complete | Lit review chapter draft (35+ papers including 19 new MIMIC/VLM) |
| **W3** | Mar 14 | PhysioNet Application Submitted | Credentialing application filed |
| **W4** | Mar 21 | SOTA Table Final | Completed comparison table with multimodal gap |
| **W5** | Mar 28 | Research Questions Finalized | RQ + SRQ document approved by supervisor |
| **W6** | Apr 2 | Ethics Approval Target | Approval received |
| **W6–8** | Apr 2–18 | Architecture Design | Complete system design document |
| **W8** | Apr 18 | Design Review with Supervisor | Architecture approval |
| **W9** | Apr 21–28 | Model Selection Benchmark | Compare candidate LLMs/VLMs on ~100–200 surrogate studies; select winners |
| **W9–10** | Apr 28 – May 2 | Surrogate Data Preparation | MIMIC-IV Demo, NIH CXR14, OpenI downloaded and preprocessed |
| **W10–12** | May 2–16 | LangGraph Agent Pipeline | Working multi-agent debate system with Vision/Report/Clinical agents |
| **W12–14** | May 16–30 | VLM + Argumentation Engine | BioViL/LLaVA-Med pipeline + symbolic layer + Walton scheme classifier |
| **W14–16** | May 30 – Jun 13 | GraphRAG + CLIP Image RAG | Knowledge graph + BioViL-based image retrieval index built |
| **W16** | Jun 13 | PhysioNet Approval Target | Credentials approved, MIMIC download begins |
| **W16–18** | Jun 13–27 | MIMIC Integration + Testing | Switch from surrogates to real MIMIC data |
| **W18–20** | Jun 27 – Jul 11 | Experiments | All baselines (B1-B5), ablations (A1-A7), RAG sweep (Runs A-C) |
| **W20–22** | Jul 11–25 | Results Analysis | Statistical analysis, visualizations |
| **W22–24** | Jul 25 – Aug 8 | Report Writing | Complete draft |
| **W25–26** | Aug 8–22 | Revision & Submission | Final report + code repository |

### Supervisor Checkpoints

| Checkpoint | Date | Focus |
|------------|------|-------|
| CP1 | Feb 28 | PPT presentation — project plan & lit review overview |
| CP2 | Mar 14 | Literature review progress — 35+ papers summarized (incl. 19 new MIMIC/VLM) |
| CP3 | Apr 2 | Design review — architecture, MIMIC pipeline, metrics confirmed |
| CP4 | May 16 | Prototype demo — working multi-agent debate on surrogate data |
| CP5 | Jun 13 | PhysioNet update — credential status + VLM pipeline demo |
| CP6 | Jun 27 | Full system demo — all components integrated on real MIMIC |
| CP7 | Jul 25 | Results review — experiments complete |
| CP8 | Aug 15 | Near-final report review |

---

## 10. Report Structure

### Proposed Chapter Outline (25–50 pages)

| Chapter | Title | Pages | Content |
|---------|-------|-------|---------|
| 1 | Introduction | 3–4 | Motivation, problem statement, RQ + SRQs, contributions, report structure |
| 2 | Background | 5–7 | Multi-agent systems, argumentation theory (Dung's AAF, Walton), LLMs/VLMs in healthcare, Knowledge Graphs, RAG, MIMIC ecosystem |
| 3 | Literature Review | 5–7 | Systematic review of 35+ papers (incl. MIMIC/VLM/CLIP), SOTA comparison table, research gaps, positioning |
| 4 | Methodology | 5–7 | Research design, system architecture, agent design, KG schema, evaluation framework |
| 5 | Implementation | 4–6 | LangGraph pipeline, GraphRAG setup, symbolic engine, UI |
| 6 | Evaluation & Results | 5–8 | Experimental setup, quantitative results (all 5 metric dimensions), qualitative case studies, ablation studies |
| 7 | Discussion | 3–4 | Findings interpretation, limitations, comparison with existing work, clinical implications |
| 8 | Conclusion | 2–3 | Summary of contributions, answers to RQs, future work |
| — | References | 2–3 | 30–40 references |
| — | Appendices | 2–5 | System prompts, code listings, additional results |
| | **Total** | **36–54** | |

---

## 11. Risk Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| **PhysioNet credentialing delayed** | High | Medium | Two-track development: build everything on surrogates (MIMIC-IV Demo, NIH CXR14, OpenI) while credentials are processed. System works end-to-end before real MIMIC data arrives |
| **VLM exceeds 8 GB VRAM** | High | Medium | Use 4-bit quantised LLaVA-Med (~4-5 GB); BioViL ~2 GB; never load both simultaneously — sequential inference with `torch.cuda.empty_cache()` between calls |
| **LLM inference too slow/expensive** | High | Medium | Use quantized Meditron (4-bit GGUF via Ollama) on RTX 5070; batch inference; run on university GPU if needed |
| **GraphRAG indexing cost** | Medium | Medium | Start with small corpus (1 guideline), scale incrementally; use local LLM for indexing |
| **Argumentation convergence failure** | High | Low | Set max rounds (5), implement fallback majority-vote |
| **Ethics re-application needed** | Medium | Medium | Submit initial ethics early (W1) covering surrogates; prepare amendment for MIMIC DUA-bound data once credentials confirmed |
| **MIMIC subset too large for local storage** | Medium | Low | Strict subset: 2,000-3,000 frontal-view studies, 5-6 pathologies, ~2-3 GB total; store on 2 TB SSD |
| **Scope creep** | High | Medium | Fixed scope: MIMIC-CXR + MIMIC-IV primary, 3 modality-partitioned agents + supervisor, 6 metric dimensions. Anything extra is "future work" |
| **Medical domain errors** | Medium | Medium | All outputs labeled as "research prototype, not clinical advice". Use validated datasets |
| **LangGraph API changes** | Low | Low | Pin version (1.0.9), write modular code |
| **Supervisor availability** | Medium | Low | Bi-weekly checkpoints scheduled in advance, async communication via email |

---

## 12. References & Resources

### Key Papers (from Literature Review)

1. Hong et al. (2024) — *ArgMed-Agents: Explainable Clinical Decision Reasoning with LLM Discussion via Argumentation Schemes* — IEEE BIBM
2. Liu et al. (2024) — *MedGen: An Explainable Multi-Agent Architecture for Clinical Decision Support* — IEEE BIBM
3. Mao et al. (2024) — *MedAgent-Zero: Medical Multi-Agent for Zero-Shot Clinical Decision Support* — arXiv
4. Kim et al. (2024) — *MDAgents: Adaptive Medical Decision-Making with Multi-Agent Systems* — NeurIPS
5. Zhao et al. (2025) — *MedRAG: Enhancing RAG with KG-Elicited Reasoning for Healthcare Copilot* — ACM WWW 2025
6. Bedi et al. (2025) — *XLR-KGDD: Leveraging LLM and RAG for KG-Based Explainable Disease Diagnosis* — Springer
7. Labrak et al. (2024) — *BioMistral: Open-Source Pretrained LLMs for Medical Domains* — ACL 2024
8. Chen et al. (2024) — *Meditron: Open Medical Foundation Models Adapted for Clinical Practice* — EPFL
9. Chicco & Jurman (2020) — *Machine learning can predict survival of patients with heart failure* — BMC Med. Inform. Decis. Mak. 20, 16
10. Edge et al. (2024) — *From Local to Global: A Graph RAG Approach* — Microsoft Research

**New MIMIC / VLM / Multimodal References:**

11. Johnson, A.E.W. et al. (2019) — *MIMIC-CXR: A De-identified Publicly Available Database of Chest Radiographs with Free-Text Reports* — Scientific Data 6, 317
12. Goldberger, A.L. et al. (2000) — *PhysioBank, PhysioToolkit, and PhysioNet: Components of a New Research Resource for Complex Physiologic Signals* — Circulation 101(23), e215–e220
13. Johnson, A.E.W. et al. (2023) — *MIMIC-IV: A Freely Accessible Electronic Health Record Dataset* — Scientific Data 10, 1
14. Johnson, A.E.W. et al. (2024) — *MIMIC-IV-Note: Deidentified Free-Text Clinical Notes* — PhysioNet
15. Irvin, J. et al. (2019) — *CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison* — AAAI 2019
16. Boecking, B. et al. (2022) — *Making the Most of Text Semantics to Improve Biomedical Vision–Language Processing (BioViL)* — ECCV 2022
17. Li, C. et al. (2023) — *LLaVA-Med: Training a Large Language-and-Vision Assistant for Biomedicine in One Day* — NeurIPS 2023
18. Zhang, Y. et al. (2023) — *PMC-VQA: Visual Instruction Tuning for Medical Visual Question Answering* — arXiv
19. Huang, S.-C. et al. (2021) — *Multimodal Fusion with Deep Neural Networks for Leveraging CT Imaging and EHR* — Scientific Reports 10, 1
20. Wang, X. et al. (2017) — *ChestX-ray8: Hospital-Scale Chest X-ray Database and Benchmarks* — CVPR 2017
21. Hayat, N. et al. (2022) — *MedCLIP: Contrastive Learning from Unpaired Medical Images and Text* — EMNLP 2022
22. Müller, P. et al. (2022) — *Joint Learning of Localized Representations from Medical Images and Reports* — ECCV 2022
23. Zhang, Y. et al. (2022) — *BiomedCLIP: A Multimodal Biomedical Foundation Model Pretrained from 15M Figure-Image Pairs* — arXiv
24. Moon, J.H. et al. (2022) — *Multi-Modal Understanding and Generation for Medical Images and Text via Vision-Language Pre-Training* — JBHI
25. Bannur, S. et al. (2023) — *BioViL-T: Learning to Exploit Temporal Context for Biomedical Vision–Language Processing* — CVPR 2023
26. Chen, Z. et al. (2024) — *CheXagent: Towards a Foundation Model for Chest X-Ray Interpretation* — arXiv
27. Miura, Y. et al. (2021) — *Improving Factual Completeness and Consistency of Image-to-Text Radiology Report Generation* — NAACL 2021
28. Nicolson, A. et al. (2023) — *Improving Chest X-Ray Report Generation by Leveraging Warm Starting* — Artificial Intelligence in Medicine
29. Yu, F. et al. (2023) — *Evaluating Progress in Automatic Chest X-Ray Radiology Report Generation* — Patterns

### Key Tools & Libraries

| Tool | Version | Install | Documentation |
|------|---------|---------|---------------|
| LangGraph | 1.0.9 | `pip install -U langgraph` | [docs.langchain.com/oss/python/langgraph](https://docs.langchain.com/oss/python/langgraph/overview) |
| Microsoft GraphRAG | 3.0.2 | `pip install graphrag` | [microsoft.github.io/graphrag](https://microsoft.github.io/graphrag/) |
| LangChain | latest | `pip install langchain` | [docs.langchain.com](https://docs.langchain.com/) |
| Neo4j Community | 5.x | Docker or installer | [neo4j.com/docs](https://neo4j.com/docs/) |
| Ollama | latest | [ollama.com](https://ollama.com/) | Local LLM serving |
| ChromaDB | latest | `pip install chromadb` | [docs.trychroma.com](https://docs.trychroma.com/) |
| scispaCy | latest | `pip install scispacy` | [allenai.github.io/scispacy](https://allenai.github.io/scispacy/) |
| NetworkX | latest | `pip install networkx` | Argumentation graph operations |
| Streamlit | latest | `pip install streamlit` | UI for visualization |
| MLflow | latest | `pip install mlflow` | Experiment tracking |
| Transformers | latest | `pip install transformers` | BioViL + LLaVA-Med model loading |
| BitsAndBytes | latest | `pip install bitsandbytes` | 4-bit quantisation for VLMs |
| Pillow | latest | `pip install Pillow` | CXR image loading and preprocessing |

### Quick Setup Commands

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install core dependencies
pip install -U langgraph langchain langchain-openai langchain-community
pip install graphrag chromadb neo4j
pip install scispacy networkx streamlit mlflow
pip install transformers torch accelerate bitsandbytes  # For VLM inference (BioViL, LLaVA-Med)
pip install Pillow  # CXR image loading

# Install medical NER model
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_lg-0.5.4.tar.gz

# Install Ollama and pull Meditron (for local inference)
# Download Ollama from https://ollama.com/
ollama pull meditron  # Or create custom Modelfile for Meditron
```

### Python Environment Requirements

```
Python >= 3.10
CUDA >= 12.0 (for GPU inference, optional)
RAM >= 16GB (32GB recommended for GraphRAG indexing)
Disk >= 50GB (for models and knowledge graph)
```

---

## Appendix A: Prototype Implementation Checklist

- [ ] **A1.** Set up Python environment with all dependencies (incl. transformers, bitsandbytes)
- [ ] **A2a.** Download surrogate datasets (MIMIC-IV Demo, NIH CXR14, OpenI)
- [ ] **A2b.** Complete CITI training + submit PhysioNet credentialing application
- [ ] **A3.** Download MIMIC subset upon credential approval (~2,000-3,000 frontal-view studies, 5-6 pathologies)
- [ ] **A4.** Set up Neo4j with medical ontology data (UMLS subset)
- [ ] **A5.** Run GraphRAG indexing on selected clinical guidelines (ACR Appropriateness, Fleischner, ESC)
- [ ] **A6.** Implement LangGraph state machine for multi-agent debate
- [ ] **A7.** Build Vision Agent pipeline: BioViL embeddings → CLIP image retrieval → LLaVA-Med 7B (4-bit) VQA
- [ ] **A8.** Build Report Agent pipeline: report section extractor → scispaCy NER → Meditron-8B (4-bit)
- [ ] **A9.** Build Clinical Agent pipeline: EHR-to-text serialiser → scispaCy NER → Meditron-8B (4-bit)
- [ ] **A10.** Write system prompts for Vision, Report, Clinical agents + Supervisor
- [ ] **A11.** Build CLIP-based Image RAG index (BioViL embeddings → ChromaDB image vectors)
- [ ] **A12.** Implement Dung's AAF with preferred extension computation
- [ ] **A13.** Implement Walton scheme classifier (LLM-based classification)
- [ ] **A14.** Build explanation generator (LLM + argumentation tree → narrative)
- [ ] **A15.** Implement all evaluation metrics (6 dimensions incl. cross-modal agreement, VLM faithfulness)
- [ ] **A16.** Run baseline experiments (B1–B4)
- [ ] **A17.** Run full system experiment (B5)
- [ ] **A18.** Run ablation experiments (A1–A7)
- [ ] **A19.** Run RAG infrastructure sweep (Run A, B, C)
- [ ] **A20.** Build Streamlit visualization dashboard (argumentation tree + CXR overlay)
- [ ] **A21.** Statistical significance testing
- [ ] **A22.** Generate figures and tables for report
- [ ] **A23.** Write dissertation report

---

## Appendix B: Example System Prompt Templates

### Vision Agent (Chest X-Ray)

```
You are a radiology AI specialist focused on chest X-ray (CXR) image
interpretation. You are part of a multidisciplinary team (MDT) debating
clinical findings for patients in the MIMIC-CXR dataset.

YOUR VISIBLE DATA (Modality Partition):
You can see ONLY:
- The chest X-ray image (frontal PA/AP view) for this study
- BioViL visual embeddings and CLIP-based image retrieval results
  (similar reference CXRs from the training set with known labels)
- LLaVA-Med 7B VQA outputs for the image (findings, pathology descriptions)

YOU CANNOT SEE:
- The radiology report text written by the radiologist
- Structured EHR data (demographics, vitals, labs, medications, diagnoses)

Principles:
- Report what you observe in the CXR image, using standard radiological
  terminology (opacities, effusions, consolidation, cardiomegaly, etc.)
- Reference CLIP-retrieved similar images to support your findings
  (e.g., "Retrieved reference images with confirmed pleural effusion show
  similar costophrenic angle blunting")
- Use Walton argumentation schemes to structure your arguments
- You will hear claims from other agents about report text and EHR data
  that you cannot independently verify — challenge them if they conflict
  with your visual observations
- Flag ambiguous findings (e.g., "Cannot distinguish small effusion from
  atelectasis at the left base — need report agent confirmation")
- Explicitly note image quality limitations (rotation, underexposure, etc.)

For each study, you will:
1. Describe key visual findings from the CXR image
2. State which CheXpert pathology labels your observations support
3. Present arguments using formal Walton argumentation schemes
4. Identify potential attacks on other agents' arguments
5. Note what data you LACK and how it limits your assessment
```

### Report Agent (Radiology Reports)

```
You are a clinical NLP specialist focused on radiology report
interpretation. You are part of a multidisciplinary team (MDT) debating
clinical findings for patients in the MIMIC dataset.

YOUR VISIBLE DATA (Modality Partition):
You can see ONLY:
- The free-text radiology report (Findings + Impression sections)
- scispaCy NER entities extracted from the report (diseases, anatomical
  structures, medications, procedures)
- Text-based RAG retrieval results from clinical guidelines

YOU CANNOT SEE:
- The actual chest X-ray image
- Structured EHR data (demographics, vitals, labs, medications, diagnoses)

Principles:
- Extract and interpret clinical findings from the radiology report text
- Distinguish between "Findings" (observations) and "Impression"
  (radiologist's interpretation/conclusions)
- Flag hedging language (e.g., "cannot exclude", "may represent",
  "questionable") — these indicate diagnostic uncertainty
- Use Walton argumentation schemes to structure your arguments
- You will hear claims from Vision Agent about image findings you cannot
  see — challenge them if they conflict with the written report
- Compare your extracted findings against guideline-based RAG retrievals
- Flag missing sections or dictation errors in the report

For each study, you will:
1. Extract key clinical findings from the radiology report
2. Map findings to CheXpert pathology labels
3. Present arguments using formal Walton argumentation schemes
4. Identify potential attacks on other agents' arguments
5. Note what data you LACK and how it limits your assessment
```

### Clinical Agent (Structured EHR)

```
You are a clinical data analyst specialising in structured electronic
health record (EHR) data interpretation. You are part of a multidisciplinary
team (MDT) debating clinical findings for patients in the MIMIC dataset.

YOUR VISIBLE DATA (Modality Partition):
You can see ONLY:
- Patient demographics (age bucket, sex)
- Admission information (admission type, location, insurance)
- Vital signs (heart rate, BP, SpO2, temperature, respiratory rate)
- Laboratory results (WBC, hemoglobin, creatinine, BNP, troponin, etc.)
- Active medications and infusions
- ICD diagnosis codes (current admission + prior history)
- Procedures performed

YOU CANNOT SEE:
- The chest X-ray image
- The radiology report text

Principles:
- Assess the patient's overall clinical context from structured data
- Flag abnormal lab values and vital signs with clinical significance
  (e.g., "Elevated BNP 1200 pg/mL suggests decompensated heart failure")
- Use ICD codes to establish prior history and comorbidity burden
- Use Walton argumentation schemes to structure your arguments
- You will hear claims from other agents about CXR findings and report
  text that you cannot independently verify — challenge them if they
  conflict with your structured data (e.g., "Report says no heart failure,
  but I see BNP > 1000 and prior ICD code for CHF")
- Assess pre-test probability of pathologies based on demographics,
  history, and labs before imaging evidence is considered

For each study, you will:
1. Summarise the patient's clinical context from structured EHR data
2. Assess which pathologies are likely given labs, vitals, and history
3. Present arguments using formal Walton argumentation schemes
4. Identify potential attacks on other agents' arguments
5. Note what data you LACK and how it limits your assessment
```

---

## Appendix C: Project Directory Structure

```
dissertation-project/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env                          # API keys (OpenAI, etc.)
│
├── data/
│   ├── mimic_cxr/                # MIMIC-CXR-JPG subset (PhysioNet 1.5.0)
│   │   ├── raw/                  # Frontal-view JPGs (~2,000-3,000 studies)
│   │   ├── processed/            # Resized/normalised images
│   │   └── embeddings/           # BioViL CLIP embeddings (pre-computed)
│   ├── mimic_iv_note/            # MIMIC-IV-Note radiology reports (PhysioNet 1.5.0)
│   │   ├── raw/                  # Original report CSVs
│   │   └── processed/            # Section-split reports (Findings/Impression)
│   ├── mimic_iv/                 # MIMIC-IV structured EHR (PhysioNet 1.5.0)
│   │   ├── raw/                  # Original CSV tables
│   │   └── processed/            # Linked & filtered per subject_id
│   ├── surrogates/               # Development datasets (fully public)
│   │   ├── mimic_iv_demo/        # MIMIC-IV Demo (100 patients)
│   │   ├── nih_cxr14/            # NIH ChestX-ray14 subset
│   │   └── openi/                # OpenI Indiana CXR reports
│   ├── knowledge/                # ACR/Fleischner/ESC guidelines PDFs
│   └── ontologies/               # UMLS, SNOMED, RadLex subsets
│
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── vision_agent.py       # Vision Agent (CXR image — BioViL + LLaVA-Med)
│   │   ├── report_agent.py       # Report Agent (radiology reports — Meditron-8B)
│   │   ├── clinical_agent.py     # Clinical Agent (structured EHR — Meditron-8B)
│   │   └── supervisor.py         # Debate moderator agent (full access)
│   ├── vlm/
│   │   ├── __init__.py
│   │   ├── biovil_encoder.py     # BioViL CLIP embedding extraction
│   │   ├── llava_med.py          # LLaVA-Med 7B inference (4-bit quantised)
│   │   └── image_rag.py          # CLIP-based image retrieval from ChromaDB
│   ├── argumentation/
│   │   ├── __init__.py
│   │   ├── framework.py          # Dung's AAF implementation
│   │   ├── schemes.py            # Walton scheme definitions
│   │   ├── resolver.py           # Preferred extension solver
│   │   └── explanation.py        # Argumentation → narrative
│   ├── knowledge/
│   │   ├── __init__.py
│   │   ├── graph_rag.py          # GraphRAG integration
│   │   ├── neo4j_client.py       # Neo4j operations
│   │   ├── kg_builder.py         # Build KG from sources
│   │   └── retriever.py          # Per-agent retrieval (text + image)
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── graph.py              # LangGraph state machine
│   │   ├── state.py              # DebateState definition
│   │   ├── modality_router.py    # Route CXR/report/EHR to correct agents
│   │   └── runner.py             # Experiment runner
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── cxr_loader.py         # MIMIC-CXR image loading + resizing
│   │   ├── report_parser.py      # Report section extraction (Findings/Impression)
│   │   ├── ehr_serialiser.py     # Structured EHR → text serialisation
│   │   └── subset_builder.py     # MIMIC subset selection (subject_id linking)
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics.py            # All evaluation metrics (6 dimensions)
│   │   ├── baselines.py          # Baseline implementations (B1-B5)
│   │   └── analysis.py           # Statistical analysis
│   └── utils/
│       ├── __init__.py
│       ├── medical_ner.py        # scispaCy entity extraction
│       └── prompts.py            # System prompt templates
│
├── ui/
│   └── app.py                    # Streamlit visualization (arg tree + CXR overlay)
│
├── experiments/
│   ├── configs/                  # Experiment configurations
│   ├── results/                  # Experiment outputs
│   └── notebooks/                # Analysis notebooks
│
├── tests/
│   ├── test_argumentation.py
│   ├── test_pipeline.py
│   ├── test_vlm.py
│   └── test_metrics.py
│
└── docs/
    ├── research_papers_literature_review.md
    ├── heriot-watt_ethics_guidelines.md
    ├── supervisor_meeting_notes.md
    └── dissertation_project_roadmap.md   # This document
```

---

*Roadmap created: February 2026 | Last updated: March 30, 2026 (MIMIC Pivot)*
*Based on: Literature review (35+ papers including 19 MIMIC/VLM), supervisor meeting notes, HWU ethics guidelines, MIMIC Feasibility Study, supervisor feedback on modality-based agent architecture*
