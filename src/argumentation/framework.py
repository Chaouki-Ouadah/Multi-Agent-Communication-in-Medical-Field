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
