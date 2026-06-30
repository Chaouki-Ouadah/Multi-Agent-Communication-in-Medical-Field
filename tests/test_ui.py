"""Card 13 — pure render-helper + sample-data tests (no Streamlit launch)."""

from __future__ import annotations

from ui.components import render
from ui.sample_data import demo_case, demo_output

from src.data.chexpert import CHEXPERT_LABELS, FOCUS_5


def test_disclaimer_present_and_not_clinical_advice() -> None:
    assert "not clinical advice" in render.disclaimer_text().lower()


def test_status_colors_static_map() -> None:
    assert render.STATUS_COLORS["accepted"] == "#15803D"
    assert render.STATUS_COLORS["attack"] == "#DC2626"


def test_kpi_cards() -> None:
    out = demo_output()
    cards = {c["label"]: c["value"] for c in render.kpi_cards(out)}
    assert "Recommendation" in cards
    assert cards["Confidence"].endswith("%")  # 0.82 → "82%"
    assert cards["Arguments"] == str(len(out.arguments))
    assert int(cards["Debate rounds"]) >= 1


def test_recommendation_prefers_focus5() -> None:
    out = demo_output()
    assert render.recommendation(out) in FOCUS_5


def test_modality_panel_lists_evidence_and_blind() -> None:
    out = demo_output()
    panel = render.modality_panel("clinical", out.arguments)
    assert panel["agent"] == "clinical"
    assert panel["claims"]  # clinical agent contributed claims
    assert all(isinstance(c["evidence"], list) for c in panel["claims"])
    assert panel["blind_to"] == ["image", "report"]  # OIDP: clinical can't see image/report


def test_argument_graph_marks_accepted_and_attacks() -> None:
    out = demo_output()
    extension = {a.claim for a in out.winning_args}
    attacks = out.debate_state["attacks"]
    dot = render.build_argument_graph(out.arguments, attacks, extension)
    src = dot.source
    assert render.STATUS_COLORS["accepted"] in src  # ≥1 accepted (green) node
    # an attack edge is drawn in red when the demo case has a conflict
    if attacks:
        assert render.STATUS_COLORS["attack"] in src


def test_pathology_rows_cover_14_and_mark_focus() -> None:
    rows = render.pathology_rows({"Cardiomegaly"})
    assert len(rows) == len(CHEXPERT_LABELS) == 14
    cardio = next(r for r in rows if r["label"] == "Cardiomegaly")
    assert cardio["predicted"] is True and cardio["focus"] is True
    no_finding = next(r for r in rows if r["label"] == "No Finding")
    assert no_finding["predicted"] is False


def test_demo_output_wellformed() -> None:
    out = demo_output()
    assert out.condition == "B5"
    assert out.arguments and out.winning_args  # debate produced + resolved arguments
    assert "not clinical advice" in out.explanation.lower()
    assert out.predicted_labels  # at least one pathology predicted


def test_demo_case_is_synthetic_no_image() -> None:
    case = demo_case()
    assert case.source == "demo" and case.image_path is None
    assert case.report_text and case.ehr_record
