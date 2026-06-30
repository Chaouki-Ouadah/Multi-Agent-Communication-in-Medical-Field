"""Multimodal dataset access: the `Case` object + the stable `BaseDatasetLoader` interface.

A `Case` is one patient study. In Track 1 the surrogate datasets do not share patients, so a Case
carries only the modality its source provides (the others are None) — full tri-modal *linked* Cases
arrive with real MIMIC (Card 15), which implements the same interface so the pipeline is unchanged.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Case:
    """One patient study. Absent modalities are None (per-modality surrogate Cases in Track 1)."""

    subject_id: str
    study_id: str
    source: str
    image_path: Path | None = None
    report_text: str | None = None
    ehr_record: dict[str, Any] | None = None
    labels: dict[str, int] = field(default_factory=dict)


class BaseDatasetLoader(ABC):
    """Stable interface for every data source (surrogate now, real MIMIC later).

    Keep this contract fixed: swapping the data source must not change the pipeline.
    """

    @abstractmethod
    def cases(self) -> Iterable[Case]:
        """Yield patient-study Cases in a deterministic order."""

    @abstractmethod
    def labels(self) -> list[str]:
        """Return the CheXpert-14 label set (prediction targets)."""

    @abstractmethod
    def modalities(self) -> dict[str, str]:
        """Map each modality this source provides to a human-readable source description."""

    @abstractmethod
    def variable_dictionary(self) -> dict[str, dict[str, Any]]:
        """Map EHR variable codes to human meaning + reference range (empty for image/report-only)."""
