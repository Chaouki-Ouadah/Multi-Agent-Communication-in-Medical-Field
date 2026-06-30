"""Card 7 — shared LLM-output parser (prompt-echo / boilerplate stripping). Pure."""

from __future__ import annotations

from src.agents._parsing import clean_findings


def test_drops_boilerplate_markers() -> None:
    text = (
        "You are a clinical data assistant. List the salient findings.\n"
        "Creatinine is elevated. Research prototype — not clinical advice."
    )
    out = clean_findings(text)
    assert out == ["Creatinine is elevated"]


def test_drops_verbatim_prompt_echo() -> None:
    prompt = "FINDINGS: cardiac silhouette enlarged\nIMPRESSION: cardiomegaly"
    # model echoes a prompt line, then adds a real finding
    text = "FINDINGS: cardiac silhouette enlarged\nThere is gross cardiomegaly"
    out = clean_findings(text, prompt)
    assert "There is gross cardiomegaly" in out
    assert "FINDINGS: cardiac silhouette enlarged" not in out


def test_keeps_real_findings() -> None:
    out = clean_findings("Bilateral pleural effusions. Mild atelectasis at the bases.")
    assert out == ["Bilateral pleural effusions", "Mild atelectasis at the bases"]


def test_drops_short_fragments() -> None:
    assert clean_findings("ok. . a. Pneumothorax on the left") == ["Pneumothorax on the left"]


def test_empty_text() -> None:
    assert clean_findings("", "some prompt") == []
