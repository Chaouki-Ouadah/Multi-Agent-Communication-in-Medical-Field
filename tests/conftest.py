"""Shared pytest fixtures."""

from __future__ import annotations

import contextlib
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Iterator
from pathlib import Path

import pytest


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


@pytest.fixture(scope="session")
def streamlit_app() -> Iterator[str]:
    """Launch the Streamlit dashboard in demo mode (no model) and yield its URL; tear down after.

    Used by the Playwright E2E. Demo mode → renders the precomputed sample case, so this runs in CI
    without Ollama/Neo4j.
    """
    import os

    port = _free_port()
    env = {**os.environ, "MEDARGUE_UI_MODE": "demo"}
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "ui/app.py",
            "--server.port",
            str(port),
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    url = f"http://localhost:{port}"
    try:
        for _ in range(90):
            if proc.poll() is not None:
                raise RuntimeError("streamlit server exited before becoming ready")
            try:
                with urllib.request.urlopen(url, timeout=1):
                    break
            except (urllib.error.URLError, OSError):
                time.sleep(1)
        else:
            raise RuntimeError("streamlit server did not become ready in time")
        yield url
    finally:
        proc.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):
            proc.wait(timeout=10)


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
