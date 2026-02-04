"""OCR confidence scoring and filtering."""

from __future__ import annotations

from bbs_converter.ocr.engine import OCRResult
from bbs_converter.utils.constants import DEFAULT_CONFIDENCE_THRESHOLD
from bbs_converter.utils.logger import get_logger

_log = get_logger("ocr.confidence")


def is_confident(
    result: OCRResult,
    threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> bool:
    """Check whether an OCR result meets the confidence threshold.

    Parameters
    ----------
    result:
        OCR extraction result.
    threshold:
        Minimum acceptable confidence (0-100).

    Returns
    -------
    bool
        True if the result's confidence is at or above the threshold.
    """
    if result.confidence < threshold:
        _log.debug(
            "OCR confidence %.1f below threshold %.1f — rejecting '%s'",
            result.confidence,
            threshold,
            result.text[:50],
        )
        return False
    return True


def filter_confident(
    results: list[OCRResult],
    threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> list[OCRResult]:
    """Filter a list of OCR results to only those above the threshold."""
    return [r for r in results if is_confident(r, threshold)]
