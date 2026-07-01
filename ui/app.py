"""medargue — Streamlit explainability dashboard (ui-spec §4).

Shows the full pipeline for a case: CXR + the 3 modality-agent panels, the Dung argument graph
(accepted vs attacked), the resolved recommendation + confidence, the per-pathology table, and an
always-visible not-clinical-advice disclaimer. Defaults to **demo mode** (precomputed sample case — no
model needed, drives the Playwright E2E); a sidebar toggle runs **live** on Ollama via the Card-12
`run_condition(B5)`. Rendering logic lives in `ui/components/render.py` (pure, unit-tested).
"""

from __future__ import annotations

import os
from typing import Any

import streamlit as st
from ui.components import render
from ui.sample_data import demo_case, demo_output

from src.argumentation.schemes import form_attacks

_AGENTS = ("vision", "report", "clinical")
_DEMO_DEFAULT = os.environ.get("MEDARGUE_UI_MODE", "demo") == "demo"

_FONT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Fira+Sans:wght@300;400;600&display=swap');
html, body, [class*="css"] { font-family: 'Fira Sans', sans-serif; }
h1, h2, h3 { font-family: 'Fira Code', monospace; }
.medargue-disclaimer {
  position: sticky; top: 0; z-index: 999; background: #FEF3C7; color: #92400E;
  border: 1px solid #D97706; border-radius: 6px; padding: 8px 14px; margin-bottom: 10px;
  font-weight: 600;
}
.blind-note { color: #64748B; font-size: 0.85em; }
</style>
"""


def _run_live(case: Any, config_name: str):  # pragma: no cover - exercised only in live mode
    """Build the real agents (Ollama) and run a full-system condition. Lazy-imported (heavy)."""
    from src.agents.clinical import ClinicalAgent
    from src.agents.llm_client import OllamaLLMClient
    from src.agents.ner import ScispacyNer
    from src.agents.report import ReportAgent
    from src.agents.supervisor import SupervisorAgent
    from src.agents.vision import VisionAgent
    from src.evaluation.baselines import BASELINES, run_condition

    class _NoVLM:
        def answer(self, image_path: Any, prompt: str) -> str:
            return ""

    class _NoRetr:
        def retrieve(self, image_path: Any, k: int = 3) -> list:
            return []

    llm = OllamaLLMClient()
    agents = {
        "vision": VisionAgent(_NoRetr(), _NoVLM()),
        "report": ReportAgent(llm=llm, ner=ScispacyNer()),
        "clinical": ClinicalAgent(
            llm=llm, variable_dictionary={"BNP": {"reference_range": (0.0, 100.0)}}
        ),
    }
    return run_condition(
        case,
        BASELINES.get(config_name, BASELINES["B5"]),
        agents=agents,
        supervisor=SupervisorAgent(llm),
        llm=llm,
    )


def _render(output: Any) -> None:
    st.markdown(
        f'<div class="medargue-disclaimer">{render.disclaimer_text()}</div>', unsafe_allow_html=True
    )
    st.title("medargue — Multi-Agent Clinical Decision Support")

    # Row 1 — KPI cards
    cards = render.kpi_cards(output)
    for col, card in zip(st.columns(len(cards)), cards, strict=True):
        col.metric(card["label"], card["value"])

    # Row 2 — CXR + 3 modality panels
    st.subheader("Modalities")
    img_col, *panel_cols = st.columns(4)
    with img_col:
        st.caption("CXR")
        case = output.debate_state.get("case") if output.debate_state else None
        path = getattr(case, "image_path", None)
        if path:
            st.image(str(path), use_container_width=True)
        else:
            st.info("No CXR image in this case — Vision agent abstains.")
    for col, agent in zip(panel_cols, _AGENTS, strict=True):
        panel = render.modality_panel(agent, output.arguments)
        with col:
            st.markdown(f"**{panel['title']}**")
            if panel["claims"]:
                for c in panel["claims"]:
                    st.markdown(
                        f"- {c['claim']}  \n  _evidence:_ {', '.join(c['evidence']) or '—'}  \n  _scheme:_ {c['scheme']}"
                    )
            else:
                st.caption("no claims")
            st.markdown(
                f"<span class='blind-note'>blind to: {', '.join(panel['blind_to'])}</span>",
                unsafe_allow_html=True,
            )

    # Row 3 — argument graph (centerpiece)
    st.subheader("Argument graph (Dung's AAF — accepted = green/bold, attacks = red)")
    extension_claims = {a.claim for a in output.winning_args}
    attacks = form_attacks(output.arguments)
    st.graphviz_chart(render.build_argument_graph(output.arguments, attacks, extension_claims))

    # Row 4 — recommendation + explanation
    st.subheader("Resolved recommendation")
    st.markdown(f"**{render.recommendation(output)}** — {output.explanation}")

    # Row 5 — per-pathology table (graph fallback)
    st.subheader("Pathology labels (14 CheXpert; focus-5 ★)")
    rows = render.pathology_rows(output.predicted_labels)
    st.dataframe(
        [
            {
                "Pathology": ("★ " if r["focus"] else "") + r["label"],
                "Predicted": "✓" if r["predicted"] else "",
            }
            for r in rows
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.caption(render.SHORT_DISCLAIMER)


def main() -> None:  # pragma: no cover - Streamlit entrypoint (covered by the Playwright E2E)
    st.set_page_config(layout="wide", page_title="medargue")
    st.markdown(_FONT_CSS, unsafe_allow_html=True)

    with st.sidebar:
        st.header("Case & configuration")
        st.selectbox("Case", ["DEMO-001 (sample)"], index=0)
        config_name = st.selectbox(
            "RAG configuration", ["B5 (full)", "B3 (no AAF)", "B1 (single LLM)"], index=0
        )
        mode_live = st.toggle("Live (Ollama)", value=not _DEMO_DEFAULT)
        run = st.button("Run analysis", type="primary")

    cfg = config_name.split()[0]
    if mode_live and run:
        with st.spinner("Running multi-agent debate on Ollama…"):
            output = _run_live(demo_case(), cfg)
    else:
        output = demo_output()
    _render(output)


if __name__ == "__main__":  # pragma: no cover
    main()
