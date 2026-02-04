"""Transparent always-on-top overlay window."""

from __future__ import annotations

from typing import Optional

import numpy as np

from bbs_converter.models import CaptureRegion
from bbs_converter.utils.exceptions import OverlayError
from bbs_converter.utils.logger import get_logger

_log = get_logger("overlay.window")

_WINDOW_NAME = "BBS Converter Overlay"


class OverlayWindow:
    """Transparent always-on-top window for displaying BB values.

    Parameters
    ----------
    region:
        Screen region the window covers (matches the capture region).
    """

    def __init__(self, region: CaptureRegion) -> None:
        self._region = region
        self._canvas: Optional[np.ndarray] = None
        self._open = False

    def open(self) -> None:
        """Create and configure the overlay window."""
        try:
            import cv2
        except ImportError as exc:
            raise OverlayError("OpenCV is required for the overlay") from exc

        cv2.namedWindow(_WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(
            _WINDOW_NAME, cv2.WND_PROP_TOPMOST, 1
        )
        cv2.resizeWindow(_WINDOW_NAME, self._region.width, self._region.height)
        cv2.moveWindow(_WINDOW_NAME, self._region.x, self._region.y)

        # Create transparent canvas (BGRA)
        self._canvas = np.zeros(
            (self._region.height, self._region.width, 4),
            dtype=np.uint8,
        )
        self._open = True
        _log.info("Overlay window opened at (%d, %d)", self._region.x, self._region.y)

    def close(self) -> None:
        """Destroy the overlay window."""
        if self._open:
            try:
                import cv2
                cv2.destroyWindow(_WINDOW_NAME)
            except Exception:
                pass
            self._open = False
            _log.info("Overlay window closed")

    @property
    def canvas(self) -> np.ndarray:
        """Return the current canvas for drawing."""
        if self._canvas is None:
            raise OverlayError("Window not open — call open() first")
        return self._canvas

    def clear(self) -> None:
        """Reset the canvas to fully transparent."""
        if self._canvas is not None:
            self._canvas[:] = 0

    def show(self) -> None:
        """Display the current canvas contents."""
        if not self._open or self._canvas is None:
            return
        import cv2
        cv2.imshow(_WINDOW_NAME, self._canvas)
        cv2.waitKey(1)

    @property
    def is_open(self) -> bool:
        return self._open

    def __enter__(self) -> OverlayWindow:
        self.open()
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
