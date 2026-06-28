"""Shared pytest fixtures."""

import pytest


@pytest.fixture
def seed() -> int:
    """Deterministic seed for reproducible surrogate generation."""
    return 42
