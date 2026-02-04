"""Full OCR pipeline: preprocess → threshold → denoise → engine."""

from __future__ import annotations

from typing import Optional

import numpy as np

from bbs_converter.ocr.cache import FrameDiffCache
from bbs_converter.ocr.confidence import is_confident
from bbs_converter.ocr.denoise import reduce_noise
from bbs_converter.ocr.engine import OCRResult, TesseractEngine
from bbs_converter.ocr.preprocessor import to_grayscale
from bbs_converter.ocr.threshold import adaptive_threshold
from bbs_converter.utils.constants import DEFAULT_CONFIDENCE_THRESHOLD
from bbs_converter.utils.logger import get_logger

_log = get_logger("ocr.pipeline")


class OCRPipeline:
    """End-to-end OCR pipeline with caching and confidence filtering.

    Parameters
    ----------
    confidence_threshold:
        Minimum confidence to accept a result.
    use_cache:
        Whether to enable frame-diff caching.
    lang:
        Tesseract language code.
    """

    def __init__(
        self,
        confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
        use_cache: bool = True,
        lang: str = "eng",
    ) -> None:
        self._engine = TesseractEngine(lang=lang)
        self._cache = FrameDiffCache() if use_cache else None
        self._confidence_threshold = confidence_threshold

    def process(self, frame: np.ndarray) -> Optional[OCRResult]:
        """Run the full OCR pipeline on a captured frame.

        Parameters
        ----------
        frame:
            Raw captured frame (BGR or BGRA).

        Returns
        -------
        OCRResult or None
            Extracted text if confidence is sufficient, else None.
        """
        gray = to_grayscale(frame)

        # Check cache first
        if self._cache is not None:
            cached = self._cache.get_if_unchanged(gray)
            if cached is not None:
                return cached

        # Preprocess
        binary = adaptive_threshold(gray)
        clean = reduce_noise(binary)

        # Extract
        result = self._engine.extract(clean)

        # Cache the result
        if self._cache is not None:
            self._cache.update(gray, result)

        # Filter by confidence
        if not is_confident(result, self._confidence_threshold):
            return None

        return result

    @property
    def cache_hit_rate(self) -> float:
        """Return the cache hit rate, or 0 if caching is disabled."""
        return self._cache.hit_rate if self._cache is not None else 0.0
