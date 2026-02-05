"""Live status dashboard showing FPS, confidence, and errors."""

from __future__ import annotations

import sys
import threading
from dataclasses import dataclass

from bbs_converter.utils.logger import get_logger

_log = get_logger("cli.status")


@dataclass
class PipelineStats:
    """Mutable container for live pipeline statistics."""

    capture_fps: float = 0.0
    ocr_confidence: float = 0.0
    cache_hit_rate: float = 0.0
    frames_processed: int = 0
    parse_errors: int = 0
    ocr_errors: int = 0


class StatusDashboard:
    """Live terminal status display.

    Periodically prints pipeline statistics to stderr.

    Parameters
    ----------
    stats:
        Shared PipelineStats instance updated by the pipeline.
    refresh_interval:
        Seconds between status updates.
    """

    def __init__(
        self,
        stats: PipelineStats,
        refresh_interval: float = 2.0,
    ) -> None:
        self._stats = stats
        self._interval = refresh_interval
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """Start the dashboard update thread."""
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the dashboard."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=3.0)
            self._thread = None

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def _run(self) -> None:
        """Print status updates at the configured interval."""
        while not self._stop_event.is_set():
            self._print_status()
            self._stop_event.wait(self._interval)

    def _print_status(self) -> None:
        """Print a single status line."""
        s = self._stats
        line = (
            f"[BBS] FPS: {s.capture_fps:.0f} | "
            f"OCR: {s.ocr_confidence:.0f}% | "
            f"Cache: {s.cache_hit_rate:.0f}% | "
            f"Frames: {s.frames_processed} | "
            f"Errors: parse={s.parse_errors} ocr={s.ocr_errors}"
        )
        sys.stderr.write(f"\r{line}")
        sys.stderr.flush()
