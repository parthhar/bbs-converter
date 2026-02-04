"""Region-of-interest extraction from captured frames."""

from __future__ import annotations

import numpy as np

from bbs_converter.models import CaptureRegion


def extract_roi(
    frame: np.ndarray,
    region: CaptureRegion,
    frame_origin_x: int = 0,
    frame_origin_y: int = 0,
) -> np.ndarray:
    """Extract a sub-region from a frame.

    Coordinates in *region* are absolute screen coordinates. The
    *frame_origin* parameters define where the frame starts on screen.

    Parameters
    ----------
    frame:
        The full captured frame.
    region:
        The absolute screen region to extract.
    frame_origin_x:
        X-coordinate of the frame's top-left corner on screen.
    frame_origin_y:
        Y-coordinate of the frame's top-left corner on screen.

    Returns
    -------
    numpy.ndarray
        The extracted sub-region, clipped to frame boundaries.
    """
    x = max(0, region.x - frame_origin_x)
    y = max(0, region.y - frame_origin_y)
    x2 = min(frame.shape[1], x + region.width)
    y2 = min(frame.shape[0], y + region.height)
    return frame[y:y2, x:x2].copy()
