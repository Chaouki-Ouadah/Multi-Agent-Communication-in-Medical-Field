"""CheXpert-14 label set + uncertainty-handling policy.

The 14 CheXpert pathology labels (Irvin et al. 2019) are the prediction targets; FOCUS_5 are the
five evaluated in the dissertation. Raw label values are 1 (positive), 0 (negative), -1 (uncertain),
or missing/None (blank). `apply_label_policy` resolves these to ints per a chosen policy.

Default policy = the CheXpert paper's per-pathology best convention: U-Ones (uncertain→positive) for
Atelectasis and Edema; U-Zeros (uncertain→negative) for Cardiomegaly, Consolidation, Pleural Effusion;
blank→0. A global flag can override to U-Ones / U-Zeros everywhere, or keep the 3-state value.
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum

# Standard CheXpert 14-label taxonomy (order is canonical).
CHEXPERT_LABELS: list[str] = [
    "No Finding",
    "Enlarged Cardiomediastinum",
    "Cardiomegaly",
    "Lung Opacity",
    "Lung Lesion",
    "Edema",
    "Consolidation",
    "Pneumonia",
    "Atelectasis",
    "Pneumothorax",
    "Pleural Effusion",
    "Pleural Other",
    "Fracture",
    "Support Devices",
]

# The five target pathologies evaluated in the dissertation (p.35).
FOCUS_5: list[str] = [
    "Cardiomegaly",
    "Pleural Effusion",
    "Pneumonia",
    "Pneumothorax",
    "Atelectasis",
]

# CheXpert-paper per-pathology uncertainty policy (Irvin et al. 2019, Table 5 best results).
_U_ONES_LABELS: frozenset[str] = frozenset({"Atelectasis", "Edema"})
_U_ZEROS_LABELS: frozenset[str] = frozenset({"Cardiomegaly", "Consolidation", "Pleural Effusion"})


class LabelPolicy(Enum):
    """How to resolve uncertain (-1) labels."""

    PER_PATHOLOGY = "per_pathology"  # CheXpert-paper best (default)
    U_ONES = "u_ones"  # uncertain -> positive, everywhere
    U_ZEROS = "u_zeros"  # uncertain -> negative, everywhere
    THREE_STATE = "three_state"  # keep -1


def _resolve(label: str, value: int, policy: LabelPolicy) -> int:
    """Resolve a single uncertain (-1) value for `label` under `policy`."""
    if value != -1:
        return value
    if policy is LabelPolicy.THREE_STATE:
        return -1
    if policy is LabelPolicy.U_ONES:
        return 1
    if policy is LabelPolicy.U_ZEROS:
        return 0
    # PER_PATHOLOGY
    if label in _U_ONES_LABELS:
        return 1
    if label in _U_ZEROS_LABELS:
        return 0
    return 0  # unlisted labels default to negative on uncertainty


def apply_label_policy(
    raw: Mapping[str, float | int | None],
    policy: LabelPolicy = LabelPolicy.PER_PATHOLOGY,
) -> dict[str, int]:
    """Map raw CheXpert values to resolved ints for ALL 14 labels.

    Missing/None labels are treated as blank → 0 (negative). Present values are coerced to int
    (1 / 0 / -1) then resolved per `policy`.
    """
    out: dict[str, int] = {}
    for label in CHEXPERT_LABELS:
        value = raw.get(label)
        if value is None:
            out[label] = 0  # blank -> negative
            continue
        out[label] = _resolve(label, int(value), policy)
    return out
