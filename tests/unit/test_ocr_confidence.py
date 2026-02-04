"""Tests for OCR confidence scoring."""

from __future__ import annotations

from bbs_converter.ocr.confidence import filter_confident, is_confident
from bbs_converter.ocr.engine import OCRResult


class TestIsConfident:
    def test_above_threshold(self) -> None:
        result = OCRResult(text="5000", confidence=90.0)
        assert is_confident(result, threshold=60.0) is True

    def test_at_threshold(self) -> None:
        result = OCRResult(text="5000", confidence=60.0)
        assert is_confident(result, threshold=60.0) is True

    def test_below_threshold(self) -> None:
        result = OCRResult(text="5000", confidence=30.0)
        assert is_confident(result, threshold=60.0) is False

    def test_zero_confidence(self) -> None:
        result = OCRResult(text="", confidence=0.0)
        assert is_confident(result, threshold=60.0) is False


class TestFilterConfident:
    def test_filters_low_confidence(self) -> None:
        results = [
            OCRResult(text="good", confidence=90.0),
            OCRResult(text="bad", confidence=20.0),
            OCRResult(text="ok", confidence=70.0),
        ]
        filtered = filter_confident(results, threshold=60.0)
        assert len(filtered) == 2
        assert all(r.confidence >= 60.0 for r in filtered)

    def test_empty_list(self) -> None:
        assert filter_confident([], threshold=60.0) == []

    def test_all_pass(self) -> None:
        results = [OCRResult(text="a", confidence=99.0)]
        assert len(filter_confident(results, threshold=50.0)) == 1
