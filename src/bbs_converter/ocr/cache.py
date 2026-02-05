"""Frame-diff cache to skip OCR on unchanged frames."""

from __future__ import annotations

import numpy as np

from bbs_converter.ocr.engine import OCRResult
from bbs_converter.utils.logger import get_logger

_log = get_logger("ocr.cache")


class FrameDiffCache:
    """Cache OCR results and skip re-processing when frames haven't changed.

    Compares the current frame to the previous one using mean absolute
    difference. If below the threshold, the cached result is returned.

    Parameters
    ----------
    diff_threshold:
        Mean pixel difference below which frames are considered identical.
    """

    def __init__(self, diff_threshold: float = 5.0) -> None:
        self._threshold = diff_threshold
        self._last_frame: np.ndarray | None = None
        self._last_result: OCRResult | None = None
        self._hits = 0
        self._misses = 0

    def get_if_unchanged(self, frame: np.ndarray) -> OCRResult | None:
        """Return the cached result if the frame hasn't changed.

        Parameters
        ----------
        frame:
            Current preprocessed frame (grayscale).

        Returns
        -------
        OCRResult or None
            Cached result if the frame is similar enough, else None.
        """
        if self._last_frame is None or self._last_result is None:
            self._misses += 1
            return None

        if self._last_frame.shape != frame.shape:
            self._misses += 1
            return None

        diff = np.mean(np.abs(frame.astype(float) - self._last_frame.astype(float)))
        if diff < self._threshold:
            self._hits += 1
            _log.debug("Cache hit (diff=%.2f)", diff)
            return self._last_result

        self._misses += 1
        return None

    def update(self, frame: np.ndarray, result: OCRResult) -> None:
        """Store the current frame and result for future comparisons."""
        self._last_frame = frame.copy()
        self._last_result = result

    @property
    def hit_rate(self) -> float:
        """Return the cache hit rate as a percentage."""
        total = self._hits + self._misses
        return (self._hits / total * 100) if total > 0 else 0.0
