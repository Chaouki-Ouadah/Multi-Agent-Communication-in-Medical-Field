# Literature Review Audit Report

**Date:** 30 March 2026
**Audited File:** `research_papers_literature_review.md`
**Trigger:** Roadmap revised to Direction 1 (Information Partitioning) — literature review must align
**Audit Scope:** (1) Roadmap alignment, (2) Research quality / peer-review status, (3) PDF cross-referencing

---

## Executive Summary

| Dimension | Score | Notes |
|-----------|-------|-------|
| Core topic coverage (MAS + Argumentation + LLM + Healthcare) | **9/10** | Excellent — papers #1–#7 and #13–#14 cover this well |
| Venue quality | **6/10** | 2 Tier D papers (#11, #12) and 1 borderline (#26) need addressing |
| Roadmap alignment | **4/10** | 5 of 7 key roadmap topics have no or weak coverage |
| PDF utilisation | **1/10** | Only 1 of 17 downloaded PDFs is used — 16 unused |
| Argumentation theory depth | **5/10** | Good surveys but missing Dung (1995) and ASPIC+ foundational references |
| RAG coverage | **3/10** | Minimal; 3 strong PDFs sitting unused |
| Trust / XAI coverage | **3/10** | Weak; multiple stronger PDFs available but unused |

**Critical finding:** 16 of 17 PDF files in the project are NOT referenced in the literature review. Several directly fill gaps created by the revised roadmap.

---

## Part 1: PDF ↔ Literature Review Cross-Reference

| # | PDF File | In Lit Review? | Lit Review # | Action |
|---|----------|:--------------:|:------------:|--------|
| 1 | ArgMed-Agents (Hong et al., IEEE BIBM 2024) | ✅ YES | #1 | No action |
| 2 | Can LLM Agents Really Debate? (Wu, Li, Li — McGill/Mila) | ❌ NO | — | **Add** — relevant to multi-agent debate quality |
| 3 | Co-design of Human-centered XAI for CDS (Panigutti, ACM 2023) | ❌ NO | — | **Add** — supports HITL / human-centred design |
| 4 | LLM-based Multi-Agent Collab for Abstract Screening (Jiang et al.) | ❌ NO | — | Optional — tangential (systematic review automation) |
| 5 | Abstract Framework for Argumentation / ASPIC+ (Prakken 2009) | ❌ NO | — | **Add** — foundational argumentation theory |
| 6 | Critique of Impure Reason: Medical LLM Reasoning (Sim & Chen, eLife 2025) | ❌ NO | — | **Add** — LLM reasoning limitations/evaluation |
| 7 | XAI for CDSS: Literature Review (Salimparsa et al., Oct 2025) | ❌ NO | — | Optional — adds depth to XAI coverage |
| 8 | XAI in CDSS: Meta-Analysis (Abbas et al., Aug 2025) | ❌ NO | — | Optional — quantitative XAI evidence |
| 9 | From Trust in Automation to Trust in AI (Wong et al., Oct 2025) | ❌ NO | — | **Add** — directly supports Trust dimension (SRQ4) |
| 10 | Human-centered AI in Healthcare (2025) | ❌ NO | — | Optional — broader context |
| 11 | Leveraging ChatGPT + XAI for CDSS (El Shawi & Jamel) | ❌ NO | — | Optional — practical ChatGPT + XAI integration |
| 12 | Methods for Solving Reasoning in AAF (Charwat et al., AI 2015) | ❌ NO | — | **Add** — foundational AAF computational methods |
| 13 | RAG for 10 LLMs: Medical Education (Ke et al., npj Digital Medicine) | ❌ NO | — | **Add** — RAG evaluation methodology, top venue |
| 14 | RAG for LLMs in Healthcare: Systematic Review (Amugongo et al., PLOS DH 2025) | ❌ NO | — | **Add** — comprehensive RAG landscape in healthcare |
| 15 | RAG in Healthcare: Comprehensive Review (Neha et al., Sep 2025) | ❌ NO | — | Optional — adds RAG depth (may overlap with #14) |
| 16 | Solving the XAI Conundrum (Bienefeld et al., Nature 2025) | ❌ NO | — | **Add** — high-impact XAI, clinician-developer bridge |
| 17 | Trust in AI-Based CDSS: Systematic Review (Tun et al.) | ❌ NO | — | **Add** — systematic trust evidence |

**Summary:** 12 PDFs recommended for addition to literature review. 4 optional. 1 already included.

---

## Part 2: Research Quality / Peer-Review Audit

### Tier Classification of All 27 Current Papers

| Tier | Description | Papers |
|------|-------------|--------|
| **A** (14) | Peer-reviewed, strong venue | #1, #2, #3, #4, #5, #6, #13, #14, #16, #18, #19, #21, #24, #27 |
| **B** (4) | Peer-reviewed, acceptable | #7 (JMIR), #15 (MDPI), #20 (Springer), #22 (BMC) |
| **C** (5) | Caution: preprint or weak venue | #8, #9, #10, #23, #25 |
| **C/D** (1) | Questionable venue | #26 |
| **D** (2) | Problematic: not peer-reviewed | #11, #12 |
| **Thesis** (1) | PhD thesis (acceptable) | #17 |

### Flagged Papers Requiring Action

#### 🔴 REMOVE — Paper #11 (Nweke et al., 2025)
- **Venue:** Asian Journal of Medical Principles and Clinical Practice (SCIENCEDOMAIN International)
- **Issue:** SCIENCEDOMAIN International (SDI) has appeared on **Beall's List of predatory publishers**. AJMPCP is not indexed in Scopus or Web of Science.
- **Action:** Remove from literature review. Silveira et al. (#6) already provides superior MAS-healthcare systematic review coverage.

#### 🔴 REMOVE — Paper #12 (Borkowski & Ben-Ari, 2024)
- **Venue:** Preprints.org
- **Issue:** Preprints.org **explicitly states papers are "not peer-reviewed."** Cannot be cited as a peer-reviewed source.
- **Action:** Remove from literature review. Content is adequately covered by other multi-agent healthcare papers.

#### 🟡 FLAG — Paper #26 (Mugambiwa & Ndlovu, 2026)
- **Venue:** Journal of Applied Informatics and Computation (Politeknik Negeri Batam, Indonesia)
- **Issue:** Very small regional journal, not indexed in Scopus/WoS. Published by a polytechnic — unusual venue for a systematic review on cutting-edge AI. Fast publication timeline raises concern.
- **Action:** Downgrade from ⭐⭐⭐⭐ to ⭐⭐⭐. Add venue quality note. With the addition of PDFs #13, #14, #15 (strong RAG papers), this paper becomes less essential. Consider removing if the 3 RAG PDFs are added.

#### 🟡 FLAG — Papers #9, #10, #25 (arXiv-only)
- **Issue:** No confirmed peer-reviewed publication. Acceptable for citing cutting-edge 2025 work, but should not be used to build critical arguments.
- **Action:** Add "[arXiv preprint]" label in the literature review. Keep — they provide necessary recent evidence on multi-agent debate approaches.

#### 🟡 FLAG — Paper #8 (Han & Choi, 2024)
- **Venue:** "Advances in Artificial Intelligence and Machine Learning" (OAJRC Publishing LLC)
- **Issue:** Not an established venue. However, 16 citations and arXiv availability suggest genuine research.
- **Action:** Add venue quality note. Keep for practical implementation reference.

#### ℹ️ NOTE — Paper #17 (Engelmann, 2023)
- **Type:** PhD Thesis (PUCRS, Brazil)
- **Issue:** Not externally peer-reviewed like a journal paper, but theses undergo committee review.
- **Action:** Label as "[PhD Thesis]" — acceptable reference for methodology/implementation detail.

#### ℹ️ NOTE — Paper #23 (Ciatto et al., 2019)
- **Venue:** CEUR Workshop Proceedings
- **Issue:** CEUR workshops have variable peer review. However, 39 citations and foundational XMAS concept justify inclusion.
- **Action:** Keep. Note venue tier in documentation.

---

## Part 3: Roadmap Alignment Gap Analysis

The revised roadmap (Direction 1: Information Partitioning) introduces several architectural elements that need literature backing:

### Gap 1: Information Partitioning / Feature-Based Agent Differentiation
- **Status:** ❌ NOT COVERED
- **What the roadmap needs:** Justification for splitting features across agents (information asymmetry vs. full-information debate)
- **Current coverage:** Paper #7 (Ke) uses multi-agent debate but all agents see the same case
- **PDF that helps:** PDF #2 (Can LLM Agents Really Debate?) — examines conditions for productive debate
- **Still needed:** Literature on "hidden profile" paradigm in group decision-making, Random Subspace Method / feature bagging, MDT effectiveness studies

### Gap 2: Microsoft GraphRAG
- **Status:** ❌ NOT COVERED
- **What the roadmap needs:** Edge et al. (2024) "From Local to Global: A Graph RAG Approach" — cited in roadmap but not reviewed
- **No PDF available** — must be downloaded
- **Action:** Add placeholder entry; download paper

### Gap 3: Tabular-to-Text / Clinical Vignette Generation
- **Status:** ❌ NOT COVERED
- **What the roadmap needs:** Clinical Vignette Generator (tabular CSV → clinical narrative) is a core component
- **No PDF available** — must find literature
- **Action:** Identify 1–2 data-to-text / clinical text generation papers

### Gap 4: Dung's Abstract Argumentation Framework (Foundational Theory)
- **Status:** 🟡 PARTIALLY COVERED (surveys mention it, but the original paper is not cited)
- **Available PDFs:** PDF #5 (Prakken 2009 — ASPIC+), PDF #12 (Charwat 2015 — AAF computational methods)
- **Action:** Add Dung (1995) as must-cite placeholder; add PDFs #5 and #12 to lit review

### Gap 5: MI Complications Prediction (Clinical Domain)
- **Status:** ❌ NOT COVERED
- **What the roadmap needs:** Domain literature on MI complication prediction using the UCI #579 dataset
- **No PDF available** — must find Golovenkin et al. (2020)
- **Action:** Add placeholder entry for dataset paper; find 1–2 ML-based MI prediction papers

### Gap 6: RAG Comparison (Vector vs Graph vs Hybrid)
- **Status:** ❌ NOT COVERED
- **Available PDFs:** PDF #13 (Ke — npj Digital Medicine), PDF #14 (Amugongo — PLOS DH), PDF #15 (Neha)
- **Action:** Add all three PDFs to lit review — they collectively ground the infrastructure sweep

### Gap 7: Knowledge Graphs in Healthcare
- **Status:** 🟡 PARTIALLY COVERED (papers #3, #20 touch on KGs)
- **No PDF available for dedicated KG survey** — consider adding PrimeKG / UMLS references
- **Action:** Lower priority, but note the gap

---

## Part 4: Terminology Updates Required (Direction 1 Alignment)

The following text in the literature review still uses pre-Direction 1 terminology:

| Location | Current Text | Required Update |
|----------|------------|-----------------|
| Component C1 description (line ~22) | "representing distinct perspectives (e.g., conservative vs. risk-tolerant)" | → "representing information-partitioned domain specialists (e.g., History & Risk, Diagnostic, Treatment & Progression)" |
| Paper #7 key insights (line ~270) | "Agent role design for diverse perspectives (conservative/risk-tolerant)" | → "Agent role design for diverse perspectives (domain-partitioned specialists)" |
| Paper #10 "How it relates" (line ~362) | "Directly relevant to your 'conservative vs. risk-tolerant' agent design" | → "Directly relevant to your information-partitioned agent design — tests whether dissent mechanisms improve debate quality" |
| Research Gaps, Gap #3 (line ~872) | "Agent Personality: Conservative vs. risk-tolerant agents is under-explored" | → "Information Partitioning: Domain-partitioned agents with information asymmetry is under-explored" |
| Research Gaps, Gap #5 (line ~874) | "Interface Design: Most papers focus on backend" | → "Feature Partitioning & MDT Analogy: No existing work partitions input features to simulate multidisciplinary team structure" |

---

## Part 5: Actions Taken

The following changes have been applied to `research_papers_literature_review.md`:

1. ✅ C1 description updated to reflect information-partitioned agents
2. ✅ Quality flags added to papers #11 (predatory), #12 (not peer-reviewed), #26 (weak venue)
3. ✅ Papers #7 and #10 "relates to your project" sections updated for Direction 1
4. ✅ Research Gaps section rewritten for information partitioning
5. ✅ New Category 7 added: Foundational Argumentation Theory (Prakken 2009 ASPIC+, Charwat 2015 AAF methods)
6. ✅ New Category 8 added: Trust & Human-Centred AI (Wong trust review, Tun trust SR, Bienefeld XAI conundrum, Panigutti co-design XAI)
7. ✅ Category 6 expanded: RAG papers added (Ke RAG evaluation, Amugongo RAG SR)
8. ✅ New Category 9 added: LLM Reasoning & Debate (Can LLM Agents Debate, Critique of Impure Reason)
9. ✅ Placeholder entries added for must-download papers (Dung 1995, Edge 2024 GraphRAG, Golovenkin 2020 MI dataset)
10. ✅ Coverage matrix updated with all new papers
11. ✅ Reading order updated
12. ✅ arXiv papers (#9, #10, #25) labelled as preprints

---

## Papers to Download (Not Yet Available as PDFs)

| Priority | Paper | Why Needed |
|----------|-------|-----------|
| 🔴 Critical | **Dung, P. M. (1995).** "On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games." *Artificial Intelligence*, 77(2), 321–357. | Foundational paper for Dung's AAF — the symbolic backbone of the entire system |
| 🔴 Critical | **Edge, D., Trinh, H., et al. (2024).** "From Local to Global: A Graph RAG Approach to Query-Focused Summarization." *Microsoft Research.* arXiv:2404.16130. | Microsoft GraphRAG — one of three RAG backends in infrastructure sweep |
| 🔴 Critical | **Golovenkin, S. E., et al. (2020).** "Myocardial Infarction Complications." *UCI Machine Learning Repository* / *GigaScience*. | Primary dataset paper — must be cited for dataset provenance |
| 🟡 Important | **Data-to-text generation paper** for clinical vignette generation justification | Tabular-to-text conversion is a core architectural component |
| 🟡 Important | **Hidden Profile paradigm** — e.g., Stasser & Titus (1985) or Lu, Yuan & McLeod (2012) meta-analysis | Information partitioning theoretical justification from social psychology |

---

*Audit conducted: 30 March 2026*
*Next action: Apply all changes to literature review file, then download missing papers before CP3 (2 April 2026)*
