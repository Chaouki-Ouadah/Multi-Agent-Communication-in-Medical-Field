# Supervisor Meeting Notes

**Date:** February 23, 2026

**Supervisor:** Radu-Casian Mihailescu

---

## Raw Transcription

### Page 1

```
PowerPoint Presentation
  W1: Lit review, methodology - steps - eval
      Put together slides — backbone of report
                    RQ → sub RQ

  - Summarize papers
    - Organize categories (i...) for papers
    - Above 15 papers

  - Recent survey papers, picture on reference — one slide
  - Research on sub-questions
  - Lit review (sub-topics)
    * Idea → Point out SOTA approaches for the topic
              Explainability — pros & cons
    SOTA table — approach, datasets, pros, cons
    Look for dataset

  - Next: decide methodology
    What dataset — which models — compare, confidence, new approach
    - Experiments to run

  (15 mins)

  - Brainstorming — we decide where to implement
  # Come up with dataset (already public & maybe compare)
  What metrics (not usual like accuracy)
    → may: explainability, process, outcome, trust

  Whole section lit review (different frameworks — argumentation and debate)
    pros/cons                                    long chain?
```

### Page 2

```
Symbolic Reasoning              @ agents
                    Argumentation bigger framework
                    Decide the winning argument

                    - LLM to explain the process

Report:   agent debating
  - Medical LLMs
  - Experiment planning, feasibility study
       April
  - May – August
  - Prototyping

  First step – research, analysis pros/cons
                     Different approaches
  Lit review: what has been published
    Platforms for using LLMs, multi-agent systems
  Medical LLMs

Dataset:
```

### Page 3

```
Datasets — maybe different dataset

- Same problem, different viewpoint. VLM, medical analysis
  Same patient blood test

Dif viewpoint — look at the same problem

  Ethics form → decides on dataset (publically available)

  Progress → PPT presentation → 2 days ahead
  Then go ahead.
  No more than two weeks
  2nd March        PPT Friday
```

---

## Interpreted Action Items

### Immediate Deadline: PPT Presentation (Friday ~Feb 27-28, 2026)

Prepare a PowerPoint presentation serving as the "backbone of the report" covering:

1. **Literature Review** — summarized findings
2. **Methodology** — proposed steps
3. **Evaluation** — how success will be measured

---

### Task Breakdown

#### 1. Literature Review & Paper Organization (First Priority)

- Summarize **15+ papers** organized into categories
- Include **recent survey papers** — one slide showing the "big picture" of references
- Define **Research Question (RQ)** and break into **sub-research questions**
- Dedicate a **whole section** comparing different **argumentation and debate frameworks** with pros/cons
- Build a **SOTA (State-of-the-Art) table** with columns:

| Approach | Datasets Used | Pros | Cons |
|----------|--------------|------|------|
| ... | ... | ... | ... |

#### 2. Dataset Selection

- Find **publicly available** medical datasets
- Concept: **same problem, different viewpoints** — e.g., same patient blood test analyzed by agents with different medical perspectives (conservative vs. risk-tolerant)
- Dataset decision tied to **ethics form** — publicly available data simplifies ethics approval
- Possibly use **multiple different datasets** for comparison

#### 3. Methodology & Metrics

- Decide methodology: which models, what to compare, novel approach
- Define evaluation metrics — **NOT just accuracy**. Focus on:
  - **Explainability** — can clinicians understand the reasoning?
  - **Process** — is the argumentation process transparent?
  - **Outcome** — does it improve decision quality?
  - **Trust** — do clinicians trust the system?

#### 4. System Architecture (Conceptual)

- **Symbolic reasoning** as the argumentation backbone framework
- **Multiple agents** debating from different viewpoints
- Argumentation framework **decides the winning argument**
- **LLM explains the process** in natural language
- Consider **medical LLMs** specifically
- Investigate existing **platforms for multi-agent LLM systems**

---

### Project Timeline

| Phase | Period | Activity |
|-------|--------|----------|
| **NOW** | Feb 23 – Mar 2 | Research, lit review, PPT preparation |
| **Phase 1** | Now – April | Research, analysis, lit review, feasibility study, experiment planning |
| **Phase 2** | May – August | Prototyping & implementation |
| **Milestone** | Friday ~Feb 27/28 | PPT presentation to supervisor |

---

### Immediate To-Do List

1. **Prepare the PPT** (due Friday ~Feb 27-28):
   - Slide(s) on literature review categories
   - SOTA comparison table
   - Research questions & sub-questions
   - Proposed methodology
   - Candidate datasets (publicly available)
   - Proposed evaluation metrics

2. **Submit Ethics Form** — decide on dataset first (publicly available simplifies this); ethics form deadline is Feb 27 per course requirements

3. **Build SOTA table** from collected papers — framework, approach, dataset used, pros, cons

4. **Identify candidate datasets** — publicly available medical datasets suitable for multi-agent argumentation

5. **Define RQ and sub-RQs** clearly

---

### Key Supervisor Guidance

- Supervisor wants to see **concrete progress** in the PPT
- Once PPT is approved ("then go ahead"), move into deeper methodology work over the following **two weeks**
- The report should cover: **agent debating, medical LLMs, experiment planning, feasibility study**
- First step is always **research & analysis** — different approaches, pros/cons
- Lit review should cover: what has been published on platforms for using LLMs in multi-agent systems, and medical LLMs specifically
- Agents should look at the **same problem from different viewpoints** (e.g., same patient data, different medical perspectives)

---

*Notes transcribed from handwritten meeting notes, February 2026*
