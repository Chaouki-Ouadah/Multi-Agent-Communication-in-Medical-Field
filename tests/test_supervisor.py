"""Card 7 — Supervisor agent: cross-modal conflict detection + convergence. Pure + live."""

from __future__ import annotations

import pytest

from src.agents.supervisor import SupervisorAgent, attacks_converged
from src.argumentation.framework import Argument, Attack


class StubLLM:
    def __init__(self, out: str) -> None:
        self.out = out
        self.prompts: list[str] = []

    def generate(self, prompt: str, system: str | None = None) -> str:
        self.prompts.append(prompt)
        return self.out


def _args() -> list[Argument]:
    return [
        Argument(agent="vision", claim="Cardiomegaly present on the chest X-ray"),
        Argument(agent="clinical", claim="No cardiac enlargement supported by the labs"),
    ]


def test_mediate_returns_attacks() -> None:
    out = (
        "Cardiomegaly present on the chest X-ray <|> "
        "No cardiac enlargement supported by the labs <|> image vs labs disagree"
    )
    attacks = SupervisorAgent(StubLLM(out)).mediate(_args())
    assert attacks and all(isinstance(a, Attack) for a in attacks)
    assert attacks[0].source_claim and attacks[0].target_claim and attacks[0].rationale


def test_mediate_no_conflict_returns_empty() -> None:
    assert SupervisorAgent(StubLLM("NONE")).mediate(_args()) == []


def test_mediate_needs_two_arguments() -> None:
    one = [Argument(agent="vision", claim="x")]
    assert SupervisorAgent(StubLLM("a <|> b <|> c")).mediate(one) == []


def test_supervisor_is_raw_data_blind() -> None:
    """Supervisor only ever receives Arguments; its prompt carries claim text, no raw modality data."""
    llm = StubLLM("NONE")
    SupervisorAgent(llm).mediate(_args())
    prompt = llm.prompts[0]
    assert "Cardiomegaly present on the chest X-ray" in prompt  # uses claim text
    assert "image_path" not in prompt and "ehr_record" not in prompt


def test_attacks_converged_rule() -> None:
    a = Attack("x", "y", "r")
    b = Attack("p", "q", "r2")
    assert attacks_converged([], []) is True
    assert attacks_converged([a], [a]) is True  # same attack, no new
    assert attacks_converged([a], [a, b]) is False  # b is new
    assert attacks_converged([a, b], [a]) is True  # fewer is still "no new"


def test_is_converged_round_cap() -> None:
    sup = SupervisorAgent(StubLLM("NONE"))
    a = Attack("x", "y", "r")
    # never settles on attacks, but round cap forces convergence
    assert sup.is_converged([], [a], round_=5, max_rounds=5) is True
    assert sup.is_converged([], [a], round_=2, max_rounds=5) is False


@pytest.mark.llm
@pytest.mark.slow
def test_supervisor_live() -> None:
    """Real Meditron mediates a clear cross-modal conflict. Local only."""
    from src.agents.llm_client import OllamaLLMClient

    args = [
        Argument(agent="vision", claim="The chest X-ray shows clear cardiomegaly."),
        Argument(agent="clinical", claim="Cardiac labs are normal; no enlargement indicated."),
    ]
    attacks = SupervisorAgent(OllamaLLMClient()).mediate(args)
    assert isinstance(attacks, list)
    assert all(isinstance(a, Attack) for a in attacks)
