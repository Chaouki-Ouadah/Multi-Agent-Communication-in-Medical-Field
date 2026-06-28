# Literature Review: Multi-Agent Argumentation Frameworks with LLM-Augmented Reasoning in Healthcare Systems

## Project Overview

**Title:** Multi-Agent Argumentation Frameworks with LLM-Augmented Reasoning in Healthcare Systems

**Degree:** MSc in AI/Data Science (Graduation Project)

**Supervisor:** Radu-Casian Mihailescu

**Project Scope:** 25-50 pages + Prototype Implementation

---

## Topic Component Breakdown

The dissertation topic encompasses the following key components:

| ID | Component | Description |
|----|-----------|-------------|
| **C1** | Multi-Agent Systems (MAS) | Multiple AI agents representing modality-specialised roles (e.g., Vision Agent, Report Agent, Clinical Agent) |
| **C2** | Large Language Models (LLMs) | Using LLMs to express arguments in fluent, clinician-style language |
| **C3** | Clinical Decision-Making | Supporting healthcare professionals in treatment decisions |
| **C4** | Argumentation Frameworks | Structured debate and reasoning using formal argumentation theory |
| **C5** | Symbolic Reasoning | Combining neural approaches with symbolic/logical reasoning |
| **C6** | Explainability & Transparency | Making AI reasoning processes transparent and interpretable |
| **C7** | Human-in-the-Loop (HITL) | Enabling clinicians to follow, contest, and interact with AI justifications |
| **C8** | Retrieval-Augmented Generation (RAG) | Integrating external knowledge sources into LLM reasoning |
| **C9** | Trust in AI | Building clinician confidence through transparent reasoning |
| **C10** | Low-Data Adaptation | Functioning effectively with limited training data |
| **C11** | Vision Language Models (VLMs) | Using VLMs for medical image understanding and multimodal reasoning |
| **C12** | Multimodal Data Fusion | Combining different clinical data modalities (images, text, EHR) |

---

## Research Papers

### Legend
- ⭐⭐⭐⭐⭐ = Directly matches topic (essential reading)
-
- ⭐⭐⭐⭐ = Highly relevant (strongly recommended)
- ⭐⭐⭐ = Relevant (recommended)
- ⭐⭐ = Partially relevant (supplementary)

---

## Category 1: Core Papers (Multi-Agent + Argumentation + LLM + Healthcare)

These papers directly address the intersection of all major topic components.

---

### 1. ArgMed-Agents: Explainable Clinical Decision Reasoning with LLM Discussion via Argumentation Schemes

| Field | Details |
|-------|---------|
| **Authors** | S. Hong, L. Xiao, X. Zhang, J. Chen |
| **Venue** | IEEE International Conference on Bioinformatics and Biomedicine (BIBM) |
| **Year** | 2024 |
| **Citations** | 24 |
| **Links** | [IEEE](https://ieeexplore.ieee.org/abstract/document/10822109/) &#124; [arXiv PDF](https://arxiv.org/pdf/2403.06294) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
ArgMed-Agents is a multi-agent framework that enables LLM-based agents to mimic clinical argumentative reasoning. The system uses argumentation schemes—formal patterns of reasoning—to structure debates between agents about clinical decisions. Agents generate explanations in a self-directed manner, improving accuracy in complex clinical decision reasoning compared to standard prompting methods.

**How it relates to your project:**
This is the closest existing work to your proposed system. It provides:
- A concrete implementation of multi-agent LLM debate for clinical decisions
- Integration of formal argumentation theory with LLMs
- Explainability through structured reasoning patterns
- Benchmark results you can compare against

**Key insights for your project:**
- Uses Walton's argumentation schemes as the theoretical foundation
- Demonstrates that structured debate improves LLM reasoning accuracy
- Provides methodology for formalizing clinical discussion as argumentation

---

### 2. MedGen: An Explainable Multi-Agent Architecture for Clinical Decision Support through Multisource Knowledge Fusion

| Field | Details |
|-------|---------|
| **Authors** | Z. Liu, L. Xiao, R. Zhu, H. Yang, M. He |
| **Venue** | IEEE BIBM |
| **Year** | 2024 |
| **Citations** | 4 |
| **Links** | [IEEE](https://ieeexplore.ieee.org/abstract/document/10822186/) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ✅ | ✅ | ⚪ |

**Summary:**
MedGen decomposes clinical decision-making into distinct stages: clinical goal setting, data collection, argumentation linking, and plan selection. This multi-agent architecture allows LLM agents to provide both reasoning evidence and a transparent reasoning process, enhancing reliability and interpretability.

**How it relates to your project:**
- Demonstrates staged decomposition of clinical reasoning (valuable for your prototype architecture)
- Shows how to fuse multiple knowledge sources with argumentation
- Addresses multidisciplinary team collaboration through agents

**Key insights for your project:**
- Modular architecture design separating concerns (goal → data → argument → decision)
- Combines RAG with argumentation for evidence-backed reasoning

---

### 3. An Interaction Model for Merging Multi-Agent Argumentation in Shared Clinical Decision Making

| Field | Details |
|-------|---------|
| **Authors** | S. Hong, L. Xiao, J. Chen |
| **Venue** | IEEE BIBM |
| **Year** | 2023 |
| **Citations** | 2 |
| **Links** | [IEEE](https://ieeexplore.ieee.org/abstract/document/10386040/) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ |

**Summary:**
This paper constructs a cognitive representation model of agents supporting computational argumentation and proposes a novel interactive argumentation framework merging method for shared decision support in healthcare. It designs an argumentation knowledge graph applicable to clinical decision making.

**How it relates to your project:**
- Foundational work for the same research group as ArgMed-Agents
- Focuses on **shared decision making** (aligning with your HITL emphasis)
- Introduces argumentation knowledge graphs—useful for your symbolic reasoning component

**Key insights for your project:**
- Knowledge graph structure for representing clinical arguments
- Interaction protocols for merging multiple agent perspectives

---

### 4. An Adaptive Multi-Agent LLM-Based Clinical Decision Support System Integrating Biomedical RAG and Web Intelligence

| Field | Details |
|-------|---------|
| **Authors** | Ç. U. Öğdü, K. Arslanoğlu, M. Karaköse |
| **Venue** | IEEE Access |
| **Year** | 2025 |
| **Citations** | 1 |
| **Links** | [IEEE](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11176078) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ✅ | ✅ |

**Summary:**
Proposes a multi-layered, adaptive Clinical Decision Support System (CDSS) comprising interacting LLM agents. Addresses shortcomings in timeliness, multi-source evidence fusion, and confidence calibration through biomedical RAG and web intelligence integration.

**How it relates to your project:**
- State-of-the-art RAG integration for clinical LLM agents
- Addresses confidence calibration (relevant to trust)
- Adaptive system design applicable to varying data availability

**Key insights for your project:**
- Architecture for integrating real-time web intelligence with biomedical knowledge
- Multi-layered agent design patterns

---

### 5. Improving Clinical Decision Support: Architecture Design of a Multi-agent System based on an Argument Quality Assessment Ontology

| Field | Details |
|-------|---------|
| **Authors** | P. Liu, L. Xiao |
| **Venue** | IEEE CBMS |
| **Year** | 2025 |
| **Citations** | - |
| **Links** | [IEEE](https://ieeexplore.ieee.org/abstract/document/10978916/) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Introduces an ontology for assessing argument quality in multi-agent clinical decision support. The experimental results show that the approach improves the quality and reliability of clinical decisions.

**How it relates to your project:**
- Provides formal methods for evaluating argument quality
- Ontology-based approach connects to symbolic reasoning requirements
- Quality assessment is crucial for your explainability goals

---

## Category 2: Multi-Agent Systems in Healthcare

---

### 6. Multi-agent Systems for Clinical Decision Support: A Systematic Review

| Field | Details |
|-------|---------|
| **Authors** | A. L. Silveira, R. da Rosa Righi, C. A. Da Costa |
| **Venue** | Applied Soft Computing |
| **Year** | 2025 |
| **Links** | [Elsevier](https://www.sciencedirect.com/science/article/pii/S1568494625017600) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Comprehensive systematic review covering multi-agent reinforcement learning (MARL), ontology-based medical knowledge representation, and generative AI—particularly LLMs—in clinical decision support systems. Addresses cross-cutting concerns including explainability.

**How it relates to your project:**
- **Essential for your literature review chapter**
- Provides comprehensive taxonomy of MAS approaches in healthcare
- Identifies research gaps you can position your work against

**Key insights for your project:**
- Use this to structure your related work section
- Identifies open challenges your project can address

---

### 7. Mitigating Cognitive Biases in Clinical Decision-Making through Multi-Agent Conversations Using Large Language Models: Simulation Study

| Field | Details |
|-------|---------|
| **Authors** | Y. Ke, R. Yang, S. A. Lie, T. X. Y. Lim, Y. Ning, I. Li |
| **Venue** | Journal of Medical Internet Research (JMIR) |
| **Year** | 2024 |
| **Citations** | 64 |
| **Links** | [JMIR](https://www.jmir.org/2024/1/e59439/) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Simulates clinical decision-making processes through multi-agent LLM conversations to mitigate cognitive biases. Demonstrates that agent debate can overcome biases that affect individual reasoning.

**How it relates to your project:**
- Directly supports your thesis that multi-agent debate improves clinical decisions
- Provides experimental methodology for evaluating bias mitigation
- High citation count indicates influential work

**Key insights for your project:**
- Agent role design for diverse perspectives (domain-partitioned specialists with information asymmetry)
- Evaluation metrics for cognitive bias reduction
- Demonstrates that multi-agent debate can overcome biases in individual reasoning — supports your information partitioning hypothesis

---

### 8. Development of a Large Language Model-based Multi-Agent Clinical Decision Support System for KTAS-Based Triage and Treatment Planning in Emergency Departments

| Field | Details |
|-------|---------|
| **Authors** | S. Han, W. Choi |
| **Venue** | Advances in Artificial Intelligence and Machine Learning |
| **Year** | 2024 |
| **Citations** | 16 |
| **Links** | [arXiv PDF](https://arxiv.org/pdf/2408.07531.pdf) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Multi-agent CDSS using Llama-3-70b for emergency department triage. Demonstrates scalable and adaptable multi-agent design that could enhance emergency medical care delivery.

**How it relates to your project:**
- Practical implementation example of multi-agent LLM in real clinical workflow
- Emergency medicine use case complements your treatment decision focus

---

## Category 3: Argumentation Frameworks & Explainability

---

### 9. Applying Metalevel Argumentation Frameworks to Support Medical Decision Making

| Field | Details |
|-------|---------|
| **Authors** | N. Kökciyan, I. Sassoon, E. Sklar, S. Modgil |
| **Venue** | IEEE Intelligent Systems |
| **Year** | 2021 |
| **Citations** | 44 |
| **Links** | [IEEE](https://ieeexplore.ieee.org/abstract/document/9321341/) &#124; [PDF](https://www.research.ed.ac.uk/files/190718426/Applying_Metalevel_KOKCIYAN_DOA04012021_AFV.pdf) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ |

**Summary:**
Introduces metalevel argumentation frameworks that enable reasoning about argument strength, preferences, and conflicts in medical DSS. Highlights key factors underlying decisions for healthcare professionals.

**How it relates to your project:**
- **Foundational theoretical work** for argumentation in medical AI
- Metalevel reasoning allows explaining *why* certain arguments win
- Directly addresses HITL by making reasoning transparent to clinicians

**Key insights for your project:**
- Argumentation semantics (grounded, preferred, stable extensions)
- Metalevel frameworks for preference handling

---

### 10. Engineering Explainable Agents: An Argumentation-Based Approach

| Field | Details |
|-------|---------|
| **Authors** | A. R. Panisson, D. C. Engelmann, R. H. Bordini |
| **Venue** | Engineering Multi-Agent Systems (EMAS) |
| **Year** | 2021 |
| **Citations** | 29 |
| **Links** | [Springer](https://link.springer.com/chapter/10.1007/978-3-030-97457-2_16) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ |

**Summary:**
Presents an argumentation-based approach for engineering explainable agents, with a healthcare application example. Agents can explain their reasoning through argumentation structures.

**How it relates to your project:**
- Provides engineering methodology for building explainable agents
- Healthcare domain example directly applicable
- BDI (Belief-Desire-Intention) agent architecture with argumentation

**Key insights for your project:**
- Agent architecture patterns for explainability
- Integration of argumentation into agent reasoning cycle

---

### 11. Linked Argumentation Graphs for Multidisciplinary Decision Support

| Field | Details |
|-------|---------|
| **Authors** | L. Xiao, D. Greer |
| **Venue** | Healthcare (MDPI) |
| **Year** | 2023 |
| **Citations** | 1 |
| **Links** | [MDPI](https://www.mdpi.com/2227-9032/11/4/585) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ |

**Summary:**
Proposes linked argumentation graphs for representing and integrating arguments from multiple medical professionals in multidisciplinary team settings.

**How it relates to your project:**
- Graph-based representation for your argumentation visualization
- Addresses multidisciplinary collaboration (maps to your diverse agent perspectives)

---

### 12. A Systematic Review of Argumentation Techniques for Multi-Agent Systems Research

| Field | Details |
|-------|---------|
| **Authors** | Á. Carrera, C. A. Iglesias |
| **Venue** | Artificial Intelligence Review |
| **Year** | 2015 |
| **Citations** | 73 |
| **Links** | [Springer](https://link.springer.com/article/10.1007/S10462-015-9435-9) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Comprehensive review of argumentation techniques in MAS research. Covers Dung's abstract argumentation framework and various extensions.

**How it relates to your project:**
- **Theoretical foundation** for argumentation in MAS
- Taxonomy of argumentation approaches you can build upon

**Key insights for your project:**
- Classification of argumentation frameworks
- Integration patterns with agent communication

---

### 13. Intentional Dialogues in Multi-Agent Systems Based on Ontologies and Argumentation

| Field | Details |
|-------|---------|
| **Authors** | D. C. Engelmann |
| **Venue** | PhD Thesis, PUCRS |
| **Year** | 2023 |
| **Links** | [PDF](https://repositorio.pucrs.br/dspace/bitstream/10923/26769/1/000509135-Texto%2Bcompleto-0.pdf) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ |

**Summary:**
PhD thesis combining MAS, ontologies, and argumentation for healthcare decision support (hospital bed allocation). Provides comprehensive theoretical and implementation details.

**How it relates to your project:**
- Full thesis on closely related topic—excellent reference for structure
- Combines symbolic (ontology) with argumentation
- Healthcare application with explainability focus

---

## Category 4: LLM Clinical Reasoning & Explainability

---

### 14. Diagnostic Reasoning Prompts Reveal the Potential for Large Language Model Interpretability in Medicine

| Field | Details |
|-------|---------|
| **Authors** | T. Savage, A. Nayak, R. Gallo, E. Rangan |
| **Venue** | NPJ Digital Medicine |
| **Year** | 2024 |
| **Citations** | 284 |
| **Links** | [Nature](https://www.nature.com/articles/s41746-024-01010-1) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Develops diagnostic reasoning prompts that enable LLMs to imitate clinical reasoning processes, revealing interpretability potential. High-impact work demonstrating LLMs can produce clinician-style explanations.

**How it relates to your project:**
- Provides prompting strategies for eliciting clinical reasoning from LLMs
- Demonstrates LLM capability to match clinician cognitive processes
- Very high citation count—foundational for LLM clinical reasoning

**Key insights for your project:**
- Prompt engineering for clinical reasoning
- Evaluation methodology for reasoning quality

---

### 15. Large Language Models are Clinical Reasoners: Reasoning-Aware Diagnosis Framework with Prompt-Generated Rationales

| Field | Details |
|-------|---------|
| **Authors** | T. Kwon, K. T. Ong, D. Kang, S. Moon, J. R. Lee |
| **Venue** | AAAI |
| **Year** | 2024 |
| **Citations** | 52 |
| **Links** | [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/29802) &#124; [PDF](https://ojs.aaai.org/index.php/AAAI/article/download/29802/31388) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Proposes a reasoning-aware diagnosis framework that generates rationales alongside diagnoses. Published at top AI venue (AAAI).

**How it relates to your project:**
- Methodology for rationale generation applicable to your LLM agents
- Benchmark framework for clinical reasoning evaluation

---

### 16. Enhancing LLM-based Clinical Reasoning in Anesthesiology via Graph-Augmented Retrieval and Explainable Generation

| Field | Details |
|-------|---------|
| **Authors** | M. Wang, Y. Shen, B. Zhao, X. Zhou, L. Sun |
| **Venue** | Health Information Science and Systems |
| **Year** | 2025 |
| **Citations** | 2 |
| **Links** | [Springer](https://link.springer.com/article/10.1007/s13755-025-00379-x) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ⚪ |

**Summary:**
Uses graph-based RAG framework to improve LLM analytical reasoning in anesthesiology. Combines knowledge graphs with RAG for explainable generation.

**How it relates to your project:**
- Graph-RAG architecture directly applicable to your prototype
- Combines symbolic (graph) with neural (LLM) approaches

---

### 17. Advances, Evaluation, and Explainability of Large Language Models in Healthcare: A Systematic Review

| Field | Details |
|-------|---------|
| **Authors** | S. U. Amin, M. Guizani, M. S. Hossain |
| **Venue** | ACM Transactions on Multimedia Computing |
| **Year** | 2025 |
| **Links** | [ACM](https://dl.acm.org/doi/abs/10.1145/3786334) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Systematic review covering LLM advances, evaluation methods, and explainability in healthcare. Addresses model transparency challenges in high-stakes care.

**How it relates to your project:**
- Comprehensive overview of LLM healthcare explainability
- Evaluation frameworks for your prototype assessment

---

### 18. A Prompt Framework for Enhancing LLM-based Explainability of Medical Machine Learning Models

| Field | Details |
|-------|---------|
| **Authors** | S. Lee, W. I. Cho, Y. Lee, D. J. Kim, K. H. Nam |
| **Venue** | BMC Medical Informatics and Decision Making |
| **Year** | 2025 |
| **Links** | [Springer](https://link.springer.com/article/10.1186/s12911-025-03239-6) |

**Relevance:** ⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Zero-shot prompting framework for LLM-based explainability of ML predictions in ICU settings. No fine-tuning required.

**How it relates to your project:**
- Practical prompting techniques for clinical explainability
- Zero-shot approach relevant to low-data scenarios

---

## Category 5: Explainability in Multi-Agent Systems (Theoretical Foundations)

---

### 19. Towards XMAS: Explainability through Multi-Agent Systems

| Field | Details |
|-------|---------|
| **Authors** | G. Ciatto, R. Calegari, A. Omicini |
| **Venue** | CEUR Workshop |
| **Year** | 2019 |
| **Citations** | 39 |
| **Links** | [PDF](https://cris.unibo.it/bitstream/11585/707345/3/paper3.pdf) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ⚪ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Proposes XMAS (eXplainable Multi-Agent Systems) framework arguing that MAS architecture naturally supports explainability. Discusses multiparty argumentation protocols.

**How it relates to your project:**
- Theoretical foundation for MAS-based explainability
- XMAS concept directly applicable to your system design

---

### 20. In-Time Explainability in Multi-Agent Systems: Challenges, Opportunities, and Roadmap

| Field | Details |
|-------|---------|
| **Authors** | F. Alzetta, P. Giorgini, A. Najjar, M. I. Schumacher |
| **Venue** | Engineering Multi-Agent Systems (EMAS/Springer) |
| **Year** | 2020 |
| **Citations** | 44 |
| **Links** | [Springer](https://link.springer.com/chapter/10.1007/978-3-030-51924-7_3) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ✅ | ⚪ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ |

**Summary:**
Discusses real-time explainability in BDI Multi-Agent Systems for healthcare applications without direct medical supervision. Proposes RTX-BDI-MAS framework.

**How it relates to your project:**
- Real-time explainability requirements for clinical settings
- BDI agent architecture with explainability extensions

---

## Category 6: RAG and Knowledge Integration

---

### 21. Multi-Agent Retrieval Augmented Generation for Clinical Decision Support: A Systematic Review and Integrative Conceptual Framework

> ⚠️ **QUALITY FLAG:** Published in Journal of Applied Informatics and Computation (Politeknik Negeri Batam, Indonesia). Not indexed in Scopus or Web of Science. Stronger RAG papers are available (#23–#24).

| Field | Details |
|-------|---------|
| **Authors** | T. Mugambiwa, B. Ndlovu |
| **Venue** | Journal of Applied Informatics and Computation |
| **Year** | 2026 |
| **Links** | [Publisher](https://jurnal.polibatam.ac.id/index.php/JAIC/article/view/11900) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ |

**Summary:**
Systematic review and conceptual framework for multi-agent RAG systems in clinical decision support.

**How it relates to your project:**
- **Directly addresses your RAG+MAS combination**
- Provides framework for integrating retrieval with multi-agent architecture

---

### 22. Emerging Medical Informatics with Case-Based Reasoning for Aiding Clinical Decision in Multi-Agent System

| Field | Details |
|-------|---------|
| **Authors** | Y. Shen, J. Colloc, A. Jacquet-Andrieu, K. Lei |
| **Venue** | Journal of Biomedical Informatics |
| **Year** | 2015 |
| **Citations** | 103 |
| **Links** | [Elsevier](https://www.sciencedirect.com/science/article/pii/S1532046415001227) |

**Relevance:** ⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Multi-agent architecture with case-based reasoning covering the whole clinical decision-making cycle.

**How it relates to your project:**
- Case-based reasoning as alternative/complement to RAG
- High citation count—established work in MAS for clinical decisions

---

### 23. Retrieval Augmented Generation for 10 Large Language Models and Its Generalizability in Assessing Medical Fitness

| Field | Details |
|-------|---------|
| **Authors** | Y. H. Ke, L. Jin, K. Elangovan, H. R. Abdullah, N. Liu, et al. |
| **Venue** | npj Digital Medicine (Nature) |
| **Year** | 2025 |
| **Links** | [Nature](https://doi.org/10.1038/s41746-025-01519-z) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ |

**Summary:**
Evaluates RAG across 10 LLMs (GPT-3.5, GPT-4, GPT-4o, Gemini, Llama 2/3, Claude) for assessing surgical fitness using 35 local and 23 international guidelines across 14 clinical scenarios (3,234 responses vs. 448 human answers). Published in a top-tier digital medicine venue.

**How it relates to your project:**
- Provides experimental methodology for comparing RAG performance across multiple LLMs — directly applicable to your infrastructure sweep comparing Vector RAG / GraphRAG / Hybrid
- Demonstrates RAG evaluation metrics (accuracy, consistency, safety) in clinical contexts
- Top-tier venue (npj Digital Medicine) — strong citation for RAG efficacy claims

---

### 24. Retrieval Augmented Generation for Large Language Models in Healthcare: A Systematic Review

| Field | Details |
|-------|---------|
| **Authors** | L. M. Amugongo, P. Mascheroni, S. Brooks, S. Doering, J. Seidel |
| **Venue** | PLOS Digital Health |
| **Year** | 2025 |
| **Links** | [PLOS](https://doi.org/10.1371/journal.pdig.0000877) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ |

**Summary:**
Systematic review of RAG applications for LLMs in healthcare. Surveys the RAG landscape, identifies common architectures, evaluation approaches, and open challenges. Full peer-review history available.

**How it relates to your project:**
- Comprehensive landscape survey of RAG in healthcare — positions your Vector/Graph/Hybrid comparison within the broader literature
- Identifies gaps in RAG evaluation methodology that your infrastructure sweep can address
- Peer-reviewed with transparent review history (PLOS) — strong methodological reference

---

## Category 7: Foundational Argumentation Theory

> These papers provide the theoretical and computational foundations for the formal argumentation layer (Dung's AAF, ASPIC+) used in the system's symbolic reasoning component.

---

### 25. An Abstract Framework for Argumentation with Structured Arguments (ASPIC+)

| Field | Details |
|-------|---------|
| **Authors** | H. Prakken |
| **Venue** | Utrecht University, Technical Report UU-CS-2009-019 |
| **Year** | 2009 |
| **Links** | [PDF available in project] |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ⚪ | ⚪ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Defines the ASPIC+ framework — a comprehensive formal framework for argumentation that extends Dung's abstract argumentation with structured arguments, defeasible reasoning rules, preference orderings, and contrariness relations. One of the most influential formalizations of structured argumentation.

**How it relates to your project:**
- **Foundational reference** for your symbolic reasoning layer — ASPIC+ extends Dung's AAF to handle structured, domain-specific arguments
- Provides the formal underpinning for how agent-generated arguments can be structured, attacked, and defeated
- Connects Walton's argumentation schemes (used in ArgMed-Agents) to formal semantics

**Key insights for your project:**
- Strict vs. defeasible rules for medical reasoning
- Preference orderings for resolving conflicts between agent arguments
- How to extend abstract argumentation to structured clinical arguments

> ℹ️ **Note:** This is a technical report, not a peer-reviewed journal paper. However, it is one of the most cited argumentation theory papers (1000+ citations across versions) and the definitive ASPIC+ reference. Acceptable as a foundational citation.

---

### 26. Methods for Solving Reasoning Problems in Abstract Argumentation — A Survey

| Field | Details |
|-------|---------|
| **Authors** | G. Charwat, W. Dvořák, S. A. Gaggl, J. P. Wallner, S. Woltran |
| **Venue** | Artificial Intelligence (Elsevier) |
| **Year** | 2015 |
| **Links** | [Elsevier](https://doi.org/10.1016/j.artint.2014.11.008) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Comprehensive survey of algorithms and computational methods for Dung's abstract argumentation frameworks. Covers grounded, preferred, stable, and semi-stable semantics; reduction-based approaches; direct algorithms; and argumentation solvers. Published in the top AI journal (Artificial Intelligence, Elsevier).

**How it relates to your project:**
- **Essential reference** for implementing Dung's AAF computations — your system needs to compute argument extensions (grounded/preferred semantics) to determine which agent arguments are accepted
- Reviews solver implementations that could inform your prototype's argumentation engine
- Published in the premier AI journal — top-tier citation

**Key insights for your project:**
- Computational complexity of different semantics (relevant to your scalability analysis)
- Algorithms for computing extensions that your prototype can implement
- Benchmark approaches for evaluating argumentation framework performance

---

### 27. On the Acceptability of Arguments and its Fundamental Role in Nonmonotonic Reasoning, Logic Programming and n-Person Games

| Field | Details |
|-------|---------|
| **Authors** | P. M. Dung |
| **Venue** | Artificial Intelligence (Elsevier), Vol. 77, Issue 2, pp. 321–357 |
| **Year** | 1995 |
| **Citations** | 4,042+ |
| **DOI** | [10.1016/0004-3702(94)00041-X](https://doi.org/10.1016/0004-3702(94)00041-X) |
| **Links** | [Elsevier](https://doi.org/10.1016/0004-3702(94)00041-X) &#124; [PDF available in project] |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
The foundational paper that introduced Abstract Argumentation Frameworks (AAFs). Defines attack relations, extensions (grounded, preferred, stable), and acceptability semantics. The most cited paper in computational argumentation — the theoretical backbone of your entire symbolic reasoning layer.

**How it relates to your project:**
- **MUST-CITE** — Dung's AAF is the core of your argumentation engine. Without this citation, the theoretical foundation is ungrounded
- Defines the semantics (grounded, preferred, stable extensions) your system uses to resolve agent disagreements
- Connects argumentation to nonmonotonic reasoning — relevant to defeasible clinical reasoning

---

## Category 8: Trust & Human-Centred AI in Healthcare

> Trust and human-centred design are critical for clinician adoption of AI-based CDSS. These papers support the Trust evaluation dimension (SRQ4) and HITL design principles.

---

### 28. From Trust in Automation to Trust in AI in Healthcare: A 30-Year Longitudinal Review and an Interdisciplinary Framework

| Field | Details |
|-------|---------|
| **Authors** | K. K. L. Wong, Y. Han, Y. Cai, W. Ouyang, H. Du, C. Liu |
| **Venue** | Bioengineering (MDPI) |
| **Year** | 2025 |
| **Links** | [MDPI](https://doi.org/10.3390/bioengineering12101070) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ✅ | ⚪ |

**Summary:**
30-year longitudinal review tracing the evolution from trust in automation to trust in AI in healthcare. Proposes an interdisciplinary framework integrating psychological, technical, and clinical perspectives on AI trust.

**How it relates to your project:**
- Directly supports your Trust evaluation dimension — provides a comprehensive theoretical framework for measuring and analysing trust in your system
- Historical perspective grounds your trust metrics in established literature
- The interdisciplinary framework can inform your Discussion chapter on clinician trust implications

---

### 29. Trust in Artificial Intelligence–Based Clinical Decision Support Systems Among Health Care Workers: Systematic Review

| Field | Details |
|-------|---------|
| **Authors** | H. M. Tun, H. A. Rahman, L. Naing, O. A. Malik |
| **Venue** | JMIR Medical Informatics |
| **Year** | 2025 |
| **Links** | [JMIR](https://doi.org/10.2196/65897) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ✅ | ⚪ |

**Summary:**
Systematic review of factors influencing health care workers' trust in AI-based CDSS. Synthesises evidence on trust barriers, facilitators, and design recommendations for trustworthy AI-CDSS.

**How it relates to your project:**
- Provides synthesised evidence on what makes clinicians trust (or distrust) AI-CDSS — directly informs your design decisions
- Actionable recommendations for building trust through transparency and explainability — validates your argumentation-based explainability approach

---

### 30. Solving the Explainable AI Conundrum by Bridging Clinicians' Needs and Developers' Goals

| Field | Details |
|-------|---------|
| **Authors** | N. Bienefeld, J. M. Boss, R. Lüthy, D. Brodbeck, J. Azzati, M. Blaser, J. Willms, E. Keller |
| **Venue** | npj Digital Medicine (Nature) |
| **Year** | 2025 |
| **Links** | [Nature](https://doi.org/10.1038/s41746-023-00837-4) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |

**Summary:**
Longitudinal multi-method study with 112 developers and clinicians co-designing an XAI solution for a CDSS. Identifies three key differences between developer and clinician mental models: opposing goals (model interpretability vs. clinical plausibility), different sources of truth (data vs. patient), and exploration vs. exploitation of knowledge.

**How it relates to your project:**
- Provides evidence-based design recommendations for XAI in CDSS — your argumentation-based explanations must bridge the developer-clinician gap identified here
- The "clinical plausibility" requirement validates your approach of using domain-specific clinical language in agent outputs
- Published in npj Digital Medicine (Nature) — very high impact

---

### 31. Co-design of Human-centered, Explainable AI for Clinical Decision Support

| Field | Details |
|-------|---------|
| **Authors** | C. Panigutti, A. Beretta, D. Fadda, F. Giannotti, D. Pedreschi, A. Perotti, et al. |
| **Venue** | ACM Transactions on Interactive Intelligent Systems |
| **Year** | 2023 |
| **Citations** | 63 |
| **Links** | [ACM](https://doi.org/10.1145/3587271) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ |

**Summary:**
Co-design methodology for building human-centred XAI for clinical decision support. Involves clinicians in the iterative design process to ensure explanations meet actual clinical needs rather than developer assumptions.

**How it relates to your project:**
- Provides co-design methodology applicable to your HITL interface design
- Demonstrates that clinician involvement in explanation design improves trust and adoption
- ACM Tier A venue with 63 citations — strong methodological reference

---

## Category 9: LLM Reasoning, Debate Quality & Information Partitioning

> These papers critically examine LLM reasoning capabilities, multi-agent debate effectiveness, and the theoretical foundations of information partitioning — essential for understanding the strengths and limitations of your LLM-augmented argumentation system and justifying the Direction 1 architecture.

---

### 32. Critique of Impure Reason: Unveiling the Reasoning Behaviour of Medical Large Language Models

| Field | Details |
|-------|---------|
| **Authors** | S. Z. Y. Sim, T. Chen |
| **Venue** | eLife |
| **Year** | 2025 |
| **Links** | [eLife](https://doi.org/10.7554/eLife.106187) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Critical analysis of reasoning behaviour in medical LLMs. Emphasises that understanding reasoning behaviour is equivalent to explainable AI (XAI) in the medical LLM context. Surveys and categorises approaches for modelling and evaluating reasoning in medical LLMs. Proposes theoretical frameworks for empowering medical professionals to evaluate LLM reasoning quality.

**How it relates to your project:**
- Provides a framework for evaluating the reasoning quality of your LLM agents — crucial for demonstrating that your agents produce valid clinical reasoning, not just plausible-sounding text
- The emphasis on reasoning behaviour over prediction accuracy aligns with your explainability goals
- eLife is a highly respected open-access journal (Diamond OA, rigorous peer review)

---

### 33. Twenty-Five Years of Hidden Profiles in Group Decision Making: A Meta-Analysis

| Field | Details |
|-------|---------|
| **Authors** | L. Lu, Y. C. Yuan, P. L. McLeod |
| **Venue** | Personality and Social Psychology Review |
| **Year** | 2012 |
| **Citations** | 180 |
| **DOI** | [10.1177/1088868311417243](https://doi.org/10.1177/1088868311417243) |
| **Links** | [SAGE](https://doi.org/10.1177/1088868311417243) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Comprehensive meta-analysis of 25 years of research on the "hidden profile" paradigm in group decision making. Hidden profiles are decision tasks where the optimal choice can only be identified if group members pool their uniquely held (unshared) information. The meta-analysis synthesizes findings on when and why groups fail to share unique information and identifies moderators (task demonstrability, group size, information distribution) that affect information pooling and decision quality.

**How it relates to your project:**
- **Foundational justification for your Direction 1 (Information Partitioning) architecture** — your system deliberately creates hidden profiles by partitioning features across agents so that no single agent sees the full picture. The meta-analysis provides the theoretical basis from social psychology for why this design can improve collective decision quality when combined with structured information exchange (argumentation)
- Identifies conditions under which hidden-profile groups succeed vs. fail — directly informs your argumentation protocol design to ensure agents actually share their unique information
- The finding that "task demonstrability" moderates success supports your use of formal argumentation (which makes reasoning explicit and demonstrable)

**Key insights for your project:**
- Information partitioning creates a hidden profile; structured argumentation is the mechanism for pooling
- Meta-analytic evidence that discussion quality (not just quantity) determines hidden-profile resolution
- Published in Personality and Social Psychology Review (top-tier) — strong citation for your theoretical framing

---

### 34. Group Decision Making in Hidden Profile Situations: Dissent as a Facilitator for Decision Quality

| Field | Details |
|-------|---------|
| **Authors** | S. Schulz-Hardt, F. C. Brodbeck, A. Mojzisch, R. Kerschreiter, D. Frey |
| **Venue** | Journal of Personality and Social Psychology |
| **Year** | 2006 |
| **Citations** | 390 |
| **DOI** | [10.1037/0022-3514.91.6.1080](https://doi.org/10.1037/0022-3514.91.6.1080) |
| **Links** | [APA](https://doi.org/10.1037/0022-3514.91.6.1080) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Experimental study demonstrating that *dissent* (genuine disagreement among group members with different information) is a critical facilitator for decision quality in hidden profile situations. Groups with pre-discussion dissent pooled significantly more unshared information and reached better decisions than homogeneous groups. The effect is driven by information exchange, not mere preference diversity.

**How it relates to your project:**
- **Directly validates your multi-agent argumentation design** — your agents are designed to disagree (because they see different feature partitions) and resolve disagreements through formal argumentation. This paper provides empirical evidence that such disagreement improves information pooling and decision quality
- Supports the hypothesis that your information-partitioned agents will outperform a single agent with access to all features (ablation A3), because the structured disagreement forces information to surface
- The finding that *information exchange* (not preference diversity alone) drives the effect validates your argumentation protocol as the mechanism for extracting value from partitioning

**Key insights for your project:**
- Dissent from different information ≠ dissent from different attitudes — supports Direction 1 over attitudinal role design
- Information exchange is the mechanism, not mere exposure to diverse opinions
- Published in JPSP (the top social psychology journal) with 390 citations — very strong citation

---

## Category 10: MIMIC Datasets & Domain Context

These papers describe the MIMIC ecosystem datasets used in the project and the CheXpert labeling infrastructure.

---

### 35. MIMIC-CXR: A De-identified Publicly Available Database of Chest Radiographs with Free-Text Reports

| Field | Details |
|-------|---------|
| **Authors** | A. E. W. Johnson, T. J. Pollard, S. J. Berkowitz, N. R. Greenbaum, M. P. Lungren, C.-Y. Deng, R. G. Mark, S. Horng |
| **Venue** | Scientific Data (Nature) |
| **Year** | 2019 |
| **DOI** | [10.1038/s41597-019-0322-0](https://doi.org/10.1038/s41597-019-0322-0) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |

**Summary:**
Foundational paper describing the MIMIC-CXR database of 377,110 chest radiographs with associated free-text radiology reports from 65,379 patients at Beth Israel Deaconess Medical Center. Images are de-identified per HIPAA Safe Harbor. Available under PhysioNet Credentialed Health Data License 1.5.0.

**How it relates to your project:**
- **Primary imaging dataset** — the CXR images that the Vision Agent processes via BioViL + LLaVA-Med
- Must be cited for dataset provenance and ethical use compliance
- Reports linked via `subject_id` to MIMIC-IV structured EHR data

**Key insights for your project:**
- Paired images + reports enable cross-modal evaluation (Vision Agent vs. Report Agent agreement)
- PhysioNet license requires CITI training and credentialing

---

### 36. MIMIC-CXR-JPG: A Large Publicly Available Database of Labeled Chest Radiographs

| Field | Details |
|-------|---------|
| **Authors** | A. E. W. Johnson, T. J. Pollard, N. R. Greenbaum, M. P. Lungren, C.-Y. Deng, Y. Peng, Z. Lu, R. G. Mark, S. J. Berkowitz, S. Horng |
| **Venue** | arXiv / PhysioNet |
| **Year** | 2019 |
| **Links** | [arXiv:1901.07042](https://arxiv.org/abs/1901.07042) &#124; [PhysioNet DOI: 10.13026/8360-t248](https://doi.org/10.13026/8360-t248) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |

**Summary:**
JPG-format version of MIMIC-CXR with structured CheXpert pathology labels (14 observations) extracted from radiology reports. Smaller file sizes than DICOM format with pre-extracted evaluation labels.

**How it relates to your project:**
- Specific dataset variant used for the project (JPG format, pre-extracted CheXpert labels)
- CheXpert labels provide ground truth for multi-label evaluation (F1, AUROC per pathology)
- Subset selection: ~2,000-3,000 frontal-view studies, 5-6 pathologies

**Key insights for your project:**
- 14 CheXpert labels enable fine-grained per-pathology evaluation
- Frontal-view filtering reduces noise from lateral/other projections

---

### 37. MIMIC-IV: A Freely Accessible Electronic Health Record Dataset

| Field | Details |
|-------|---------|
| **Authors** | A. E. W. Johnson, L. Bulgarelli, L. Shen, A. Gayles, A. Shammout, S. Horng, T. J. Pollard, S. Hao, B. Moody, B. Gow, L.-W. H. Lehman, L. A. Celi, R. G. Mark |
| **Venue** | Scientific Data (Nature) |
| **Year** | 2023 |
| **DOI** | [10.1038/s41597-022-01899-x](https://doi.org/10.1038/s41597-022-01899-x) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |

**Summary:**
Foundational paper for the MIMIC-IV structured EHR database covering 299,712 patients at BIDMC. Provides structured clinical data — diagnoses (ICD codes), lab results, vital signs, medications, procedures — linked to MIMIC-CXR via `subject_id`.

**How it relates to your project:**
- Primary structured data source for the **Clinical Agent** (demographics, vitals, labs, meds, ICD codes)
- `subject_id` linkage enables true multimodal patient studies (image + report + EHR)

**Key insights for your project:**
- MIMIC-IV Demo (100 patients) available as a public surrogate for development
- Rich temporal data enables clinical context assessment

---

### 38. MIMIC-IV-Note: Deidentified Free-Text Clinical Notes

| Field | Details |
|-------|---------|
| **Authors** | A. Johnson, T. Pollard, R. Mark |
| **Venue** | PhysioNet |
| **Year** | 2023 |
| **DOI** | [10.13026/1n74-ne17](https://doi.org/10.13026/1n74-ne17) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |

**Summary:**
Dataset resource providing 331,794 discharge summaries and 2,321,355 radiology reports linked to MIMIC-IV via `subject_id`. The radiology reports are the primary text data for the Report Agent.

**How it relates to your project:**
- Primary text data source for the **Report Agent** (Findings + Impression sections)
- Reports provide the free-text grounding for CheXpert labels
- Section extraction (Findings vs. Impression) is a preprocessing step

**Key insights for your project:**
- Report structure (Findings/Impression) enables structured extraction
- Hedging language analysis possible for uncertainty modelling

---

### 39. CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Comparison

| Field | Details |
|-------|---------|
| **Authors** | J. Irvin, P. Rajpurkar, M. Ko, Y. Yu, S. Ciurea-Ilcus, C. Chute, H. Marklund, B. Haghgoo, R. Ball, K. Shpanskaya, J. Seekins, D. A. Mong, S. S. Halabi, J. K. Sandberg, R. Jones, D. B. Larson, C. P. Langlotz, B. N. Patel, M. P. Lungren, A. Y. Ng |
| **Venue** | AAAI Conference on Artificial Intelligence |
| **Year** | 2019 |
| **DOI** | [10.1609/aaai.v33i01.3301590](https://doi.org/10.1609/aaai.v33i01.3301590) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
Introduces the CheXpert labeler — an automated NLP-based tool that extracts 14 pathology labels (with uncertainty handling: positive, negative, uncertain, blank) from radiology reports. Trained on 224,316 CXR studies from Stanford.

**How it relates to your project:**
- The CheXpert labeler produced the structured ground-truth labels in MIMIC-CXR-JPG
- 14-label taxonomy defines the project's evaluation targets (macro-F1, per-pathology AUROC)
- Uncertainty labels (U-labels) require explicit handling in evaluation protocol

**Key insights for your project:**
- U-label handling strategy needed: treat as positive, negative, or exclude
- Expert comparison data enables human-vs-system calibration

---

## Category 11: Vision Language Models (VLMs) in Medical Imaging

These papers describe VLMs and foundation models relevant to the Vision Agent's multimodal reasoning pipeline.

---

### 40. LLaVA-Med: Training a Large Language-and-Vision Assistant for Biomedicine in One Day

| Field | Details |
|-------|---------|
| **Authors** | C. Li, C. Wong, S. Zhang, N. Usuyama, H. Liu, J. Yang, T. Naumann, H. Poon, J. Gao |
| **Venue** | NeurIPS |
| **Year** | 2023 |
| **Links** | [arXiv:2306.00890](https://arxiv.org/abs/2306.00890) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |

**Summary:**
Cost-efficient method for training a biomedical multimodal conversational assistant by fine-tuning LLaVA on biomedical image-text data generated via GPT-4. Achieves strong performance on biomedical VQA benchmarks.

**How it relates to your project:**
- **Primary VLM for the Vision Agent** — LLaVA-Med 7B (4-bit quantised) processes CXR images and generates text findings
- Demonstrates open-ended medical image QA capability needed for argumentation

**Key insights for your project:**
- 7B parameter model fits within RTX 5070 8GB VRAM budget at 4-bit quantisation
- Fine-tuned on biomedical data — domain-adapted for clinical image understanding

---

### 41. MedCLIP: Contrastive Learning from Unpaired Medical Images and Text

| Field | Details |
|-------|---------|
| **Authors** | Z. Wang, Z. Wu, D. Agarwal, J. Sun |
| **Venue** | EMNLP |
| **Year** | 2022 |
| **Links** | [EMNLP Proceedings](https://aclanthology.org/2022.emnlp-main.256/) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Proposes decoupled contrastive learning enabling medical CLIP training from unpaired images and text, overcoming the paired-data bottleneck. Alternative medical CLIP variant to BioViL.

**How it relates to your project:**
- Comparison point for BioViL in the literature review's CLIP backbone selection
- Demonstrates alternative approach to medical image-text alignment

**Key insights for your project:**
- Unpaired training is advantageous when paired data is scarce
- Performance comparison with BioViL justifies BioViL selection (CXR-specific vs. general medical)

---

### 42. Foundation Models for Generalist Medical Artificial Intelligence

| Field | Details |
|-------|---------|
| **Authors** | M. Moor, O. Banerjee, Z. S. H. Abad, H. M. Krumholz, J. Leskovec, E. J. Topol, P. Rajpurkar |
| **Venue** | Nature |
| **Year** | 2023 |
| **DOI** | [10.1038/s41586-023-05881-4](https://doi.org/10.1038/s41586-023-05881-4) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |

**Summary:**
Landmark *Nature* survey defining the landscape of foundation models (including multimodal VLMs) in medicine. Positions VLMs as the frontier of clinical AI.

**How it relates to your project:**
- Provides conceptual framing for why VLMs are central to modern clinical AI
- Positions the project within the broader foundation-model paradigm

**Key insights for your project:**
- Survey taxonomy helps justify modality-based agent design as a novel fusion approach
- Identifies gap: no foundation model combines argumentation with multimodal reasoning

---

## Category 12: Multimodal Clinical AI & Fusion

These papers provide the theoretical and empirical basis for combining different clinical data modalities.

---

### 43. Multimodal Biomedical AI

| Field | Details |
|-------|---------|
| **Authors** | J. N. Acosta, G. J. Falcone, P. Rajpurkar, E. J. Topol |
| **Venue** | Nature Medicine |
| **Year** | 2022 |
| **DOI** | [10.1038/s41591-022-01981-2](https://doi.org/10.1038/s41591-022-01981-2) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ✅ |

**Summary:**
Comprehensive *Nature Medicine* review of multimodal AI in biomedicine covering fusion strategies for imaging, text, genomics, and EHR data. Provides taxonomy of early, late, and joint fusion.

**How it relates to your project:**
- Contextualises the project's modality-based agent architecture as a novel form of **late argumentation-based fusion**
- Existing approaches use neural fusion; yours uses formal debate as the fusion mechanism

**Key insights for your project:**
- Late fusion typically outperforms early fusion for heterogeneous modalities
- Argumentation-based fusion is unprecedented — a key novelty claim

---

### 44. Fusion of Medical Imaging and Electronic Health Records Using Deep Learning: A Systematic Review

| Field | Details |
|-------|---------|
| **Authors** | S.-C. Huang, A. Pareek, S. Seyyedi, I. Banerjee, M. P. Lungren |
| **Venue** | npj Digital Medicine |
| **Year** | 2020 |
| **DOI** | [10.1038/s41746-020-00341-z](https://doi.org/10.1038/s41746-020-00341-z) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |

**Summary:**
Systematic review of deep learning approaches combining medical images with structured EHR data. Catalogues fusion architectures for CXR + clinical data combinations.

**How it relates to your project:**
- Directly relevant: reviews the same modality combination (CXR + EHR) the project uses
- All reviewed approaches use neural fusion — yours uses argumentation, filling a clear gap

**Key insights for your project:**
- CXR + EHR fusion consistently outperforms single-modality approaches
- No reviewed system uses formal argumentation for fusion — project's key novelty

---

### 45. Multimodal Machine Learning in Precision Health: A Scoping Review

| Field | Details |
|-------|---------|
| **Authors** | A. Kline, H. Wang, Y. Li, S. Dennis, M. Hutch, Z. Xu, F. Wang, F. Cheng, Y. Luo |
| **Venue** | npj Digital Medicine |
| **Year** | 2022 |
| **DOI** | [10.1038/s41746-022-00712-8](https://doi.org/10.1038/s41746-022-00712-8) |

**Relevance:** ⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ |

**Summary:**
Broad scoping review of 128 multimodal ML studies across imaging, clinical notes, EHR, and omics data. Positions existing neural fusion approaches.

**How it relates to your project:**
- Establishes that all existing multimodal approaches use neural networks for fusion
- The project's argumentation-based fusion via modality-partitioned agents is entirely novel

**Key insights for your project:**
- 128 studies reviewed, none using formal argumentation for multimodal fusion
- Strongest positioning evidence for the project's novelty claim

---

## Category 13: Radiology Report Generation & Understanding

These papers address automated radiology report analysis and generation — relevant to the Report Agent's pipeline.

---

### 46. R2Gen: Generating Radiology Reports via Memory-Driven Transformer

| Field | Details |
|-------|---------|
| **Authors** | Z. Chen, Y. Song, T.-H. Chang, X. Wan |
| **Venue** | EMNLP |
| **Year** | 2020 |
| **DOI** | [10.18653/v1/2020.emnlp-main.112](https://doi.org/10.18653/v1/2020.emnlp-main.112) |

**Relevance:** ⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Memory-driven transformer for automated radiology report generation with a relational memory module. Establishes SOTA baseline for CXR report generation.

**How it relates to your project:**
- Baseline comparison: Vision Agent's image-derived findings can be compared against automated report generation approaches
- Validates that CXR → text is a tractable task

**Key insights for your project:**
- Memory module concept parallels RAG retrieval of similar prior cases
- BLEU/ROUGE metrics from this work applicable to explanation quality evaluation

---

### 47. CheXbert: Combining Automatic Labelers and Expert Annotations for Accurate Radiology Report Labeling

| Field | Details |
|-------|---------|
| **Authors** | A. Smit, S. Jain, P. Rajpurkar, A. Pareek, A. Y. Ng, M. P. Lungren |
| **Venue** | EMNLP |
| **Year** | 2020 |
| **DOI** | [10.18653/v1/2020.emnlp-main.117](https://doi.org/10.18653/v1/2020.emnlp-main.117) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |

**Summary:**
BERT-based automatic labeler for extracting structured pathology labels from radiology reports, improving over rule-based CheXpert labeler. Combines automatic labels with expert annotations.

**How it relates to your project:**
- Potential NLP component for the Report Agent's text-to-label extraction pipeline
- Alternative to rule-based CheXpert labeler for Report Agent preprocessing

**Key insights for your project:**
- BERT-based extraction more accurate than rule-based for certain pathologies
- Could serve as secondary evaluation: compare Report Agent's label extraction against CheXbert

---

### 48. Improving Factual Completeness and Consistency of Image-to-Text Radiology Report Generation

| Field | Details |
|-------|---------|
| **Authors** | Y. Miura, Y. Zhang, E. B. Tsai, C. P. Langlotz, D. Jurafsky |
| **Venue** | NAACL |
| **Year** | 2021 |
| **Links** | [ACL Anthology](https://aclanthology.org/2021.naacl-main.416/) |

**Relevance:** ⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Addresses factual consistency between generated reports and source images. Uses reward-based training with factual completeness and consistency metrics.

**How it relates to your project:**
- Cross-modal factual consistency is central to the project's cross-modal agreement metric
- Vision Agent vs. Report Agent disagreements serve a similar factual consistency function

**Key insights for your project:**
- Factual completeness metrics applicable to VLM faithfulness evaluation
- Argumentation-based cross-checking provides an interpretable alternative to reward-based approaches

---

## Category 14: CLIP-Based Image Retrieval in Medical Settings

These papers describe CLIP and its medical variants used for the Vision Agent's image RAG pipeline.

---

### 49. CLIP: Learning Transferable Visual Models From Natural Language Supervision

| Field | Details |
|-------|---------|
| **Authors** | A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, G. Krueger, I. Sutskever |
| **Venue** | ICML |
| **Year** | 2021 |
| **Links** | [PMLR](https://proceedings.mlr.press/v139/radford21a.html) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Foundational paper introducing Contrastive Language-Image Pre-training (CLIP). Trains a joint image-text embedding space from 400M web-scraped image-text pairs. All medical CLIP variants (BioViL, MedCLIP, GLoRIA) extend this work.

**How it relates to your project:**
- Foundational paradigm for the project's CLIP-based image RAG pipeline
- BioViL's architecture directly descends from CLIP

**Key insights for your project:**
- Zero-shot transfer via textual descriptions enables flexible image retrieval
- Embedding similarity enables case-based retrieval without task-specific training

---

### 50. GLoRIA: A Multimodal Global-Local Representation Learning Framework

| Field | Details |
|-------|---------|
| **Authors** | S.-C. Huang, L. Shen, M. P. Lungren, S. Yeung |
| **Venue** | ICCV |
| **Year** | 2021 |
| **Links** | [IEEE](https://ieeexplore.ieee.org/document/9710099) |

**Relevance:** ⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Contrastive learning framework learning both global and local (region-level) representations from medical image-report pairs, including CXR data. Alternative to BioViL for fine-grained CXR embeddings.

**How it relates to your project:**
- Alternative CLIP variant for CXR image retrieval — comparison point for BioViL selection
- Region-level representations could enable anatomy-aware retrieval

**Key insights for your project:**
- Local attention mechanism provides anatomical grounding — future work direction
- Trained on CXR-report pairs from Stanford dataset

---

### 51. CheXzero: Expert-Level Detection of Pathologies from Unannotated Chest X-ray Images

| Field | Details |
|-------|---------|
| **Authors** | E. Tiu, E. Talius, P. Patel, C. P. Langlotz, A. Y. Ng, P. Rajpurkar |
| **Venue** | Nature Biomedical Engineering |
| **Year** | 2022 |
| **DOI** | [10.1038/s41551-022-00936-9](https://doi.org/10.1038/s41551-022-00936-9) |

**Relevance:** ⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
CLIP-style model (CheXzero) trained on MIMIC-CXR image-report pairs achieves expert-level zero-shot CXR pathology detection without explicit labels. Published in *Nature Biomedical Engineering*.

**How it relates to your project:**
- Validates CLIP embeddings as viable for CXR understanding on the **same MIMIC-CXR data** the project uses
- Expert-level zero-shot performance demonstrates the power of contrastive pre-training on CXR

**Key insights for your project:**
- Zero-shot pathology detection from CLIP embeddings — validates image RAG approach
- Trained on MIMIC-CXR — directly applicable embedding quality benchmark

---

### 52. ConVIRT: Contrastive Learning of Medical Visual Representations from Paired Images and Text

| Field | Details |
|-------|---------|
| **Authors** | Y. Zhang, H. Jiang, Y. Miura, C. D. Manning, C. P. Langlotz |
| **Venue** | MLHC (PMLR 182) |
| **Year** | 2022 |
| **Links** | [PMLR](https://proceedings.mlr.press/v182/zhang22a.html) |

**Relevance:** ⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Early and influential paper applying contrastive image-text pre-training to medical data, pre-dating BioViL and MedCLIP. Establishes that paired CXR-report data produces transferable visual representations.

**How it relates to your project:**
- Conceptual foundation for the project's CLIP-based image RAG
- Demonstrates that CXR-report contrastive pre-training yields strong visual features

**Key insights for your project:**
- Paired medical data (CXR + report) provides the training signal for all medical CLIP variants
- Pre-dates BioViL but establishes the same paradigm

---

### 53. BioViL: Making the Most of Text Semantics to Improve Biomedical Vision-Language Processing

| Field | Details |
|-------|---------|
| **Authors** | B. Boecking, N. Usuyama, S. Bannur, D. C. Castro, A. Schwaighofer, S. Hyland, M. Wetscherek, T. Naumann, A. Nori, J. Alvarez-Valle, H. Poon, O. Oktay |
| **Venue** | ECCV |
| **Year** | 2022 |
| **DOI** | [10.1007/978-3-031-20059-5_1](https://doi.org/10.1007/978-3-031-20059-5_1) |

**Relevance:** ⭐⭐⭐⭐⭐

**Components Covered:**
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ |

**Summary:**
Introduces BioViL, a biomedical vision-language model with a radiology-specific text encoder (CXR-BERT) that improves phrase grounding in CXR images. CXR-specific, peer-reviewed (ECCV 2022), and MIT-licensed.

**How it relates to your project:**
- **Selected as the primary CLIP embedding backbone** for the Vision Agent's image RAG retrieval pipeline
- CXR-specific training provides superior embeddings compared to general-purpose CLIP variants
- Replaces BiomedCLIP (arXiv-only) as the peer-reviewed alternative

**Key insights for your project:**
- Radiology-specific text encoder (CXR-BERT) improves medical text alignment
- ~400M params, ~2 GB VRAM — fits comfortably alongside other models
- MIT license — no usage restrictions for academic research

---

## Summary: Coverage Matrix

| Paper | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | Relevance |
|-------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|-----------|
| 1. ArgMed-Agents | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 2. MedGen | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 3. Interaction Model | ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 4. Adaptive CDSS | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 5. Argument Quality | ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 6. MAS-CDSS Review | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 7. Cognitive Biases | ✅ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 8. Emergency Triage | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 9. Metalevel Arg. | ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 10. Explainable Agents | ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 11. Linked Arg. Graphs | ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 12. Arg. Techniques Review | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 13. Intentional Dialogues | ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 14. Diagnostic Reasoning | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 15. Reasoning-Aware Dx | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 16. Graph-Aug. Retrieval | ⚪ | ✅ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 17. LLMs Healthcare Review | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 18. Prompt Framework | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐ |
| 19. XMAS | ✅ | ⚪ | ⚪ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 20. In-Time Explainability | ✅ | ⚪ | ✅ | ⚪ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 21. Multi-Agent RAG | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐ ⚠️ |
| 22. Case-Based Reasoning | ✅ | ⚪ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐ |
| 23. RAG for 10 LLMs | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 24. RAG Healthcare SR | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 25. ASPIC+ (Prakken) | ⚪ | ⚪ | ⚪ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 26. AAF Methods Survey | ⚪ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 27. Dung (1995) | ⚪ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 28. Trust 30-Year Review | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 29. Trust in AI-CDSS SR | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 30. XAI Conundrum | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 31. Co-design XAI | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 32. Critique of Reason | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 33. Hidden Profile Meta | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 34. Hidden Profile Dissent | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 35. MIMIC-CXR | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⭐⭐⭐⭐⭐ |
| 36. MIMIC-CXR-JPG | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⭐⭐⭐⭐⭐ |
| 37. MIMIC-IV | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⭐⭐⭐⭐⭐ |
| 38. MIMIC-IV-Note | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⭐⭐⭐⭐⭐ |
| 39. CheXpert | ⚪ | ⚪ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐⭐ |
| 40. LLaVA-Med | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| 41. MedCLIP | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⭐⭐⭐⭐ |
| 42. Foundation Models | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ✅ | ⭐⭐⭐⭐ |
| 43. Multimodal Biomed AI | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ✅ | ⭐⭐⭐⭐ |
| 44. Imaging + EHR Fusion | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⭐⭐⭐⭐ |
| 45. Multimodal ML Review | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⭐⭐⭐ |
| 46. R2Gen | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⭐⭐⭐ |
| 47. CheXbert | ⚪ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⭐⭐⭐⭐ |
| 48. Factual Completeness | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⭐⭐⭐ |
| 49. CLIP | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⭐⭐⭐⭐ |
| 50. GLoRIA | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⭐⭐⭐ |
| 51. CheXzero | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⭐⭐⭐⭐ |
| 52. ConVIRT | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⭐⭐⭐ |
| 53. BioViL | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ | ⚪ | ✅ | ⚪ | ⭐⭐⭐⭐⭐ |

> ⚠️ = Quality concern flagged (weak venue). All papers now have PDFs available.

---

## Recommended Reading Order

### Phase 1: Core Understanding
1. **ArgMed-Agents** (#1) — Most directly relevant, start here
2. **MedGen** (#2) — Architecture patterns
3. **Mitigating Cognitive Biases** (#7) — Multi-agent debate methodology
4. **MAS-CDSS Systematic Review** (#6) — Literature landscape
5. **Hidden Profile Meta-Analysis** (#33) — Information partitioning justification
6. **Hidden Profile Dissent** (#34) — Dissent as facilitator for decision quality

### Phase 2: Theoretical Foundations
7. **Dung's AAF** (#27) — Foundational argumentation semantics
8. **ASPIC+ Framework** (#25) — Structured argumentation extension
9. **AAF Methods Survey** (#26) — Computational methods for argumentation
10. **Metalevel Argumentation** (#9) — Medical argumentation theory
11. **Systematic Review of Argumentation** (#12) — Argumentation in MAS

### Phase 3: Design & Implementation
12. **Interaction Model** (#3) — Argumentation knowledge graphs
13. **Adaptive CDSS with RAG** (#4) — RAG integration
14. **Graph-Augmented Retrieval** (#16) — Graph-RAG approach (peer-reviewed)
15. **RAG for 10 LLMs** (#23) — RAG comparison methodology
16. **RAG Healthcare SR** (#24) — RAG landscape in healthcare
17. **Engineering Explainable Agents** (#10) — Implementation methodology
18. **Diagnostic Reasoning Prompts** (#14) — LLM clinical reasoning

### Phase 4: Trust, XAI & Evaluation
19. **Solving the XAI Conundrum** (#30) — Clinician-developer bridge
20. **Co-design of XAI** (#31) — Human-centred XAI methodology
21. **Trust 30-Year Review** (#28) — Trust theoretical framework
22. **Trust in AI-CDSS SR** (#29) — Trust factors synthesis
23. **Critique of Impure Reason** (#32) — LLM reasoning evaluation
24. **In-Time Explainability** (#20) — Real-time requirements
25. **Intentional Dialogues Thesis** (#13) — Full implementation reference

### Phase 5: MIMIC Ecosystem & Multimodal AI (New)
26. **MIMIC-CXR** (#35) — Primary imaging dataset
27. **MIMIC-CXR-JPG** (#36) — JPG format with CheXpert labels
28. **MIMIC-IV** (#37) — Structured EHR database
29. **MIMIC-IV-Note** (#38) — Radiology reports
30. **CheXpert** (#39) — Labeling infrastructure and evaluation taxonomy
31. **LLaVA-Med** (#40) — Primary VLM for Vision Agent
32. **BioViL** (#53) — CLIP embedding backbone for Image RAG
33. **Foundation Models Survey** (#42) — VLM landscape context
34. **Multimodal Biomedical AI** (#43) — Fusion strategy taxonomy
35. **Imaging + EHR Fusion** (#44) — CXR + EHR fusion systematic review

### Phase 6: CLIP & Report Understanding (Supplementary)
36. **CLIP** (#49) — Foundational contrastive learning paradigm
37. **CheXzero** (#51) — CLIP on MIMIC-CXR validation
38. **CheXbert** (#47) — Automated report labeling
39. **Factual Completeness** (#48) — Cross-modal consistency

---

## Research Gaps Your Project Can Address

Based on this literature analysis (updated for MIMIC multimodal pivot with modality-based agent partitioning), your project can contribute to:

1. **Integration Gap:** Few papers combine ALL of: MAS + LLM/VLM + Argumentation + RAG + HITL in a single system
2. **Modality-Based Partitioning:** No existing work assigns different clinical data modalities (CXR images, radiology reports, structured EHR) to separate agents that debate via formal argumentation — this is the core novelty. The hidden profile paradigm (Lu et al., 2012; Schulz-Hardt et al., 2006) provides the theoretical basis from social psychology, applied for the first time to multimodal clinical data
3. **Argumentation-Based Multimodal Fusion:** All 128 multimodal health AI studies reviewed by Kline et al. (2022) use neural fusion. No existing system uses formal argumentation as the fusion mechanism for multimodal clinical data
4. **CLIP Image RAG + GraphRAG for Argumentation:** No published system combines CLIP-based image retrieval with knowledge-graph-grounded text retrieval within a formal argumentation framework
5. **Infrastructure Comparison:** No head-to-head comparison of Vector RAG vs. GraphRAG vs. Multimodal Hybrid RAG (with CLIP image retrieval) within the same multi-agent argumentation system
6. **Symbolic-Neural Integration:** Combining Dung's AAF and Walton's argumentation schemes with VLM-generated evidence from chest X-rays remains entirely unexplored
7. **Human-in-the-Loop:** Most systems focus on autonomous reasoning; your interactive approach with clinician oversight is novel
8. **Domain-Specific Validation:** No existing multi-agent argumentation system has been validated on MIMIC's multimodal clinical data (CXR + report + EHR)

---

## Key Research Groups to Follow

1. **Liang Xiao's Group (China)** — ArgMed-Agents, MedGen, Interaction Model, Argument Quality
2. **Kökciyan/Sassoon/Sklar/Modgil** — Metalevel argumentation for medical AI
3. **Bordini/Panisson/Engelmann (PUCRS, Brazil)** — Explainable agents with argumentation
4. **Woltran/Dvořák/Gaggl (Vienna/Dresden)** — Computational argumentation, AAF solvers
5. **JMIR / npj Digital Medicine** — Trust, RAG evaluation, clinical AI
6. **Schulz-Hardt / Brodbeck (Göttingen/Munich)** — Hidden profile / group decision making
7. **Rajpurkar Group (Harvard/Stanford)** — CheXpert, CheXzero, foundation models, multimodal AI
8. **Microsoft Health Futures** — BioViL, LLaVA-Med, biomedical VLMs
9. **MIT Lab for Computational Physiology** — MIMIC datasets, PhysioNet

---

> **Note on GraphRAG:** The Microsoft GraphRAG paper (Edge et al., 2024) was removed as it is arXiv-only with no peer-reviewed publication. For the infrastructure sweep, cite the open-source software ([github.com/microsoft/graphrag](https://github.com/microsoft/graphrag)) and use paper #16 (Wang et al., 2025, Springer) as the peer-reviewed academic reference for graph-based RAG.

---

*Document updated: 6 April 2026 (MIMIC pivot — MI dataset paper removed, 19 new MIMIC/VLM/multimodal papers added)*
*Total papers: 53 (34 original + 19 new; all peer-reviewed venues or accepted technical reports)*
*Papers removed: 1 (#35 Golovenkin MI dataset — no longer relevant after MIMIC pivot)*
*Papers added: 19 (#35-53: 5 MIMIC datasets, 3 VLMs, 3 multimodal fusion, 3 report generation, 5 CLIP retrieval)*
*New component categories: C11 (Vision Language Models), C12 (Multimodal Data Fusion)*
*Papers flagged for caution: 2 (#8 weak venue OAJRC, #21 unindexed venue)*
*All 53 papers now have PDFs available in the project folder*
