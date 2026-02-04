"""Tesseract OCR engine wrapper."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from bbs_converter.utils.exceptions import OCRError
from bbs_converter.utils.logger import get_logger

_log = get_logger("ocr.engine")


@dataclass(frozen=True)
class OCRResult:
    """Result of an OCR extraction."""

    text: str
    confidence: float


class TesseractEngine:
    """Wrapper around pytesseract for text extraction.

    Parameters
    ----------
    lang:
        Tesseract language code.
    psm:
        Page segmentation mode (default 7 = single line).
    """

    def __init__(self, lang: str = "eng", psm: int = 7) -> None:
        self._lang = lang
        self._config = f"--psm {psm}"

    def extract(self, image: np.ndarray) -> OCRResult:
        """Run OCR on a preprocessed image.

        Parameters
        ----------
        image:
            Grayscale or binary preprocessed image.

        Returns
        -------
        OCRResult
            Extracted text and average confidence score.

        Raises
        ------
        OCRError
            If Tesseract fails.
        """
        try:
            import pytesseract
        except ImportError as exc:
            raise OCRError("pytesseract is required for OCR") from exc

        try:
            data = pytesseract.image_to_data(
                image,
                lang=self._lang,
                config=self._config,
                output_type=pytesseract.Output.DICT,
            )
        except Exception as exc:
            raise OCRError(f"Tesseract extraction failed: {exc}") from exc

        texts: list[str] = []
        confidences: list[float] = []

        for i, conf in enumerate(data["conf"]):
            conf_val = float(conf)
            if conf_val > 0:
                word = data["text"][i].strip()
                if word:
                    texts.append(word)
                    confidences.append(conf_val)

        text = " ".join(texts)
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
        return OCRResult(text=text, confidence=avg_conf)
