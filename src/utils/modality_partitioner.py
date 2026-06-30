"""Modality partitioner — project a `Case` into per-agent views (OIDP).

Each agent sees ONLY its own modality. Views are frozen dataclasses that carry just the allowed
payload (+ ids for provenance); reading any other modality raises `AttributeError`, so information
asymmetry is enforced structurally, not by convention. No view carries ground-truth `labels`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.data.loaders import Case

# The single raw-data field each agent modality is allowed to see (drives leakage/disjointness tests).
RAW_MODALITY_FIELDS: dict[str, str] = {
    "vision": "image_path",
    "report": "report_text",
    "clinical": "ehr_record",
}


@dataclass(frozen=True)
class VisionView:
    """What the Vision Agent sees: the CXR image only."""

    subject_id: str
    study_id: str
    image_path: Path | None


@dataclass(frozen=True)
class ReportView:
    """What the Report Agent sees: the radiology report text only."""

    subject_id: str
    study_id: str
    report_text: str | None


@dataclass(frozen=True)
class ClinicalView:
    """What the Clinical Agent sees: the structured EHR record only."""

    subject_id: str
    study_id: str
    ehr_record: dict[str, Any] | None


@dataclass(frozen=True)
class SupervisorView:
    """What the Supervisor sees: the agents' text arguments only — never raw data."""

    subject_id: str
    study_id: str
    arguments: list[Any]


def vision_view(case: Case) -> VisionView:
    return VisionView(case.subject_id, case.study_id, case.image_path)


def report_view(case: Case) -> ReportView:
    return ReportView(case.subject_id, case.study_id, case.report_text)


def clinical_view(case: Case) -> ClinicalView:
    return ClinicalView(case.subject_id, case.study_id, case.ehr_record)


def supervisor_view(case: Case, arguments: list[Any]) -> SupervisorView:
    return SupervisorView(case.subject_id, case.study_id, list(arguments))
