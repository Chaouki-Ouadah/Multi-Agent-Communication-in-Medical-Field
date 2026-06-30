"""Shared LLM-output parsing for the modality agents.

`clean_findings` splits an LLM's free-text answer into individual finding statements while dropping
**prompt echo** and instruction/boilerplate lines. Local instruct models (Meditron via Ollama) often
restate the prompt — "You are a clinical data assistant...", the disclaimer, the section headers —
which the naive splitter wrapped into junk `Argument`s (the Card-5/Card-6 bug). This central helper
fixes that for Vision, Report, and Clinical alike.
"""

from __future__ import annotations

import re

# Instruction / boilerplate fragments the models tend to echo back. A candidate finding whose
# normalised form contains any of these is dropped (it is prompt text, not a clinical finding).
_BOILERPLATE_MARKERS: tuple[str, ...] = (
    "you are a",
    "research prototype",
    "not clinical advice",
    "one per sentence",
    "list the salient",
    "clinical entities",
    "structured ehr",
    "report sections",
    "reference range",
    "name any abnormalities",
    "describe the chest",
    "for reference",
    "↑/↓/✓",
)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def clean_findings(text: str, prompt: str = "") -> list[str]:
    """Split `text` into finding statements, dropping prompt-echo and boilerplate lines.

    A candidate is dropped when it (a) is ≤2 chars, (b) matches a whole line of `prompt`
    verbatim (the model echoed the prompt), or (c) contains an instruction/boilerplate marker.
    """
    prompt_lines = {_norm(line) for line in prompt.splitlines() if line.strip()}
    findings: list[str] = []
    for part in re.split(r"[.\n;]+", text):
        candidate = part.strip()
        if len(candidate) <= 2:
            continue
        norm = _norm(candidate)
        if norm in prompt_lines:  # verbatim prompt echo
            continue
        if any(marker in norm for marker in _BOILERPLATE_MARKERS):
            continue
        findings.append(candidate)
    return findings
