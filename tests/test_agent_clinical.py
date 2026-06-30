"""Card 6 — Clinical Agent (EHR-only; serialisation + Meditron -> Arguments)."""

from __future__ import annotations

import pytest

from src.agents.clinical import ClinicalAgent
from src.argumentation.framework import Argument
from src.data.loaders import Case
from src.utils.modality_partitioner import clinical_view

_VARDICT = {
    "Creatinine": {"reference_range": (0.6, 1.3)},
    "Potassium": {"reference_range": (3.5, 5.1)},
}
_EHR = {
    "demographics": {"gender": "M", "anchor_age": 54},
    "labs": {"Creatinine": 2.4, "Potassium": 4.1},
}


class StubLLM:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def generate(self, prompt: str, system: str | None = None) -> str:
        self.calls.append(prompt)
        return "Elevated creatinine suggests renal impairment. Potassium normal."


def _clinical_view(ehr: dict | None = _EHR):
    return clinical_view(Case(subject_id="c1", study_id="c1", source="test", ehr_record=ehr))


def test_clinical_returns_scheme_labelled_arguments() -> None:
    args = ClinicalAgent(llm=StubLLM(), variable_dictionary=_VARDICT).analyse(_clinical_view())
    assert isinstance(args, list) and args
    assert all(isinstance(a, Argument) for a in args)
    assert all(a.agent == "clinical" and a.scheme for a in args)


def test_clinical_cites_abnormal_labs_as_evidence() -> None:
    args = ClinicalAgent(llm=StubLLM(), variable_dictionary=_VARDICT).analyse(_clinical_view())
    # Creatinine 2.4 is abnormal (>1.3) -> should appear as evidence somewhere
    assert any(any("Creatinine" in e for e in a.evidence) for a in args)


def test_clinical_is_ehr_only() -> None:
    view = _clinical_view()
    assert not hasattr(view, "image_path") and not hasattr(view, "report_text")
    llm = StubLLM()
    ClinicalAgent(llm=llm, variable_dictionary=_VARDICT).analyse(view)
    assert llm.calls and "Creatinine" in llm.calls[0]  # prompt built from EHR only


def test_clinical_empty() -> None:
    assert (
        ClinicalAgent(llm=StubLLM(), variable_dictionary=_VARDICT).analyse(_clinical_view(None))
        == []
    )


@pytest.mark.llm
@pytest.mark.slow
def test_clinical_agent_live() -> None:
    """Real Meditron on a serialised EHR. Local only."""
    from src.agents.llm_client import OllamaLLMClient

    args = ClinicalAgent(llm=OllamaLLMClient(), variable_dictionary=_VARDICT).analyse(
        _clinical_view()
    )
    assert args and all(a.agent == "clinical" and a.scheme for a in args)
