"""Baselines B1-B5 + ablations A1-A7 as config-toggled system conditions (dissertation §4.6.3/4.6.4).

Each condition is a `SystemConfig`; `run_condition` composes the EXISTING pipeline pieces — a
configurable debate driver, the symbolic layer (`form_attacks` → `AAF` → `preferred_extensions`), the
`generate_explanation` narrative, and the retrievers — according to the config. Nothing in
`pipeline/graph.py` is modified; the evaluation layer owns the orchestration so any component can be
toggled on/off.

Model access is injected (agents / supervisor / llm / retriever) so unit tests run on mocks. B1 uses a
local Ollama model in place of GPT-4o for now (configurable `llm_model`; documented deviation). B4
("closest published system") is external and cannot be run here — its slot raises NotImplementedError.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol

from src.argumentation.explanation import DISCLAIMER, generate_explanation
from src.argumentation.framework import AAF, Argument
from src.argumentation.resolver import preferred_extensions
from src.argumentation.schemes import form_attacks
from src.data.chexpert import FOCUS_5
from src.utils.modality_partitioner import clinical_view, report_view, vision_view

_NEGATION = ("no ", "without ", "no evidence of", "negative for", "absent", "unlikely")
_ALL_AGENTS = ("vision", "report", "clinical")


class _Agent(Protocol):
    agent_name: str

    def analyse(self, view: Any, opponents: list[Argument] | None = None) -> list[Argument]: ...


class _Supervisor(Protocol):
    def mediate(self, arguments: list[Argument]) -> list[Any]: ...


class _LLM(Protocol):
    def generate(self, prompt: str, system: str | None = None) -> str: ...


class _Retriever(Protocol):
    def retrieve(self, query: Any, k: int = 5) -> list[Any]: ...


@dataclass(frozen=True)
class SystemConfig:
    """Which components are active for a baseline/ablation condition."""

    name: str
    single_agent: bool = False
    agents: frozenset[str] = frozenset(_ALL_AGENTS)
    partitioning: bool = True  # OIDP — agents see only their modality
    retrieval: str | None = None  # None | "vector" | "hybrid"
    use_argumentation: bool = True  # Dung's AAF preferred-extension resolution
    llm_model: str = "meditron"
    external: bool = False  # B4 — external published system, not runnable here


@dataclass
class ConditionOutput:
    """A single condition's output for a case — enough for the six-dimension metrics to score it."""

    condition: str
    predicted_labels: set[str]
    explanation: str
    winning_args: list[Argument] = field(default_factory=list)
    arguments: list[Argument] = field(default_factory=list)
    debate_state: dict[str, Any] | None = None
    retrieved: list[Any] = field(default_factory=list)
    confidence: float | None = None


# ── condition presets (Tables 4.6 / 4.7) ─────────────────────────────────────
BASELINES: dict[str, SystemConfig] = {
    "B1": SystemConfig(
        "B1",
        single_agent=True,
        agents=frozenset(),
        partitioning=False,
        retrieval=None,
        use_argumentation=False,
        llm_model="qwen2.5:14b",
    ),
    "B2": SystemConfig(
        "B2",
        single_agent=True,
        agents=frozenset(),
        partitioning=False,
        retrieval="vector",
        use_argumentation=False,
        llm_model="qwen2.5:14b",
    ),
    "B3": SystemConfig(
        "B3", single_agent=False, partitioning=True, retrieval=None, use_argumentation=False
    ),
    "B4": SystemConfig("B4", external=True),
    "B5": SystemConfig(
        "B5", single_agent=False, partitioning=True, retrieval="hybrid", use_argumentation=True
    ),
}

ABLATIONS: dict[str, SystemConfig] = {
    "A1": SystemConfig(
        "A1", retrieval="vector", use_argumentation=True
    ),  # no image RAG (text-only)
    "A2": SystemConfig("A2", retrieval="hybrid", use_argumentation=False),  # no symbolic layer
    "A3": SystemConfig(
        "A3", retrieval="hybrid", use_argumentation=True, partitioning=False
    ),  # no OIDP
    "A4": SystemConfig(
        "A4", single_agent=True, agents=frozenset(), retrieval="hybrid", use_argumentation=True
    ),  # single agent
    "A5": SystemConfig(
        "A5", retrieval="hybrid", use_argumentation=True, llm_model="llama3.1:8b"
    ),  # general LLM
    "A6": SystemConfig(
        "A6", agents=frozenset({"report", "clinical"}), retrieval="hybrid", use_argumentation=True
    ),  # no vision
    "A7": SystemConfig(
        "A7", agents=frozenset({"vision", "report"}), retrieval="hybrid", use_argumentation=True
    ),  # no clinical
}

ALL_CONDITIONS: dict[str, SystemConfig] = {**BASELINES, **ABLATIONS}


def _extract_labels(text: str, args: Sequence[Argument] = ()) -> set[str]:
    """Map free text + argument claims to FOCUS_5 pathology labels (negation-aware, deterministic)."""
    haystack = (text + " " + " ".join(a.claim for a in args)).lower()
    found: set[str] = set()
    for label in FOCUS_5:
        low = label.lower()
        idx = haystack.find(low)
        while idx != -1:
            prefix = haystack[max(0, idx - 20) : idx]
            if not any(cue in prefix for cue in _NEGATION):
                found.add(label)
                break
            idx = haystack.find(low, idx + 1)
    return found


def _views(case: Any, config: SystemConfig) -> dict[str, Any]:
    """Per-agent views: partitioned (OIDP) or the full case (partitioning off, A3)."""
    if config.partitioning:
        return {
            "vision": vision_view(case),
            "report": report_view(case),
            "clinical": clinical_view(case),
        }
    return dict.fromkeys(_ALL_AGENTS, case)  # full visibility


def _query(case: Any) -> str:
    labs = (case.ehr_record or {}).get("labs", {}) if case.ehr_record else {}
    return (case.report_text or "") + " " + " ".join(f"{k}={v}" for k, v in labs.items())


def _debate(
    case: Any,
    active: list[_Agent],
    supervisor: _Supervisor,
    config: SystemConfig,
    max_rounds: int = 5,
) -> dict[str, Any]:
    """Configurable multi-agent debate driver (variable agent set + partitioning). Returns a state dict."""
    from src.agents.supervisor import attacks_converged

    views = _views(case, config)
    arguments: list[Argument] = []
    attacks: list[Any] = []
    round_ = 0
    converged = False
    while not converged and round_ < max_rounds:
        round_ += 1
        prior = list(arguments)
        new_args: list[Argument] = []
        for agent in active:
            opponents = [a for a in prior if a.agent != agent.agent_name]
            new_args += agent.analyse(views[agent.agent_name], opponents or None)
        arguments += new_args
        prev_attacks = attacks
        attacks = supervisor.mediate(arguments)
        converged = round_ >= max_rounds or attacks_converged(prev_attacks, attacks)
    return {"arguments": arguments, "attacks": attacks, "round": round_, "converged": converged}


def run_condition(
    case: Any,
    config: SystemConfig,
    *,
    agents: dict[str, _Agent],
    supervisor: _Supervisor | None = None,
    llm: _LLM | None = None,
    retriever: _Retriever | None = None,
) -> ConditionOutput:
    """Run one baseline/ablation condition on a case and return its scored-ready output."""
    if config.external:
        raise NotImplementedError(
            f"{config.name}: external published system (B4) — compared manually, not runnable here"
        )

    retrieved: list[Any] = []
    if config.retrieval and retriever is not None:
        retrieved = retriever.retrieve(_query(case))

    # ── single-LLM path (B1, B2, A4) ──
    if config.single_agent:
        if llm is None:
            raise ValueError(f"{config.name}: single-agent condition needs an llm")
        ctx = ""
        if retrieved:
            ctx = "\nContext: " + " ".join(getattr(r, "content", str(r)) for r in retrieved)
        labs = (case.ehr_record or {}).get("labs", {}) if case.ehr_record else {}
        prompt = (
            "You are a clinical assistant. From the case, list the likely chest pathologies.\n"
            f"REPORT: {case.report_text or 'n/a'}\nEHR labs: {labs}{ctx}\n({DISCLAIMER})"
        )
        text = llm.generate(prompt)
        explanation = text if DISCLAIMER in text else f"{text}\n{DISCLAIMER}"
        return ConditionOutput(
            condition=config.name,
            predicted_labels=_extract_labels(text),
            explanation=explanation,
            retrieved=retrieved,
        )

    # ── multi-agent debate path (B3, B5, A1-A3, A5-A7) ──
    if supervisor is None:
        raise ValueError(f"{config.name}: multi-agent condition needs a supervisor")
    active = [agents[n] for n in _ALL_AGENTS if n in config.agents and n in agents]
    state = _debate(case, active, supervisor, config)
    arguments: list[Argument] = state["arguments"]

    winning: list[Argument] = []
    if config.use_argumentation:
        aaf = AAF(arguments, form_attacks(arguments))
        extension = preferred_extensions(aaf)[0] if arguments else set()
        winning = [aaf.argument(c) for c in extension if c in aaf.claims]
        explanation = generate_explanation(aaf, extension, state["attacks"])
        labels = _extract_labels("", winning)
    else:
        body = "; ".join(a.claim for a in arguments)
        explanation = f"Debate findings: {body}\n{DISCLAIMER}"
        labels = _extract_labels("", arguments)

    return ConditionOutput(
        condition=config.name,
        predicted_labels=labels,
        explanation=explanation,
        winning_args=winning,
        arguments=arguments,
        debate_state=state,
        retrieved=retrieved,
    )
