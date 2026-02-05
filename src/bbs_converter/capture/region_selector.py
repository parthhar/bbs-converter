"""Interactive screen region selection UI.

Uses tkinter for the initial control dialog and OpenCV for the
screenshot display / rectangle selection (works reliably on macOS
Retina with the system Python's Tk 8.5).
"""

from __future__ import annotations

import os
import subprocess
import tempfile
import time
import tkinter as tk
from collections.abc import Callable

import cv2
import numpy as np
from PIL import Image

from bbs_converter.capture.monitor import list_monitors
from bbs_converter.models import CaptureRegion
from bbs_converter.utils.exceptions import CaptureError
from bbs_converter.utils.logger import get_logger

_log = get_logger("capture.region_selector")

_KEY_ENTER = 13
_KEY_R = ord("r")
_KEY_ESC = 27
_WINDOW_NAME = "BBS Converter"


def _capture_screenshot() -> tuple[np.ndarray, float]:
    """Take a screenshot and return (BGR image, retina_scale).

    Uses macOS ``screencapture`` for reliable capture, falling back to
    ``mss`` on other platforms.
    """
    monitors = list_monitors()
    primary = monitors[0]

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        subprocess.run(["screencapture", "-x", tmp_path], check=True)
        pil_img = Image.open(tmp_path)
        rgb = np.array(pil_img.convert("RGB"))
    finally:
        os.unlink(tmp_path)

    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    retina_scale = bgr.shape[1] / primary.width

    _log.info(
        "Captured %dx%d (retina_scale=%.1fx, logical=%dx%d)",
        bgr.shape[1], bgr.shape[0],
        retina_scale, primary.width, primary.height,
    )

    return bgr, retina_scale


def _select_roi_cv2(
    screenshot_bgr: np.ndarray, retina_scale: float,
) -> tuple[int, int, int, int] | str:
    """Show *screenshot_bgr* fullscreen and let the user draw a ROI.

    Keybinds:
        ENTER  — confirm selection
        R      — retake screenshot
        ESC    — cancel

    Returns ``(x, y, w, h)`` in the **screenshot image** pixel space,
    or the string ``"retake"`` / ``"cancel"``.
    """
    img_h, img_w = screenshot_bgr.shape[:2]

    # State shared with mouse callback
    state: dict = {
        "drawing": False,
        "x1": 0, "y1": 0, "x2": 0, "y2": 0,
        "has_rect": False,
    }

    def _mouse_cb(event: int, x: int, y: int, _f: int, _p: object) -> None:
        if event == cv2.EVENT_LBUTTONDOWN:
            state["drawing"] = True
            state["x1"] = x
            state["y1"] = y
            state["x2"] = x
            state["y2"] = y
            state["has_rect"] = False
        elif event == cv2.EVENT_MOUSEMOVE and state["drawing"]:
            state["x2"] = x
            state["y2"] = y
        elif event == cv2.EVENT_LBUTTONUP:
            state["drawing"] = False
            state["x2"] = x
            state["y2"] = y
            w = abs(state["x2"] - state["x1"])
            h = abs(state["y2"] - state["y1"])
            state["has_rect"] = w > 2 and h > 2

    # Fullscreen window
    cv2.namedWindow(_WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        _WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN,
    )
    cv2.setMouseCallback(_WINDOW_NAME, _mouse_cb)

    # Get screen size for scaling (use the display image at screen res)
    # We read it from the fullscreen window after setting it up
    screen_w, screen_h = img_w, img_h
    try:
        rect = cv2.getWindowImageRect(_WINDOW_NAME)
        if rect[2] > 0 and rect[3] > 0:
            screen_w, screen_h = rect[2], rect[3]
    except cv2.error:
        pass

    scale = min(screen_w / img_w, screen_h / img_h, 1.0)
    disp_w = int(img_w * scale)
    disp_h = int(img_h * scale)
    display_base = cv2.resize(
        screenshot_bgr, (disp_w, disp_h), interpolation=cv2.INTER_AREA,
    )

    # Pad to full screen size (center the image)
    canvas = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)
    off_x = (screen_w - disp_w) // 2
    off_y = (screen_h - disp_h) // 2

    hint = "Drag to select region  |  ENTER: confirm  |  R: retake  |  ESC: cancel"

    result: tuple[int, int, int, int] | str = "cancel"

    while True:
        frame = canvas.copy()
        frame[off_y:off_y + disp_h, off_x:off_x + disp_w] = display_base

        # Draw selection rectangle
        if state["drawing"] or state["has_rect"]:
            cv2.rectangle(
                frame,
                (state["x1"], state["y1"]),
                (state["x2"], state["y2"]),
                (0, 255, 0), 2,
            )
            # Show dimensions in logical pixels
            rx = abs(state["x2"] - state["x1"])
            ry = abs(state["y2"] - state["y1"])
            lw = int(rx / scale / retina_scale)
            lh = int(ry / scale / retina_scale)
            dim_text = f"{lw} x {lh} px"
            tx = min(state["x1"], state["x2"])
            ty = min(state["y1"], state["y2"]) - 10
            cv2.putText(
                frame, dim_text, (tx, max(ty, 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2,
            )

        # Hint bar at bottom
        cv2.putText(
            frame, hint, (10, screen_h - 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1,
        )

        cv2.imshow(_WINDOW_NAME, frame)
        key = cv2.waitKey(16) & 0xFF

        if key == _KEY_ENTER and state["has_rect"]:
            # Map display coords → image coords (remove padding + scale)
            x1 = min(state["x1"], state["x2"]) - off_x
            y1 = min(state["y1"], state["y2"]) - off_y
            x2 = max(state["x1"], state["x2"]) - off_x
            y2 = max(state["y1"], state["y2"]) - off_y
            # Clamp to image bounds
            x1 = max(0, min(x1, disp_w))
            y1 = max(0, min(y1, disp_h))
            x2 = max(0, min(x2, disp_w))
            y2 = max(0, min(y2, disp_h))
            result = (
                int(x1 / scale), int(y1 / scale),
                int((x2 - x1) / scale), int((y2 - y1) / scale),
            )
            break
        elif key == _KEY_R:
            result = "retake"
            break
        elif key == _KEY_ESC:
            result = "cancel"
            break

    cv2.destroyWindow(_WINDOW_NAME)
    cv2.waitKey(1)
    return result


class _Phase1Dialog:
    """Tkinter dialog: 'Capture Screenshot' / 'Cancel'."""

    def __init__(self) -> None:
        self._action: str = "cancel"

        self._root = tk.Tk()
        self._root.title("BBS Converter — Region Selector")
        self._root.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self._root.geometry("420x180")
        self._root.resizable(False, False)

        # Center on screen
        self._root.update_idletasks()
        sw = self._root.winfo_screenwidth()
        sh = self._root.winfo_screenheight()
        self._root.geometry(f"+{(sw - 420) // 2}+{(sh - 180) // 2}")

        frame = tk.Frame(self._root, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(
            frame,
            text="Arrange your poker window, then click\n"
            '"Capture Screenshot" to take a snapshot.',
            justify=tk.CENTER,
            font=("Helvetica", 13),
        ).pack(pady=(0, 16))

        btn_frame = tk.Frame(frame)
        btn_frame.pack()

        tk.Button(
            btn_frame,
            text="Capture Screenshot",
            command=self._on_capture,
            width=20,
            font=("Helvetica", 12),
        ).pack(side=tk.LEFT, padx=6)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=self._on_cancel,
            width=10,
            font=("Helvetica", 12),
        ).pack(side=tk.LEFT, padx=6)

    def _on_capture(self) -> None:
        self._action = "capture"
        self._root.destroy()

    def _on_cancel(self) -> None:
        self._action = "cancel"
        self._root.destroy()

    def run(self) -> str:
        """Run the dialog and return ``'capture'`` or ``'cancel'``."""
        self._root.mainloop()
        return self._action


def select_region(
    on_frame: Callable[[np.ndarray], None] | None = None,
    delay: int = 0,
) -> CaptureRegion:
    """Launch an interactive region selector.

    Phase 1 (tkinter): control dialog with Capture / Cancel.
    Phase 2 (OpenCV):  screenshot displayed; user draws a rectangle.

    Parameters
    ----------
    on_frame:
        Optional callback invoked with the screenshot array (RGB).
    delay:
        Accepted for backwards compatibility but ignored.

    Returns
    -------
    CaptureRegion
        The user-selected screen region in logical (mss) coordinates.

    Raises
    ------
    CaptureError
        If no region is selected or the user cancels.
    """
    monitors = list_monitors()
    primary = monitors[0]

    while True:
        # --- Phase 1: prompt ---
        action = _Phase1Dialog().run()
        if action == "cancel":
            raise CaptureError("No region selected (cancelled)")

        # Small delay so the tkinter window fully disappears
        time.sleep(0.4)

        # --- Capture ---
        screenshot_bgr, retina_scale = _capture_screenshot()

        if on_frame is not None:
            rgb = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2RGB)
            on_frame(rgb)

        # --- Phase 2: ROI selection via OpenCV (fullscreen) ---
        roi = _select_roi_cv2(screenshot_bgr, retina_scale)

        if roi == "retake":
            _log.info("Retake requested, capturing again")
            continue
        if roi == "cancel":
            raise CaptureError("No region selected (cancelled)")

        img_x, img_y, img_w, img_h = roi

        # Convert Retina image pixels → logical screen coords for mss
        logical_x = int(img_x / retina_scale)
        logical_y = int(img_y / retina_scale)
        logical_w = int(img_w / retina_scale)
        logical_h = int(img_h / retina_scale)

        result = CaptureRegion(
            x=primary.left + logical_x,
            y=primary.top + logical_y,
            width=logical_w,
            height=logical_h,
        )

        _log.info("Region selected: %s", result)
        return result
