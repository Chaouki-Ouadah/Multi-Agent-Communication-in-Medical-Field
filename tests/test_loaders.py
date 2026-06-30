"""Card 1 — multimodal loader + surrogate datasets + CheXpert-14 label handling.

Per-modality Cases (Track 1): each surrogate carries one modality; absent modalities are None.
Label policy defaults to the CheXpert paper (Irvin et al. 2019) per-pathology convention.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.data.chestxray14 import ChestXray14Loader
from src.data.chexpert import (
    CHEXPERT_LABELS,
    FOCUS_5,
    LabelPolicy,
    apply_label_policy,
)
from src.data.loaders import BaseDatasetLoader, Case
from src.data.mimic_demo import MimicDemoLoader
from src.data.openi import OpenILoader

FIXTURES = Path(__file__).parent / "fixtures"


# ── CheXpert label set + policy ──────────────────────────────────────────────
def test_label_set() -> None:
    assert len(CHEXPERT_LABELS) == 14
    assert set(FOCUS_5).issubset(set(CHEXPERT_LABELS))


def test_label_policy_per_pathology_default() -> None:
    raw = {"Atelectasis": -1, "Edema": -1, "Cardiomegaly": -1, "Consolidation": -1, "Pneumonia": 1}
    out = apply_label_policy(raw)  # default = PER_PATHOLOGY
    assert out["Atelectasis"] == 1  # U-Ones
    assert out["Edema"] == 1  # U-Ones
    assert out["Cardiomegaly"] == 0  # U-Zeros
    assert out["Consolidation"] == 0  # U-Zeros
    assert out["Pneumonia"] == 1  # certain positive


def test_label_policy_blank_is_negative() -> None:
    out = apply_label_policy({})  # nothing present
    assert set(out) == set(CHEXPERT_LABELS)
    assert all(v == 0 for v in out.values())


def test_label_policy_global_overrides() -> None:
    raw = {"Cardiomegaly": -1, "Atelectasis": -1}
    assert apply_label_policy(raw, LabelPolicy.U_ONES)["Cardiomegaly"] == 1
    assert apply_label_policy(raw, LabelPolicy.U_ZEROS)["Atelectasis"] == 0


def test_label_policy_three_state_preserves_uncertain() -> None:
    out = apply_label_policy({"Pneumonia": -1}, LabelPolicy.THREE_STATE)
    assert out["Pneumonia"] == -1


# ── ABC conformance ──────────────────────────────────────────────────────────
@pytest.fixture
def loaders() -> list[BaseDatasetLoader]:
    return [
        ChestXray14Loader(FIXTURES / "chestxray14"),
        OpenILoader(FIXTURES / "openi"),
        MimicDemoLoader(FIXTURES / "mimic_demo"),
    ]


def test_all_loaders_satisfy_abc(loaders: list[BaseDatasetLoader]) -> None:
    for ld in loaders:
        assert isinstance(ld, BaseDatasetLoader)
        assert ld.labels() == CHEXPERT_LABELS
        assert isinstance(ld.modalities(), dict) and ld.modalities()
        assert isinstance(ld.variable_dictionary(), dict)
        assert all(isinstance(c, Case) for c in ld.cases())


# ── Per-modality Case shapes ─────────────────────────────────────────────────
def test_chestxray14_case_shape() -> None:
    cases = list(ChestXray14Loader(FIXTURES / "chestxray14").cases())
    assert len(cases) == 4
    c = cases[0]
    assert c.image_path is not None and c.report_text is None and c.ehr_record is None
    assert c.source == "chestxray14"


def test_openi_case_shape() -> None:
    cases = list(OpenILoader(FIXTURES / "openi").cases())
    assert len(cases) == 2
    c = cases[0]
    assert c.image_path is not None and c.report_text is not None and c.ehr_record is None
    assert "cardiomegaly" in c.report_text.lower()


def test_mimic_demo_case_shape() -> None:
    cases = list(MimicDemoLoader(FIXTURES / "mimic_demo").cases())
    assert len(cases) == 2  # two subjects
    c = next(c for c in cases if c.subject_id == "9000001")
    assert c.image_path is None and c.report_text is None
    assert c.ehr_record is not None
    assert "Creatinine" in c.ehr_record["labs"]
    assert c.ehr_record["demographics"]["anchor_age"] == 67


# ── NIH-14 → CheXpert-14 mapping (overlap only) ──────────────────────────────
def test_chestxray14_label_map() -> None:
    cases = {c.subject_id: c for c in ChestXray14Loader(FIXTURES / "chestxray14").cases()}
    # FAKE0001: Cardiomegaly|Effusion -> Cardiomegaly + Pleural Effusion positive
    assert cases["FAKE0001"].labels["Cardiomegaly"] == 1
    assert cases["FAKE0001"].labels["Pleural Effusion"] == 1
    # FAKE0002: No Finding -> No Finding 1, pathologies 0
    assert cases["FAKE0002"].labels["No Finding"] == 1
    assert cases["FAKE0002"].labels["Cardiomegaly"] == 0
    # FAKE0003: Pneumonia|Infiltration -> Pneumonia 1; Infiltration is NIH-only, absent from CheXpert
    assert cases["FAKE0003"].labels["Pneumonia"] == 1
    assert "Infiltration" not in cases["FAKE0003"].labels


# ── Determinism ──────────────────────────────────────────────────────────────
def test_deterministic_order() -> None:
    a = [c.subject_id for c in ChestXray14Loader(FIXTURES / "chestxray14").cases()]
    b = [c.subject_id for c in ChestXray14Loader(FIXTURES / "chestxray14").cases()]
    assert a == b


# ── No real data committed (fixtures must be synthetic) ──────────────────────
def test_fixtures_are_synthetic() -> None:
    cxr = [c.subject_id for c in ChestXray14Loader(FIXTURES / "chestxray14").cases()]
    assert all(sid.startswith("FAKE") for sid in cxr)
    mimic = [c.subject_id for c in MimicDemoLoader(FIXTURES / "mimic_demo").cases()]
    assert all(int(sid) >= 9_000_000 for sid in mimic)  # sentinel synthetic range
