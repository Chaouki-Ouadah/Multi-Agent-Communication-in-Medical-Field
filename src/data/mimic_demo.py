"""MimicDemoLoader — MIMIC-IV Demo surrogate (structured-EHR modality for the Clinical Agent).

Reads the open-access MIMIC-IV Demo tables (`patients.csv`, `d_labitems.csv`, `labevents.csv`) and
yields one EHR-only Case per subject. `ehr_record` = {"demographics": {...}, "labs": {label: value}}.
`variable_dictionary` maps each lab item to its meaning + a reference range (for the agent's ↑/↓/✓).
"""

from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from src.data.chexpert import CHEXPERT_LABELS
from src.data.loaders import BaseDatasetLoader, Case

# Minimal reference ranges (adult) for known lab items — extend as more items appear.
_REFERENCE_RANGES: dict[str, tuple[float, float]] = {
    "Creatinine": (0.6, 1.3),
    "Potassium": (3.5, 5.1),
}


class MimicDemoLoader(BaseDatasetLoader):
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)

    def _read(self, name: str) -> list[dict[str, str]]:
        with (self.root / name).open(newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))

    def cases(self) -> Iterable[Case]:
        item_label = {r["itemid"]: r["label"] for r in self._read("d_labitems.csv")}
        patients = {r["subject_id"]: r for r in self._read("patients.csv")}
        labs: dict[str, dict[str, float]] = {sid: {} for sid in patients}
        for ev in self._read("labevents.csv"):
            sid = ev["subject_id"]
            label = item_label.get(ev["itemid"])
            if sid in labs and label and ev.get("valuenum"):
                labs[sid][label] = float(ev["valuenum"])
        for sid in sorted(patients):  # deterministic order
            p = patients[sid]
            yield Case(
                subject_id=sid,
                study_id=sid,
                source="mimic_demo",
                ehr_record={
                    "demographics": {"gender": p["gender"], "anchor_age": int(p["anchor_age"])},
                    "labs": labs[sid],
                },
            )

    def labels(self) -> list[str]:
        return CHEXPERT_LABELS

    def modalities(self) -> dict[str, str]:
        return {"ehr": "MIMIC-IV Demo"}

    def variable_dictionary(self) -> dict[str, dict[str, Any]]:
        out: dict[str, dict[str, Any]] = {}
        for r in self._read("d_labitems.csv"):
            label = r["label"]
            entry: dict[str, Any] = {
                "itemid": r["itemid"],
                "fluid": r.get("fluid", ""),
                "category": r.get("category", ""),
            }
            if label in _REFERENCE_RANGES:
                entry["reference_range"] = _REFERENCE_RANGES[label]
            out[label] = entry
        return out
