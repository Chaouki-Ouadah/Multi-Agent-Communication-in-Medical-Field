"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def seed() -> int:
    """Deterministic seed for reproducible surrogate generation."""
    return 42


@pytest.fixture
def sample_cxr(tmp_path: Path) -> Path:
    """Write a small synthetic grayscale PNG (stand-in CXR) — no real image committed.

    Sufficient for model-client smoke tests (returns a vector / a string); not a real radiograph.
    """
    from PIL import Image  # local import: only needed when this fixture is used

    rng_gray = bytes((i * 7) % 256 for i in range(224 * 224))
    img = Image.frombytes("L", (224, 224), rng_gray).convert("RGB")
    out = tmp_path / "synthetic_cxr.png"
    img.save(out)
    return out
