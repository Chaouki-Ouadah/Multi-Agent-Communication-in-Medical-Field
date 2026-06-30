"""Card 5 — Report Agent (report-only; sections + scispaCy NER + Meditron -> Arguments).

Pure tests use a stub NER + stub LLM. Live test uses real scispaCy + Meditron (local, GPU/Ollama).
"""

from __future__ import annotations

import pytest

from src.agents.report import ReportAgent
from src.argumentation.framework import Argument
from src.data.loaders import Case
from src.utils.modality_partitioner import report_view

_REPORT = "FINDINGS: The cardiac silhouette is enlarged. IMPRESSION: Cardiomegaly."


class StubNer:
    def __init__(self) -> None:
        self.seen: list[str] = []

    def entities(self, text: str) -> list[str]:
        self.seen.append(text)
        return ["cardiac silhouette", "Cardiomegaly"]


class StubLLM:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def generate(self, prompt: str, system: str | None = None) -> str:
        self.calls.append(prompt)
        return "Enlarged cardiac silhouette. Cardiomegaly present."


def _report_view():
    return report_view(Case(subject_id="r1", study_id="r1", source="test", report_text=_REPORT))


def test_report_returns_scheme_labelled_arguments() -> None:
    args = ReportAgent(llm=StubLLM(), ner=StubNer()).analyse(_report_view())
    assert isinstance(args, list) and args
    assert all(isinstance(a, Argument) for a in args)
    assert all(a.agent == "report" and a.scheme for a in args)
    # the radiologist impression carries Expert Opinion
    assert any(a.scheme == "Argument from Expert Opinion" for a in args)


def test_report_cites_ner_entities() -> None:
    args = ReportAgent(llm=StubLLM(), ner=StubNer()).analyse(_report_view())
    assert any("Cardiomegaly" in a.evidence for a in args)


def test_report_is_report_only() -> None:
    view = _report_view()
    assert not hasattr(view, "image_path") and not hasattr(view, "ehr_record")
    ner, llm = StubNer(), StubLLM()
    ReportAgent(llm=llm, ner=ner).analyse(view)
    assert ner.seen and _REPORT in ner.seen[0]  # NER only saw the report text


def test_report_empty_text() -> None:
    view = report_view(Case(subject_id="r0", study_id="r0", source="test", report_text=""))
    assert ReportAgent(llm=StubLLM(), ner=StubNer()).analyse(view) == []


@pytest.mark.llm
@pytest.mark.slow
def test_report_agent_live() -> None:
    """Real scispaCy NER + Meditron on a report. Local only."""
    from src.agents.llm_client import OllamaLLMClient
    from src.agents.ner import ScispacyNer

    args = ReportAgent(llm=OllamaLLMClient(), ner=ScispacyNer()).analyse(_report_view())
    assert args and all(a.agent == "report" and a.scheme for a in args)
