"""Dung's Abstract Argumentation Framework — shared `Argument`/`Attack` types + the `AAF` graph.

`Argument` is what every agent emits (Vision/Report/Clinical); `Attack` is a directed conflict the
Supervisor detects (Card 7). `AAF` (Card 8) wraps a NetworkX digraph ⟨A, R⟩ — nodes are arguments
(keyed by claim string), edges are attacks — over which `resolver.py` computes preferred extensions.
The Walton-scheme enum + critical questions arrive in Card 9.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import networkx as nx


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


class AAF:
    """Dung's Abstract Argumentation Framework ⟨A, R⟩ as a NetworkX digraph.

    Nodes are arguments keyed by their `claim` string (the `Argument` is stored as the node's
    ``argument`` attribute); a directed edge ``s -> t`` means claim ``s`` attacks claim ``t``.
    Attacks whose endpoints are not both present as argument nodes are ignored (dangling). If two
    arguments share an identical claim the first registered wins the node (claims are effectively
    unique in practice).
    """

    def __init__(self, arguments: list[Argument], attacks: list[Attack]) -> None:
        self.graph: nx.DiGraph = nx.DiGraph()
        for arg in arguments:
            if arg.claim not in self.graph:
                self.graph.add_node(arg.claim, argument=arg)
        for atk in attacks:
            if atk.source_claim in self.graph and atk.target_claim in self.graph:
                self.graph.add_edge(atk.source_claim, atk.target_claim, attack=atk)

    @property
    def claims(self) -> list[str]:
        """All argument claim-ids (node identities)."""
        return list(self.graph.nodes)

    @property
    def arguments(self) -> list[Argument]:
        """The `Argument` objects backing the nodes."""
        return [data["argument"] for _, data in self.graph.nodes(data=True)]

    def argument(self, claim: str) -> Argument:
        """The `Argument` stored at node `claim`."""
        argument: Argument = self.graph.nodes[claim]["argument"]
        return argument

    def attackers(self, claim: str) -> list[str]:
        """Claims that directly attack `claim`."""
        return list(self.graph.predecessors(claim))

    def attacks(self, source: str, target: str) -> bool:
        """True if `source` attacks `target`."""
        return self.graph.has_edge(source, target)
