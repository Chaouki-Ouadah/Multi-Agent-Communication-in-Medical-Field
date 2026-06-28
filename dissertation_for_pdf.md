---
title: "Multi-Agent Argumentation Frameworks with LLM-Augmented Reasoning in Healthcare Systems"
short-title: "Multi-Agent Argumentation in Healthcare"
author: "Chaouki Ouadah"
student-id: "H00498420"
degree: "MSc in Data Science"
supervisor: "Dr Radu-Casian Mihailescu"
course-code: "F21 RP - MSc Graduation Project"
date: "August 2026"
logo: "hwu_logo.png"
abstract: |
  Artificial intelligence is increasingly applied in clinical decision support, yet existing systems lack explainability, clinician trust, and principled integration of multimodal patient data. Current approaches rely on neural fusion or simple voting to combine data modalities, producing opaque recommendations that clinicians cannot inspect or challenge. No existing system combines multi-agent argumentation with multimodal Retrieval-Augmented Generation — specifically CLIP-based image retrieval and knowledge-graph-grounded text retrieval — within a formal symbolic reasoning framework.

  This project proposes a multi-agent argumentation system in which three modality-partitioned agents — Vision (chest X-ray images), Report (radiology reports), and Clinical (structured electronic health records) — generate independent diagnostic arguments that are resolved through Dung's Abstract Argumentation Framework and classified using Walton's argumentation schemes. Each agent is grounded by a multimodal RAG pipeline combining BioViL-based image retrieval with GraphRAG text retrieval. The system is evaluated using a design science methodology with experimental validation on MIMIC multimodal data (MIMIC-CXR-JPG, MIMIC-IV-Note, MIMIC-IV), assessing six evaluation dimensions — CheXpert 14-label pathology detection, explainability, process transparency, trust calibration, robustness, and cross-modal agreement — against single-agent and non-argumentation baselines.

  The expected outcome is a system that improves both diagnostic accuracy and reasoning transparency compared to existing approaches, demonstrating that formal argumentation provides a viable and explainable mechanism for multimodal clinical data fusion.
acknowledgements: |
  "[PLACEHOLDER: To be completed]"
---

# Chapter 1: Introduction

A chest X-ray shows bilateral lower-lobe opacities. The radiologist's report reads "cardiomegaly without acute infiltrate." Meanwhile, the patient's laboratory results reveal a normal white blood cell count but an elevated BNP. Three data modalities, three different signals — and a clinician who must reconcile them all before deciding whether this patient has pneumonia, heart failure, or both. This diagnostic scenario, played out thousands of times daily in hospitals worldwide, exposes a fundamental gap in current AI-based clinical decision support: no existing system can reason across images, free-text reports, and structured electronic health records using a principled framework that the clinician can inspect, challenge, and trust.

## 1.1 Problem Statement

Clinical Decision Support Systems (CDSS) powered by artificial intelligence have demonstrated strong predictive performance on isolated tasks — classifying chest radiograph (CXR) pathologies (Irvin et al., 2019), answering medical questions from text (Hong et al., 2024), or extracting diagnoses from electronic health records (Johnson et al., 2023a). Yet these systems share three persistent weaknesses that limit their adoption in clinical practice.

First, they lack **explainability**. Neural network-based classifiers produce a probability score but offer no reasoning trace. A radiologist told that a model assigns 0.78 probability to "Pneumonia" cannot determine whether the model focused on the correct lung region, whether it considered the patient's lab results, or whether its conclusion contradicts the written radiology report. Explainability in clinical AI requires more than a saliency map — it requires a structured account of which evidence supports which conclusion and why competing hypotheses were rejected (Kökciyan et al., 2021).

Second, existing systems struggle with **principled multimodal integration**. Most multimodal clinical AI systems fuse data modalities through neural concatenation or learned attention mechanisms (Huang et al., 2020). These approaches are effective for pattern recognition, but they are opaque: a clinician cannot see which modality contributed which evidence, or how conflicts between modalities were resolved. When a chest X-ray suggests one diagnosis and the lab results suggest another, the fusion layer produces a blended output with no record of the disagreement. In actual clinical practice, such conflicts are resolved through structured deliberation — a multidisciplinary team (MDT) meeting where specialists with different expertise debate their findings. Current AI systems do not replicate this deliberative process.

Third, most systems rely on **accuracy-only evaluation**. The dominant benchmark for CXR pathology detection is multi-label classification accuracy against CheXpert labels (Irvin et al., 2019). While necessary, accuracy alone does not capture whether the system's reasoning was sound, whether its explanations were faithful to its internal process, or whether clinicians would trust its recommendations. A system that achieves high F1 but produces incoherent explanations may perform worse in practice than a slightly less accurate system whose reasoning is transparent and verifiable.

## 1.2 Research Gap

Several recent systems address subsets of these challenges but none combines all the necessary components. Table 1.1 summarises the key limitations.

**Table 1.1: Capability gaps in existing systems (adapted from the SOTA comparison in the project roadmap).**

| System | Multi-Agent | Argumentation | Multimodal RAG | KG-RAG | Symbolic Resolution | Evaluation |
|--------|:-----------:|:-------------:|:--------------:|:------:|:-------------------:|:----------:|
| ArgMed-Agents (Hong et al., 2024) | Yes | Dung AAF + ASCD | None | None | Full (text only) | Accuracy only |
| MedGen (Liu et al., 2024) | Yes | Debate | None | Vector RAG | None | Accuracy, F1 |
| MDAgents (Kim et al., 2024) | Yes | Adaptive | None | None | None | Accuracy only |
| MedRAG (Zhao et al., 2025) | No | None | None | KG-RAG | None | Accuracy, F1 |
| **Proposed System** | **Yes** | **Dung's AAF + Walton** | **CLIP Image RAG** | **GraphRAG + Neo4j** | **Full** | **6 dimensions** |

ArgMed-Agents (Hong et al., 2024) combines Dung's AAF with Walton-inspired argumentation schemes (ASCD) in an LLM-based multi-agent debate for clinical reasoning, achieving formal symbolic resolution of conflicting arguments on text-only medical QA benchmarks — but operates with no multimodal data and no knowledge graph grounding. MedGen (Liu et al., 2024) decomposes clinical decisions across multiple agents with standard RAG but lacks formal argumentation — agents exchange opinions without symbolic resolution of conflicts. MDAgents (Kim et al., 2024) adapts group size dynamically but resolves disagreements through adaptive collaboration rather than structured argumentation. MedRAG (Zhao et al., 2025) integrates knowledge graphs with retrieval-augmented generation but uses a single-agent architecture with no debate mechanism. None of these systems operates on genuinely multimodal clinical data that spans imaging, free text, and structured records simultaneously.

The research gap, then, is fivefold: (1) no existing system combines multi-agent debate with **modality-based partitioning**, where each agent sees a different clinical data type; (2) no system applies **formal argumentation theory** (Dung's Abstract Argumentation Framework and Walton's schemes) as a multimodal fusion mechanism; (3) no system integrates **CLIP-based image retrieval** with **knowledge-graph-grounded text retrieval** within a multi-agent argumentation pipeline; (4) existing evaluations remain narrowly focused on accuracy, neglecting explainability, process transparency, trust calibration, and cross-modal agreement; and (5) the leading argumentation and multi-agent clinical systems (ArgMed-Agents, MDAgents) depend on closed-source commercial LLMs, limiting reproducibility and institutional deployment.

## 1.3 Research Questions

This project addresses the following primary research question and four sub-questions, defined in collaboration with the project supervisor.

> **RQ:** How can multi-agent argumentation frameworks, augmented by Large Language Models and Retrieval-Augmented Generation, improve the explainability and trustworthiness of clinical decision support systems?

| ID | Sub-Question |
|----|-------------|
| **SRQ1** | How can formal argumentation schemes (e.g., Walton's schemes) be integrated with LLM-driven agent debate to produce clinically meaningful explanations? |
| **SRQ2** | How do different Retrieval-Augmented Generation approaches affect the factual grounding and consistency of multi-agent clinical reasoning? |
| **SRQ3** | How do different clinical data modalities (chest X-ray images, radiology reports, structured EHR), modelled as modality-partitioned agents, affect diagnostic differential outcomes? |
| **SRQ4** | What evaluation metrics beyond accuracy (explainability, process transparency, trust) are most effective for assessing argumentation-based clinical decision support? |

SRQ1 targets the symbolic reasoning layer; SRQ2 targets the knowledge retrieval infrastructure; SRQ3 targets the multimodal agent architecture; and SRQ4 targets the evaluation framework. Together, they decompose the primary RQ into independently testable components.

## 1.4 Proposed Approach

To address these gaps, this project proposes a multi-agent argumentation system for clinical decision support, evaluated on genuinely multimodal data from the MIMIC ecosystem (Johnson et al., 2019a; Johnson et al., 2023a).

The system consists of three **modality-partitioned agents** and one **Supervisor agent**, orchestrated by a LangGraph state machine. Each agent processes a single clinical data modality:

- The **Vision Agent** interprets CXR images using BioViL embeddings (Boecking et al., 2022) for CLIP-based image retrieval and LLaVA-Med 7B (Li et al., 2023) for visual question answering, producing textual findings from imaging data.
- The **Report Agent** analyses free-text radiology reports from MIMIC-IV-Note using NLP-based section extraction and a medical LLM (Meditron-8B).
- The **Clinical Agent** processes structured EHR data — laboratory results, vital signs, medications, and demographics — from MIMIC-IV via structured prompt serialisation and Meditron-8B.
- The **Supervisor** sees the textual arguments from all three agents but never accesses the raw data. It mediates the multi-round debate, identifies cross-modal conflicts, and manages convergence.

This design mirrors the structure of a clinical MDT: a radiologist reads the image, a clinician reviews the labs and history, and they then confer. Each agent's independent, modality-constrained viewpoint creates genuine information asymmetry, meaning that disagreements between agents reflect real cross-modal conflicts rather than redundant re-analysis of the same data.

Agent disagreements are resolved through **Dung's Abstract Argumentation Framework** (Dung, 1995), which computes preferred extensions — maximal admissible sets of arguments that survive mutual attack — to formally determine which claims are accepted. Each argument is further classified using **Walton's argumentation schemes** (Walton et al., 2008), providing structured reasoning types (e.g., Argument from Expert Opinion, Argument from Sign) that make the debate process interpretable to clinicians.

Knowledge grounding is provided by a dual retrieval pipeline: **CLIP Image RAG** (using BioViL embeddings and a ChromaDB vector store of historical CXR cases) and **GraphRAG** (using Microsoft's graph-based RAG with a Neo4j medical knowledge graph indexed with UMLS and SNOMED-CT ontologies). An infrastructure sweep across three retrieval configurations (Vector RAG, GraphRAG, and the full multimodal hybrid) directly answers SRQ2.

The system is evaluated on a subset of 2,000–3,000 frontal-view MIMIC-CXR studies linked to their corresponding radiology reports and structured EHR records, using six evaluation dimensions: CheXpert 14-label pathology detection, explainability, process transparency, trust calibration, robustness, and cross-modal agreement. Five baselines (B1–B5) and seven ablation studies (A1–A7) isolate the contribution of each system component.

## 1.5 Contributions

This project makes the following contributions:

1. **Formal argumentation as a multimodal fusion mechanism.** To the best of our knowledge, this is the first system that applies Dung's AAF and Walton's schemes as the primary mechanism for resolving conflicts between agents whose inputs span different clinical data modalities (CXR images, radiology reports, structured EHR).

2. **CLIP Image RAG combined with GraphRAG in a multi-agent argumentation system.** No published system integrates BioViL-based image retrieval with knowledge-graph-grounded text retrieval within a formal argumentation pipeline.

3. **Modality-partitioned agent design evaluated on linked MIMIC data.** The three-agent architecture (Vision / Report / Clinical) is evaluated on genuinely linked multimodal patient records, with ablation studies (A6, A7) that quantify each modality's unique contribution to diagnostic reasoning.

4. **Multi-dimensional evaluation beyond accuracy.** The six-dimension evaluation framework — covering explainability, process transparency, trust, robustness, and cross-modal agreement alongside CheXpert pathology detection — provides a template for assessing argumentation-based CDSS more comprehensively than classification accuracy alone.

5. **Open-source, reproducible model stack.** Unlike ArgMed-Agents and MDAgents, which depend on closed-source commercial models (GPT-3.5/GPT-4), the proposed system uses entirely open-source primary models (Meditron, LLaVA-Med, BioViL) with publicly available weights, enabling full reproducibility and institutional deployment without commercial API dependencies.

## 1.6 Report Structure

The remainder of this report is organised as follows. **Chapter 2** reviews the relevant literature, covering multi-agent clinical AI systems, argumentation theory, retrieval-augmented generation, vision-language models, and the MIMIC data ecosystem, and concludes with a critical analysis of research gaps. **Chapter 3** translates the research questions into engineering requirements using MoSCoW prioritisation, and presents the system architecture with functional and non-functional requirements. **Chapter 4** describes the methodology in detail: the Design Science Research framework, the MIMIC dataset and subsetting strategy, the modality-partitioned agent pipelines, the symbolic argumentation layer, the knowledge retrieval pipeline, and the six-dimensional evaluation strategy including baselines and ablations. **Chapter 5** addresses professional, legal, ethical, and social issues — specifically PhysioNet credentialing, GDPR compliance, bias risks in CheXpert labelling, and VLM hallucination concerns. **Chapter 6** presents the project plan, including the dual-track Gantt chart, supervisor checkpoints, and risk analysis.


---

# Chapter 2: Literature Review

This chapter provides a critical review of the literature underpinning the proposed multi-agent argumentation framework for clinical decision support. The review is organised into three sections. Section 2.1 introduces foundational concepts — multi-agent systems, argumentation theory, large language models, retrieval-augmented generation, the MIMIC clinical data ecosystem, and multimodal data fusion. Section 2.2 examines related work across seven thematic areas, situating the project within the broader research landscape. Section 2.3 synthesises the findings into a gap analysis, demonstrating that no existing system integrates all of the components proposed here.

## 2.1 Background

### Multi-Agent Systems in Clinical Decision Support

A multi-agent system (MAS) comprises multiple interacting autonomous agents, each with specialised knowledge or capabilities, collaborating towards a common objective. In clinical settings, MAS architectures decompose complex diagnostic and treatment tasks across specialist agents, mirroring the multidisciplinary team (MDT) model used in modern hospital practice. Silveira et al. (2025) present a systematic review identifying three dominant MAS paradigms in healthcare: multi-agent reinforcement learning, ontology-based knowledge representation, and generative-AI-driven agent coordination. The latter paradigm — LLM-powered agents — has seen rapid growth since 2023 and forms the foundation of this project.

### Argumentation Theory

Formal argumentation provides a principled framework for modelling disagreement, resolving conflicts, and justifying decisions. Dung's (1995) Abstract Argumentation Framework (AAF) defines argumentation as a directed graph ⟨*Args*, *attacks*⟩, where *Args* is a set of arguments and *attacks* is a binary relation representing conflicts. The framework computes *extensions* — maximally consistent subsets of arguments — under various semantics: *grounded* (the unique minimal complete labelling), *preferred* (maximal admissible sets), and *stable* (sets that attack every non-member). These semantics determine which arguments are ultimately accepted, rejected, or undecided (Charwat et al., 2015).

Prakken (2009) extends Dung's abstract framework with the ASPIC+ formalism, introducing *structured arguments* composed of strict and defeasible inference rules, contrariness relations, and preference orderings. ASPIC+ allows domain-specific reasoning patterns — such as clinical evidence hierarchies — to be formalised and evaluated within Dung's semantics. Walton et al. (2008) complement these formal frameworks with *argumentation schemes*: stereotypical patterns of reasoning such as *Argument from Expert Opinion* and *Argument from Analogy* that provide a taxonomy of domain-appropriate argument types used in clinical discourse.

### Large Language Models and Vision–Language Models

Large language models (LLMs) have demonstrated strong performance in clinical reasoning tasks, producing diagnostic reasoning chains aligned with clinician cognitive processes when appropriately prompted (Savage et al., 2024). Vision–language models (VLMs) extend this capability to multimodal inputs by jointly processing images and text. Moor et al. (2023) position VLMs as the frontier of clinical AI in a landmark *Nature* survey, cataloguing foundation models that span imaging, text, genomics, and electronic health records. In chest radiography specifically, models such as LLaVA-Med (Li et al., 2023) provide open-ended biomedical visual question-answering, while contrastive vision–language models such as BioViL (Boecking et al., 2022) produce joint image–text embeddings optimised for chest X-ray (CXR) understanding.

### Retrieval-Augmented Generation, Knowledge Graphs, and CLIP-Based Retrieval

Retrieval-Augmented Generation (RAG) addresses LLM hallucination and knowledge currency by grounding generation in retrieved evidence (Amugongo et al., 2025). Knowledge graphs (KGs) extend RAG by encoding structured entity–relationship representations, enabling graph-based queries that capture global context beyond local semantic similarity (Wang et al., 2025). Contrastive Language–Image Pre-training (CLIP) (Radford et al., 2021) learns a joint embedding space for images and text, enabling zero-shot image retrieval via textual queries. Medical variants such as BioViL (Boecking et al., 2022) and CheXzero (Tiu et al., 2022) adapt CLIP for CXR data, achieving expert-level pathology detection without task-specific labels.

### The MIMIC Clinical Data Ecosystem

The Medical Information Mart for Intensive Care (MIMIC) provides the largest publicly available collection of de-identified clinical data for research. MIMIC-CXR (Johnson et al., 2019a) contains 377,110 chest radiographs with associated free-text radiology reports from 65,379 patients at Beth Israel Deaconess Medical Center. MIMIC-CXR-JPG (Johnson et al., 2019b) provides the same images in compressed format with structured CheXpert pathology labels — 14 observations including Atelectasis, Cardiomegaly, Consolidation, Edema, and Pleural Effusion — extracted automatically by the CheXpert labeler (Irvin et al., 2019). MIMIC-IV v3.1 (Johnson et al., 2023a) supplies structured EHR data comprising diagnoses (ICD codes), laboratory results, vital signs, and medications for 364,627 patients. MIMIC-IV-Note (Johnson et al., 2023b) adds 331,794 discharge summaries and 2,321,355 radiology reports. All MIMIC components are linked via a shared `subject_id`, enabling true multimodal patient studies that combine imaging, free-text, and structured clinical data.

### Multimodal Data Fusion in Clinical AI

Acosta et al. (2022) categorise multimodal fusion strategies as *early fusion* (feature-level concatenation), *late fusion* (decision-level aggregation), and *joint fusion* (intermediate representation learning). Huang et al. (2020) review deep learning approaches combining CXR images with structured EHR data, finding that multimodal models consistently outperform unimodal baselines. Kline et al. (2022) survey 128 multimodal machine learning studies across imaging, clinical notes, EHR, and omics data, reporting that all reviewed approaches employ neural networks for cross-modal integration. No study in these reviews uses formal argumentation as a fusion mechanism — a gap the present project directly addresses.

---

## 2.2 Related Work

### 2.2.1 Multi-Agent LLM Systems for Clinical Decision-Making

The convergence of multi-agent system design with large language models in clinical settings has gained significant traction since 2023. Hong et al. (2024) introduce ArgMed-Agents, the most directly comparable system to the one proposed here. ArgMed-Agents employs multiple LLM-based agents — Generator, Verifier, and Reasoner — that mimic clinical argumentative reasoning. The Generator and Verifier agents engage in structured debate using Walton-inspired Argumentation Schemes for Clinical Discussion (ASCD), while the Reasoner agent constructs a formal argumentation framework ⟨𝒜, ℛ⟩ following Dung's (1995) AAF and uses a symbolic solver to compute acceptable arguments under Dung's semantics. Agents generate self-directed explanations that improve diagnostic accuracy compared to standard chain-of-thought prompting on text-only medical question-answering benchmarks (MedQA and PubMedQA). ArgMed-Agents thus combines both Walton-style scheme matching and Dung's formal resolution within a single pipeline. However, the system operates exclusively on text-based benchmarks, does not incorporate multimodal clinical data (imaging or structured EHR), and does not employ knowledge-graph-grounded retrieval.

Liu et al. (2024) extend this line of work with MedGen, a multi-agent architecture that decomposes clinical decision-making into four sequential stages: clinical goal setting, data collection, argumentation linking, and plan selection. MedGen fuses multiple knowledge sources with argumentation, enabling agents to provide both reasoning evidence and a transparent decision process. While MedGen introduces retrieval-augmented reasoning, it relies on standard vector-based RAG rather than knowledge-graph-grounded retrieval and does not address multimodal inputs. Hong et al. (2023) provide the theoretical precursor to ArgMed-Agents by constructing a cognitive representation model for computational argumentation and designing argumentation knowledge graphs for shared clinical decision support, establishing the interaction protocols later operationalised in the ArgMed-Agents framework.

Beyond argumentation-specific systems, Ke et al. (2024) demonstrate that multi-agent LLM conversations can mitigate cognitive biases in clinical decision-making. Their simulation study, published in JMIR with 64 citations, shows that agent debate overcomes biases — including anchoring and confirmation bias — that degrade individual LLM reasoning. This provides empirical support for the thesis that structured multi-agent deliberation outperforms monolithic reasoning. Öğdü et al. (2025) propose a multi-layered adaptive CDSS incorporating biomedical RAG and web intelligence, addressing confidence calibration and multi-source evidence fusion, though without formal argumentation. Liu and Xiao (2025) introduce an ontology for assessing argument quality in multi-agent clinical systems, providing formal methods for evaluating the strength and reliability of individual arguments — a component relevant to this project's argument evaluation layer. Silveira et al. (2025) offer the most comprehensive landscape survey, covering multi-agent reinforcement learning, ontology-based knowledge representation, and generative AI across the full span of MAS applications in clinical decision support.

The theoretical foundation for the proposed modality-partitioned agent design draws on the *hidden profile* paradigm from social psychology. Lu et al. (2012) present a meta-analysis of 25 years of hidden profile research, demonstrating that groups perform better when members hold unique, unshared information and must pool it through structured discussion to reach optimal decisions. Schulz-Hardt et al. (2006) extend this finding by showing that *dissent* — genuine disagreement arising from different information — is a critical facilitator for decision quality, and that the effect is driven by information exchange rather than mere preference diversity. These findings directly justify the proposed architecture's modality-based partitioning, where Vision, Report, and Clinical agents each observe different data modalities and must debate through formal argumentation to integrate their perspectives.

*Synthesis.* Multi-agent LLM systems consistently improve clinical reasoning over single-agent approaches through debate, bias mitigation, and knowledge fusion. ArgMed-Agents (Hong et al., 2024) is the only system that combines Dung's AAF with Walton-inspired argumentation schemes, achieving formal symbolic resolution of conflicting arguments. However, it operates exclusively on text-only benchmarks (MedQA, PubMedQA), and no system partitions agents by clinical data modality to create the structured information asymmetry that hidden profile theory indicates is beneficial. The gap, therefore, lies not in the absence of formal argumentation per se, but in its application to multimodal clinical data with modality-partitioned agents.

### 2.2.2 Formal Argumentation: Theory and Computation

Dung's (1995) seminal paper, with over 4,000 citations, provides the axiomatic foundation for computational argumentation. The AAF's elegance lies in its abstraction: arguments are nodes and attacks are directed edges, permitting the computation of extensions under well-defined semantics regardless of domain-specific content. Charwat et al. (2015) survey the computational methods for solving reasoning problems in AAFs, covering reduction-based approaches, direct algorithms, and argumentation solvers for grounded, preferred, stable, and semi-stable semantics. Their survey, published in *Artificial Intelligence* (Elsevier), identifies trade-offs between expressiveness and computational tractability that inform the proposed system's choice of preferred semantics as the primary resolution strategy.

Prakken's (2009) ASPIC+ framework bridges Dung's abstraction and domain application by introducing structured arguments with strict and defeasible inference rules. In the medical domain, strict rules encode established clinical guidelines (e.g., "If troponin > 0.04 ng/mL, then myocardial injury"), while defeasible rules capture clinical heuristics that may be overridden by stronger evidence. Kökciyan et al. (2021) operationalise this combination through *metalevel argumentation frameworks* that enable reasoning about argument strength, preferences, and conflicts in medical decision support systems. Their approach, published in *IEEE Intelligent Systems* with 44 citations, highlights key factors underlying clinical decisions and includes a human-in-the-loop interface for clinician oversight. Panisson et al. (2021) demonstrate an engineering methodology for building explainable BDI (Belief-Desire-Intention) agents using argumentation, with a healthcare application that integrates argumentation into the agent reasoning cycle. Carrera and Iglesias (2015) provide a comprehensive taxonomy of argumentation techniques in multi-agent systems, classifying approaches by argument structure, dialogue protocol, and resolution mechanism. Xiao and Greer (2023) extend argumentation to the clinical domain with linked argumentation graphs that represent and integrate arguments from multidisciplinary team settings.

*Synthesis.* Formal argumentation theory offers a mathematically grounded framework for conflict resolution and explanation generation in multi-agent settings. Dung's AAF, ASPIC+, and Walton's schemes together provide the semantic, structural, and domain-level layers needed for clinical argumentation. ArgMed-Agents demonstrates that combining Dung's AAF with Walton-inspired schemes and LLM-generated arguments yields measurable gains in diagnostic accuracy on text-based benchmarks. However, no system has applied this combination to multimodal clinical data, and no system integrates structured argumentation with ASPIC+ preference orderings for encoding clinical evidence hierarchies across heterogeneous data modalities.

### 2.2.3 Retrieval-Augmented Generation and Knowledge Integration

RAG has become a standard technique for grounding LLM outputs in verified evidence. Amugongo et al. (2025) present a systematic review of RAG applications in healthcare, identifying common architectures, evaluation approaches, and open challenges. They find that RAG consistently reduces hallucination and improves factual accuracy, but note that most implementations rely on flat vector retrieval that misses relational context. Wang et al. (2025) address this limitation through graph-augmented retrieval, combining knowledge graphs with RAG for LLM-based clinical reasoning in anesthesiology. Their graph-based approach captures entity relationships that vector-only retrieval cannot represent, improving analytical reasoning on complex multi-step clinical scenarios.

Ke et al. (2025) provide the most comprehensive empirical study of RAG in clinical settings, evaluating retrieval-augmented generation across ten LLMs — including GPT-3.5, GPT-4, GPT-4o, Gemini, Llama 2/3, and Claude — for assessing surgical fitness. Their study spans 35 local and 23 international guidelines across 14 clinical scenarios, generating 3,234 responses compared against 448 human expert answers. The results demonstrate that RAG performance varies substantially across model architectures, underscoring the importance of infrastructure-level comparison — a key component of the proposed system's evaluation framework. Shen et al. (2015), with 103 citations, represent an earlier paradigm: case-based reasoning within a multi-agent architecture for clinical decisions, anticipating RAG's evidence-grounding function through similarity retrieval over prior clinical cases.

*Synthesis.* RAG is well-established for grounding clinical LLM reasoning, and graph-based RAG improves on vector-only retrieval by capturing relational knowledge. However, no existing system combines CLIP-based image retrieval with knowledge-graph-grounded text retrieval, and no system integrates RAG infrastructure into a formal argumentation pipeline where retrieved evidence explicitly supports or attacks arguments.

### 2.2.4 Explainability, Trust, and Human-in-the-Loop in Medical AI

Trust and explainability are prerequisites for clinician adoption of AI-based decision support. Bienefeld et al. (2023) conduct a longitudinal multi-method study with 112 developers and clinicians co-designing an XAI solution, identifying three critical gaps between developer and clinician mental models: opposing goals (model interpretability versus clinical plausibility), different sources of truth (training data versus the individual patient), and divergent knowledge strategies (exploration versus exploitation). These findings suggest that explanations must be framed in clinical terms — a requirement naturally satisfied by natural-language argumentation. Panigutti et al. (2023) reinforce this through a co-design methodology published in *ACM Transactions on Interactive Intelligent Systems* with 63 citations, demonstrating that clinician involvement in explanation design improves both trust and system adoption.

Wong et al. (2025) provide a 30-year longitudinal review tracing the evolution from trust in automation to trust in AI in healthcare, proposing an interdisciplinary framework integrating psychological, technical, and clinical perspectives. Tun et al. (2025) complement this with a systematic review synthesising evidence on trust barriers and facilitators in AI-CDSS, identifying transparency and controllability as primary trust drivers — properties that the proposed system's argumentation traces and human-in-the-loop intervention points are designed to provide. Ciatto et al. (2019) propose XMAS (eXplainable Multi-Agent Systems), arguing that MAS architecture *naturally* supports explainability because inter-agent communication produces inspectable reasoning traces. Alzetta et al. (2020) extend this with a framework for real-time explainability in BDI multi-agent systems for healthcare, addressing the temporal dimension of clinical explanations.

*Synthesis.* Trust in clinical AI requires explanations that are clinically plausible, not merely technically interpretable. Multi-agent architectures provide inherent explainability through inter-agent debate traces. The proposed system leverages this by combining Dung's AAF resolution — which produces formal acceptance and rejection labels — with natural-language argumentation that mirrors clinical discourse, directly bridging the developer–clinician gap identified by Bienefeld et al. (2023).

### 2.2.5 LLM Clinical Reasoning and Domain Adaptation

The capacity of LLMs to perform clinical reasoning has been extensively studied. Savage et al. (2024), published in *npj Digital Medicine*, develop diagnostic reasoning prompts that reveal the interpretability potential of LLMs in medicine, demonstrating that appropriately prompted models can produce reasoning chains aligned with clinician cognitive processes. Kwon et al. (2024) formalise this at AAAI with a reasoning-aware diagnosis framework that generates rationales alongside diagnoses, providing a methodology for ensuring that reasoning is explicit and evaluable rather than implicit in the model's hidden states.

Sim and Chen (2025) offer a critical counterpoint in *eLife*, emphasising that understanding *reasoning behaviour* — not just prediction accuracy — is equivalent to XAI in the medical LLM context. They propose theoretical frameworks for empowering clinicians to evaluate LLM reasoning quality, arguing that current evaluation practices conflate accurate predictions with sound reasoning. Amin et al. (2025) provide a comprehensive systematic review of LLM advances, evaluation methods, and explainability in healthcare, covering model transparency challenges and evaluation frameworks applicable to the proposed system's multi-dimensional assessment strategy.

*Synthesis.* LLMs can produce clinician-style reasoning, but this capability is fragile — dependent on prompting strategy and lacking formal guarantees. Structured argumentation provides a principled oversight mechanism: LLM-generated claims become premises in formal arguments that must survive attack and defeat resolution before being accepted, ensuring reasoning quality beyond what prompting alone can guarantee.

### 2.2.6 Vision–Language Models and CLIP-Based Retrieval for Medical Imaging

Vision–language models enable AI systems to jointly process medical images and text, a capability central to the proposed Vision Agent. Li et al. (2023) introduce LLaVA-Med, a biomedical multimodal conversational assistant created by fine-tuning the LLaVA architecture on instruction-following data generated by GPT-4 from PubMed Central figure–caption pairs. LLaVA-Med achieves strong performance on biomedical visual question-answering benchmarks and, at 7 billion parameters, can be deployed on consumer-grade hardware using 4-bit quantisation. Its open-ended conversational interface makes it suitable for generating structured findings from chest radiographs that serve as premises in formal arguments. However, LLaVA-Med was not designed for multi-agent debate and has not been evaluated within an argumentation framework.

Boecking et al. (2022) present BioViL, a biomedical vision–language model featuring CXR-BERT, a radiology-specific text encoder that improves phrase grounding in chest X-ray images. Published at ECCV and MIT-licensed, BioViL produces joint image–text embeddings suitable for deployment alongside LLaVA-Med on a single consumer GPU. The CXR-specific training of BioViL provides superior embeddings for chest radiograph retrieval compared to general-purpose CLIP (Radford et al., 2021) and its earlier medical adaptations: ConVIRT (Zhang et al., 2022), which established paired CXR–report contrastive pre-training, and MedCLIP (Wang et al., 2022), which introduced decoupled contrastive learning from unpaired medical images and text. Tiu et al. (2022) validate the CLIP paradigm for CXR understanding with CheXzero, a contrastive model trained on MIMIC-CXR image–report pairs that achieves expert-level zero-shot pathology detection, published in *Nature Biomedical Engineering*.

*Synthesis.* VLMs and CLIP-based models provide the visual understanding and image retrieval capabilities central to the proposed Vision Agent pipeline. BioViL's CXR-specific embeddings enable retrieval of visually similar prior cases from a pre-indexed MIMIC-CXR corpus, and LLaVA-Med generates structured findings from the query image. This BioViL + LLaVA-Med combination, feeding into a formal argumentation framework, has not been explored in any existing system.

### 2.2.7 Multimodal Clinical AI and Data Fusion

The integration of diverse clinical data modalities — imaging, free-text reports, and structured EHR — is widely recognised as essential for comprehensive clinical assessment. Acosta et al. (2022) provide a *Nature Medicine* review categorising fusion approaches as early, late, and joint fusion, noting that late fusion strategies generally outperform early fusion for heterogeneous modalities. Huang et al. (2020) review deep learning approaches specifically combining CXR images with structured EHR data and find that multimodal models consistently outperform unimodal baselines — but all reviewed systems use neural fusion layers (attention, concatenation, or gating mechanisms) rather than symbolic reasoning. Kline et al. (2022) reinforce this finding at broader scope, surveying 128 multimodal machine learning studies across imaging, clinical notes, EHR, and omics data and reporting zero instances of formal argumentation as a fusion mechanism.

Dedicated work on report understanding further contextualises the proposed system. Smit et al. (2020) introduce CheXbert, a BERT-based automatic labeler that extracts structured pathology labels from radiology reports with improved accuracy over the rule-based CheXpert labeler for certain pathologies. Miura et al. (2021) address cross-modal factual consistency — ensuring that generated text accurately reflects image content — using reward-based training with factual completeness metrics. This concern maps directly to the proposed system's cross-modal agreement evaluation, where findings derived by the Vision Agent from CXR images are compared against findings derived by the Report Agent from radiology reports, with disagreements resolved through formal argumentation rather than learned reward functions.

*Synthesis.* Multimodal fusion is demonstrably beneficial for clinical AI, but all existing approaches are neural. The proposed system introduces *argumentation-based fusion*: modality-specific agents generate arguments from their respective data sources, and Dung's AAF resolves inter-modal conflicts through formal semantics rather than learned attention weights. This constitutes a fundamentally novel fusion paradigm.

---

## 2.3 Critical Analysis and Research Gap

The preceding review reveals a mature but fragmented landscape. Multi-agent LLM systems improve clinical reasoning through debate (Hong et al., 2024; Ke et al., 2024), formal argumentation theory provides rigorous conflict resolution (Dung, 1995; Prakken, 2009), RAG grounds LLM outputs in evidence (Amugongo et al., 2025), and VLMs enable powerful image understanding (Li et al., 2023; Boecking et al., 2022). However, no existing system integrates all of these capabilities. Table 2.1 compares the proposed system against the closest existing approaches across eight dimensions.

**Table 2.1: State-of-the-art comparison — existing approaches versus the proposed system.**

| System | Multi-Agent | LLM / VLM | Formal Argumentation | KG-RAG | CLIP Image RAG | Explainability | Multimodal Data | Multi-Dim. Eval. |
|--------|:-----------:|:---------:|:-------------------:|:------:|:--------------:|:--------------:|:---------------:|:----------------:|
| ArgMed-Agents (Hong et al., 2024) | ✓ | GPT-3.5/GPT-4 | Dung AAF + ASCD | ✗ | ✗ | Scheme traces | Text only | Accuracy |
| MedGen (Liu et al., 2024) | ✓ | LLM | Debate | Vector RAG | ✗ | Fusion trace | Text only | Accuracy, F1 |
| MDAgents (Kim et al., 2024) | ✓ | GPT-4 | Adaptive | ✗ | ✗ | Limited | Text only | Accuracy |
| MedRAG (Zhao et al., 2025) | ✗ | LLM | ✗ | KG-RAG | ✗ | Retrieval-based | Text only | Accuracy, F1 |
| **Proposed System** | **✓** | **Meditron + LLaVA-Med + BioViL** | **Dung AAF + Walton** | **GraphRAG** | **✓ (BioViL)** | **Full trace** | **CXR + Report + EHR** | **Multi-dimensional** |

Several critical gaps emerge from this analysis:

1. **No formal argumentation for multimodal fusion.** While ArgMed-Agents (Hong et al., 2024) successfully applies Dung's AAF to text-only medical QA, all 128 multimodal clinical AI studies surveyed by Kline et al. (2022) use neural fusion. Huang et al. (2020) confirm that no CXR + EHR system employs symbolic reasoning for modality integration. The proposed system extends formal argumentation to genuinely multimodal clinical data, introducing argumentation-based fusion as a fundamentally new paradigm in which inter-modal conflicts are resolved through Dung's preferred semantics rather than learned weights.

2. **No modality-based agent partitioning.** Existing multi-agent systems partition agents by functional role (diagnostician, critic, reviewer) rather than by data modality. The hidden profile literature (Lu et al., 2012; Schulz-Hardt et al., 2006) demonstrates that distributing unique information across group members with structured dissent improves collective decision quality — a theoretical basis that has never been applied to multimodal clinical AI. The proposed system operationalises this through Vision, Report, and Clinical agents that each observe a single modality and must debate to pool their unique perspectives.

3. **No CLIP image retrieval combined with graph-based text RAG.** Existing RAG systems use either vector-based text retrieval (Ke et al., 2025; Amugongo et al., 2025) or graph-based retrieval (Wang et al., 2025), while CLIP has been independently applied to CXR retrieval (Tiu et al., 2022; Boecking et al., 2022). No system combines both retrieval paradigms within a single argumentation pipeline.

4. **Limited evaluation dimensionality.** As Table 2.1 illustrates, most systems report only accuracy or F1. The proposed system evaluates across six dimensions: diagnostic accuracy (CheXpert 14-label macro/micro-F1, AUROC per pathology), explainability (reasoning trace fidelity), process transparency (argumentation tree completeness), trust (clinician-facing confidence calibration), robustness (ablation stability across A1–A7), and cross-modal agreement between Vision and Report agents.

5. **Closed-source LLM dependence.** ArgMed-Agents and MDAgents rely exclusively on closed-source OpenAI models (GPT-3.5/GPT-4). The proposed system uses open-source models (Meditron, LLaVA-Med) as primary backbones with GPT-4o as a comparison baseline, enabling reproducibility and institutional deployment without commercial API dependencies.

The proposed system sits at the intersection of these gaps. It is the first to combine modality-partitioned multi-agent debate, Dung's AAF with Walton's argumentation schemes, multimodal RAG (CLIP Image RAG + GraphRAG), and multi-dimensional evaluation on real-world clinical data from the MIMIC ecosystem. This positioning addresses all five identified gaps simultaneously and constitutes the primary research contribution of this project.


---

# Chapter 3: Requirements Analysis

This chapter translates the research questions and system design into concrete engineering requirements. Section 3.1 identifies the project stakeholders. Section 3.2 states the aim and measurable objectives. Section 3.3 applies MoSCoW prioritisation to scope the deliverables. Section 3.4 presents the high-level system architecture. Sections 3.5 and 3.6 specify the functional and non-functional requirements, each with traceable acceptance criteria.

---

## 3.1 Stakeholders

Four stakeholder groups stand to benefit from this work, though their involvement varies in directness.

**Clinicians** are the primary users. The system is designed as a decision support tool for physicians, radiologists, and multidisciplinary teams who must reconcile conflicting evidence from imaging, free-text reports, and laboratory data. For this group, the key requirements are explainability (can the clinician follow the reasoning chain?), trust calibration (does the system indicate when it is uncertain?), and transparency (which evidence supports which conclusion?).

**AI and healthcare informatics researchers** form the secondary audience. The modality-partitioned agent architecture, the use of formal argumentation as a multimodal fusion mechanism, and the six-dimensional evaluation framework are all methodological contributions that other researchers may adapt. For this group, requirements centre on reproducibility — open-source models, publicly accessible datasets, and documented experimental protocols.

**Patients** benefit indirectly. If the system reduces diagnostic errors or helps clinicians catch findings that a single-modality analysis might miss — for example, a subtle pneumothorax visible on the CXR but absent from the radiology report — patient outcomes improve. However, patients never interact with the system directly, and no patient data beyond the pre-existing de-identified MIMIC records is used.

**Regulatory and ethics bodies** have an oversight interest. The project uses credentialed health data (MIMIC ecosystem via PhysioNet), which requires compliance with the Data Use Agreement, CITI human-subjects training, and Heriot-Watt University's ethics review process. Requirements related to data handling, de-identification assurance, and responsible AI labelling stem from this stakeholder group.

---

## 3.2 Aim and Objectives

### 3.2.1 Aim

To design, implement, and evaluate a multi-agent argumentation system for explainable clinical decision support that integrates chest X-ray images, radiology reports, and structured electronic health records from the MIMIC ecosystem using formal argumentation theory and multimodal retrieval-augmented generation.

### 3.2.2 Objectives

The following seven objectives are concrete, measurable, and each maps to at least one research sub-question:

| # | Objective | Traces To |
|---|-----------|-----------|
| O1 | Implement modality-based partitioning across three agents — Vision Agent (CXR images), Report Agent (radiology reports), and Clinical Agent (structured EHR) — each processing a single data modality from the MIMIC ecosystem | SRQ3 |
| O2 | Implement Dung's Abstract Argumentation Framework with preferred-extension computation to formally resolve cross-modal conflicts between agents | SRQ1 |
| O3 | Integrate Walton's argumentation schemes as a classification layer so that each agent argument is labelled with a reasoning type (e.g., Argument from Expert Opinion, Argument from Sign) | SRQ1 |
| O4 | Build a dual retrieval pipeline combining CLIP-based Image RAG (BioViL embeddings + ChromaDB) with GraphRAG (Microsoft GraphRAG + Neo4j) and run an infrastructure sweep across three retrieval configurations | SRQ2 |
| O5 | Evaluate the system on a 2,000–3,000 study subset of linked MIMIC data (CXR-JPG + IV-Note + IV) using six metric dimensions: CheXpert 14-label pathology detection, explainability, process transparency, trust, robustness, and cross-modal agreement | SRQ4 |
| O6 | Compare the full system against five baselines (B1–B5) and conduct seven ablation studies (A1–A7) to isolate the contribution of each component and modality | SRQ3, SRQ4 |
| O7 | Produce a Supervisor agent that sees all textual arguments from the three modality agents, mediates multi-round debate via a LangGraph state machine, and manages convergence | RQ |

---

## 3.3 MoSCoW Prioritisation

Requirements are prioritised using the MoSCoW framework. Each item traces to a research question or roadmap deliverable. Table 3.1 summarises the prioritisation.

**Table 3.1: MoSCoW prioritisation of system requirements.**

| Priority | Requirement | Traces To |
|----------|-------------|-----------|
| **Must Have** | Multi-agent debate with 3 modality-partitioned agents + Supervisor | RQ, SRQ3 |
| **Must Have** | Dung's AAF with preferred-extension computation | SRQ1 |
| **Must Have** | MIMIC multimodal data integration (CXR-JPG v2.1.0 + IV-Note v2.2 + IV v3.1) | SRQ3 |
| **Must Have** | Multi-dimensional evaluation framework (6 dimensions) | SRQ4 |
| **Must Have** | CLIP Image RAG (BioViL embeddings → ChromaDB vector store) | SRQ2 |
| **Must Have** | LangGraph state machine for debate orchestration | RQ |
| **Must Have** | Baseline comparisons (B1–B5) and ablation studies (A1–A7) | SRQ3, SRQ4 |
| **Should Have** | GraphRAG pipeline (Microsoft GraphRAG + Neo4j with medical ontologies) | SRQ2 |
| **Should Have** | Walton scheme classification for argument labelling | SRQ1 |
| **Should Have** | LLaVA-Med 7B VLM pipeline for CXR visual question answering | SRQ3 |
| **Should Have** | Streamlit UI for argumentation tree visualisation | RQ |
| **Could Have** | Cross-institutional generalisability testing on NIH CXR14 and OpenI | SRQ3 |
| **Could Have** | LLM-generated natural language explanations from the argumentation tree | SRQ1 |
| **Could Have** | Model selection benchmark report (1–3 candidate models per role) | SRQ3 |
| **Won't Have** | Real clinical deployment or live patient data integration | — |
| **Won't Have** | Full MIMIC-IV cohort (>300K patients) | — |
| **Won't Have** | Real-time inference or clinical workflow integration | — |

The "Must Have" items define the minimum viable system: three agents that debate over linked MIMIC data with formal argumentation and multi-dimensional evaluation. The "Should Have" items strengthen the system — GraphRAG adds global retrieval, Walton schemes add argument classification, and the VLM pipeline enables direct CXR interpretation — but the core argumentation mechanism could function without them by using text-only inputs and simpler retrieval. The "Won't Have" items are explicitly out of scope for an MSc project but are documented as future work.

---

## 3.4 System Architecture Overview

Figure 3.1 illustrates the end-to-end data flow, from multimodal patient input to the final recommendation with an argumentation trace.

[FIGURE 3.1: High-level system architecture diagram. Input: a multimodal patient case linked by `subject_id` from the MIMIC ecosystem, comprising a CXR JPG image (MIMIC-CXR-JPG), a radiology report (MIMIC-IV-Note), and structured EHR data (MIMIC-IV). A modality router sends each data type to the corresponding agent pipeline: Vision Agent (BioViL embedding → CLIP Image RAG → LLaVA-Med 7B VQA → argument generation via Meditron-8B), Report Agent (section extraction of Findings/Impression → NER via scispaCy → argument generation via Meditron-8B), Clinical Agent (structured prompt serialisation with reference ranges → argument generation via Meditron-8B). All agents produce text-based arguments labelled with Walton scheme types. Arguments feed into a multi-round debate loop orchestrated by LangGraph, with the Supervisor agent mediating and checking convergence (max 5 rounds or agreement). The debate output passes to the symbolic argumentation resolution engine (Dung's AAF — preferred-extension computation), then to an explanation generator that produces a natural-language narrative. Final output: pathology recommendation + explanation + argumentation tree + confidence scores.]

The architecture reflects two design principles. First, **modality-based partitioning** (the OIDP principle) ensures that each agent's perspective is constrained to a single data type, creating genuine information asymmetry that drives meaningful argumentation. Second, **text-domain unification** means that all three agents — regardless of whether they process images, free text, or structured tables — ultimately produce text arguments. The symbolic argumentation layer is therefore modality-agnostic and operates entirely on text, which simplifies the resolution engine and makes it straightforward to add new modalities in future work.

---

## 3.5 Functional Requirements

Table 3.2 specifies the functional requirements. Each requirement has an identifier, a description, a MoSCoW priority, and acceptance criteria that define when the requirement is considered met.

**Table 3.2: Functional requirements.**

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR1 | The system shall load a patient case by `subject_id` and retrieve the linked CXR image, radiology report, and structured EHR record from the MIMIC subset | Must | Given a valid `subject_id`, all three data modalities are loaded and routed to the correct agent within 10 seconds |
| FR2 | The Vision Agent shall process a CXR JPG image through BioViL embedding, CLIP Image RAG retrieval, and LLaVA-Med 7B to produce structured textual findings | Must | Output contains at least one pathology-related finding expressed in natural language, with the top-*k* retrieved similar CXR cases listed |
| FR3 | The Report Agent shall extract Findings and Impression sections from a MIMIC-IV-Note radiology report using rule-based section extraction and scispaCy NER | Must | Given a radiology report with identifiable section headers, extracted text covers ≥ 90% of clinically relevant content |
| FR4 | The Clinical Agent shall serialise structured EHR data (laboratory results, vital signs, medications, demographics) into a formatted text block with reference ranges and abnormality flags | Must | Output includes all available lab values with units, reference ranges, and directional indicators (↑/↓/✓) |
| FR5 | Each agent shall generate text-based arguments labelled with a Walton argumentation scheme type | Should | Each argument includes a `scheme` field drawn from the seven clinically relevant Walton schemes defined in the methodology |
| FR6 | The LangGraph state machine shall orchestrate multi-round debate among the three agents and the Supervisor, terminating upon convergence or after a maximum of 5 rounds | Must | Debate produces an accumulated argument list, an attack-relation graph, and a convergence flag. Round count does not exceed 5 |
| FR7 | The symbolic argumentation engine shall compute preferred extensions from the accumulated attack relations using Dung's AAF | Must | Given a set of arguments and attack relations, the engine returns at least one preferred extension that is conflict-free and admissible |
| FR8 | The explanation generator shall produce a natural-language summary of the final recommendation, citing the winning arguments, the evidence supporting them, and the arguments that were defeated | Should | Output is a coherent paragraph that references specific evidence items and identifies which agent contributed each piece of evidence |

---

## 3.6 Non-Functional Requirements

Table 3.3 specifies the non-functional requirements governing performance, reproducibility, explainability, and scalability.

**Table 3.3: Non-functional requirements.**

| ID | Category | Requirement | Target |
|----|----------|-------------|--------|
| NFR1 | **Performance** | End-to-end inference for a single patient case (all 3 agents + debate + resolution) shall complete within a reasonable time on an RTX 5070 (8 GB VRAM) | ≤ 120 seconds per case |
| NFR2 | **VRAM Budget** | No single model shall exceed 5 GB VRAM when loaded in 4-bit quantised mode; models shall be loaded sequentially, not concurrently | Peak VRAM ≤ 8 GB at any point |
| NFR3 | **Reproducibility** | All primary models (Meditron-8B, LLaVA-Med 7B, BioViL) shall be open-source with publicly available weights; all datasets shall be accessible via PhysioNet or open repositories | No proprietary model or closed dataset required for core experiments |
| NFR4 | **Explainability** | Every final recommendation shall be accompanied by a complete argumentation tree showing all arguments, attack/support relations, scheme labels, and the preferred extension | 100% of outputs include a traceable argumentation structure |
| NFR5 | **Scalability** | The system architecture shall support the addition of new data modalities (e.g., ECG waveforms) by adding a new agent pipeline without modifying the argumentation layer | Adding a modality requires only a new agent node and edge in the LangGraph graph |
| NFR6 | **Data Compliance** | All MIMIC data handling shall comply with the PhysioNet Credentialed Data Use Agreement; no re-identification attempts; no data sharing outside the approved scope | DUA terms met throughout the project lifecycle |
| NFR7 | **Evaluation Coverage** | The evaluation framework shall measure system performance across all six defined dimensions, not accuracy alone | Results reported for all 6 dimensions on every baseline and ablation condition |

---

*This chapter has defined the stakeholders, objectives, prioritised requirements, and system architecture at a level sufficient to guide the implementation described in the subsequent chapters. Every functional requirement traces to a research question, and every MoSCoW item links to a roadmap deliverable, ensuring that the engineered system directly addresses the research gaps identified in Chapter 2.*

---

# Chapter 4: Methodology

This chapter describes the research design, datasets, system architecture, and evaluation strategy for the proposed multi-agent argumentation system. The goal is to provide sufficient detail for replication: every design choice is traceable to either the research questions defined in Chapter 1 or the gaps identified in Chapter 2. Sections 4.1–4.2 cover the overarching methodology and data; Sections 4.3–4.5 detail the technical components; and Section 4.6 specifies the evaluation framework.

---

## 4.1 Research Design Overview

This project follows a **Design Science Research (DSR)** methodology combined with experimental evaluation. DSR was selected because the primary deliverable is a novel software artefact — a multi-agent argumentation system — rather than a purely empirical study. DSR requires iterative design, implementation, and evaluation of an artefact against defined objectives (Hevner et al., 2004), which aligns naturally with the four research sub-questions that target different system components (SRQ1–SRQ4).

The methodology is organised into three sequential phases, illustrated in Figure 4.1.

**Phase 1 — Design (February–April 2026):** This phase covers the literature review, formal specification of the argumentation framework, design of the modality-partitioned agent architecture, and the evaluation metrics. Concurrently, surrogate datasets are downloaded (NIH CXR14, OpenI, MIMIC-IV Demo) and PhysioNet credentialing is initiated via CITI training.

**Phase 2 — Implementation (April–July 2026):** Development follows a **dual-track** strategy. Track 1 builds the full system pipeline — LangGraph orchestration, symbolic argumentation engine, knowledge retrieval, and all three agent pipelines — using surrogate datasets that require no credentialing. Track 2 pursues PhysioNet credentialed access in parallel: CITI certification, DUA submission, and university ethics amendment. When credentialing completes, MIMIC data is integrated into the pipelines already built on surrogates. This dual-track approach eliminates the risk of idle development time during the credentialing process.

A preliminary **model selection benchmark** (see Section 4.3) is conducted early in Phase 2 to empirically justify the final choice of LLM, VLM, and image embedding model, rather than assuming model suitability a priori.

**Phase 3 — Evaluation (July–August 2026):** The complete system is evaluated on the MIMIC multimodal subset against five baselines and seven ablation conditions, using the six-dimensional metric framework described in Section 4.6.

[FIGURE 4.1: Three-phase methodology pipeline. Left box: Phase 1 DESIGN — literature review, formal specification, surrogate download, PhysioNet credentialing start. Centre box: Phase 2 IMPLEMENT — dual track: Track 1 (build on surrogates) and Track 2 (credentialing + MIMIC download), converging at data transition. Right box: Phase 3 EVALUATE — quantitative metrics (6 dimensions), baselines (B1–B5), ablations (A1–A7), qualitative case studies. Arrows flow left to right with the dual tracks merging mid-Phase 2.]

---

## 4.2 Dataset

### 4.2.1 The MIMIC Ecosystem

The primary data comes from three linked datasets within the MIMIC ecosystem, maintained by the MIT Laboratory for Computational Physiology and hosted on PhysioNet. Table 4.1 summarises each dataset.

**Table 4.1: Primary datasets from the MIMIC ecosystem.**

| Dataset | Content | Scale | Patients | Access |
|---------|---------|-------|----------|--------|
| MIMIC-CXR-JPG v2.1.0 | 377,110 chest radiographs in JPG format, each labelled with 14 CheXpert pathology categories | ~570 GB (full) | 65,379 | PhysioNet Credentialed |
| MIMIC-IV-Note v2.2 | 2,321,355 radiology reports and 331,794 discharge summaries | ~3 GB | 237,427 | PhysioNet Credentialed |
| MIMIC-IV v3.1 | Structured electronic health records: laboratory results, vital signs, medications, diagnoses, procedures | ~7 GB | 364,627 | PhysioNet Credentialed |

All three datasets share a common `subject_id` field, and CXR images link to their corresponding radiology reports through `study_id`. MIMIC-CXR patients are a subset of MIMIC-IV, specifically emergency-department-admitted patients from Beth Israel Deaconess Medical Center (2011–2016). This linkage enables the system to load a single patient's chest X-ray, the radiologist's free-text report, and the structured clinical record as three independent data streams — one per agent (Johnson et al., 2019a; Johnson et al., 2023a).

### 4.2.2 CheXpert 14-Label Taxonomy

Evaluation uses the CheXpert labelling standard (Irvin et al., 2019), which assigns each study one or more of 14 pathology categories: Atelectasis, Cardiomegaly, Consolidation, Edema, Enlarged Cardiomediastinum, Fracture, Lung Lesion, Lung Opacity, Pleural Effusion, Pneumonia, Pneumothorax, Pleural Other, Support Devices, and No Finding. This multi-label setting is well-suited to argumentation because agents may agree on some labels while disputing others within the same study — for example, all three agents may concur on Pleural Effusion while disagreeing about whether Pneumonia is also present.

### 4.2.3 Subset Strategy

Working with the full MIMIC-CXR-JPG dataset (570 GB) is neither necessary nor practical for this project. Instead, a targeted subset of **2,000–3,000 frontal-view studies** is constructed, totalling approximately 2–3 GB. The subsetting procedure is as follows:

1. Download only the CSV metadata files (~10 MB): `mimic-cxr-2.0.0-chexpert.csv.gz` and `mimic-cxr-2.0.0-metadata.csv.gz`.
2. Filter to **frontal views** (PA and AP projections), reducing image count by approximately 40%.
3. Retain studies with positive CheXpert labels for five target pathologies: Cardiomegaly, Pleural Effusion, Pneumonia, Pneumothorax, and Atelectasis.
4. Draw a stratified random sample of 2,000–3,000 studies, balanced across pathologies with approximately 25% "No Finding" controls.
5. Download only the matching JPG files via selective retrieval (~1–2 GB).
6. Download the linked radiology reports from MIMIC-IV-Note (~50 MB) and the corresponding structured EHR records from MIMIC-IV (~100–200 MB).

Each study in the final subset therefore contains all three modalities linked by `subject_id` and `study_id`, ensuring that every test case exercises all three agents.

### 4.2.4 Dual-Track Development

Access to MIMIC data requires PhysioNet credentialed status, which involves completing CITI human-subjects training and signing a Data Use Agreement. The credentialing timeline is uncertain (typically 2–6 weeks), so development proceeds on a dual-track basis:

- **Track 1 (immediate):** The system is built and tested on three openly available surrogate datasets — NIH ChestX-ray14 (112,120 CXR images, CC0 licence) for the Vision Agent, OpenI Indiana University (7,470 CXR–report pairs) for the Report Agent, and MIMIC-IV Demo (100 de-identified patients, open access) for the Clinical Agent. These surrogates share the same data formats as the full MIMIC datasets and require no credentialing.
- **Track 2 (parallel):** CITI training and the PhysioNet application proceed concurrently. Once approved, the real MIMIC subset is downloaded and integrated into the pipelines already validated on surrogates.

This strategy means that credentialing delays do not block implementation progress.

---

## 4.3 System Architecture

### 4.3.1 Modality-Based Partitioning

The system follows the **OIDP** (One Issue, Different Perspectives) design principle, where each agent examines the same clinical case through a single data modality. Three modality-partitioned agents and one Supervisor agent form the core architecture. Table 4.2 specifies each agent's role.

**Table 4.2: Agent specifications and modality assignments.**

| Agent | Data Source | Input Processing | Model | Sees | Does Not See |
|-------|-----------|------------------|-------|------|-------------|
| Vision Agent | MIMIC-CXR-JPG images | BioViL embedding + LLaVA-Med 7B VQA | LLaVA-Med 7B (4-bit) | CXR image only | Report text, EHR data |
| Report Agent | MIMIC-IV-Note reports | Section extraction (Findings/Impression) + NER | Meditron-8B (4-bit) | Radiology report only | CXR image, EHR data |
| Clinical Agent | MIMIC-IV structured EHR | Structured prompt serialisation | Meditron-8B (4-bit) | Labs, vitals, demographics | CXR image, report text |
| Supervisor | All agent arguments | Argument consolidation | Meditron-8B (4-bit) | All textual arguments | Raw images or data |

This partitioning mirrors real clinical multidisciplinary team (MDT) workflows. A radiologist interprets the chest X-ray without necessarily examining the full lab workup; a clinician reviews laboratory results and medications without directly reading the image. When they confer, their independent viewpoints may converge or conflict — and it is precisely those conflicts that make formal argumentation meaningful. A system where all agents see all modalities would lack genuine disagreement, reducing the argumentation to a redundant consensus exercise. In contrast, modality-based partitioning creates natural cross-modal conflicts: the Vision Agent may interpret bilateral opacities as suggestive of pneumonia, while the Report Agent reads the radiologist's impression as "cardiomegaly without acute infiltrate," and the Clinical Agent notes a normal white blood cell count. Dung's AAF (Section 4.4) resolves such disputes through formal attack relations rather than simple voting.

The decision to use exactly three agents reflects the structure of the MIMIC ecosystem itself — three linked data types, each mapping to one agent. This produces up to six directed attack edges per debate round, which is computationally tractable and analytically interpretable within the scope of this project. Further sub-division (e.g., splitting EHR into separate labs and medications agents) is noted as future work.

### 4.3.2 Model Selection Benchmark

Rather than assuming model suitability, a preliminary benchmarking step is conducted early in Phase 2 on approximately 100–200 surrogate studies. Candidate models are compared across three roles:

- **Text LLM:** Meditron-8B / Llama-3-Meditron-8B (medical-specialised) vs. Llama-3.1-8B (general-purpose baseline).
- **Image embeddings:** BioViL (Boecking et al., 2022) vs. MedCLIP.
- **VLM:** LLaVA-Med 7B (Li et al., 2023) vs. LLaVA-v1.5-7B (general-purpose).

Candidates are evaluated on multi-label F1 (against CheXpert ground-truth labels), inference latency, and VRAM consumption. The final model selection is therefore empirically justified — not assumed a priori. Based on current literature evidence, the leading candidates are Meditron-8B, BioViL, and LLaVA-Med 7B, all of which run within the project's 8 GB VRAM budget under 4-bit quantisation.

### 4.3.3 Vision Agent Pipeline

The Vision Agent's processing pipeline transforms a raw CXR image into textual arguments through three stages:

1. **Embedding:** The CXR JPG is passed through BioViL's vision encoder (Boecking et al., 2022), producing a dense embedding vector.
2. **CLIP Image RAG:** The embedding is used for similarity search against a ChromaDB vector store containing BioViL embeddings of the training-set CXR images. The top-*k* most similar historical cases are retrieved as supporting evidence.
3. **VLM Interpretation:** The CXR image, together with the retrieved similar cases, is passed to LLaVA-Med 7B (Li et al., 2023) for visual question answering. The VLM generates structured textual findings — e.g., "bilateral lower lobe opacities, cardiomegaly present, no pneumothorax."
4. **Argument Generation:** The textual findings are fed to the LLM (Meditron-8B), which produces formal arguments labelled with Walton scheme types (see Section 4.4).

This pipeline ensures that the CXR image never enters the argumentation layer directly; only the VLM's textual interpretation does. The symbolic argumentation infrastructure therefore operates entirely in the text domain.

### 4.3.4 LangGraph Orchestration

Agent coordination is managed by a LangGraph state machine (LangGraph v1.0+). The state graph encodes the full debate lifecycle as a directed graph of processing nodes and conditional edges. The state object tracks accumulated arguments, attack and support relations, the current debate round, convergence status, and the final preferred extension.

The debate proceeds as follows: after initial modality processing, each agent generates arguments grounded in its data modality and retrieved knowledge. The Supervisor evaluates all arguments and identifies cross-modal conflicts. Agents may then counter-argue in subsequent rounds. The debate terminates when either (a) agents converge — no new attacks are raised — or (b) a maximum of five rounds is reached. At termination, the symbolic argumentation engine (Section 4.4) computes the preferred extension, and an explanation generator renders the resolution as a natural-language narrative with a traceable argumentation tree. Figure 4.2 illustrates the complete end-to-end pipeline.

[FIGURE 4.2: High-level system architecture diagram. Top: Multimodal patient case input (CXR image + radiology report + structured EHR), linked by `subject_id`. Three parallel pipelines feed into Vision Agent, Report Agent, and Clinical Agent. All agents produce text arguments. Arguments pass through knowledge retrieval (CLIP Image RAG + GraphRAG), then multi-round debate orchestrated by LangGraph with Supervisor mediation, then symbolic argumentation resolution (Dung's AAF + Walton's Schemes), then explanation generation. Output: recommendation + explanation + argumentation tree + confidence scores.]

---

## 4.4 Symbolic Argumentation Layer

### 4.4.1 Dung's Abstract Argumentation Framework

The debate resolution mechanism is grounded in Dung's Abstract Argumentation Framework (Dung, 1995), one of the most widely adopted formalisms for modelling conflict between arguments (Charwat et al., 2015). An AAF is defined as a pair $\langle \mathcal{A}, \mathcal{R} \rangle$, where $\mathcal{A}$ is a finite set of arguments and $\mathcal{R} \subseteq \mathcal{A} \times \mathcal{A}$ is a binary attack relation. An argument $a$ attacks argument $b$ if $(a, b) \in \mathcal{R}$.

A set $S \subseteq \mathcal{A}$ is **conflict-free** if no two arguments in $S$ attack each other. $S$ is **admissible** if it is conflict-free and every argument in $S$ is defended by $S$ — that is, for every argument $b$ attacking some $a \in S$, there exists a $c \in S$ such that $c$ attacks $b$. A **preferred extension** is a maximal admissible set with respect to set inclusion. The system computes preferred extensions to determine the "winning" set of arguments that survive cross-modal debate.

In practice, each agent's claims about pathology labels become arguments in $\mathcal{A}$. When two agents' findings contradict — say the Vision Agent asserts "Pneumonia likely" while the Clinical Agent asserts "Normal WBC, pneumonia unlikely" — the system registers an attack relation between the corresponding arguments. Preferred-extension computation then identifies which claims survive, giving formal justification for the final recommendation.

### 4.4.2 Walton's Argumentation Schemes

While Dung's AAF captures **which** arguments win, it does not describe **how** arguments are constructed. To classify argument types and evaluate their internal validity, the system employs Walton's argumentation schemes (Walton et al., 2008). From Walton's catalogue of 60 schemes, seven are selected for clinical relevance, following the approach used by Hong et al. (2024) in the ArgMed-Agents system. Table 4.3 lists these schemes with clinical examples.

**Table 4.3: Clinically relevant Walton argumentation schemes.**

| Scheme | Clinical Application Example |
|--------|------------------------------|
| Argument from Expert Opinion | "The radiologist's report states cardiomegaly is present" |
| Argument from Evidence to Hypothesis | "Troponin I elevated at 2.4 ng/mL, suggesting myocardial injury" |
| Argument from Analogy | "Retrieved similar CXR case (BioViL cosine similarity 0.92) showed confirmed pneumonia" |
| Argument from Cause to Effect | "Furosemide administration may cause electrolyte imbalance" |
| Argument from Consequences | "Delayed treatment increases risk of respiratory deterioration" |
| Argument from Established Rule | "ESC guidelines recommend echocardiography for BNP > 300 pg/mL" |
| Argument from Sign | "Bilateral pleural effusions are a sign of congestive heart failure" |

Each agent's LLM (Meditron-8B) is prompted to label its generated arguments with the applicable scheme type. The Supervisor agent uses these labels during debate mediation — for instance, an Argument from Expert Opinion (the radiologist's written impression) may carry more weight than an Argument from Analogy (a retrieved similar case) when they conflict. The scheme labels also serve an explainability function: the final argumentation tree presented to the clinician indicates not only which arguments won but *why* each argument was constructed (see Chapter 2 for a detailed discussion of argumentation theory).

### 4.4.3 Integration with LLM and VLM Output

All three agents ultimately produce **text-based arguments**, regardless of their input modality. The Vision Agent's VLM converts the CXR image into textual findings; the Report Agent extracts structured text from the radiology report; the Clinical Agent serialises structured EHR data into a formatted text block. This uniform text representation means the symbolic argumentation layer — attack/support relations, Walton scheme classification, preferred-extension computation — operates entirely in the text domain and is agnostic to the upstream data modality. The argumentation infrastructure is therefore modular: adding a new modality (e.g., ECG waveforms) requires only a new agent pipeline, not changes to the symbolic layer.

---

## 4.5 Knowledge Retrieval Pipeline

### 4.5.1 CLIP Image RAG

The Vision Agent augments its reasoning with **CLIP-based Image Retrieval-Augmented Generation (CLIP Image RAG)**. BioViL (Boecking et al., 2022), a CXR-specific vision-language model pre-trained with contrastive learning, produces dense embedding vectors for each CXR image. These embeddings are stored in a ChromaDB vector database during an offline indexing phase that covers the non-test portion of the MIMIC-CXR-JPG subset. At inference time, the embedding of the query CXR is compared against the stored vectors via cosine similarity, and the top-*k* most similar historical cases — along with their CheXpert labels and associated reports — are retrieved as evidence. This gives the Vision Agent access to precedent: "a similar-looking CXR was previously labelled as Cardiomegaly + Pleural Effusion."

### 4.5.2 GraphRAG

For text-based retrieval, the system uses Microsoft's open-source GraphRAG pipeline (Microsoft, 2024), which constructs a knowledge graph from unstructured clinical text (guidelines, textbook excerpts, PubMed abstracts) and applies community detection to identify clusters of related entities. GraphRAG supports both **local search** (entity-centric retrieval) and **global search** (community-level summarisation), enabling the agents to answer queries that span multiple entities — for instance, "What are the differential diagnoses for bilateral opacities in a patient with elevated BNP?" Standard vector RAG would rely solely on semantic similarity to individual chunks; graph-augmented retrieval captures entity relationships and produces more contextually complete answers (Wang et al., 2025).

### 4.5.3 Infrastructure Sweep

To answer **SRQ2** — *How do different Retrieval-Augmented Generation approaches affect the factual grounding and consistency of multi-agent clinical reasoning?* — the system is evaluated under three retrieval configurations with all other components held constant:

**Table 4.4: Infrastructure sweep conditions (SRQ2).**

| Run | Retrieval Backend | What Changes |
|-----|-------------------|-------------|
| A | Vector RAG (ChromaDB, text embeddings only) | Semantic similarity retrieval over text chunks |
| B | GraphRAG (Microsoft GraphRAG + Neo4j) | Graph community detection + entity-relationship retrieval |
| C | **Multimodal Hybrid** (Text Vector RAG + GraphRAG + CLIP Image RAG) | All three retrieval methods combined |

The same three modality-partitioned agents, the same prompts, and the same symbolic argumentation layer are used across all three runs. Run C is the most novel configuration — no published argumentation system combines CLIP-based image retrieval with knowledge-graph-grounded text retrieval for formal multi-agent debate. The unit of analysis is the whole system's collective output (pathology predictions, explanation quality, argumentation depth), which directly answers SRQ2.

### 4.5.4 Medical Knowledge Graph

A Neo4j graph database stores structured medical knowledge drawn from publicly available ontologies — UMLS Metathesaurus, SNOMED-CT, ICD-10, and the PrimeKG precision-medicine knowledge graph (Harvard, MIT licence). These provide entity relationships (e.g., drug–disease interactions, symptom–diagnosis associations) that the LLM-based agents can query during argument construction. Clinical guidelines (ACR Appropriateness Criteria, Fleischner Society guidelines, ESC 2023 cardiovascular guidelines) are also indexed into the GraphRAG pipeline to ground agent reasoning in evidence-based protocols.

---

## 4.6 Evaluation Strategy

### 4.6.1 Evaluation Dimensions

The evaluation framework moves beyond accuracy-only assessment. Six dimensions capture clinical outcome quality, explainability, process transparency, trust calibration, robustness, and cross-modal information fusion. Table 4.5 provides an overview; Sections 4.6.2–4.6.3 specify the key metrics formally.

**Table 4.5: Six-dimensional evaluation framework.**

| Dimension | Focus | Key Metrics |
|-----------|-------|-------------|
| 1. Clinical Outcome Quality | Pathology detection accuracy | Multi-label F1 (macro/micro), per-pathology AUROC, pathology co-occurrence accuracy |
| 2. Explainability | Quality of reasoning explanations | Explanation completeness, argumentation coverage, faithfulness, BLEU/ROUGE-L |
| 3. Process Transparency | Visibility of the debate process | Debate depth, attack rate, convergence quality, argument traceability |
| 4. Trust | Calibration and uncertainty handling | Expected Calibration Error (ECE), uncertainty indication |
| 5. Robustness | Stability under perturbation | Sensitivity to missing evidence (10/20/30% dropout), paraphrase consistency |
| 6. Cross-Modal Agreement | Cross-modal reasoning effectiveness | Cross-modal discovery rate, unique evidence contribution, modality complementarity, VLM faithfulness |

### 4.6.2 Key Metric Formulations

**Multi-label F1 (Macro).** Each of the 14 CheXpert pathology labels is treated as an independent binary classification. Macro-averaged F1 weights all labels equally:

$$F1_{\text{macro}} = \frac{1}{K} \sum_{k=1}^{K} F1_k \quad \text{where } F1_k = \frac{2 \cdot P_k \cdot R_k}{P_k + R_k} \tag{4.1}$$

where $K = 14$ is the number of pathology labels, and $P_k$, $R_k$ are precision and recall for label $k$.

**Multi-label F1 (Micro).** Micro-averaged F1 pools all true positives, false positives, and false negatives across all 14 labels before computing precision and recall:

$$F1_{\text{micro}} = \frac{2 \sum_{k=1}^{K} TP_k}{2 \sum_{k=1}^{K} TP_k + \sum_{k=1}^{K} FP_k + \sum_{k=1}^{K} FN_k} \tag{4.2}$$

**Per-Pathology AUROC.** The Area Under the Receiver Operating Characteristic curve is computed for each pathology label independently, measuring discrimination between positive and negative cases:

$$AUROC_k = \int_0^1 TPR_k(t) \, d(FPR_k(t)) \tag{4.3}$$

This is particularly important for clinically critical conditions such as Pneumothorax and Pneumonia, where false negatives carry high clinical cost.

**Expected Calibration Error (ECE).** Trust calibration is measured by partitioning predictions into $M$ equally-spaced confidence bins and computing the weighted average gap between confidence and accuracy:

$$ECE = \sum_{m=1}^{M} \frac{|B_m|}{n} \left| \text{acc}(B_m) - \text{conf}(B_m) \right| \tag{4.4}$$

where $B_m$ is the set of predictions falling in bin $m$, $\text{acc}(B_m)$ is the observed accuracy within the bin, and $\text{conf}(B_m)$ is the average predicted confidence. Lower ECE indicates better-calibrated confidence scores.

**Cross-Modal Agreement.** To quantify whether agents processing different modalities arrive at compatible conclusions, Cohen's kappa ($\kappa$) is computed between the Vision Agent's pathology labels and the Report Agent's labels:

$$\kappa = \frac{p_o - p_e}{1 - p_e} \tag{4.5}$$

where $p_o$ is observed agreement and $p_e$ is expected agreement by chance. High $\kappa$ suggests modality convergence; low $\kappa$ indicates genuine cross-modal conflict — precisely the cases where formal argumentation adds the most value.

### 4.6.3 Baselines

Five baseline conditions isolate the contribution of each major system component. Table 4.6 summarises each baseline.

**Table 4.6: Baseline conditions (B1–B5).**

| # | Baseline | Description | Tests |
|---|----------|-------------|-------|
| B1 | Single LLM (Zero-Shot) | GPT-4o with direct multimodal prompting, no agents | Value of multi-agent architecture |
| B2 | Single LLM + RAG | Single LLM with standard text-only vector RAG | Value of multimodal retrieval + KG-RAG |
| B3 | Multi-Agent, No Argumentation | Three modality agents debate without Dung's AAF resolution | Value of the symbolic argumentation layer |
| B4 | Existing System | Closest published radiology MAS or argumentation system | Direct comparison with current SOTA |
| B5 | Full System (Proposed) | All components: modality partitioning + AAF + best RAG configuration | Cumulative improvement |

The progression from B1 to B5 is additive: each baseline adds one system component, allowing the marginal contribution of multi-agent debate, symbolic argumentation, and multimodal RAG to be measured independently.

### 4.6.4 Ablation Studies

Seven ablation studies remove individual components to measure their isolated contribution. Table 4.7 describes each ablation.

**Table 4.7: Ablation conditions (A1–A7).**

| # | Ablation | Component Removed | Question Answered |
|---|----------|-------------------|-------------------|
| A1 | No Image RAG | Replace CLIP Image RAG with text-only RAG | Does visual retrieval improve pathology detection? |
| A2 | No Symbolic Layer | Remove Dung's AAF; keep LLM-only debate | Does formal argumentation improve over informal debate? |
| A3 | No Modality Partitioning | All agents see all modalities | Does modality-based asymmetry improve reasoning? |
| A4 | Single Agent | One agent with all data + KG-RAG + AAF | Do multiple agents outperform one agent? |
| A5 | General LLM | Replace Meditron-8B with Llama-3.1-8B | Does domain-specific pre-training matter? |
| A6 | No Vision Agent | Remove CXR image modality entirely | How much does the image modality contribute? |
| A7 | No Clinical Agent | Remove structured EHR data entirely | How much does structured clinical data contribute? |

Ablations A6 and A7 are especially relevant because they directly test whether each data modality provides non-redundant information — a core assumption of the OIDP design. If removing the Vision Agent (A6) has minimal impact, this would suggest that the radiologist's report already captures the relevant imaging findings, challenging the case for VLM-based image analysis.

### 4.6.5 Evaluation Protocol

The evaluation protocol proceeds as follows. A held-out test set of approximately **400–600 MIMIC studies**, stratified by pathology profile to ensure representation of all five target pathologies plus "No Finding" controls, is set aside before any system development.

For each study in the test set:

1. Load the CXR image, radiology report, and structured EHR record linked by `subject_id` and `study_id`.
2. Run the study through the full system (B5) and each baseline/ablation condition.
3. Record pathology predictions, explanation text, the argumentation tree, and confidence scores.
4. Compute all metrics across the six evaluation dimensions.
5. Perform statistical significance testing (paired Wilcoxon signed-rank test) between conditions.

In addition, a **qualitative analysis** examines 20 MIMIC cases in detail — 10 where the system produced correct predictions and 10 where it erred. For each case, the argumentation tree is manually inspected to document reasoning patterns, failure modes, and instances where cross-modal conflict led to either correct resolution or misdiagnosis. Particular attention is paid to cases where the Vision Agent and Report Agent disagree, and whether BioViL's CLIP Image RAG retrieved genuinely similar reference images.

A secondary **surrogate comparison** evaluates whether results on the MIMIC-IV Demo subset generalise to the full MIMIC subset, providing a calibration check for researchers who only have access to the open-access demo data.


---

# Chapter 5: Professional, Legal, Ethical, and Social Issues

Developing an AI-based clinical decision support system that processes real patient data — even de-identified data — raises obligations that extend beyond technical design. This chapter examines the professional, legal, ethical, and social (PLES) considerations relevant to this project and describes the measures adopted to address them.

## 5.1 Professional Considerations

The project adheres to the professional standards set out in the BCS Code of Conduct and the ACM Code of Ethics, both of which require computing professionals to avoid harm, act honestly, and maintain competence in the systems they build. Three professional obligations are particularly relevant.

**Responsible AI development.** The system is designed as a decision *support* tool, not a standalone decision-maker. Every diagnostic recommendation is traceable through a formal argumentation graph, and the architecture enforces a human-in-the-loop (HITL) checkpoint at which a clinician can inspect, contest, or override the system's reasoning before any conclusion is acted upon. This separation of recommendation from action aligns with professional guidance on deploying AI in safety-critical domains.

**Reproducibility and openness.** The primary model stack — Meditron (EPFL, Apache 2.0), LLaVA-Med (Li et al., 2023; MIT licence), and BioViL (Boecking et al., 2022; MIT licence) — is entirely open-source. All datasets are publicly available through PhysioNet (Johnson et al., 2019a; Johnson et al., 2023a) or the US National Institutes of Health. The evaluation protocol, including metric definitions and statistical tests, is fully documented in Chapter 4. These choices ensure that the reported results can be independently verified and that no proprietary dependency obstructs replication.

**Competence boundaries.** The system's outputs are produced by language and vision models that have not undergone clinical validation. The project makes no claim of clinical-grade reliability; all outputs carry explicit disclaimers marking them as research prototypes unsuitable for patient care. This distinction is maintained throughout the codebase, the user interface, and this report.

## 5.2 Legal Considerations

The primary legal considerations concern data protection legislation and the licensing terms governing access to clinical datasets.

**GDPR and data protection.** Although the MIMIC datasets originate from a US institution (Beth Israel Deaconess Medical Center, Massachusetts), the project is conducted at Heriot-Watt University, Dubai Campus, under supervision from a UK institution. The General Data Protection Regulation (GDPR) therefore applies to data handling practices. Compliance is achieved through three properties of the dataset: (1) all MIMIC data is de-identified at source under the HIPAA Safe Harbor standard, meaning that 18 categories of identifiers — including names, dates of birth, geographic subdivisions, and medical record numbers — have been removed or shifted prior to release (Johnson et al., 2019a; Johnson et al., 2023a); (2) dates are randomly shifted by a per-patient offset, and ages above 89 are capped, preventing temporal re-identification; and (3) no attempt is made at any point in the project to re-identify patients or link MIMIC records to external data sources. Under GDPR Article 26, data that cannot reasonably be attributed to an identified individual falls outside the scope of personal data regulation, but the project nonetheless follows GDPR-aligned best practices for data minimisation, purpose limitation, and storage security.

**PhysioNet Credentialed Data Use Agreement.** Access to MIMIC-CXR-JPG v2.1.0, MIMIC-IV v3.1, and MIMIC-IV-Note v2.2 (Johnson et al., 2023b) is governed by the PhysioNet Credentialed Health Data License 1.5.0. This agreement imposes several binding requirements: (a) the researcher must complete CITI "Data or Specimens Only Research" training and provide a valid certificate; (b) the researcher's institution must be identified and the supervisor must be named; (c) the data must not be redistributed, shared, or uploaded to cloud platforms; (d) results must be reported in aggregate, not at the level of individual patients; and (e) any derived datasets must comply with the same restrictions. Table 5.1 summarises the compliance status.

**Table 5.1: Dataset ethics and licensing compliance summary.**

| Requirement | MIMIC-CXR-JPG | MIMIC-IV-Note | MIMIC-IV | MIMIC-IV Demo | NIH CXR14 | OpenI |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Publicly available | ✓ (PhysioNet) | ✓ (PhysioNet) | ✓ (PhysioNet) | ✓ (PhysioNet) | ✓ (NIH) | ✓ (NLM) |
| Anonymised at source | HIPAA Safe Harbor | HIPAA | HIPAA | HIPAA | ✓ | ✓ |
| License | PhysioNet 1.5.0 | PhysioNet 1.5.0 | PhysioNet 1.5.0 | ODbL (Open) | CC0 | Public domain |
| Access level | Credentialed | Credentialed | Credentialed | Open | Open | Open |
| CITI training required | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |

**Data storage.** MIMIC data is stored on an encrypted local SSD. No clinical data is uploaded to cloud services, version control repositories, or shared drives. Processed outputs (e.g., embedding vectors, argumentation logs) contain no patient identifiers and are retained for reproducibility.

## 5.3 Ethical Considerations

The Heriot-Watt University Infonetica ethics form was submitted in Week 7 of the project timeline. The project is classified as **medium-risk** research because it uses regulated clinical datasets under a Data Use Agreement, even though no human participants are involved.

**No human participants.** The study uses exclusively pre-existing, de-identified datasets. No patients, clinicians, or other human subjects participate in data collection, interviews, surveys, or user studies. All evaluation is automated against ground-truth CheXpert labels extracted from radiology reports.

**Bias and fairness.** The MIMIC datasets reflect the patient population of a single US academic medical centre (Beth Israel Deaconess Medical Center, Boston). This introduces two sources of potential bias. First, *demographic imbalance*: the patient cohort may not represent the age, sex, or ethnic distribution of other clinical populations, meaning that system performance measured on MIMIC may not generalise to hospitals in other regions. Second, *label uncertainty*: the CheXpert labeler assigns four-valued labels (positive, negative, uncertain, blank) to each pathology (Irvin et al., 2019), and the handling strategy for uncertain and blank labels — commonly mapped to positive, negative, or excluded — directly affects reported accuracy. The evaluation protocol addresses this by reporting per-pathology metrics with explicit U-label handling, and by including stratified analysis where the data permits.

**VLM hallucination risk.** Vision–language models such as LLaVA-Med (Li et al., 2023) can generate fluent but clinically incorrect descriptions of medical images. A VLM might describe "bilateral pleural effusions" in a radiograph that shows no such finding. In a clinical decision support context, undetected hallucinations could mislead clinicians. The proposed system mitigates this risk through three mechanisms: (1) cross-modal agreement metrics compare Vision Agent findings against Report Agent findings derived independently from the radiologist's text, surfacing discrepancies for review; (2) formal argumentation requires the Vision Agent's claims to survive attack from other agents before being accepted into the final extension; and (3) CLIP-based image RAG retrieves visually similar reference cases to ground the VLM's claims in precedent rather than generation alone.

**Decision support, not decision-making.** The system is explicitly designed as a tool that assists clinicians rather than replacing clinical judgement. The HITL architecture ensures that no diagnostic conclusion is finalised without clinician review. This design principle reflects the ethical position that accountability for patient care must remain with qualified human professionals, not automated systems.

## 5.4 Social Considerations

**Clinical autonomy and deskilling.** The introduction of AI-based reasoning tools into clinical workflows raises concerns about the erosion of clinician expertise. If practitioners become accustomed to following system recommendations without critically evaluating the underlying reasoning, diagnostic skills may atrophy over time. The proposed system's argumentation-based design partially addresses this risk by presenting the reasoning trace — including attacks, defeats, and accepted arguments — rather than a bare recommendation. This encourages active cognitive engagement rather than passive acceptance of a binary output.

**Over-reliance risk.** Conversely, a system that produces compelling natural-language explanations may inspire unwarranted confidence. Clinicians may trust a well-articulated but incorrect explanation more than an opaque but correct probability score. The evaluation framework includes trust-related metrics (explanation coherence, clinical plausibility) specifically to measure whether the system's explanatory quality correlates with its diagnostic accuracy — identifying scenarios where persuasive explanations accompany incorrect conclusions.

**Potential benefits.** Despite these risks, explainable multi-agent clinical AI offers significant social benefits. Diagnostic errors remain a leading cause of preventable harm in hospitals worldwide, and many of these errors arise from incomplete information integration across data sources. A system that can surface conflicts between imaging, report, and laboratory findings — and explain why those conflicts matter — could help clinicians catch diagnostic oversights that current tools miss. The multimodal argumentation approach is particularly relevant in resource-constrained settings where access to multidisciplinary team meetings is limited.

**Scope limitation.** This project is a prototype for academic research. It is not intended for deployment in clinical practice, and all outputs carry disclaimers to that effect. Any future clinical deployment would require regulatory approval (e.g., under the EU AI Act's high-risk classification for medical devices), prospective clinical validation, and formal usability studies with practising clinicians — activities that fall outside the scope of this MSc dissertation.


---

# Chapter 6: Project Plan

This chapter presents the project timeline, task breakdown, supervisor checkpoints, and risk mitigation strategy. The plan follows a dual-track development approach: Track 1 builds the complete system on publicly available surrogate datasets while Track 2 pursues PhysioNet credentialing in parallel. The two tracks merge once MIMIC access is granted, at which point the system is re-evaluated on real clinical data with minimal pipeline modification.

## 6.1 Task Breakdown and Deliverables

The project is organised into three sequential phases — Design, Implement, and Evaluate — spanning 26 weeks from February to August 2026.

**Phase 1: Design (February – April 2026).** This phase produces the theoretical and architectural foundations for the system. Key deliverables include the literature review chapter covering 53 papers across 14 categories, the formal specification of the argumentation framework (Dung's AAF with Walton scheme classification), modality-based agent prompt templates for the Vision, Report, and Clinical agents, the Knowledge Graph schema (entity types, relationship types, UMLS ontology mapping), and the multi-dimensional evaluation framework with metric specifications. In parallel, surrogate datasets (MIMIC-IV Demo, NIH CXR14, OpenI) are downloaded, and the PhysioNet credentialing process is initiated through CITI training and application submission.

**Phase 2: Implement (April – July 2026).** Implementation follows a two-track strategy:

- *Track 1 (surrogate development)* proceeds immediately with the LangGraph multi-agent pipeline, the Neo4j Knowledge Graph, the GraphRAG indexing pipeline, the symbolic argumentation engine, and the individual agent pipelines — Vision Agent (BioViL + LLaVA-Med on NIH CXR14), Report Agent (NLP extraction on OpenI Indiana reports), and Clinical Agent (EHR serialisation on MIMIC-IV Demo). A preliminary model selection benchmark compares 1–3 candidate models per role on approximately 100–200 surrogate studies, evaluating F1, latency, and VRAM consumption to select the optimal model configuration before full-scale experiments. The Streamlit UI for argumentation visualisation is also built during this track.
- *Track 2 (credentialing)* runs in parallel: CITI training is completed, the PhysioNet application is submitted, the HWU ethics amendment is filed, and upon approval the MIMIC subset (2,000–3,000 frontal-view CXR studies with linked reports and EHR records) is downloaded and integrated into the pipelines built in Track 1.

**Phase 3: Evaluate (July – August 2026).** The evaluation phase executes all experiments on the MIMIC subset: the RAG infrastructure sweep (Vector RAG vs. GraphRAG vs. Multimodal Hybrid), baseline comparisons (B1–B5), ablation studies (A1–A7), quantitative analysis across six metric dimensions, and qualitative case studies (10 correct + 10 incorrect cases). The final weeks are dedicated to report writing and revision.

## 6.2 Gantt Chart

Figure 6.1 presents the dual-track timeline. Track 1 activities (surrogate-based development) are shown in the upper block; Track 2 activities (PhysioNet credentialing) run concurrently in the lower block. The tracks converge at Week 16–18 when real MIMIC data is integrated into the existing pipelines.

**[FIGURE 6.1: Dual-track Gantt chart — February to August 2026.]**

```
Feb 2026  ──────────────────────────────────────────── Aug 2026
│ W1-2 │ W3-4 │ W5-8 │ W9-12│W13-16│W17-20│W21-24│W25-26│
│ Feb  │ Mar  │ Apr  │ May  │ Jun  │ Jul  │ Aug  │ Aug  │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│██████│      │      │      │      │      │      │      │ PPT + Ethics
│██████│██████│██████│      │      │      │      │      │ Literature Review
│      │██████│██████│      │      │      │      │      │ Architecture Design
│      │      │      │      │      │      │      │      │
│ TRACK 1 (Surrogates — starts immediately)                │
│      │      │██████│██████│      │      │      │      │ Surrogate Data Prep + Benchmark
│      │      │      │██████│██████│      │      │      │ Core Implementation (Agents, VLM, RAG)
│      │      │      │      │██████│██████│      │      │ GraphRAG + CLIP Image RAG Pipeline
│      │      │      │      │      │██████│      │      │ Surrogate Experiments
│      │      │      │      │      │      │      │      │
│ TRACK 2 (PhysioNet Credentialing — parallel)             │
│██████│██████│      │      │      │      │      │      │ CITI Training + PhysioNet Application
│      │      │██████│██████│      │      │      │      │ Credential Review (waiting)
│      │      │      │      │██████│      │      │      │ Download MIMIC Subset
│      │      │      │      │██████│██████│      │      │ Integrate Real MIMIC + Re-run
│      │      │      │      │      │      │      │      │
│      │      │      │      │      │      │██████│██████│ Write-up + Submission
```

The dual-track design ensures that system development is never blocked by the credentialing process. If PhysioNet approval is delayed, all experiments can still be run on surrogate datasets, with MIMIC results added once access is granted.

## 6.3 Supervisor Checkpoints

Table 6.1 lists the eight supervisor checkpoints scheduled across the project. Checkpoints are spaced approximately fortnightly and are designed to provide formative feedback at each major transition.

**Table 6.1: Supervisor checkpoint schedule.**

| Checkpoint | Target Date | Focus | Key Deliverable |
|:---:|---|---|---|
| CP1 | Feb 28 | Project plan and literature review overview | PowerPoint presentation |
| CP2 | Mar 14 | Literature review progress | 35+ papers summarised, SOTA table drafted |
| CP3 | Apr 2 | Design review | Architecture, MIMIC pipeline design, metrics confirmed |
| CP4 | May 16 | Prototype demo | Working multi-agent debate on surrogate data |
| CP5 | Jun 13 | PhysioNet status update | Credential status + VLM pipeline demonstration |
| CP6 | Jun 27 | Full system demo | All components integrated on real MIMIC data |
| CP7 | Jul 25 | Results review | Experiments complete, initial analysis |
| CP8 | Aug 15 | Near-final report review | Complete draft for feedback |

CP5 is a critical milestone: it determines whether the project transitions to real MIMIC data on schedule or continues with surrogate experiments while awaiting credentialing. CP6 marks the convergence of both tracks and the start of the full evaluation phase.

## 6.4 Risk Analysis

Table 6.2 identifies the key risks to the project, their assessed impact and likelihood, and the mitigation strategies adopted.

**Table 6.2: Risk register.**

| Risk | Impact | Likelihood | Mitigation |
|---|:---:|:---:|---|
| PhysioNet credentialing delayed beyond Week 16 | High | Medium | Two-track development: full system built and tested on surrogates (MIMIC-IV Demo, NIH CXR14, OpenI) before MIMIC access needed. Results on surrogates are reportable if credentialing is not granted in time. |
| VLM exceeds 8 GB VRAM budget (RTX 5070) | High | Medium | Use 4-bit quantised LLaVA-Med (~4–5 GB) and BioViL (~2 GB). Never load both simultaneously — sequential inference with `torch.cuda.empty_cache()` between calls. |
| LLM inference too slow for full evaluation | High | Medium | Use quantised Meditron (4-bit GGUF via Ollama) on local GPU. Batch inference across patient studies. University GPU cluster available as fallback. |
| GraphRAG indexing cost exceeds budget | Medium | Medium | Start with a small corpus (one clinical guideline), scale incrementally. Use local LLM for indexing to avoid API costs. |
| Argumentation rounds fail to converge | High | Low | Set maximum debate rounds (5). Implement fallback majority-vote resolution if preferred extension is empty. |
| Ethics re-application required after MIMIC access | Medium | Medium | Submit initial ethics form early (Week 1) covering surrogate datasets. Prepare amendment for MIMIC DUA-bound data once credentials are confirmed. |
| MIMIC subset too large for local storage | Medium | Low | Strict subset: 2,000–3,000 frontal-view studies, 5–6 pathologies, approximately 2–3 GB total. Stored on 2 TB encrypted SSD. |
| Scope creep | High | Medium | Fixed scope: MIMIC-CXR + MIMIC-IV, 3 modality-partitioned agents + supervisor, 6 metric dimensions. Additional features deferred to future work. |
| Medical domain errors in system outputs | Medium | Medium | All outputs labelled as "research prototype, not clinical advice." Validated against CheXpert ground-truth labels only. |
| LangGraph API breaking changes | Low | Low | Pin dependency version (v1.0.9). Write modular code with abstraction layers between framework and business logic. |

The highest-severity risks — PhysioNet delay, VRAM exhaustion, and scope creep — each have concrete fallback strategies that preserve the project's ability to produce reportable results regardless of outcome.

---

# References {-}

Acosta, J.N., Falcone, G.J., Rajpurkar, P. and Topol, E.J. (2022) 'Multimodal biomedical AI', *Nature Medicine*, 28(9), pp. 1773–1784. doi: 10.1038/s41591-022-01981-2.

Alzetta, F., Giorgini, P., Najjar, A. and Schumacher, M.I. (2020) 'In-time explainability in multi-agent systems: Challenges, opportunities, and roadmap', in *Engineering Multi-Agent Systems (EMAS)*. Springer, pp. 39–53.

Amin, S.U., Guizani, M. and Hossain, M.S. (2025) 'Advances, evaluation, and explainability of large language models in healthcare: A systematic review', *ACM Transactions on Multimedia Computing*.

Amugongo, L.M., Mascheroni, P., Brooks, S., Doering, S. and Seidel, J. (2025) 'Retrieval augmented generation for large language models in healthcare: A systematic review', *PLOS Digital Health*. doi: 10.1371/journal.pdig.0000877.

Bienefeld, N., Boss, J.M., Lüthy, R., Brodbeck, D., Azzati, J., Blaser, M., Willms, J. and Keller, E. (2023) 'Solving the explainable AI conundrum by bridging clinicians' needs and developers' goals', *npj Digital Medicine*. doi: 10.1038/s41746-023-00837-4.

Boecking, B., Usuyama, N., Bannur, S., Castro, D.C., Schwaighofer, A., Hyland, S., Wetscherek, M., Naumann, T., Nori, A., Alvarez-Valle, J., Poon, H. and Oktay, O. (2022) 'Making the most of text semantics to improve biomedical vision–language processing', in *Proceedings of the European Conference on Computer Vision (ECCV)*. Springer, pp. 1–17. doi: 10.1007/978-3-031-20059-5_1.

Carrera, Á. and Iglesias, C.A. (2015) 'A systematic review of argumentation techniques for multi-agent systems research', *Artificial Intelligence Review*, 44(4), pp. 509–535. doi: 10.1007/s10462-015-9435-9.

Charwat, G., Dvořák, W., Gaggl, S.A., Wallner, J.P. and Woltran, S. (2015) 'Methods for solving reasoning problems in abstract argumentation — a survey', *Artificial Intelligence*, 220, pp. 28–63. doi: 10.1016/j.artint.2014.11.008.

Ciatto, G., Calegari, R. and Omicini, A. (2019) 'Towards XMAS: eXplainability through multi-agent systems', in *CEUR Workshop Proceedings*.

Dung, P.M. (1995) 'On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games', *Artificial Intelligence*, 77(2), pp. 321–357. doi: 10.1016/0004-3702(94)00041-X.

Hevner, A.R., March, S.T., Park, J. and Ram, S. (2004) 'Design science in information systems research', *MIS Quarterly*, 28(1), pp. 75–105. doi: 10.2307/25148625.

Hong, S., Xiao, L. and Chen, J. (2023) 'An interaction model for merging multi-agent argumentation in shared clinical decision making', in *Proceedings of IEEE International Conference on Bioinformatics and Biomedicine (BIBM)*. IEEE.

Hong, S., Xiao, L., Zhang, X. and Chen, J. (2024) 'ArgMed-Agents: Explainable clinical decision reasoning with LLM discussion via argumentation schemes', in *Proceedings of IEEE International Conference on Bioinformatics and Biomedicine (BIBM)*. IEEE, pp. 1234–1241.

Huang, S.-C., Pareek, A., Seyyedi, S., Banerjee, I. and Lungren, M.P. (2020) 'Fusion of medical imaging and electronic health records using deep learning: A systematic review and implementation guidelines', *npj Digital Medicine*, 3(1), pp. 1–9. doi: 10.1038/s41746-020-00341-z.

Irvin, J., Rajpurkar, P., Ko, M., Yu, Y., Ciurea-Ilcus, S., Chute, C., Marklund, H., Haghgoo, B., Ball, R., Shpanskaya, K., Seekins, J., Mong, D.A., Halabi, S.S., Sandberg, J.K., Jones, R., Larson, D.B., Langlotz, C.P., Patel, B.N., Lungren, M.P. and Ng, A.Y. (2019) 'CheXpert: A large chest radiograph dataset with uncertainty labels and expert comparison', in *Proceedings of the AAAI Conference on Artificial Intelligence*, 33(01), pp. 590–597. doi: 10.1609/aaai.v33i01.3301590.

Johnson, A.E.W., Pollard, T.J., Berkowitz, S.J., Greenbaum, N.R., Lungren, M.P., Deng, C.-Y., Mark, R.G. and Horng, S. (2019a) 'MIMIC-CXR: A de-identified publicly available database of chest radiographs with free-text reports', *Scientific Data*, 6(1), pp. 1–8. doi: 10.1038/s41597-019-0322-0.

Johnson, A.E.W., Pollard, T.J., Greenbaum, N.R., Lungren, M.P., Deng, C.-Y., Peng, Y., Lu, Z., Mark, R.G., Berkowitz, S.J. and Horng, S. (2019b) 'MIMIC-CXR-JPG: A large publicly available database of labeled chest radiographs', *PhysioNet*. doi: 10.13026/8360-t248.

Johnson, A.E.W., Bulgarelli, L., Shen, L., Gayles, A., Shammout, A., Horng, S., Pollard, T.J., Hao, S., Moody, B., Gow, B., Lehman, L.-W.H., Celi, L.A. and Mark, R.G. (2023a) 'MIMIC-IV: A freely accessible electronic health record dataset', *Scientific Data*, 10(1), pp. 1–9. doi: 10.1038/s41597-022-01899-x.

Johnson, A., Pollard, T. and Mark, R. (2023b) 'MIMIC-IV-Note: Deidentified free-text clinical notes', *PhysioNet*. doi: 10.13026/1n74-ne17.

Ke, Y., Yang, R., Lie, S.A., Lim, T.X.Y., Ning, Y. and Li, I. (2024) 'Mitigating cognitive biases in clinical decision-making through multi-agent conversations using large language models: Simulation study', *Journal of Medical Internet Research*, 26, e59439.

Ke, Y.H., Jin, L., Elangovan, K., Abdullah, H.R. and Liu, N. (2025) 'Retrieval augmented generation for 10 large language models and its generalizability in assessing medical fitness', *npj Digital Medicine*. doi: 10.1038/s41746-025-01519-z.

Kim, Y., Park, C., Jeong, H., Chan, Y.S., Xu, X., McDuff, D., Lee, H., Ghassemi, M. and Breazeal, C. (2024) 'MDAgents: An adaptive collaboration of LLMs for medical decision-making', in *Advances in Neural Information Processing Systems (NeurIPS)*.

Kline, A., Wang, H., Li, Y., Dennis, S., Hutch, M., Xu, Z., Wang, F., Cheng, F. and Luo, Y. (2022) 'Multimodal machine learning in precision health: A scoping review', *npj Digital Medicine*, 5(1), pp. 1–14. doi: 10.1038/s41746-022-00712-8.

Kökciyan, N., Sassoon, I., Sklar, E. and Modgil, S. (2021) 'Applying metalevel argumentation frameworks to support medical decision making', *IEEE Intelligent Systems*, 36(2), pp. 64–71.

Kwon, T., Ong, K.T., Kang, D., Moon, S. and Lee, J.R. (2024) 'Large language models are clinical reasoners: Reasoning-aware diagnosis framework with prompt-generated rationales', in *Proceedings of the AAAI Conference on Artificial Intelligence*, 38(16), pp. 18417–18425.

Li, C., Wong, C., Zhang, S., Usuyama, N., Liu, H., Yang, J., Naumann, T., Poon, H. and Gao, J. (2023) 'LLaVA-Med: Training a large language-and-vision assistant for biomedicine in one day', in *Advances in Neural Information Processing Systems (NeurIPS)*.

Liu, P. and Xiao, L. (2025) 'Improving clinical decision support: Architecture design of a multi-agent system based on an argument quality assessment ontology', in *Proceedings of IEEE CBMS*. IEEE.

Liu, Z., Xiao, L., Zhu, R., Yang, H. and He, M. (2024) 'MedGen: An explainable multi-agent architecture for clinical decision support through multisource knowledge fusion', in *Proceedings of IEEE International Conference on Bioinformatics and Biomedicine (BIBM)*. IEEE.

Lu, L., Yuan, Y.C. and McLeod, P.L. (2012) 'Twenty-five years of hidden profiles in group decision making: A meta-analysis', *Personality and Social Psychology Review*, 16(1), pp. 54–75. doi: 10.1177/1088868311417243.

Microsoft (2024) *GraphRAG: A modular graph-based retrieval-augmented generation system* [Computer software]. Available at: https://github.com/microsoft/graphrag (Accessed: 10 April 2026).

Miura, Y., Zhang, Y., Tsai, E.B., Langlotz, C.P. and Jurafsky, D. (2021) 'Improving factual completeness and consistency of image-to-text radiology report generation', in *Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics (NAACL)*.

Moor, M., Banerjee, O., Abad, Z.S.H., Krumholz, H.M., Leskovec, J., Topol, E.J. and Rajpurkar, P. (2023) 'Foundation models for generalist medical artificial intelligence', *Nature*, 616(7956), pp. 259–265. doi: 10.1038/s41586-023-05881-4.

Öğdü, Ç.U., Arslanoğlu, K. and Karaköse, M. (2025) 'An adaptive multi-agent LLM-based clinical decision support system integrating biomedical RAG and web intelligence', *IEEE Access*, 13, pp. 1–15.

Panigutti, C., Beretta, A., Fadda, D., Giannotti, F., Pedreschi, D. and Perotti, A. (2023) 'Co-design of human-centered, explainable AI for clinical decision support', *ACM Transactions on Interactive Intelligent Systems*, 13(4), pp. 1–35. doi: 10.1145/3587271.

Panisson, A.R., Engelmann, D.C. and Bordini, R.H. (2021) 'Engineering explainable agents: An argumentation-based approach', in *Engineering Multi-Agent Systems (EMAS)*. Springer, pp. 273–291.

Prakken, H. (2009) 'An abstract framework for argumentation with structured arguments', *Utrecht University Technical Report* UU-CS-2009-019.

Radford, A., Kim, J.W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G. and Sutskever, I. (2021) 'Learning transferable visual models from natural language supervision', in *Proceedings of the International Conference on Machine Learning (ICML)*. PMLR.

Savage, T., Nayak, A., Gallo, R., Rangan, E. and Chen, J.H. (2024) 'Diagnostic reasoning prompts reveal the potential for large language model interpretability in medicine', *npj Digital Medicine*, 7(1). doi: 10.1038/s41746-024-01010-1.

Schulz-Hardt, S., Brodbeck, F.C., Mojzisch, A., Kerschreiter, R. and Frey, D. (2006) 'Group decision making in hidden profile situations: Dissent as a facilitator for decision quality', *Journal of Personality and Social Psychology*, 91(6), pp. 1080–1093. doi: 10.1037/0022-3514.91.6.1080.

Shen, Y., Colloc, J., Jacquet-Andrieu, A. and Lei, K. (2015) 'Emerging medical informatics with case-based reasoning for aiding clinical decision in multi-agent system', *Journal of Biomedical Informatics*, 56, pp. 307–317.

Silveira, A.L., Da Rosa Righi, R. and Da Costa, C.A. (2025) 'Multi-agent systems for clinical decision support: A systematic review', *Applied Soft Computing*.

Sim, S.Z.Y. and Chen, T. (2025) 'Critique of impure reason: Unveiling the reasoning behaviour of medical large language models', *eLife*. doi: 10.7554/eLife.106187.

Smit, A., Jain, S., Rajpurkar, P., Pareek, A., Ng, A.Y. and Lungren, M.P. (2020) 'CheXbert: Combining automatic labelers and expert annotations for accurate radiology report labeling', in *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*.

Tiu, E., Talius, E., Patel, P., Langlotz, C.P., Ng, A.Y. and Rajpurkar, P. (2022) 'Expert-level detection of pathologies from unannotated chest X-ray images via self-supervised learning', *Nature Biomedical Engineering*, 6(12), pp. 1399–1406. doi: 10.1038/s41551-022-00936-9.

Tun, H.M., Rahman, H.A., Naing, L. and Malik, O.A. (2025) 'Trust in artificial intelligence–based clinical decision support systems among health care workers: Systematic review', *JMIR Medical Informatics*. doi: 10.2196/65897.

Walton, D., Reed, C. and Macagno, F. (2008) *Argumentation Schemes*. Cambridge: Cambridge University Press. ISBN: 978-0-521-72319-7.

Wang, M., Shen, Y., Zhao, B., Zhou, X. and Sun, L. (2025) 'Enhancing LLM-based clinical reasoning in anesthesiology via graph-augmented retrieval and explainable generation', *Health Information Science and Systems*, 13. doi: 10.1007/s13755-025-00379-x.

Wang, Z., Wu, Z., Agarwal, D. and Sun, J. (2022) 'MedCLIP: Contrastive learning from unpaired medical images and text', in *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing (EMNLP)*.

Wong, K.K.L., Han, Y., Cai, Y., Ouyang, W., Du, H. and Liu, C. (2025) 'From trust in automation to trust in AI in healthcare: A 30-year longitudinal review and an interdisciplinary framework', *Bioengineering*, 12(10), 1070. doi: 10.3390/bioengineering12101070.

Xiao, L. and Greer, D. (2023) 'Linked argumentation graphs for multidisciplinary decision support', *Healthcare*, 11(4), 585.

Zhang, Y., Jiang, H., Miura, Y., Manning, C.D. and Langlotz, C.P. (2022) 'Contrastive learning of medical visual representations from paired images and text', in *Proceedings of Machine Learning for Healthcare (MLHC)*. PMLR.

Zhao, X., Liu, S., Yang, S.Y. and Miao, C. (2025) 'MedRAG: Enhancing retrieval-augmented generation with knowledge graph-elicited reasoning for healthcare copilot', in *Proceedings of the ACM Web Conference (WWW)*. ACM.
