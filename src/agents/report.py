"""Report Agent — report-only radiology-text reasoning (OIDP).

Pipeline: take the report-only `ReportView` (Card 2) → extract Findings/Impression sections →
run scispaCy clinical NER → prompt Meditron with the sections + entities → parse into scheme-labelled
`Argument`s. The radiologist's stated impression is an "Argument from Expert Opinion"; LLM-derived
findings are "Argument from Sign". The agent sees ONLY the report (never the image or EHR).
"""

from __future__ import annotations

from typing import Protocol

from src.agents._parsing import clean_findings
from src.argumentation.framework import Argument
from src.utils.modality_partitioner import ReportView
from src.utils.report_sections import extract_sections


class _LLM(Protocol):
    def generate(self, prompt: str, system: str | None = None) -> str: ...


class _Ner(Protocol):
    def entities(self, text: str) -> list[str]: ...


_DISCLAIMER = "Research prototype — not clinical advice."


def _opponent_block(opponents: list[Argument] | None) -> str:
    """Render OTHER specialists' text claims for a counter-argument round (OIDP: text only)."""
    if not opponents:
        return ""
    claims = "; ".join(a.claim for a in opponents if a.claim)
    if not claims:
        return ""
    return (
        f"Other specialists (image/EHR) argue: {claims}. "
        "Defend or refine your report-based findings against these claims.\n"
    )


class ReportAgent:
    """Produces report-grounded arguments from a radiology report."""

    agent_name = "report"

    def __init__(self, llm: _LLM, ner: _Ner) -> None:
        self.llm = llm
        self.ner = ner

    def _prompt(
        self, sections: dict[str, str], entities: list[str], opponents: list[Argument] | None = None
    ) -> str:
        ents = ", ".join(entities) if entities else "none extracted"
        return (
            "You are a radiology report assistant. From the report sections and clinical entities, "
            "list the salient chest findings, one per sentence.\n"
            f"FINDINGS: {sections['findings'] or 'n/a'}\n"
            f"IMPRESSION: {sections['impression'] or 'n/a'}\n"
            f"Clinical entities (scispaCy): {ents}\n"
            f"{_opponent_block(opponents)}"
            f"({_DISCLAIMER})"
        )

    def analyse(self, view: ReportView, opponents: list[Argument] | None = None) -> list[Argument]:
        text = view.report_text or ""
        if not text.strip():
            return []
        sections = extract_sections(text)
        entities = self.ner.entities(text)
        prompt = self._prompt(sections, entities, opponents)
        output = self.llm.generate(prompt)

        args: list[Argument] = []
        if sections["impression"]:
            args.append(
                Argument(
                    agent=self.agent_name,
                    claim=sections["impression"],
                    evidence=entities,
                    scheme="Argument from Expert Opinion",
                )
            )
        for finding in clean_findings(output, prompt):
            args.append(
                Argument(
                    agent=self.agent_name,
                    claim=finding,
                    evidence=entities,
                    scheme="Argument from Sign",
                )
            )
        return args
