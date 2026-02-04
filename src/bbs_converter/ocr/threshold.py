"""Adaptive binarization for OCR preprocessing."""

from __future__ import annotations

import cv2
import numpy as np


def adaptive_threshold(
    gray: np.ndarray,
    block_size: int = 11,
    constant: int = 2,
) -> np.ndarray:
    """Apply adaptive thresholding to a grayscale image.

    Uses Gaussian-weighted mean for local threshold calculation,
    which handles uneven lighting common in screen captures.

    Parameters
    ----------
    gray:
        Single-channel grayscale image.
    block_size:
        Size of the neighborhood for threshold calculation (must be odd).
    constant:
        Constant subtracted from the mean.

    Returns
    -------
    numpy.ndarray
        Binary image (0 or 255).
    """
    return cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size,
        constant,
    )
