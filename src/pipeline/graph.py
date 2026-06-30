"""LangGraph debate state machine: 3 modality agents counter-argue, Supervisor mediates (≤5 rounds).

Per the dissertation (pp.39, 41) and IMPLEMENTATION_CONTEXT.md §6.6. Each round the agents node runs
Vision → Report → Clinical (each given the OTHER agents' text claims as `opponents`, OIDP preserved —
never raw data), then the supervisor node detects cross-modal conflicts (`Attack`s) and decides
convergence: stop when no NEW attack is raised, or when the round cap (5) is hit.

`build_debate_graph(...)` compiles the graph from injected agents + supervisor (all mockable, so the
orchestration is unit-testable with no live model). `run_debate(case, ...)` builds the per-agent views
from a `Case` and runs the debate to termination, returning the final `DebateState`.
"""

from __future__ import annotations

from typing import Any, Protocol

from langgraph.graph import END, START, StateGraph

from src.agents.supervisor import attacks_converged
from src.argumentation.framework import Argument, Attack
from src.pipeline.state import DebateState
from src.utils.modality_partitioner import clinical_view, report_view, vision_view

MAX_ROUNDS = 5


class _Agent(Protocol):
    agent_name: str

    def analyse(self, view: Any, opponents: list[Argument] | None = None) -> list[Argument]: ...


class _Supervisor(Protocol):
    def mediate(self, arguments: list[Argument]) -> list[Attack]: ...


def build_debate_graph(
    vision: _Agent,
    report: _Agent,
    clinical: _Agent,
    supervisor: _Supervisor,
    max_rounds: int = MAX_ROUNDS,
) -> Any:
    """Compile the multi-round debate graph from the three agents + supervisor."""
    agents = (vision, report, clinical)

    def agents_node(state: DebateState) -> dict[str, list[Argument]]:
        prior = state.get("arguments", [])  # accumulated from previous rounds only
        new_args: list[Argument] = []
        for agent in agents:
            view = state["views"].get(agent.agent_name)
            opponents = [a for a in prior if a.agent != agent.agent_name]
            new_args += agent.analyse(view, opponents or None)
        return {"arguments": new_args}  # operator.add reducer appends across rounds

    def supervisor_node(state: DebateState) -> dict[str, Any]:
        prev = state.get("attacks", [])
        new_attacks = supervisor.mediate(state["arguments"])
        round_ = state.get("round", 0) + 1
        converged = round_ >= max_rounds or attacks_converged(prev, new_attacks)
        return {"attacks": new_attacks, "round": round_, "converged": converged}

    def route(state: DebateState) -> str:
        return "end" if state["converged"] else "continue"

    graph = StateGraph(DebateState)
    graph.add_node("agents", agents_node)
    graph.add_node("supervisor", supervisor_node)
    graph.add_edge(START, "agents")
    graph.add_edge("agents", "supervisor")
    graph.add_conditional_edges("supervisor", route, {"continue": "agents", "end": END})
    return graph.compile()


def run_debate(
    case: Any,
    vision: _Agent,
    report: _Agent,
    clinical: _Agent,
    supervisor: _Supervisor,
    max_rounds: int = MAX_ROUNDS,
) -> DebateState:
    """Build per-agent modality views from `case` and run the debate to termination."""
    graph = build_debate_graph(vision, report, clinical, supervisor, max_rounds)
    initial: DebateState = {
        "case": case,
        "views": {
            "vision": vision_view(case),
            "report": report_view(case),
            "clinical": clinical_view(case),
        },
        "arguments": [],
        "attacks": [],
        "round": 0,
        "converged": False,
        "extension": [],
        "explanation": "",
    }
    return graph.invoke(initial)
