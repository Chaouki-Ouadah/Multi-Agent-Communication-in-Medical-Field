"""OpenILoader — OpenI Indiana University surrogate (report modality for the Report Agent).

OpenI provides CXR image + radiology-report pairs. Reads `openi.csv` (uid, image, report_text,
labels) and yields image+report Cases (no EHR). Labels are taken from the provided `labels` column
(CheXpert names, comma/pipe separated) when present; otherwise empty (no auto-labelling in Card 1).
"""

from __future__ import annotations

import csv
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from src.data.chexpert import CHEXPERT_LABELS
from src.data.loaders import BaseDatasetLoader, Case


class OpenILoader(BaseDatasetLoader):
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self._csv = self.root / "openi.csv"

    def cases(self) -> Iterable[Case]:
        with self._csv.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                positive = {
                    tok.strip()
                    for tok in re.split(r"[|,]", row.get("labels", ""))
                    if tok.strip() in CHEXPERT_LABELS
                }
                labels = {label: (1 if label in positive else 0) for label in CHEXPERT_LABELS}
                uid = row["uid"]
                yield Case(
                    subject_id=uid,
                    study_id=uid,
                    source="openi",
                    image_path=self.root / row["image"],
                    report_text=row["report_text"],
                    labels=labels,
                )

    def labels(self) -> list[str]:
        return CHEXPERT_LABELS

    def modalities(self) -> dict[str, str]:
        return {"image": "OpenI Indiana", "report": "OpenI Indiana"}

    def variable_dictionary(self) -> dict[str, dict[str, Any]]:
        return {}
