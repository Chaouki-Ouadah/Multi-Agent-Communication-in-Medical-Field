"""Dung's argumentation semantics over an `AAF` — preferred extensions.

Implements the classical Dung definitions (conflict-free → admissible → preferred) and returns the
**preferred extensions** (maximal admissible sets) — the sets of arguments that mutually survive the
cross-modal debate. Per IMPLEMENTATION_CONTEXT §4 (dissertation pp.41-43).

Preferred-extension enumeration is exponential in general. We bound it by enumerating subsets only of
the *controversial* arguments (those touched by an attack); unattacked/isolated arguments are always
admissible and are added to every candidate. The Supervisor yields few attacks, so the controversial
subgraph is small in practice. Swap in a dedicated solver if a future debate makes it large.
"""

from __future__ import annotations

from itertools import combinations

from src.argumentation.framework import AAF


def conflict_free(aaf: AAF, subset: set[str]) -> bool:
    """No argument in `subset` attacks another argument in `subset`."""
    return not any(aaf.attacks(a, b) for a in subset for b in subset)


def defends(aaf: AAF, subset: set[str], claim: str) -> bool:
    """`subset` defends `claim`: every attacker of `claim` is itself attacked by some member."""
    return all(
        any(aaf.attacks(member, attacker) for member in subset) for attacker in aaf.attackers(claim)
    )


def admissible(aaf: AAF, subset: set[str]) -> bool:
    """Conflict-free and self-defending: `subset` defends each of its own members."""
    return conflict_free(aaf, subset) and all(defends(aaf, subset, c) for c in subset)


def preferred_extensions(aaf: AAF) -> list[set[str]]:
    """Return the preferred extensions (maximal admissible sets) of the AAF.

    Always returns at least one extension (``[set()]`` for an empty/degenerate framework, since the
    empty set is admissible).
    """
    nodes = aaf.claims
    isolated = {n for n in nodes if aaf.graph.degree(n) == 0}
    controversial = [n for n in nodes if aaf.graph.degree(n) > 0]

    admissible_sets: list[set[str]] = []
    for size in range(len(controversial) + 1):
        for combo in combinations(controversial, size):
            candidate = set(combo) | isolated
            if admissible(aaf, candidate):
                admissible_sets.append(candidate)

    # keep only the maximal sets (not a strict subset of any other admissible set)
    preferred: list[set[str]] = []
    for s in admissible_sets:
        if any(s < other for other in admissible_sets):
            continue
        if s not in preferred:
            preferred.append(s)
    return preferred or [set()]
