"""ChestXray14Loader — NIH ChestX-ray14 surrogate (image modality for the Vision Agent).

Reads `Data_Entry_2017.csv` (image filename + pipe-separated finding labels) and yields image-only
Cases. NIH's 14 findings overlap CheXpert only partially; non-overlapping findings (Infiltration,
Mass, Nodule, Emphysema, Fibrosis, Pleural_Thickening, Hernia) are dropped — Cases carry the
CheXpert-14 label set only.
"""

from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from src.data.chexpert import CHEXPERT_LABELS
from src.data.loaders import BaseDatasetLoader, Case

# NIH ChestX-ray14 finding name -> CheXpert label (overlap only).
NIH_TO_CHEXPERT: dict[str, str] = {
    "Atelectasis": "Atelectasis",
    "Cardiomegaly": "Cardiomegaly",
    "Effusion": "Pleural Effusion",
    "Pneumonia": "Pneumonia",
    "Pneumothorax": "Pneumothorax",
    "Consolidation": "Consolidation",
    "Edema": "Edema",
}


class ChestXray14Loader(BaseDatasetLoader):
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self._csv = self.root / "Data_Entry_2017.csv"

    def cases(self) -> Iterable[Case]:
        with self._csv.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                findings = [f.strip() for f in row["Finding Labels"].split("|") if f.strip()]
                positive = {NIH_TO_CHEXPERT[f] for f in findings if f in NIH_TO_CHEXPERT}
                labels = {label: (1 if label in positive else 0) for label in CHEXPERT_LABELS}
                labels["No Finding"] = 1 if "No Finding" in findings else 0
                patient = row["Patient ID"]
                yield Case(
                    subject_id=patient,
                    study_id=f"{patient}_{row.get('Follow-up #', '0')}",
                    source="chestxray14",
                    image_path=self.root / "images" / row["Image Index"],
                    labels=labels,
                )

    def labels(self) -> list[str]:
        return CHEXPERT_LABELS

    def modalities(self) -> dict[str, str]:
        return {"image": "NIH ChestX-ray14"}

    def variable_dictionary(self) -> dict[str, dict[str, Any]]:
        return {}
