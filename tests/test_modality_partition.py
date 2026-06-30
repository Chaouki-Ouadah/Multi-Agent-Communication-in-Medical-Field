"""Card 2 — modality partitioner: per-agent Case views with enforced information asymmetry (OIDP).

Each agent view exposes ONLY its modality (+ ids); reading another modality is structurally
impossible (no attribute). Views never carry ground-truth labels.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from src.data.loaders import Case
from src.utils.modality_partitioner import (
    RAW_MODALITY_FIELDS,
    ClinicalView,
    ReportView,
    SupervisorView,
    VisionView,
    clinical_view,
    report_view,
    supervisor_view,
    vision_view,
)


@pytest.fixture
def case() -> Case:
    return Case(
        subject_id="FAKE0001",
        study_id="FAKE0001_0",
        source="test",
        image_path=Path("img/FAKE0001.png"),
        report_text="FINDINGS: cardiomegaly.",
        ehr_record={"labs": {"Creatinine": 1.2}},
        labels={"Cardiomegaly": 1},
    )


# ── Each view exposes its own modality (+ ids) ───────────────────────────────
def test_views_expose_their_modality(case: Case) -> None:
    assert vision_view(case).image_path == case.image_path
    assert report_view(case).report_text == case.report_text
    assert clinical_view(case).ehr_record == case.ehr_record
    sv = supervisor_view(case, ["arg-a", "arg-b"])
    assert sv.arguments == ["arg-a", "arg-b"]
    for v in (vision_view(case), report_view(case), clinical_view(case), sv):
        assert v.subject_id == "FAKE0001" and v.study_id == "FAKE0001_0"


# ── Leakage: a view must NOT expose other modalities ─────────────────────────
def test_no_cross_modality_leakage(case: Case) -> None:
    assert not hasattr(vision_view(case), "report_text")
    assert not hasattr(vision_view(case), "ehr_record")
    assert not hasattr(report_view(case), "image_path")
    assert not hasattr(report_view(case), "ehr_record")
    assert not hasattr(clinical_view(case), "image_path")
    assert not hasattr(clinical_view(case), "report_text")


def test_supervisor_is_raw_data_blind(case: Case) -> None:
    sv = supervisor_view(case, [])
    for field in ("image_path", "report_text", "ehr_record"):
        assert not hasattr(sv, field)


# ── No view carries ground-truth labels ──────────────────────────────────────
def test_views_carry_no_labels(case: Case) -> None:
    for v in (vision_view(case), report_view(case), clinical_view(case), supervisor_view(case, [])):
        assert not hasattr(v, "labels")


# ── Raw-modality fields are pairwise disjoint and cover the 3 modalities ─────
def test_raw_modality_fields_disjoint() -> None:
    vals = list(RAW_MODALITY_FIELDS.values())
    assert set(vals) == {"image_path", "report_text", "ehr_record"}
    assert len(vals) == len(set(vals))  # pairwise disjoint


# ── Views are immutable (frozen) ─────────────────────────────────────────────
def test_views_are_frozen(case: Case) -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        vision_view(case).image_path = Path("other.png")  # type: ignore[misc]


# ── Works when a modality is absent ──────────────────────────────────────────
def test_view_handles_absent_modality() -> None:
    ehr_only = Case(
        subject_id="9000001", study_id="9000001", source="mimic_demo", ehr_record={"labs": {}}
    )
    assert vision_view(ehr_only).image_path is None
    assert clinical_view(ehr_only).ehr_record == {"labs": {}}


def test_view_types(case: Case) -> None:
    assert isinstance(vision_view(case), VisionView)
    assert isinstance(report_view(case), ReportView)
    assert isinstance(clinical_view(case), ClinicalView)
    assert isinstance(supervisor_view(case, []), SupervisorView)
