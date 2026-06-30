"""Supervisor Agent — cross-modal conflict detection + debate convergence (Card 7).

The Supervisor is **raw-data-blind**: it sees ONLY the three agents' text `Argument`s (their claims),
never any image / report / EHR. It prompts Meditron to name pairs of claims that contradict each other
across specialists and returns them as `Attack`s. The debate orchestrator (pipeline/graph.py) uses
`attacks_converged` together with a round cap to decide when to stop (no new attacks OR round == 5).
"""

from __future__ import annotations

from typing import Protocol

from src.argumentation.framework import Argument, Attack

_DELIM = "<|>"


class _LLM(Protocol):
    def generate(self, prompt: str, system: str | None = None) -> str: ...


def attacks_converged(prev: list[Attack], new: list[Attack]) -> bool:
    """True when `new` raises no attack that was not already in `prev` (debate settled)."""
    return not (set(new) - set(prev))


class SupervisorAgent:
    """Detects cross-modal conflicts among the agents' arguments (text claims only)."""

    agent_name = "supervisor"

    def __init__(self, llm: _LLM) -> None:
        self.llm = llm

    def _prompt(self, arguments: list[Argument]) -> str:
        claims = "\n".join(f"- [{a.agent}] {a.claim}" for a in arguments)
        return (
            "You are a clinical debate supervisor. Below are claims from three specialists "
            "(vision/report/clinical). Identify pairs of claims that CONTRADICT each other across "
            "specialists. For each conflict, output one line exactly as:\n"
            f"<source claim> {_DELIM} <target claim> {_DELIM} <reason>\n"
            "If there are no contradictions, output NONE.\n\n"
            f"{claims}\n"
        )

    def _parse(self, text: str) -> list[Attack]:
        attacks: list[Attack] = []
        for line in text.splitlines():
            line = line.strip().lstrip("-* ").strip()
            if not line or line.upper().startswith("NONE"):
                continue
            parts = [p.strip() for p in line.split(_DELIM)]
            if len(parts) >= 2 and parts[0] and parts[1]:
                rationale = parts[2] if len(parts) >= 3 else ""
                attacks.append(
                    Attack(source_claim=parts[0], target_claim=parts[1], rationale=rationale)
                )
        return attacks

    def mediate(self, arguments: list[Argument]) -> list[Attack]:
        """Return cross-modal conflicts (attacks) among the given arguments. Needs ≥2 to conflict."""
        if len(arguments) < 2:
            return []
        return self._parse(self.llm.generate(self._prompt(arguments)))

    def is_converged(
        self, prev: list[Attack], new: list[Attack], round_: int, max_rounds: int
    ) -> bool:
        """Debate has settled: no new attacks this round, or the round cap was reached."""
        return round_ >= max_rounds or attacks_converged(prev, new)
