"""scispaCy clinical NER (mockable) for the Report Agent.

Lazy-loads a scispaCy `en_core_sci_*` model and extracts unique clinical entity spans from text.
Injected into the Report Agent so unit tests use a stub (no model load).
"""

from __future__ import annotations

import os
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Ner(Protocol):
    """Text-in, list-of-entity-spans-out."""

    def entities(self, text: str) -> list[str]: ...


class ScispacyNer:
    """Real scispaCy clinical NER, model loaded lazily on first call."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.environ.get("SCISPACY_MODEL", "en_core_sci_sm")
        self._nlp: Any = None

    @property
    def is_loaded(self) -> bool:
        return self._nlp is not None

    def _ensure(self) -> Any:
        if self._nlp is None:
            import spacy

            self._nlp = spacy.load(self.model)
        return self._nlp

    def entities(self, text: str) -> list[str]:
        nlp = self._ensure()
        seen: list[str] = []
        for ent in nlp(text).ents:
            span = ent.text.strip()
            if span and span not in seen:
                seen.append(span)
        return seen
