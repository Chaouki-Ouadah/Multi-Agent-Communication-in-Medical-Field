"""Six-dimension evaluation metrics (dissertation Table 4.5 / §4.6.2).

Pure, deterministic, numpy-only (no sklearn) so fixtures are exact and reproducible. Covers the five
formalised metrics — F1 macro/micro (eqs 4.1/4.2), per-pathology AUROC (4.3), ECE (4.4), Cohen's κ
(4.5) — plus the deterministic process-transparency, explainability, and cross-modal helpers named in
Table 4.5. Robustness (perturbation runs) + BLEU + LLM-judged faithfulness are experiment-driven and
deferred to Card 12.

Label arrays are 2D `[N, K]` binary (N studies by K pathology labels). Undefined cases (e.g. AUROC for a
single-class label) return `nan` rather than raising.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import numpy as np

_DISCLAIMER_MARKER = "not clinical advice"


# ── D1 Clinical outcome quality ──────────────────────────────────────────────
def _precision_recall(tp: float, fp: float, fn: float) -> tuple[float, float]:
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return precision, recall


def _f1(p: float, r: float) -> float:
    return 2 * p * r / (p + r) if (p + r) > 0 else 0.0


def f1_macro(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Macro-averaged F1 over the K labels (eq 4.1) — each label weighted equally."""
    yt, yp = np.asarray(y_true), np.asarray(y_pred)
    f1s: list[float] = []
    for k in range(yt.shape[1]):
        tp = float(np.sum((yt[:, k] == 1) & (yp[:, k] == 1)))
        fp = float(np.sum((yt[:, k] == 0) & (yp[:, k] == 1)))
        fn = float(np.sum((yt[:, k] == 1) & (yp[:, k] == 0)))
        p, r = _precision_recall(tp, fp, fn)
        f1s.append(_f1(p, r))
    return float(np.mean(f1s)) if f1s else 0.0


def f1_micro(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Micro-averaged F1 — pool TP/FP/FN across all labels first (eq 4.2)."""
    yt, yp = np.asarray(y_true), np.asarray(y_pred)
    tp = float(np.sum((yt == 1) & (yp == 1)))
    fp = float(np.sum((yt == 0) & (yp == 1)))
    fn = float(np.sum((yt == 1) & (yp == 0)))
    denom = 2 * tp + fp + fn
    return (2 * tp) / denom if denom > 0 else 0.0


def _auroc_binary(labels: np.ndarray, scores: np.ndarray) -> float:
    """AUROC via the rank (Mann-Whitney U) identity with tie-aware average ranks. nan if one class."""
    pos = labels == 1
    n_pos = int(np.sum(pos))
    n_neg = int(np.sum(~pos))
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    order = np.argsort(scores, kind="mergesort")
    ranks = np.empty(len(scores), dtype=float)
    ranks[order] = np.arange(1, len(scores) + 1)
    # average ranks within tie groups
    sorted_scores = scores[order]
    i = 0
    while i < len(sorted_scores):
        j = i
        while j + 1 < len(sorted_scores) and sorted_scores[j + 1] == sorted_scores[i]:
            j += 1
        if j > i:
            avg = (ranks[order[i]] + ranks[order[j]]) / 2.0
            for t in range(i, j + 1):
                ranks[order[t]] = avg
        i = j + 1
    sum_pos_ranks = float(np.sum(ranks[pos]))
    return (sum_pos_ranks - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def per_pathology_auroc(
    y_true: np.ndarray, y_score: np.ndarray, labels: Sequence[str]
) -> dict[str, float]:
    """Per-label AUROC (eq 4.3); a label with only one class present yields nan."""
    yt, ys = np.asarray(y_true), np.asarray(y_score, dtype=float)
    return {label: _auroc_binary(yt[:, k], ys[:, k]) for k, label in enumerate(labels)}


def cooccurrence_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Fraction of studies whose full label vector (co-occurrence pattern) is predicted exactly."""
    yt, yp = np.asarray(y_true), np.asarray(y_pred)
    if yt.shape[0] == 0:
        return 0.0
    return float(np.mean(np.all(yt == yp, axis=1)))


# ── D4 Trust: calibration ────────────────────────────────────────────────────
def expected_calibration_error(
    confidences: np.ndarray, correct: np.ndarray, n_bins: int = 10
) -> float:
    """ECE (eq 4.4): weighted average gap between confidence and accuracy across M bins."""
    conf = np.asarray(confidences, dtype=float)
    corr = np.asarray(correct, dtype=float)
    n = len(conf)
    if n == 0:
        return 0.0
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    for m in range(n_bins):
        lo, hi = edges[m], edges[m + 1]
        in_bin = (conf > lo) & (conf <= hi) if m > 0 else (conf >= lo) & (conf <= hi)
        count = int(np.sum(in_bin))
        if count == 0:
            continue
        acc = float(np.mean(corr[in_bin]))
        avg_conf = float(np.mean(conf[in_bin]))
        ece += (count / n) * abs(acc - avg_conf)
    return ece


# ── D6 Cross-modal agreement ─────────────────────────────────────────────────
def cohen_kappa(rater_a: np.ndarray, rater_b: np.ndarray) -> float:
    """Cohen's κ (eq 4.5) between two raters' paired categorical labels (Vision vs Report)."""
    a, b = np.asarray(rater_a), np.asarray(rater_b)
    n = len(a)
    if n == 0:
        return 0.0
    p_o = float(np.mean(a == b))
    categories = set(a.tolist()) | set(b.tolist())
    p_e = sum((np.mean(a == c)) * (np.mean(b == c)) for c in categories)
    if math_isclose(p_e, 1.0):
        return 1.0 if math_isclose(p_o, 1.0) else 0.0
    return (p_o - p_e) / (1 - p_e)


def math_isclose(x: float, y: float, tol: float = 1e-12) -> bool:
    return abs(x - y) <= tol


def cross_modal_discovery_rate(vision: Sequence[str], report: Sequence[str]) -> float:
    """Distinct findings surfaced across both modalities relative to the richer single modality."""
    union = set(vision) | set(report)
    largest = max(len(set(vision)), len(set(report)), 1)
    return len(union) / largest


def unique_evidence_contribution(vision: Sequence[str], report: Sequence[str]) -> float:
    """Fraction of distinct findings contributed by exactly one modality (not shared)."""
    sv, sr = set(vision), set(report)
    union = sv | sr
    if not union:
        return 0.0
    unique = sv ^ sr  # symmetric difference = findings unique to one modality
    return len(unique) / len(union)


# ── D2 Explainability ────────────────────────────────────────────────────────
def _lcs_len(a: Sequence[str], b: Sequence[str]) -> int:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = (
                dp[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(dp[i - 1][j], dp[i][j - 1])
            )
    return dp[m][n]


def rouge_l(candidate: str, reference: str) -> float:
    """ROUGE-L F-measure (LCS-based, pure). 1.0 identical, 0.0 disjoint."""
    cand, ref = candidate.split(), reference.split()
    if not cand or not ref:
        return 0.0
    lcs = _lcs_len(cand, ref)
    if lcs == 0:
        return 0.0
    precision, recall = lcs / len(cand), lcs / len(ref)
    return 2 * precision * recall / (precision + recall)


def explanation_completeness(text: str) -> bool:
    """A complete explanation names at least one finding and carries the not-clinical-advice disclaimer."""
    if _DISCLAIMER_MARKER not in text.lower():
        return False
    # at least some substantive content beyond the disclaimer line
    body = text.lower().replace(_DISCLAIMER_MARKER, "").strip(" .—-")
    return len(body) > 0


def argumentation_coverage(text: str, winning_args: Sequence[Any]) -> float:
    """Fraction of the winning arguments' claims that appear in the explanation narrative."""
    if not winning_args:
        return 0.0
    low = text.lower()
    hits = sum(1 for a in winning_args if a.claim.lower() in low)
    return hits / len(winning_args)


# ── D3 Process transparency (from a DebateState-like mapping) ────────────────
def debate_depth(state: dict[str, Any]) -> int:
    """Number of debate rounds executed."""
    return int(state.get("round", 0))


def attack_rate(state: dict[str, Any]) -> float:
    """Attacks raised per debate round (intensity of cross-modal conflict)."""
    rounds = max(1, int(state.get("round", 0)))
    return len(state.get("attacks", [])) / rounds


def convergence_quality(state: dict[str, Any], max_rounds: int = 5) -> float:
    """1.0 if converged immediately, decaying toward 0 if it ran to the round cap without converging."""
    rounds = int(state.get("round", 0))
    if not state.get("converged", False):
        return 0.0
    return max(0.0, (max_rounds - rounds + 1) / max_rounds)


def argument_traceability(arguments: Sequence[Any]) -> float:
    """Fraction of arguments that cite at least one piece of supporting evidence."""
    if not arguments:
        return 0.0
    traced = sum(1 for a in arguments if getattr(a, "evidence", None))
    return traced / len(arguments)


# expose a registry for downstream harnesses (Card 12) without forcing imports
METRIC_REGISTRY: dict[str, Callable[..., Any]] = {
    "f1_macro": f1_macro,
    "f1_micro": f1_micro,
    "per_pathology_auroc": per_pathology_auroc,
    "cooccurrence_accuracy": cooccurrence_accuracy,
    "expected_calibration_error": expected_calibration_error,
    "cohen_kappa": cohen_kappa,
    "cross_modal_discovery_rate": cross_modal_discovery_rate,
    "unique_evidence_contribution": unique_evidence_contribution,
    "rouge_l": rouge_l,
    "explanation_completeness": explanation_completeness,
    "argumentation_coverage": argumentation_coverage,
    "debate_depth": debate_depth,
    "attack_rate": attack_rate,
    "convergence_quality": convergence_quality,
    "argument_traceability": argument_traceability,
}
