"""Card 13 — Playwright E2E against the live Streamlit app (demo mode). Marker: e2e.

Non-skipped: launches the real dashboard (no model — demo sample case) and asserts the whole pipeline
renders: disclaimer, recommendation, the three modality panels, the argument graph, the pathology table.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


def test_app_loads_full_pipeline(page: Page, streamlit_app: str) -> None:
    page.goto(streamlit_app, wait_until="domcontentloaded")

    # sticky disclaimer banner (mandatory, ui-spec §5)
    expect(page.get_by_text("not clinical advice", exact=False).first).to_be_visible(timeout=45_000)

    # title + resolved recommendation
    expect(
        page.get_by_text("Multi-Agent Clinical Decision Support", exact=False).first
    ).to_be_visible()
    expect(page.get_by_text("Resolved recommendation", exact=False).first).to_be_visible()

    # the three modality panels
    for header in ("Vision (CXR)", "Report (text)", "Clinical (EHR)"):
        expect(page.get_by_text(header, exact=False).first).to_be_visible()

    # argument graph (centerpiece) + pathology table fallback
    expect(page.get_by_text("Argument graph", exact=False).first).to_be_visible()
    expect(page.get_by_text("Pathology labels", exact=False).first).to_be_visible()
