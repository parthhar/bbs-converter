"""Image preprocessing for OCR — grayscale conversion."""

from __future__ import annotations

import cv2
import numpy as np


def to_grayscale(frame: np.ndarray) -> np.ndarray:
    """Convert a BGR or BGRA frame to grayscale.

    Parameters
    ----------
    frame:
        Input image as a numpy array (BGR or BGRA).

    Returns
    -------
    numpy.ndarray
        Single-channel grayscale image.
    """
    if frame.ndim == 2:
        return frame

    channels = frame.shape[2]
    if channels == 4:
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
