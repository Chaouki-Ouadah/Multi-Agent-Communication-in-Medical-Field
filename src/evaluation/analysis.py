"""Results analysis: aggregate per-condition scores, paired Wilcoxon comparison, ablation deltas.

Supports the dissertation's statistical protocol (§4.6.5): metric scores are collected per condition
across the test set, conditions are compared with a paired Wilcoxon signed-rank test, and each
ablation's delta from the full system (B5) quantifies that component's contribution.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from scipy.stats import wilcoxon


def aggregate_results(
    scores_by_condition: dict[str, Sequence[float]],
) -> dict[str, dict[str, float]]:
    """Per-condition mean / std / n over the test set."""
    out: dict[str, dict[str, float]] = {}
    for condition, scores in scores_by_condition.items():
        arr = np.asarray(list(scores), dtype=float)
        out[condition] = {
            "mean": float(np.mean(arr)) if arr.size else 0.0,
            "std": float(np.std(arr)) if arr.size else 0.0,
            "n": int(arr.size),
        }
    return out


def wilcoxon_compare(scores_a: Sequence[float], scores_b: Sequence[float]) -> dict[str, float]:
    """Paired Wilcoxon signed-rank test between two conditions' per-case scores.

    Returns `{"statistic", "pvalue"}`. If the two are identical (all differences zero — Wilcoxon is
    undefined), report `pvalue=1.0` (no significant difference) rather than raising.
    """
    a = np.asarray(list(scores_a), dtype=float)
    b = np.asarray(list(scores_b), dtype=float)
    if a.size != b.size:
        raise ValueError("paired test needs equal-length score lists")
    if a.size == 0 or np.allclose(a, b):
        return {"statistic": 0.0, "pvalue": 1.0}
    statistic, pvalue = wilcoxon(a, b)
    return {"statistic": float(statistic), "pvalue": float(pvalue)}


def ablation_delta(full_scores: Sequence[float], ablated_scores: Sequence[float]) -> float:
    """Mean performance drop when a component is removed (full minus ablated) - its contribution."""
    full = np.asarray(list(full_scores), dtype=float)
    ablated = np.asarray(list(ablated_scores), dtype=float)
    if full.size == 0 or ablated.size == 0:
        return 0.0
    return float(np.mean(full) - np.mean(ablated))
