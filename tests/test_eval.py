"""Card 11 — six-dimension evaluation metrics. Pure (numpy), hand-computed fixtures."""

from __future__ import annotations

import math

import numpy as np

from src.argumentation.framework import Argument, Attack
from src.evaluation.metrics import (
    argument_traceability,
    argumentation_coverage,
    attack_rate,
    cohen_kappa,
    convergence_quality,
    cooccurrence_accuracy,
    cross_modal_discovery_rate,
    debate_depth,
    expected_calibration_error,
    explanation_completeness,
    f1_macro,
    f1_micro,
    per_pathology_auroc,
    rouge_l,
    unique_evidence_contribution,
)


# ── D1 Clinical: F1 macro / micro ────────────────────────────────────────────
def test_f1_macro_hand() -> None:
    # label0: TP=1,FP=0,FN=1 → P=1,R=0.5,F1=2/3 ; label1: perfect → F1=1 ; macro=(2/3+1)/2
    y_true = np.array([[1, 1], [1, 1]])
    y_pred = np.array([[1, 1], [0, 1]])
    assert math.isclose(f1_macro(y_true, y_pred), (2 / 3 + 1.0) / 2, rel_tol=1e-9)


def test_f1_micro_hand() -> None:
    # pooled: TP=3, FP=0, FN=1 → micro F1 = 2*3/(2*3+0+1)=6/7
    y_true = np.array([[1, 1], [1, 1]])
    y_pred = np.array([[1, 1], [0, 1]])
    assert math.isclose(f1_micro(y_true, y_pred), 6 / 7, rel_tol=1e-9)


def test_f1_all_correct_is_one() -> None:
    y = np.array([[1, 0], [0, 1]])
    assert math.isclose(f1_macro(y, y), 1.0) and math.isclose(f1_micro(y, y), 1.0)


# ── D1: per-pathology AUROC ──────────────────────────────────────────────────
def test_auroc_per_label() -> None:
    # label "a": scores perfectly separate the one positive from negatives → AUROC 1.0
    y_true = np.array([[1], [0], [0]])
    y_score = np.array([[0.9], [0.2], [0.1]])
    out = per_pathology_auroc(y_true, y_score, ["a"])
    assert math.isclose(out["a"], 1.0)


def test_auroc_ties() -> None:
    # one positive, one negative with equal score → AUROC 0.5 (tie → average rank)
    y_true = np.array([[1], [0]])
    y_score = np.array([[0.5], [0.5]])
    assert math.isclose(per_pathology_auroc(y_true, y_score, ["a"])["a"], 0.5)


def test_auroc_single_class_is_nan() -> None:
    y_true = np.array([[1], [1]])  # no negatives → undefined
    y_score = np.array([[0.9], [0.1]])
    assert math.isnan(per_pathology_auroc(y_true, y_score, ["a"])["a"])


# ── D4 Trust: ECE ────────────────────────────────────────────────────────────
def test_ece_perfect_is_zero() -> None:
    # confidence equals accuracy in every bin → ECE 0
    conf = np.array([1.0, 1.0, 0.0, 0.0])
    correct = np.array([1, 1, 0, 0])
    assert math.isclose(expected_calibration_error(conf, correct, n_bins=10), 0.0, abs_tol=1e-9)


def test_ece_known_gap() -> None:
    # all 4 preds in one bin (conf 0.8), accuracy 0.5 → ECE = |0.5-0.8| = 0.3
    conf = np.array([0.8, 0.8, 0.8, 0.8])
    correct = np.array([1, 1, 0, 0])
    assert math.isclose(expected_calibration_error(conf, correct, n_bins=5), 0.3, abs_tol=1e-9)


# ── D6 Cross-modal: Cohen's kappa ────────────────────────────────────────────
def test_kappa_perfect() -> None:
    a = np.array([1, 0, 1, 0])
    assert math.isclose(cohen_kappa(a, a), 1.0)


def test_kappa_chance_is_zero() -> None:
    # observed agreement == expected by chance → kappa 0
    a = np.array([1, 1, 0, 0])
    b = np.array([1, 0, 1, 0])
    assert math.isclose(cohen_kappa(a, b), 0.0, abs_tol=1e-9)


def test_cross_modal_discovery_and_unique() -> None:
    vision = ["cardiomegaly", "effusion"]
    report = ["cardiomegaly", "pneumonia"]
    # discovery rate = union size relative to the larger single modality
    assert cross_modal_discovery_rate(vision, report) >= 1.0
    # effusion unique to vision; pneumonia unique to report → 2 unique of 3 distinct
    assert math.isclose(unique_evidence_contribution(vision, report), 2 / 3, rel_tol=1e-9)


# ── D2 Explainability ────────────────────────────────────────────────────────
def test_rouge_l() -> None:
    assert math.isclose(rouge_l("a b c", "a b c"), 1.0)
    assert math.isclose(rouge_l("x y z", "a b c"), 0.0)
    # LCS("a b c d", "a c d") = "a c d" len 3 → R=3/3, P=3/4, F=2PR/(P+R)
    f = rouge_l("a b c d", "a c d")
    assert 0.0 < f < 1.0


def test_explanation_completeness_and_coverage() -> None:
    winners = [Argument(agent="clinical", claim="BNP elevated", evidence=["BNP ↑"])]
    text = "Winning: BNP elevated (evidence: BNP ↑). Research prototype — not clinical advice."
    assert explanation_completeness(text) is True
    assert math.isclose(argumentation_coverage(text, winners), 1.0)
    # missing disclaimer → not complete
    assert explanation_completeness("BNP elevated.") is False


# ── D3 Process transparency (from DebateState-like dict) ─────────────────────
def _state() -> dict:
    args = [
        Argument(agent="vision", claim="Cardiomegaly", evidence=["x"]),
        Argument(agent="report", claim="No cardiomegaly", evidence=[]),
    ]
    return {
        "arguments": args,
        "attacks": [Attack("Cardiomegaly", "No cardiomegaly", "r")],
        "round": 3,
        "converged": True,
    }


def test_process_transparency_from_state() -> None:
    s = _state()
    assert debate_depth(s) == 3
    assert attack_rate(s) > 0.0
    assert convergence_quality(s) > 0.0  # converged before the cap
    assert math.isclose(argument_traceability(s["arguments"]), 0.5)  # 1 of 2 has evidence


def test_cooccurrence_accuracy() -> None:
    # exact row matches: row0 matches, row1 differs → 0.5
    y_true = np.array([[1, 0], [1, 1]])
    y_pred = np.array([[1, 0], [0, 1]])
    assert math.isclose(cooccurrence_accuracy(y_true, y_pred), 0.5)
