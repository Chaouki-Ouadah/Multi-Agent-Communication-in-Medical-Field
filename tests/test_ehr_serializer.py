"""Card 6 — EHR serialiser (pure): labs + demographics -> text with ref-range flags."""

from __future__ import annotations

from src.utils.ehr_serializer import serialize_ehr

_VARDICT = {
    "Creatinine": {"reference_range": (0.6, 1.3)},
    "Potassium": {"reference_range": (3.5, 5.1)},
    "Glucose": {},  # no reference range
}


def _record(creat: float, k: float, glu: float) -> dict:
    return {
        "demographics": {"gender": "F", "anchor_age": 67},
        "labs": {"Creatinine": creat, "Potassium": k, "Glucose": glu},
    }


def test_flags_high_low_ok() -> None:
    text = serialize_ehr(_record(2.4, 3.0, 90), _VARDICT)
    assert "Creatinine" in text and "↑" in text  # 2.4 > 1.3
    assert "↓" in text  # Potassium 3.0 < 3.5
    # Glucose has no range -> no flag token attached to its line
    glucose_line = next(ln for ln in text.splitlines() if "Glucose" in ln)
    assert "↑" not in glucose_line and "↓" not in glucose_line and "✓" not in glucose_line


def test_flag_within_range_is_ok() -> None:
    text = serialize_ehr(_record(1.0, 4.1, 90), _VARDICT)
    creat_line = next(ln for ln in text.splitlines() if "Creatinine" in ln)
    assert "✓" in creat_line  # 1.0 within 0.6-1.3


def test_demographics_present() -> None:
    text = serialize_ehr(_record(1.0, 4.1, 90), _VARDICT)
    assert "67" in text and ("F" in text or "female" in text.lower())


def test_deterministic() -> None:
    a = serialize_ehr(_record(1.0, 4.1, 90), _VARDICT)
    b = serialize_ehr(_record(1.0, 4.1, 90), _VARDICT)
    assert a == b


def test_empty_record() -> None:
    assert serialize_ehr({}, _VARDICT) == "" or "no" in serialize_ehr({}, _VARDICT).lower()
