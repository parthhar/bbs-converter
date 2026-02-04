"""Tests for frame-diff OCR cache."""

from __future__ import annotations

import numpy as np

from bbs_converter.ocr.cache import FrameDiffCache
from bbs_converter.ocr.engine import OCRResult


class TestFrameDiffCache:
    def test_miss_on_first_frame(self) -> None:
        cache = FrameDiffCache()
        frame = np.zeros((50, 100), dtype=np.uint8)
        assert cache.get_if_unchanged(frame) is None

    def test_hit_on_identical_frame(self) -> None:
        cache = FrameDiffCache()
        frame = np.ones((50, 100), dtype=np.uint8) * 128
        result = OCRResult(text="5000", confidence=90.0)
        cache.update(frame, result)
        cached = cache.get_if_unchanged(frame)
        assert cached is not None
        assert cached.text == "5000"

    def test_miss_on_different_frame(self) -> None:
        cache = FrameDiffCache(diff_threshold=5.0)
        frame1 = np.zeros((50, 100), dtype=np.uint8)
        frame2 = np.ones((50, 100), dtype=np.uint8) * 200
        result = OCRResult(text="5000", confidence=90.0)
        cache.update(frame1, result)
        assert cache.get_if_unchanged(frame2) is None

    def test_hit_on_similar_frame(self) -> None:
        cache = FrameDiffCache(diff_threshold=10.0)
        frame1 = np.ones((50, 100), dtype=np.uint8) * 128
        frame2 = np.ones((50, 100), dtype=np.uint8) * 130  # diff = 2
        result = OCRResult(text="5000", confidence=90.0)
        cache.update(frame1, result)
        assert cache.get_if_unchanged(frame2) is not None

    def test_miss_on_shape_change(self) -> None:
        cache = FrameDiffCache()
        frame1 = np.zeros((50, 100), dtype=np.uint8)
        frame2 = np.zeros((60, 100), dtype=np.uint8)
        result = OCRResult(text="5000", confidence=90.0)
        cache.update(frame1, result)
        assert cache.get_if_unchanged(frame2) is None

    def test_hit_rate(self) -> None:
        cache = FrameDiffCache()
        frame = np.zeros((50, 100), dtype=np.uint8)
        result = OCRResult(text="x", confidence=90.0)

        cache.get_if_unchanged(frame)  # miss
        cache.update(frame, result)
        cache.get_if_unchanged(frame)  # hit
        cache.get_if_unchanged(frame)  # hit

        assert cache.hit_rate == (2 / 3) * 100

    def test_initial_hit_rate_is_zero(self) -> None:
        cache = FrameDiffCache()
        assert cache.hit_rate == 0.0
