"""Card 7 — LangGraph multi-round debate orchestration. Pure (mock agents + supervisor) + live."""

from __future__ import annotations

import pytest

from src.argumentation.framework import Argument, Attack
from src.pipeline.graph import build_debate_graph, run_debate


class RecordingAgent:
    """Mock modality agent: emits one claim, records the opponents it was given each round."""

    def __init__(self, name: str) -> None:
        self.agent_name = name
        self.opponents_seen: list[list[Argument] | None] = []

    def analyse(self, view: object, opponents: list[Argument] | None = None) -> list[Argument]:
        self.opponents_seen.append(opponents)
        return [Argument(agent=self.agent_name, claim=f"{self.agent_name} finding")]


class NeverConvergeSupervisor:
    """Raises a fresh, distinct attack every round → debate only stops at the round cap."""

    def __init__(self) -> None:
        self.calls = 0

    def mediate(self, arguments: list[Argument]) -> list[Attack]:
        self.calls += 1
        return [Attack(f"s{self.calls}", f"t{self.calls}", "r")]


class ConvergeSupervisor:
    """Finds no conflict → debate converges in round 1."""

    def mediate(self, arguments: list[Argument]) -> list[Attack]:
        return []


def _agents() -> tuple[RecordingAgent, RecordingAgent, RecordingAgent]:
    return RecordingAgent("vision"), RecordingAgent("report"), RecordingAgent("clinical")


def _initial() -> dict:
    return {
        "case": None,
        "views": {"vision": None, "report": None, "clinical": None},
        "arguments": [],
        "attacks": [],
        "round": 0,
        "converged": False,
        "extension": [],
        "explanation": "",
    }


def test_round_cap_enforced() -> None:
    v, r, c = _agents()
    graph = build_debate_graph(v, r, c, NeverConvergeSupervisor(), max_rounds=5)
    final = graph.invoke(_initial())
    assert final["round"] == 5
    assert final["converged"] is True


def test_converges_early_when_no_attacks() -> None:
    v, r, c = _agents()
    graph = build_debate_graph(v, r, c, ConvergeSupervisor(), max_rounds=5)
    final = graph.invoke(_initial())
    assert final["round"] == 1
    assert final["converged"] is True
    assert final["attacks"] == []


def test_arguments_accumulate_across_rounds() -> None:
    v, r, c = _agents()
    graph = build_debate_graph(v, r, c, NeverConvergeSupervisor(), max_rounds=5)
    final = graph.invoke(_initial())
    # 3 agents over 5 rounds
    assert len(final["arguments"]) == 15


def test_counter_argument_opponents_wired() -> None:
    v, r, c = _agents()
    graph = build_debate_graph(v, r, c, NeverConvergeSupervisor(), max_rounds=3)
    graph.invoke(_initial())
    # round 1: no prior arguments → opponents None (initial reading)
    assert v.opponents_seen[0] is None
    # round 2: vision receives the OTHER agents' claims (never its own)
    assert v.opponents_seen[1] is not None
    assert all(a.agent != "vision" for a in v.opponents_seen[1])
    assert {a.agent for a in v.opponents_seen[1]} == {"report", "clinical"}


def test_run_debate_builds_views() -> None:
    from src.data.loaders import Case

    case = Case(
        subject_id="1",
        study_id="1",
        source="test",
        report_text="FINDINGS: clear. IMPRESSION: normal.",
    )
    v, r, c = _agents()
    final = run_debate(case, v, r, c, ConvergeSupervisor())
    assert final["case"] is case
    assert final["round"] == 1 and final["converged"] is True


@pytest.mark.llm
@pytest.mark.slow
def test_debate_live() -> None:
    """Real Report + Clinical + Supervisor (Meditron) debate one case to termination. Local only.

    Vision is wired with real clients but the case has no image (image_path=None) → it abstains,
    so this exercises the orchestration end-to-end without the heavy CXR/index path (covered in
    Card 4's live test).
    """
    from src.agents.clinical import ClinicalAgent
    from src.agents.llm_client import OllamaLLMClient
    from src.agents.ner import ScispacyNer
    from src.agents.report import ReportAgent
    from src.agents.supervisor import SupervisorAgent
    from src.agents.vision import VisionAgent
    from src.data.loaders import Case

    class _NoImageRetriever:
        def retrieve(self, image_path, k: int = 3):  # pragma: no cover - not reached (no image)
            return []

    class _NoVLM:
        def answer(self, image_path, prompt: str) -> str:  # pragma: no cover - not reached
            return ""

    llm = OllamaLLMClient()
    vardict = {"BNP": {"reference_range": (0.0, 100.0)}}
    case = Case(
        subject_id="9",
        study_id="9",
        source="test",
        image_path=None,
        report_text="FINDINGS: enlarged cardiac silhouette. IMPRESSION: cardiomegaly.",
        ehr_record={"demographics": {"gender": "F", "anchor_age": 72}, "labs": {"BNP": 850.0}},
    )
    final = run_debate(
        case,
        VisionAgent(_NoImageRetriever(), _NoVLM()),
        ReportAgent(llm=llm, ner=ScispacyNer()),
        ClinicalAgent(llm=llm, variable_dictionary=vardict),
        SupervisorAgent(llm),
    )
    assert 1 <= final["round"] <= 5
    assert final["converged"] is True
    assert final["arguments"], "debate produced no arguments"
    # prompt-echo fix: no instruction/boilerplate junk leaked into claims
    assert not any("not clinical advice" in a.claim.lower() for a in final["arguments"])
    assert not any(a.claim.lower().startswith("you are a") for a in final["arguments"])
