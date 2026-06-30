"""LangGraph `DebateState` — the shared state threaded through the multi-round debate.

Per IMPLEMENTATION_CONTEXT.md Appendix C. `arguments` uses an `operator.add` reducer so each round's
agent output is appended (not overwritten). `attacks`/`round`/`converged` are last-write-wins (set by
the supervisor node). `extension` (Card 8 — preferred extension) and `explanation` (Card 9 — narrative)
stay empty here and are filled by later cards.
"""

from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict

from src.argumentation.framework import Argument, Attack


class DebateState(TypedDict):
    """State of one multi-agent debate over a single `Case`."""

    case: Any  # the Case under debate (loaders.Case); Any to avoid a hard import cycle
    views: dict[str, Any]  # {"vision": VisionView, "report": ReportView, "clinical": ClinicalView}
    arguments: Annotated[list[Argument], operator.add]  # accumulates across rounds
    attacks: list[Attack]  # cross-modal conflicts detected this round (supervisor)
    round: int  # debate round counter (1-based once started, capped at max_rounds)
    converged: bool  # True when no new attacks were raised, or the round cap was hit
    extension: list[Argument]  # Card 8: Dung preferred extension (empty until then)
    explanation: str  # Card 9: narrative explanation (empty until then)
