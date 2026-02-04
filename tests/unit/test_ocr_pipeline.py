"""Tests for end-to-end OCR pipeline."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np

from bbs_converter.ocr.engine import OCRResult
from bbs_converter.ocr.pipeline import OCRPipeline


class TestOCRPipeline:
    def _make_pipeline(self, **kwargs) -> OCRPipeline:
        return OCRPipeline(**kwargs)

    def _mock_engine_extract(self, text: str, confidence: float):
        return patch.object(
            OCRPipeline,
            "_OCRPipeline__engine_extract",
            return_value=OCRResult(text=text, confidence=confidence),
        )

    def test_process_returns_result(self) -> None:
        pipeline = self._make_pipeline(confidence_threshold=60.0, use_cache=False)
        result = OCRResult(text="5000", confidence=90.0)

        with patch.object(pipeline._engine, "extract", return_value=result):
            frame = np.random.randint(0, 256, (100, 200, 3), dtype=np.uint8)
            out = pipeline.process(frame)

        assert out is not None
        assert out.text == "5000"

    def test_low_confidence_returns_none(self) -> None:
        pipeline = self._make_pipeline(confidence_threshold=60.0, use_cache=False)
        result = OCRResult(text="???", confidence=20.0)

        with patch.object(pipeline._engine, "extract", return_value=result):
            frame = np.random.randint(0, 256, (100, 200, 3), dtype=np.uint8)
            out = pipeline.process(frame)

        assert out is None

    def test_cache_returns_cached_result(self) -> None:
        pipeline = self._make_pipeline(confidence_threshold=60.0, use_cache=True)
        result = OCRResult(text="5000", confidence=90.0)

        with patch.object(pipeline._engine, "extract", return_value=result):
            frame = np.ones((100, 200, 3), dtype=np.uint8) * 128
            out1 = pipeline.process(frame)
            out2 = pipeline.process(frame)  # should use cache

        assert out1 is not None
        assert out2 is not None
        assert out2.text == out1.text
        assert pipeline.cache_hit_rate > 0

    def test_cache_disabled(self) -> None:
        pipeline = self._make_pipeline(use_cache=False)
        result = OCRResult(text="5000", confidence=90.0)

        with patch.object(pipeline._engine, "extract", return_value=result):
            frame = np.ones((100, 200, 3), dtype=np.uint8) * 128
            pipeline.process(frame)

        assert pipeline.cache_hit_rate == 0.0
