"""Radiology report section extractor (Findings / Impression).

Pulls the FINDINGS and IMPRESSION sections out of a free-text radiology report (case-insensitive
headers; works on single-line or multi-line reports). Missing sections come back as empty strings.
"""

from __future__ import annotations

import re


def extract_sections(text: str) -> dict[str, str]:
    """Return {"findings": ..., "impression": ...} from a radiology report."""
    out = {"findings": "", "impression": ""}
    if not text:
        return out
    findings = re.search(r"findings\s*:(.*?)(?=impression\s*:|$)", text, re.IGNORECASE | re.DOTALL)
    impression = re.search(r"impression\s*:(.*)", text, re.IGNORECASE | re.DOTALL)
    if findings:
        out["findings"] = findings.group(1).strip()
    if impression:
        out["impression"] = impression.group(1).strip()
    return out
