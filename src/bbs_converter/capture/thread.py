"""Capture thread lifecycle manager."""

from __future__ import annotations

import threading

from bbs_converter.capture.fps_controller import FPSController
from bbs_converter.capture.frame_buffer import FrameBuffer
from bbs_converter.capture.grabber import FrameGrabber
from bbs_converter.models import CaptureRegion
from bbs_converter.utils.logger import get_logger

_log = get_logger("capture.thread")


class CaptureThread:
    """Manages a background thread that continuously captures frames.

    Parameters
    ----------
    region:
        Screen region to capture.
    buffer:
        Thread-safe buffer to push frames into.
    fps:
        Target capture frame rate.
    """

    def __init__(
        self,
        region: CaptureRegion,
        buffer: FrameBuffer,
        fps: int = 30,
    ) -> None:
        self._region = region
        self._buffer = buffer
        self._fps_ctrl = FPSController(target_fps=fps)
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """Start the capture thread."""
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        _log.info("Capture thread started (target %d FPS)", self._fps_ctrl.target_fps)

    def stop(self, timeout: float = 2.0) -> None:
        """Signal the capture thread to stop and wait for it."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=timeout)
            self._thread = None
        _log.info("Capture thread stopped")

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    @property
    def actual_fps(self) -> float:
        return self._fps_ctrl.actual_fps

    def _run(self) -> None:
        """Main capture loop executed on the background thread."""
        with FrameGrabber(self._region) as grabber:
            while not self._stop_event.is_set():
                frame = grabber.grab()
                self._buffer.put(frame)
                self._fps_ctrl.tick()
