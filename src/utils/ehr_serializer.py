"""EHR serialiser: a structured record -> a compact text block with reference-range flags.

Turns `{"demographics": {...}, "labs": {label: value}}` into lines the Clinical Agent's LLM can read,
annotating each lab with ↑ (above range) / ↓ (below range) / ✓ (within range) using the loader's
`variable_dictionary` reference ranges. Labs without a known range get no flag.
"""

from __future__ import annotations

from typing import Any


def _flag(value: float, lo: float, hi: float) -> str:
    if value > hi:
        return "↑"
    if value < lo:
        return "↓"
    return "✓"


def serialize_ehr(ehr_record: dict[str, Any], variable_dictionary: dict[str, Any]) -> str:
    """Render an EHR record as a text block with ↑/↓/✓ reference-range flags (deterministic order)."""
    if not ehr_record:
        return ""
    lines: list[str] = []
    demo = ehr_record.get("demographics") or {}
    if demo:
        lines.append("Demographics: " + ", ".join(f"{k}={v}" for k, v in demo.items()))
    labs = ehr_record.get("labs") or {}
    for label in sorted(labs):  # deterministic
        value = labs[label]
        ref = (variable_dictionary.get(label) or {}).get("reference_range")
        if ref is not None and value is not None:
            lo, hi = ref
            lines.append(f"{label}: {value} [{_flag(float(value), lo, hi)} vs {lo}-{hi}]")
        else:
            lines.append(f"{label}: {value}")
    return "\n".join(lines)
