"""Interactive screen region selection UI."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from bbs_converter.capture.monitor import list_monitors
from bbs_converter.models import CaptureRegion
from bbs_converter.utils.exceptions import CaptureError
from bbs_converter.utils.logger import get_logger

_log = get_logger("capture.region_selector")


def select_region(
    on_frame: Callable[[np.ndarray], None] | None = None,
) -> CaptureRegion:
    """Launch an interactive region selector.

    Captures a screenshot of the primary monitor and lets the user
    draw a rectangle using OpenCV's ``selectROI``.

    Parameters
    ----------
    on_frame:
        Optional callback invoked with the screenshot before selection.

    Returns
    -------
    CaptureRegion
        The user-selected screen region.

    Raises
    ------
    CaptureError
        If no region is selected or the selection is empty.
    """
    try:
        import cv2
        import mss
    except ImportError as exc:
        raise CaptureError(f"Missing dependency for region selector: {exc}") from exc

    monitors = list_monitors()
    primary = monitors[0]

    with mss.mss() as sct:
        monitor_dict = {
            "left": primary.left,
            "top": primary.top,
            "width": primary.width,
            "height": primary.height,
        }
        screenshot = np.array(sct.grab(monitor_dict))

    # Convert BGRA to BGR for OpenCV display
    frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    if on_frame is not None:
        on_frame(frame)

    _log.info("Opening region selector — draw a rectangle and press Enter")
    roi = cv2.selectROI("Select Capture Region", frame, fromCenter=False)
    cv2.destroyAllWindows()

    x, y, w, h = (int(v) for v in roi)
    if w == 0 or h == 0:
        raise CaptureError("No region selected (empty rectangle)")

    region = CaptureRegion(
        x=primary.left + x,
        y=primary.top + y,
        width=w,
        height=h,
    )
    _log.info("Region selected: %s", region)
    return region
