"""Noise reduction filters for OCR preprocessing."""

from __future__ import annotations

import cv2
import numpy as np


def reduce_noise(
    image: np.ndarray,
    kernel_size: int = 3,
) -> np.ndarray:
    """Apply median blur to reduce salt-and-pepper noise.

    Parameters
    ----------
    image:
        Grayscale or binary image.
    kernel_size:
        Size of the median filter kernel (must be odd).

    Returns
    -------
    numpy.ndarray
        Denoised image.
    """
    return cv2.medianBlur(image, kernel_size)
