"""Capture frames from a screen region using mss."""

from __future__ import annotations

import mss
import mss.tools
import numpy as np

from bbs_converter.models import CaptureRegion
from bbs_converter.utils.exceptions import CaptureError


class FrameGrabber:
    """Captures frames from a defined screen region.

    Parameters
    ----------
    region:
        The screen region to capture.
    """

    def __init__(self, region: CaptureRegion) -> None:
        self._region = region
        self._monitor = region.to_mss_monitor()
        self._sct: mss.mss | None = None

    def open(self) -> None:
        """Initialize the mss capture context."""
        self._sct = mss.mss()

    def close(self) -> None:
        """Release the mss capture context."""
        if self._sct is not None:
            self._sct.close()
            self._sct = None

    def grab(self) -> np.ndarray:
        """Capture a single frame as a numpy array (BGRA).

        Returns
        -------
        numpy.ndarray
            Frame pixels in BGRA format, shape (height, width, 4).

        Raises
        ------
        CaptureError
            If the grabber has not been opened.
        """
        if self._sct is None:
            raise CaptureError("FrameGrabber is not open — call open() first")

        screenshot = self._sct.grab(self._monitor)
        return np.array(screenshot)

    def __enter__(self) -> FrameGrabber:
        self.open()
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
