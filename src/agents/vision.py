"""Vision Agent — image-only chest-X-ray reasoning (OIDP).

Pipeline: take the image-only `VisionView` → retrieve similar precedent CXRs via CLIP Image RAG →
prompt LLaVA-Med (VQA) with the image + precedent labels → parse the findings into scheme-labelled
`Argument`s. The agent sees ONLY the image (a `VisionView`); it never reads the report or EHR.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Protocol

from src.argumentation.framework import Argument
from src.knowledge.retriever import Precedent
from src.utils.modality_partitioner import VisionView


class _Retriever(Protocol):
    def retrieve(self, image_path: Path, k: int = 3) -> list[Precedent]: ...


class _VLM(Protocol):
    def answer(self, image_path: Path, prompt: str) -> str: ...


_DISCLAIMER = "Research prototype — not clinical advice."


def _split_findings(text: str) -> list[str]:
    """Split VLM free text into individual finding statements."""
    parts = re.split(r"[.\n;]+", text)
    return [p.strip() for p in parts if len(p.strip()) > 2]


class VisionAgent:
    """Produces image-grounded arguments from a CXR via CLIP Image RAG + LLaVA-Med."""

    agent_name = "vision"

    def __init__(self, retriever: _Retriever, vlm: _VLM, k: int = 3) -> None:
        self.retriever = retriever
        self.vlm = vlm
        self.k = k

    def _prompt(self, precedents: list[Precedent]) -> str:
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
            f"sentence, naming any abnormalities you see.{ctx} ({_DISCLAIMER})"
        )

    def analyse(self, view: VisionView) -> list[Argument]:
        image_path = view.image_path
        if image_path is None:
            return []
        precedents = self.retriever.retrieve(image_path, self.k)
        precedent_labels = sorted({lbl for p in precedents for lbl in p.labels})
        text = self.vlm.answer(image_path, self._prompt(precedents))

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
        for finding in _split_findings(text):
            args.append(
                Argument(
                    agent=self.agent_name,
                    claim=finding,
                    evidence=precedent_labels,
                    scheme="Argument from Sign",
                )
            )
        return args
