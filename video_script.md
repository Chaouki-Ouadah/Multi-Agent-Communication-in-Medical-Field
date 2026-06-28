# Project Plan Video — Narration Script

**Target duration:** 3:00  |  **Pace:** ~150 wpm  |  **Total:** ~450 words

---

## Slide 1 — Title *(0:00 – 0:15)*

Hello. my name is  Chaouki Ouadah, and this is my MSc graduation project at Heriot-Watt University Dubai, supervised by Dr Radu-Casian Mihailescu.

The project is titled *Multi-Agent Argumentation Frameworks with LLM-Augmented Reasoning in Healthcare Systems*.

---

## Slide 2 — Motivation & Research Questions *(0:15 – 0:50)*

So, what's the problem? Today's clinical AI can predict conditions like pneumonia from chest X-rays — but it can't explain *why*. Doctors get a score with no reasoning behind it. And when you combine images, reports, and lab results, conflicts between these data sources stay completely hidden.

That leads to our main question: can we use multi-agent argumentation, powered by large language models, to make clinical decision support both accurate *and* explainable?

We break this down into four sub-questions — around debate-based explanations, retrieval-augmented grounding, multi-modal agent design, and evaluation beyond accuracy.

---

## Slide 3 — Architecture & Preparation Work *(0:50 – 1:30)*

Here's the high-level idea. We have three specialised agents — one for X-ray images, one for radiology reports, and one for structured clinical data. Each uses domain-specific models like LLaVA-Med and Meditron.

These agents don't just vote — they *debate*. A LangGraph supervisor orchestrates multi-round argumentation using Dung's framework and Walton's argumentation schemes. The result is a diagnosis with a full, traceable reasoning chain.

In terms of preparation: the literature review is done — fifty-three papers across seven themes. The architecture is designed. Surrogate datasets are ready, and ethics approval is secured.

---

## Slide 4 — Project Plan, Risks & Ethics *(1:30 – 2:10)*

The project runs twenty-six weeks in three phases. Design wraps up in April, implementation runs from April through July, and evaluation fills the final month before the August deadline.

A key design choice: we build on surrogate data first while MIMIC credentialing completes in parallel — so progress is never blocked.

For risks — the main ones are dataset access delays, GPU memory limits, and debate non-convergence. Each has a concrete mitigation, from four-bit quantisation to capped debate rounds.

On ethics: the system is strictly decision *support*, never replacement. No human participants are involved, and all data handling follows PhysioNet and GDPR requirements.

---

## Slide 5 — Evaluation Strategy & Feasibility *(2:10 – 2:50)*

We evaluate across six dimensions — clinical accuracy, explainability, transparency, trust calibration, robustness, and cross-modal agreement. Five baselines and seven ablations let us isolate the contribution of each component.

The stack is entirely open-source and fits on consumer hardware with four-bit quantisation. Eight fortnightly supervisor checkpoints keep everything on track.

---

## Slide 6 — Thank You *(2:50 – 3:00)*

To sum up — this project brings together argumentation theory, LLMs, and multimodal retrieval to build clinical AI that can actually explain its reasoning. Thank you for watching.

---

*End of script — estimated runtime: 3:00 (~450 spoken words)*
