"""Clinical Agent — EHR-only structured-data reasoning (OIDP).

Pipeline: take the EHR-only `ClinicalView` (Card 2) → serialise labs/vitals with reference-range
flags → prompt Meditron → parse findings into scheme-labelled `Argument`s ("Argument from Evidence
to Hypothesis"). Evidence cites the abnormal (flagged) labs. The agent sees ONLY the EHR.
"""

from __future__ import annotations

from typing import Any, Protocol

from src.agents._parsing import clean_findings
from src.argumentation.framework import Argument
from src.utils.ehr_serializer import _flag, serialize_ehr
from src.utils.modality_partitioner import ClinicalView


class _LLM(Protocol):
    def generate(self, prompt: str, system: str | None = None) -> str: ...


_DISCLAIMER = "Research prototype — not clinical advice."


def _opponent_block(opponents: list[Argument] | None) -> str:
    """Render OTHER specialists' text claims for a counter-argument round (OIDP: text only)."""
    if not opponents:
        return ""
    claims = "; ".join(a.claim for a in opponents if a.claim)
    if not claims:
        return ""
    return (
        f"Other specialists (image/report) argue: {claims}. "
        "Defend or refine your EHR-based findings against these claims.\n"
    )


class ClinicalAgent:
    """Produces EHR-grounded arguments from structured labs/vitals."""

    agent_name = "clinical"

    def __init__(self, llm: _LLM, variable_dictionary: dict[str, Any]) -> None:
        self.llm = llm
        self.variable_dictionary = variable_dictionary

    def _abnormal(self, ehr_record: dict[str, Any]) -> list[str]:
        out: list[str] = []
        for label in sorted(ehr_record.get("labs") or {}):
            value = ehr_record["labs"][label]
            ref = (self.variable_dictionary.get(label) or {}).get("reference_range")
            if ref is None or value is None:
                continue
            flag = _flag(float(value), ref[0], ref[1])
            if flag in ("↑", "↓"):
                out.append(f"{label} {flag}")
        return out

    def _prompt(self, block: str, opponents: list[Argument] | None = None) -> str:
        return (
            "You are a clinical data assistant. From the structured EHR (↑/↓/✓ mark values vs "
            "reference range), list the salient clinical findings, one per sentence.\n"
            f"{block}\n{_opponent_block(opponents)}({_DISCLAIMER})"
        )

    def analyse(
        self, view: ClinicalView, opponents: list[Argument] | None = None
    ) -> list[Argument]:
        ehr = view.ehr_record
        if not ehr:
            return []
        block = serialize_ehr(ehr, self.variable_dictionary)
        evidence = self._abnormal(ehr)
        prompt = self._prompt(block, opponents)
        output = self.llm.generate(prompt)
        return [
            Argument(
                agent=self.agent_name,
                claim=finding,
                evidence=evidence,
                scheme="Argument from Evidence to Hypothesis",
            )
            for finding in clean_findings(output, prompt)
        ]
