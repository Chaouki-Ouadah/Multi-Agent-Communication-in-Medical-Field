"""Card 8 — Dung's AAF + preferred-extension resolver. Pure (no LLM).

Toy graphs use single-letter claims a/b/c…; arguments carry the claim as their `claim` field.
"""

from __future__ import annotations

from src.argumentation.framework import AAF, Argument, Attack
from src.argumentation.resolver import (
    admissible,
    conflict_free,
    defends,
    preferred_extensions,
)


def _arg(claim: str) -> Argument:
    return Argument(agent="test", claim=claim)


def _aaf(claims: list[str], edges: list[tuple[str, str]]) -> AAF:
    args = [_arg(c) for c in claims]
    attacks = [Attack(source_claim=s, target_claim=t) for s, t in edges]
    return AAF(args, attacks)


# ── AAF build ────────────────────────────────────────────────────────────────
def test_aaf_build_nodes_edges() -> None:
    aaf = _aaf(["a", "b", "c"], [("a", "b")])
    assert set(aaf.claims) == {"a", "b", "c"}
    assert aaf.attackers("b") == ["a"]
    assert aaf.attackers("a") == []
    assert aaf.argument("a").claim == "a"


def test_dangling_attack_ignored() -> None:
    # an attack referencing a non-existent claim does not create a phantom node/edge
    args = [_arg("a"), _arg("b")]
    attacks = [Attack("a", "b"), Attack("a", "ghost")]
    aaf = AAF(args, attacks)
    assert set(aaf.claims) == {"a", "b"}
    assert aaf.attackers("b") == ["a"]


# ── semantics units ──────────────────────────────────────────────────────────
def test_conflict_free() -> None:
    aaf = _aaf(["a", "b"], [("a", "b")])
    assert conflict_free(aaf, {"a"}) is True
    assert conflict_free(aaf, {"a", "b"}) is False  # a attacks b


def test_admissible_defends() -> None:
    # a -> b -> c : {a} defends a (unattacked); {a, c} defends c (a attacks its attacker b)
    aaf = _aaf(["a", "b", "c"], [("a", "b"), ("b", "c")])
    assert defends(aaf, {"a"}, "a") is True
    assert defends(aaf, {"a", "c"}, "c") is True
    assert admissible(aaf, {"a", "c"}) is True
    assert admissible(aaf, {"c"}) is False  # b attacks c, c can't defend itself


# ── preferred extensions (AC) ────────────────────────────────────────────────
def test_no_attacks_all_in() -> None:
    aaf = _aaf(["a", "b", "c"], [])
    exts = preferred_extensions(aaf)
    assert exts == [{"a", "b", "c"}]


def test_single_attack() -> None:
    # a -> b : a unattacked, b defeated → one extension {a}
    aaf = _aaf(["a", "b"], [("a", "b")])
    assert preferred_extensions(aaf) == [{"a"}]


def test_two_cycle_two_extensions() -> None:
    aaf = _aaf(["a", "b"], [("a", "b"), ("b", "a")])
    exts = preferred_extensions(aaf)
    assert len(exts) == 2
    assert {"a"} in exts and {"b"} in exts


def test_odd_cycle_empty() -> None:
    # 3-cycle a->b->c->a : no non-empty admissible set → empty preferred extension
    aaf = _aaf(["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")])
    assert preferred_extensions(aaf) == [set()]


def test_defended_arg_included() -> None:
    # a -> b -> c : {a, c} is the preferred extension; c is defended by a
    aaf = _aaf(["a", "b", "c"], [("a", "b"), ("b", "c")])
    exts = preferred_extensions(aaf)
    assert exts == [{"a", "c"}]
    assert any("c" in e for e in exts)


def test_preferred_are_maximal_admissible() -> None:
    # mixed: a<->b 2-cycle plus isolated d, plus e->f
    aaf = _aaf(["a", "b", "d", "e", "f"], [("a", "b"), ("b", "a"), ("e", "f")])
    exts = preferred_extensions(aaf)
    # every extension is admissible
    assert all(admissible(aaf, e) for e in exts)
    # none is a subset of another (maximality)
    assert not any(e < g for e in exts for g in exts if e != g)
    # d and e (unattacked) appear in every extension
    assert all({"d", "e"} <= e for e in exts)


def test_empty_aaf() -> None:
    aaf = AAF([], [])
    assert preferred_extensions(aaf) == [set()]
