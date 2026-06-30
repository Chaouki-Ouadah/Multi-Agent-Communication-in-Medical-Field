"""Real BioViL-T CXR image-embedding client (powers CLIP Image RAG for the Vision Agent).

Uses Microsoft's `health_multimodal` (hi-ml-multimodal) — the canonical BioViL/BioViL-T API
(Boecking et al.), which applies the correct CXR-specific preprocessing (HF `AutoImageProcessor`
does not support this model). The inference engine is built lazily on first `embed_image()`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import numpy as np

# BioViL-T projects images into a 128-d joint image/text space.
BIOVIL_EMBED_DIM = 128


@runtime_checkable
class ImageEmbedder(Protocol):
    """Image-in, vector-out embedder for retrieval."""

    embed_dim: int

    def embed_image(self, image_path: Path) -> np.ndarray: ...


class BioViLEmbedder:
    """Real CXR image embedder (Microsoft BioViL-T via health_multimodal), loaded lazily."""

    def __init__(self) -> None:
        self._engine: Any = None
        self._embed_dim = BIOVIL_EMBED_DIM

    @property
    def is_loaded(self) -> bool:
        return self._engine is not None

    @property
    def embed_dim(self) -> int:
        return self._embed_dim

    def _ensure(self) -> Any:
        if self._engine is None:
            from health_multimodal.image import get_image_inference
            from health_multimodal.image.utils import ImageModelType

            self._engine = get_image_inference(ImageModelType.BIOVIL_T)
        return self._engine

    def embed_image(self, image_path: Path) -> np.ndarray:
        engine = self._ensure()
        tensor = engine.get_projected_global_embedding(Path(image_path))
        vec = tensor.detach().cpu().numpy().astype(np.float32).reshape(-1)
        self._embed_dim = int(vec.shape[0])
        return vec
