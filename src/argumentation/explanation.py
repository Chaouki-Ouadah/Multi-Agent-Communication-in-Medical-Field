"""Explanation generator: a winning preferred extension + arg tree → clinical narrative.

Turns the symbolic result (the surviving arguments + the attacks that were resolved) into
clinician-readable prose for the explainability layer (SRQ1). Pure — takes an `AAF` and a chosen
extension (a set of claim-ids, as returned by `resolver.preferred_extensions`). Every narrative ends
with the not-clinical-advice disclaimer (research-prototype guardrail, IMPLEMENTATION_CONTEXT §10).
"""

from __future__ import annotations

from src.argumentation.framework import AAF, Attack
from src.argumentation.schemes import scheme_from_label

DISCLAIMER = "Research prototype — not clinical advice."


def _scheme_phrase(scheme_label: str) -> str:
    scheme = scheme_from_label(scheme_label)
    return scheme.label if scheme else (scheme_label or "Argument")


def generate_explanation(aaf: AAF, extension: set[str], attacks: list[Attack] | None = None) -> str:
    """Render the winning arguments (+ resolved conflicts) as a narrative ending in the disclaimer."""
    lines: list[str] = []
    winners = [aaf.argument(claim) for claim in extension if claim in aaf.claims]

    if not winners:
        lines.append("No arguments survived the cross-modal debate; the evidence was inconclusive.")
    else:
        lines.append("Winning arguments after cross-modal argumentation:")
        for arg in winners:
            evidence = f" (evidence: {', '.join(arg.evidence)})" if arg.evidence else ""
            lines.append(f"- [{arg.agent}] {arg.claim} — {_scheme_phrase(arg.scheme)}{evidence}")

    if attacks:
        lines.append(f"Resolved {len(attacks)} cross-modal conflict(s) to reach this position.")

    lines.append("")
    lines.append(DISCLAIMER)
    return "\n".join(lines)
