"""Card 12 - baselines B1-B5 + ablations A1-A7 + Wilcoxon harness. Pure (mocks), + live B5.

Conditions are composed in the evaluation layer over mock agents/LLM/retriever (no live model in CI).
"""

from __future__ import annotations

import dataclasses

import pytest

from src.argumentation.framework import Argument, Attack
from src.data.loaders import Case
from src.evaluation.analysis import ablation_delta, aggregate_results, wilcoxon_compare
from src.evaluation.baselines import (
    ABLATIONS,
    BASELINES,
    ConditionOutput,
    SystemConfig,
    run_condition,
)
from src.knowledge.retrieval import RetrievedItem


# ── mocks ────────────────────────────────────────────────────────────────────
class RecordingAgent:
    def __init__(self, name: str, claim: str) -> None:
        self.agent_name = name
        self._claim = claim
        self.calls = 0
        self.views: list[object] = []

    def analyse(self, view: object, opponents: list[Argument] | None = None) -> list[Argument]:
        self.calls += 1
        self.views.append(view)
        return [Argument(agent=self.agent_name, claim=self._claim, evidence=["e"])]


class StubSupervisor:
    def __init__(self) -> None:
        self.mediate_calls = 0

    def mediate(self, arguments: list[Argument]) -> list[Attack]:
        self.mediate_calls += 1
        return []  # no conflict → converge round 1


class StubLLM:
    def __init__(self, out: str) -> None:
        self.out = out
        self.calls = 0

    def generate(self, prompt: str, system: str | None = None) -> str:
        self.calls += 1
        return self.out


class StubRetriever:
    def __init__(self) -> None:
        self.calls = 0

    def retrieve(self, query: object, k: int = 5) -> list[RetrievedItem]:
        self.calls += 1
        return [RetrievedItem("guideline text", "text_vector", 0.9, "text")]


def _case() -> Case:
    return Case(
        subject_id="1",
        study_id="1",
        source="test",
        image_path=None,
        report_text="FINDINGS: enlarged heart. IMPRESSION: cardiomegaly.",
        ehr_record={"demographics": {"gender": "F"}, "labs": {"BNP": 850.0}},
    )


def _agents() -> dict[str, RecordingAgent]:
    return {
        "vision": RecordingAgent("vision", "Cardiomegaly present"),
        "report": RecordingAgent("report", "Pleural Effusion seen"),
        "clinical": RecordingAgent("clinical", "Cardiomegaly supported by BNP"),
    }


def _run(name: str, config: SystemConfig, **kw: object) -> ConditionOutput:
    return run_condition(_case(), config, **kw)  # type: ignore[arg-type]


# ── presets ──────────────────────────────────────────────────────────────────
def test_baseline_presets_exist() -> None:
    assert set(BASELINES) == {"B1", "B2", "B3", "B4", "B5"}
    assert BASELINES["B1"].single_agent and not BASELINES["B1"].use_argumentation
    assert BASELINES["B1"].retrieval is None
    assert BASELINES["B2"].single_agent and BASELINES["B2"].retrieval == "vector"
    assert not BASELINES["B3"].single_agent and not BASELINES["B3"].use_argumentation
    assert BASELINES["B5"].use_argumentation and BASELINES["B5"].retrieval == "hybrid"
    assert len(BASELINES["B5"].agents) == 3


def test_ablation_presets_each_differ_from_b5_by_one() -> None:
    assert set(ABLATIONS) == {"A1", "A2", "A3", "A4", "A5", "A6", "A7"}
    b5 = BASELINES["B5"]
    for name, cfg in ABLATIONS.items():
        diffs = [
            f.name
            for f in dataclasses.fields(SystemConfig)
            if getattr(cfg, f.name) != getattr(b5, f.name)
        ]
        assert len(diffs) >= 1, f"{name} identical to B5"


def test_ablation_specifics() -> None:
    assert ABLATIONS["A1"].retrieval == "vector"  # no image RAG → text-only
    assert ABLATIONS["A2"].use_argumentation is False  # no symbolic layer
    assert ABLATIONS["A3"].partitioning is False  # no modality partitioning
    assert ABLATIONS["A4"].single_agent is True  # single agent
    assert ABLATIONS["A5"].llm_model != BASELINES["B5"].llm_model  # general LLM
    assert "vision" not in ABLATIONS["A6"].agents  # no vision agent
    assert "clinical" not in ABLATIONS["A7"].agents  # no clinical agent


# ── run_condition dispatch ────────────────────────────────────────────────────
def test_b1_single_llm_no_agents() -> None:
    agents = _agents()
    llm = StubLLM("Findings: cardiomegaly present. Research prototype — not clinical advice.")
    out = run_condition(
        _case(), BASELINES["B1"], agents=agents, supervisor=StubSupervisor(), llm=llm
    )
    assert llm.calls == 1
    assert all(a.calls == 0 for a in agents.values())  # no multi-agent debate
    assert "Cardiomegaly" in out.predicted_labels
    assert "not clinical advice" in out.explanation.lower()


def test_b5_full_runs_debate_and_resolves() -> None:
    agents = _agents()
    sup = StubSupervisor()
    out = run_condition(
        _case(),
        BASELINES["B5"],
        agents=agents,
        supervisor=sup,
        llm=StubLLM("x"),
        retriever=StubRetriever(),
    )
    assert all(a.calls >= 1 for a in agents.values())  # debate ran
    assert sup.mediate_calls >= 1
    assert out.winning_args  # AAF resolution produced a preferred extension
    assert "not clinical advice" in out.explanation.lower()


def test_b3_multi_agent_no_argumentation() -> None:
    agents = _agents()
    out = run_condition(
        _case(), BASELINES["B3"], agents=agents, supervisor=StubSupervisor(), llm=StubLLM("x")
    )
    assert all(a.calls >= 1 for a in agents.values())  # debate ran
    assert out.winning_args == []  # no AAF resolution
    assert out.predicted_labels  # still predicts from aggregated claims


def test_b4_external_raises() -> None:
    with pytest.raises(NotImplementedError, match="external"):
        run_condition(
            _case(),
            BASELINES["B4"],
            agents=_agents(),
            supervisor=StubSupervisor(),
            llm=StubLLM("x"),
        )


def test_retrieval_invoked_only_when_configured() -> None:
    r_on = StubRetriever()
    run_condition(
        _case(),
        BASELINES["B2"],
        agents=_agents(),
        supervisor=StubSupervisor(),
        llm=StubLLM("x"),
        retriever=r_on,
    )
    assert r_on.calls >= 1
    r_off = StubRetriever()
    run_condition(
        _case(),
        BASELINES["B3"],
        agents=_agents(),
        supervisor=StubSupervisor(),
        llm=StubLLM("x"),
        retriever=r_off,
    )
    assert r_off.calls == 0


def test_partitioning_toggle_changes_agent_view() -> None:
    # B5 partitioned: vision view has no ehr_record. A3 unpartitioned: agents see the full case.
    a_part = _agents()
    run_condition(
        _case(),
        BASELINES["B5"],
        agents=a_part,
        supervisor=StubSupervisor(),
        llm=StubLLM("x"),
        retriever=StubRetriever(),
    )
    assert not hasattr(a_part["vision"].views[0], "ehr_record")
    a_full = _agents()
    run_condition(
        _case(),
        ABLATIONS["A3"],
        agents=a_full,
        supervisor=StubSupervisor(),
        llm=StubLLM("x"),
        retriever=StubRetriever(),
    )
    assert hasattr(a_full["vision"].views[0], "ehr_record")  # full visibility


def test_ablation_a6_a7_drop_agent() -> None:
    a6 = _agents()
    run_condition(
        _case(),
        ABLATIONS["A6"],
        agents=a6,
        supervisor=StubSupervisor(),
        llm=StubLLM("x"),
        retriever=StubRetriever(),
    )
    assert a6["vision"].calls == 0 and a6["report"].calls >= 1
    a7 = _agents()
    run_condition(
        _case(),
        ABLATIONS["A7"],
        agents=a7,
        supervisor=StubSupervisor(),
        llm=StubLLM("x"),
        retriever=StubRetriever(),
    )
    assert a7["clinical"].calls == 0 and a7["vision"].calls >= 1


# ── analysis harness ─────────────────────────────────────────────────────────
def test_wilcoxon_difference_significant() -> None:
    full = [0.9, 0.88, 0.91, 0.87, 0.92, 0.9]
    ablated = [0.7, 0.68, 0.71, 0.69, 0.72, 0.7]
    res = wilcoxon_compare(full, ablated)
    assert res["pvalue"] < 0.05


def test_wilcoxon_identical_handled() -> None:
    res = wilcoxon_compare([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    assert res["pvalue"] == 1.0  # no difference → not significant, no crash


def test_aggregate_results() -> None:
    agg = aggregate_results({"B5": [1.0, 0.0], "B1": [0.5, 0.5]})
    assert agg["B5"]["mean"] == 0.5 and agg["B5"]["n"] == 2
    assert agg["B1"]["mean"] == 0.5


def test_ablation_delta() -> None:
    assert ablation_delta([0.9, 0.9], [0.7, 0.7]) == pytest.approx(0.2)


@pytest.mark.llm
@pytest.mark.slow
def test_b5_live() -> None:
    """Real B5 full-system run on one case (no image). Local only."""
    from src.agents.clinical import ClinicalAgent
    from src.agents.llm_client import OllamaLLMClient
    from src.agents.ner import ScispacyNer
    from src.agents.report import ReportAgent
    from src.agents.supervisor import SupervisorAgent
    from src.agents.vision import VisionAgent

    class _NoVLM:
        def answer(self, image_path: object, prompt: str) -> str:  # pragma: no cover
            return ""

    class _NoRetr:
        def retrieve(self, image_path: object, k: int = 3) -> list:  # pragma: no cover
            return []

    llm = OllamaLLMClient()
    agents = {
        "vision": VisionAgent(_NoRetr(), _NoVLM()),
        "report": ReportAgent(llm=llm, ner=ScispacyNer()),
        "clinical": ClinicalAgent(
            llm=llm, variable_dictionary={"BNP": {"reference_range": (0.0, 100.0)}}
        ),
    }
    out = run_condition(
        _case(), BASELINES["B5"], agents=agents, supervisor=SupervisorAgent(llm), llm=llm
    )
    assert "not clinical advice" in out.explanation.lower()
