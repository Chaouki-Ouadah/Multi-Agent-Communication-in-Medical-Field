"""Vision Agent — image-only chest-X-ray reasoning (OIDP).

Pipeline: take the image-only `VisionView` → retrieve similar precedent CXRs via CLIP Image RAG →
prompt LLaVA-Med (VQA) with the image + precedent labels → parse the findings into scheme-labelled
`Argument`s. The agent sees ONLY the image (a `VisionView`); it never reads the report or EHR.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from src.agents._parsing import clean_findings
from src.argumentation.framework import Argument
from src.knowledge.retriever import Precedent
from src.utils.modality_partitioner import VisionView


class _Retriever(Protocol):
    def retrieve(self, image_path: Path, k: int = 3) -> list[Precedent]: ...


class _VLM(Protocol):
    def answer(self, image_path: Path, prompt: str) -> str: ...


_DISCLAIMER = "Research prototype — not clinical advice."


def _opponent_block(opponents: list[Argument] | None) -> str:
    """Render OTHER specialists' text claims for a counter-argument round (OIDP: text only)."""
    if not opponents:
        return ""
    claims = "; ".join(a.claim for a in opponents if a.claim)
    if not claims:
        return ""
    return (
        " Other specialists (report/EHR) argue: "
        f"{claims}. Defend or refine your image-based reading against these claims."
    )


class VisionAgent:
    """Produces image-grounded arguments from a CXR via CLIP Image RAG + LLaVA-Med."""

    agent_name = "vision"

    def __init__(self, retriever: _Retriever, vlm: _VLM, k: int = 3) -> None:
        self.retriever = retriever
        self.vlm = vlm
        self.k = k

    def _prompt(self, precedents: list[Precedent], opponents: list[Argument] | None = None) -> str:
        ctx = ""
        if precedents:
            labels = sorted({lbl for p in precedents for lbl in p.labels})
            if labels:
                ctx = (
                    " For reference, visually similar prior chest X-rays were labelled: "
                    + ", ".join(labels)
                    + "."
                )
        return (
            "You are a radiology vision assistant. Describe the chest X-ray findings, one per "
            f"sentence, naming any abnormalities you see.{ctx}{_opponent_block(opponents)} "
            f"({_DISCLAIMER})"
        )

    def analyse(self, view: VisionView, opponents: list[Argument] | None = None) -> list[Argument]:
        image_path = view.image_path
        if image_path is None:
            return []
        precedents = self.retriever.retrieve(image_path, self.k)
        precedent_labels = sorted({lbl for p in precedents for lbl in p.labels})
        prompt = self._prompt(precedents, opponents)
        text = self.vlm.answer(image_path, prompt)

        args: list[Argument] = []
        if precedent_labels:
            args.append(
                Argument(
                    agent=self.agent_name,
                    claim=f"Similar prior CXRs were labelled: {', '.join(precedent_labels)}",
                    evidence=precedent_labels,
                    scheme="Argument from Analogy",
                )
            )
        for finding in clean_findings(text, prompt):
            args.append(
                Argument(
                    agent=self.agent_name,
                    claim=finding,
                    evidence=precedent_labels,
                    scheme="Argument from Sign",
                )
            )
        return args
