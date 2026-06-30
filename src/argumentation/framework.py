"""Dung's Abstract Argumentation Framework — shared `Argument` type.

`Argument` is what every agent emits (Vision/Report/Clinical) and what the symbolic layer reasons
over. The AAF graph itself (arguments + attack relation) + the Walton-scheme enum + critical
questions are added in later cards (8/9); here we define the minimal, shared argument record.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Argument:
    """One agent's claim, with its supporting evidence and (Walton) scheme label.

    `scheme` is a free-text label for now; Card 9 formalises the Walton-7 enum + critical questions.
    `confidence` is optional (source decided in a later card).
    """

    agent: str
    claim: str
    evidence: list[str] = field(default_factory=list)
    scheme: str = ""
    confidence: float | None = None


@dataclass(frozen=True)
class Attack:
    """A directed conflict: `source_claim` attacks `target_claim` (with a short `rationale`).

    Emitted by the Supervisor's cross-modal conflict detection (Card 7). The symbolic layer
    (Card 8) builds Dung's AAF + preferred extensions from a debate's list of `Attack`s; Card 9
    attaches Walton critical-question labels. Frozen + hashable so convergence can compare
    attack sets across debate rounds.
    """

    source_claim: str
    target_claim: str
    rationale: str = ""
