"""Card 9 — Walton 7 schemes + lexical attack-former + explanation narrative. Pure (no LLM)."""

from __future__ import annotations

from src.argumentation.explanation import DISCLAIMER, generate_explanation
from src.argumentation.framework import AAF, Argument
from src.argumentation.resolver import preferred_extensions
from src.argumentation.schemes import (
    CRITICAL_QUESTIONS,
    WaltonScheme,
    form_attacks,
    scheme_from_label,
)


# ── 7 Walton schemes ─────────────────────────────────────────────────────────
def test_seven_schemes_enumerable() -> None:
    assert len(WaltonScheme) == 7
    labels = [s.label for s in WaltonScheme]
    assert len(set(labels)) == 7  # unique
    assert all(label.startswith("Argument from") for label in labels)


def test_every_scheme_has_critical_questions() -> None:
    for scheme in WaltonScheme:
        assert CRITICAL_QUESTIONS[scheme], f"{scheme} has no critical questions"
        assert all(q.strip().endswith("?") for q in CRITICAL_QUESTIONS[scheme])


def test_scheme_from_label_round_trips_in_use_labels() -> None:
    # the four labels the agents actually emit (Cards 4-6)
    assert scheme_from_label("Argument from Expert Opinion") is WaltonScheme.EXPERT_OPINION
    assert scheme_from_label("Argument from Sign") is WaltonScheme.SIGN
    assert scheme_from_label("Argument from Analogy") is WaltonScheme.ANALOGY
    assert (
        scheme_from_label("Argument from Evidence to Hypothesis")
        is WaltonScheme.EVIDENCE_TO_HYPOTHESIS
    )
    assert scheme_from_label("nonsense") is None


# ── lexical attack-former ────────────────────────────────────────────────────
def _vision(claim: str) -> Argument:
    return Argument(agent="vision", claim=claim, scheme="Argument from Sign")


def _clinical(claim: str) -> Argument:
    return Argument(agent="clinical", claim=claim, scheme="Argument from Evidence to Hypothesis")


def test_form_attacks_contradiction_two_cycle() -> None:
    # dissertation example: image says pneumonia likely, labs say pneumonia unlikely
    args = [_vision("Pneumonia likely"), _clinical("Normal WBC, pneumonia unlikely")]
    attacks = form_attacks(args)
    pairs = {(a.source_claim, a.target_claim) for a in attacks}
    assert ("Pneumonia likely", "Normal WBC, pneumonia unlikely") in pairs
    assert ("Normal WBC, pneumonia unlikely", "Pneumonia likely") in pairs  # bidirectional


def test_no_attack_on_agreement() -> None:
    args = [_vision("Cardiomegaly present"), _clinical("Cardiomegaly supported by BNP")]
    assert form_attacks(args) == []  # share term, neither negated → agreement, not conflict


def test_no_self_attack_same_agent() -> None:
    args = [_vision("Pneumonia likely"), _vision("No pneumonia")]
    assert form_attacks(args) == []  # same agent → not a cross-modal attack


def test_negation_forms_attack() -> None:
    args = [_vision("Pleural effusion present"), _clinical("No pleural effusion")]
    assert form_attacks(args), "negation of a shared term should form an attack"


# ── explanation narrative ────────────────────────────────────────────────────
def _aaf_with_attacks(args: list[Argument]) -> AAF:
    return AAF(args, form_attacks(args))


def test_explanation_ends_with_disclaimer() -> None:
    args = [_vision("Cardiomegaly present"), _clinical("BNP elevated")]
    aaf = _aaf_with_attacks(args)
    ext = preferred_extensions(aaf)[0]
    text = generate_explanation(aaf, ext)
    assert text.strip().endswith(DISCLAIMER)


def test_explanation_lists_winners_and_evidence() -> None:
    a = Argument(
        agent="clinical", claim="BNP elevated", evidence=["BNP ↑"], scheme="Argument from Sign"
    )
    aaf = AAF([a], [])
    ext = preferred_extensions(aaf)[0]
    text = generate_explanation(aaf, ext)
    assert "BNP elevated" in text
    assert "BNP ↑" in text  # evidence cited
    assert "clinical" in text  # agent named


def test_empty_extension_has_disclaimer() -> None:
    text = generate_explanation(AAF([], []), set())
    assert text.strip().endswith(DISCLAIMER)


def test_end_to_end_extension_to_narrative() -> None:
    # contradiction → 2-cycle → two extensions; explain one of them
    args = [_vision("Pneumonia likely"), _clinical("Pneumonia unlikely")]
    aaf = _aaf_with_attacks(args)
    exts = preferred_extensions(aaf)
    assert len(exts) == 2  # competing readings
    text = generate_explanation(aaf, exts[0], attacks=form_attacks(args))
    assert DISCLAIMER in text
    assert any(claim in text for claim in ("Pneumonia likely", "Pneumonia unlikely"))
