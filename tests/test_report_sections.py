"""Card 5 — radiology report section extraction (pure, no model)."""

from __future__ import annotations

from src.utils.report_sections import extract_sections


def test_extract_findings_and_impression() -> None:
    text = (
        "FINDINGS: The cardiac silhouette is enlarged. Lungs are clear.\n"
        "IMPRESSION: Cardiomegaly without acute pulmonary disease."
    )
    s = extract_sections(text)
    assert "cardiac silhouette is enlarged" in s["findings"].lower()
    assert "cardiomegaly" in s["impression"].lower()


def test_missing_section_is_empty() -> None:
    s = extract_sections("IMPRESSION: No acute findings.")
    assert s["impression"]
    assert s["findings"] == ""


def test_case_insensitive_headers() -> None:
    s = extract_sections("Findings: bilateral effusions. impression: heart failure.")
    assert "effusions" in s["findings"].lower()
    assert "heart failure" in s["impression"].lower()


def test_empty_text() -> None:
    s = extract_sections("")
    assert s == {"findings": "", "impression": ""}
