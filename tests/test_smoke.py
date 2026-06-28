"""Smoke test: package + submodules import cleanly. Keeps CI green pre-implementation."""

import importlib

import pytest

MODULES = [
    "src",
    "src.data",
    "src.agents",
    "src.argumentation",
    "src.knowledge",
    "src.pipeline",
    "src.evaluation",
    "src.utils",
]


@pytest.mark.parametrize("mod", MODULES)
def test_imports(mod: str) -> None:
    importlib.import_module(mod)
