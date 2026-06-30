"""Walton's argumentation schemes (7 clinical) + critical questions + a lexical attack-former.

Per IMPLEMENTATION_CONTEXT §4 / SRQ1 (dissertation pp.41-43). The agents (Cards 4-6) already tag each
`Argument` with a scheme string; `WaltonScheme` formalises the 7 clinically-relevant schemes and their
critical questions, and `scheme_from_label` maps the emitted strings to the enum.

`form_attacks` is a **deterministic, symbolic** contradiction detector (complementing the Card-7 LLM
Supervisor): two claims from *different* agents attack each other when they share a significant clinical
term but exactly one is negated/uncertain. Mutual contradictions are emitted in both directions so the
AAF forms a 2-cycle (the dissertation's Pneumonia-vs-normal-WBC example → two competing extensions).
"""

from __future__ import annotations

import re
from enum import Enum

from src.argumentation.framework import Argument, Attack


class WaltonScheme(Enum):
    """The 7 clinically-relevant Walton schemes; ``value`` is the canonical agent label."""

    EXPERT_OPINION = "Argument from Expert Opinion"
    EVIDENCE_TO_HYPOTHESIS = "Argument from Evidence to Hypothesis"
    ANALOGY = "Argument from Analogy"
    CAUSE_TO_EFFECT = "Argument from Cause to Effect"
    CONSEQUENCES = "Argument from Consequences"
    ESTABLISHED_RULE = "Argument from Established Rule"
    SIGN = "Argument from Sign"

    @property
    def label(self) -> str:
        return self.value


# Walton critical questions per scheme — drive the explainability of each argument.
CRITICAL_QUESTIONS: dict[WaltonScheme, list[str]] = {
    WaltonScheme.EXPERT_OPINION: [
        "Is the source a genuine expert in this domain?",
        "Is the assertion within the expert's field of competence?",
        "Is the expert's opinion consistent with other experts?",
    ],
    WaltonScheme.EVIDENCE_TO_HYPOTHESIS: [
        "Does the evidence actually support the hypothesis?",
        "Are there alternative hypotheses that explain the evidence?",
        "Is the evidence reliable and correctly measured?",
    ],
    WaltonScheme.ANALOGY: [
        "Are the two cases similar in the relevant respects?",
        "Are there important differences that break the analogy?",
        "Is there a more apt comparison case?",
    ],
    WaltonScheme.CAUSE_TO_EFFECT: [
        "Is the causal link between the events well established?",
        "Could the effect arise from another cause?",
        "Are the conditions for the causal relation present here?",
    ],
    WaltonScheme.CONSEQUENCES: [
        "How likely are the cited consequences to occur?",
        "Are there countervailing consequences of the opposite action?",
        "Is the evidence for the consequences sound?",
    ],
    WaltonScheme.ESTABLISHED_RULE: [
        "Is the rule actually established and applicable here?",
        "Does an exception to the rule apply in this case?",
        "Is the rule correctly stated?",
    ],
    WaltonScheme.SIGN: [
        "Is the sign reliably correlated with the finding?",
        "Could the sign be present without the finding?",
        "Are there other signs that point the other way?",
    ],
}

_LABEL_TO_SCHEME: dict[str, WaltonScheme] = {s.label: s for s in WaltonScheme}

# Negation / uncertainty cues — presence flips a claim's polarity on its clinical term.
_NEGATION_CUES: tuple[str, ...] = (
    "no evidence of",
    "negative for",
    "rule out",
    "ruled out",
    "without",
    "absent",
    "unlikely",
    "not ",
    "no ",
)

# Generic / non-discriminating tokens that must not count as the shared clinical term.
_STOPWORDS: frozenset[str] = frozenset(
    {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "of",
        "on",
        "in",
        "at",
        "to",
        "and",
        "or",
        "with",
        "without",
        "for",
        "by",
        "present",
        "likely",
        "unlikely",
        "absent",
        "normal",
        "abnormal",
        "evidence",
        "finding",
        "findings",
        "no",
        "not",
        "negative",
        "positive",
        "shows",
        "show",
        "seen",
        "suggests",
        "consistent",
        "there",
        "mild",
        "moderate",
        "severe",
    }
)


def scheme_from_label(label: str) -> WaltonScheme | None:
    """Map an `Argument.scheme` string to its `WaltonScheme`, or None if unrecognised."""
    return _LABEL_TO_SCHEME.get(label)


def _content_tokens(claim: str) -> set[str]:
    tokens = re.findall(r"[a-z]+", claim.lower())
    return {t for t in tokens if len(t) > 3 and t not in _STOPWORDS}


def _is_negated(claim: str) -> bool:
    return any(cue in claim.lower() for cue in _NEGATION_CUES)


def _contradicts(a: Argument, b: Argument) -> bool:
    """True if `a` and `b` share a clinical term but exactly one is negated (opposite polarity)."""
    if not (_content_tokens(a.claim) & _content_tokens(b.claim)):
        return False
    return _is_negated(a.claim) != _is_negated(b.claim)


def form_attacks(arguments: list[Argument]) -> list[Attack]:
    """Form symbolic attacks between contradictory cross-agent claims (bidirectional on conflict)."""
    attacks: list[Attack] = []
    for i, a in enumerate(arguments):
        for b in arguments[i + 1 :]:
            if a.agent == b.agent:
                continue  # cross-modal conflicts only (OIDP)
            if _contradicts(a, b):
                rationale = "Shared clinical term with opposite polarity (negation)."
                attacks.append(Attack(a.claim, b.claim, rationale))
                attacks.append(Attack(b.claim, a.claim, rationale))
    return attacks
