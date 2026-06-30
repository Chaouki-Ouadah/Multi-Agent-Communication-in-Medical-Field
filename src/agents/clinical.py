"""Clinical Agent — EHR-only structured-data reasoning (OIDP).

Pipeline: take the EHR-only `ClinicalView` (Card 2) → serialise labs/vitals with reference-range
flags → prompt Meditron → parse findings into scheme-labelled `Argument`s ("Argument from Evidence
to Hypothesis"). Evidence cites the abnormal (flagged) labs. The agent sees ONLY the EHR.
"""

from __future__ import annotations

import re
from typing import Any, Protocol

from src.argumentation.framework import Argument
from src.utils.ehr_serializer import _flag, serialize_ehr
from src.utils.modality_partitioner import ClinicalView


class _LLM(Protocol):
    def generate(self, prompt: str, system: str | None = None) -> str: ...


_DISCLAIMER = "Research prototype — not clinical advice."


def _split_findings(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"[.\n;]+", text) if len(p.strip()) > 2]


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

    def _prompt(self, block: str) -> str:
        return (
            "You are a clinical data assistant. From the structured EHR (↑/↓/✓ mark values vs "
            "reference range), list the salient clinical findings, one per sentence.\n"
            f"{block}\n({_DISCLAIMER})"
        )

    def analyse(self, view: ClinicalView) -> list[Argument]:
        ehr = view.ehr_record
        if not ehr:
            return []
        block = serialize_ehr(ehr, self.variable_dictionary)
        evidence = self._abnormal(ehr)
        output = self.llm.generate(self._prompt(block))
        return [
            Argument(
                agent=self.agent_name,
                claim=finding,
                evidence=evidence,
                scheme="Argument from Evidence to Hypothesis",
            )
            for finding in _split_findings(output)
        ]
