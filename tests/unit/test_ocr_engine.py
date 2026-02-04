"""Tests for Tesseract engine wrapper."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from bbs_converter.ocr.engine import OCRResult, TesseractEngine
from bbs_converter.utils.exceptions import OCRError


class TestTesseractEngine:
    def _mock_pytesseract(self, data: dict) -> MagicMock:
        mock = MagicMock()
        mock.image_to_data.return_value = data
        mock.Output.DICT = "dict"
        return mock

    def test_extracts_text(self) -> None:
        data = {
            "text": ["Hello", "World", ""],
            "conf": [90.0, 85.0, -1],
        }
        mock_pt = self._mock_pytesseract(data)
        engine = TesseractEngine()
        image = np.zeros((50, 200), dtype=np.uint8)

        import sys
        with patch.dict(sys.modules, {"pytesseract": mock_pt}):
            result = engine.extract(image)

        assert result.text == "Hello World"
        assert result.confidence == pytest.approx(87.5)

    def test_empty_result(self) -> None:
        data = {"text": ["", ""], "conf": [-1, -1]}
        mock_pt = self._mock_pytesseract(data)
        engine = TesseractEngine()
        image = np.zeros((50, 200), dtype=np.uint8)

        import sys
        with patch.dict(sys.modules, {"pytesseract": mock_pt}):
            result = engine.extract(image)

        assert result.text == ""
        assert result.confidence == 0.0

    def test_ocr_result_is_frozen(self) -> None:
        result = OCRResult(text="test", confidence=90.0)
        with pytest.raises(AttributeError):
            result.text = "changed"  # type: ignore[misc]

    def test_extraction_failure_raises_ocr_error(self) -> None:
        mock_pt = MagicMock()
        mock_pt.image_to_data.side_effect = RuntimeError("tesseract not found")
        mock_pt.Output.DICT = "dict"
        engine = TesseractEngine()
        image = np.zeros((50, 200), dtype=np.uint8)

        import sys
        with patch.dict(sys.modules, {"pytesseract": mock_pt}):
            with pytest.raises(OCRError, match="Tesseract extraction failed"):
                engine.extract(image)
