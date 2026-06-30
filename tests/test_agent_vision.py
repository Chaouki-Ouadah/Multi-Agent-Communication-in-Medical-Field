"""Card 4 — Vision Agent (image-only; CLIP Image RAG precedent + LLaVA-Med VQA -> Arguments).

Pure tests use stub retriever + stub VLM (no model/network). Live GPU test lives separately.
"""

from __future__ import annotations

import dataclasses
import os
from pathlib import Path

import pytest

from src.agents.vision import VisionAgent
from src.argumentation.framework import Argument
from src.data.loaders import Case
from src.knowledge.retriever import Precedent
from src.utils.modality_partitioner import vision_view

_SLICE = Path(os.environ.get("CHESTXRAY14_DIR", "data/chestxray14"))


class StubRetriever:
    def __init__(self) -> None:
        self.queried_with: list[Path] = []

    def retrieve(self, image_path: Path, k: int = 3) -> list[Precedent]:
        self.queried_with.append(image_path)
        return [Precedent(id="p1", labels=["Cardiomegaly"], distance=0.1)]


class StubVLM:
    def __init__(self) -> None:
        self.calls: list[tuple[Path, str]] = []

    def answer(self, image_path: Path, prompt: str) -> str:
        self.calls.append((image_path, prompt))
        return "Cardiomegaly is present. No pneumothorax."


def _vision_view():
    case = Case(
        subject_id="FAKE1", study_id="FAKE1", source="test", image_path=Path("img/FAKE1.png")
    )
    return vision_view(case)


def test_argument_shape() -> None:
    a = Argument(agent="vision", claim="Cardiomegaly", evidence=["Cardiomegaly"], scheme="Sign")
    assert a.agent == "vision" and a.claim and a.scheme
    with __import__("pytest").raises(dataclasses.FrozenInstanceError):
        a.claim = "x"  # type: ignore[misc]


def test_vision_returns_scheme_labelled_arguments() -> None:
    agent = VisionAgent(retriever=StubRetriever(), vlm=StubVLM())
    args = agent.analyse(_vision_view())
    assert isinstance(args, list) and args
    assert all(isinstance(a, Argument) for a in args)
    assert all(a.agent == "vision" and a.scheme for a in args)
    # at least one claim derived from the VLM text
    assert any("cardiomegaly" in a.claim.lower() for a in args)


def test_vision_cites_retrieved_precedent() -> None:
    agent = VisionAgent(retriever=StubRetriever(), vlm=StubVLM())
    args = agent.analyse(_vision_view())
    # the retrieved precedent label appears as evidence in some argument
    assert any("Cardiomegaly" in a.evidence for a in args)


def test_vision_is_image_only() -> None:
    view = _vision_view()
    assert not hasattr(view, "report_text") and not hasattr(view, "ehr_record")
    retr, vlm = StubRetriever(), StubVLM()
    VisionAgent(retriever=retr, vlm=vlm).analyse(view)
    # agent only ever passed the image path (never report/EHR)
    assert retr.queried_with == [view.image_path]
    assert vlm.calls[0][0] == view.image_path


@pytest.mark.llm
@pytest.mark.slow
def test_vision_agent_live() -> None:
    """Real CLIP Image RAG (BioViL+Chroma) + LLaVA-Med over the NIH slice. Local GPU only."""
    if not (_SLICE / "Data_Entry_2017.csv").exists():
        pytest.skip("NIH ChestX-ray14 slice not present (run scripts/fetch_chestxray14_slice.py)")
    from src.agents.embeddings import BioViLEmbedder
    from src.agents.vlm_client import LlavaMedClient
    from src.data.chestxray14 import ChestXray14Loader
    from src.knowledge.retriever import ClipImageRetriever

    cases = [
        c for c in ChestXray14Loader(_SLICE).cases() if c.image_path and c.image_path.exists()
    ][:15]
    assert cases, "no slice images found"
    retriever = ClipImageRetriever(BioViLEmbedder())
    retriever.build_index(
        (c.image_path.name, c.image_path, [k for k, v in c.labels.items() if v]) for c in cases
    )
    agent = VisionAgent(retriever=retriever, vlm=LlavaMedClient())
    args = agent.analyse(vision_view(cases[0]))
    assert args and all(a.agent == "vision" and a.scheme for a in args)
