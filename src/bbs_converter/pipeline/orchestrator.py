"""Main pipeline orchestrator: capture → OCR → parse → convert → overlay."""

from __future__ import annotations

import threading
from typing import Optional

import numpy as np

from bbs_converter.capture.frame_buffer import FrameBuffer
from bbs_converter.capture.thread import CaptureThread
from bbs_converter.converter.batch import convert_table
from bbs_converter.models import BBState, CaptureRegion
from bbs_converter.ocr.engine import OCRResult
from bbs_converter.ocr.pipeline import OCRPipeline
from bbs_converter.overlay.loop import OverlayLoop
from bbs_converter.parser.assembler import assemble_table_state
from bbs_converter.parser.sanitizer import sanitize
from bbs_converter.utils.exceptions import ParserError, PipelineError
from bbs_converter.utils.logger import get_logger

_log = get_logger("pipeline.orchestrator")


class PipelineOrchestrator:
    """Coordinates the full processing pipeline.

    Parameters
    ----------
    region:
        Screen capture region.
    fps:
        Target capture FPS.
    confidence_threshold:
        OCR confidence threshold.
    """

    def __init__(
        self,
        region: CaptureRegion,
        fps: int = 30,
        confidence_threshold: float = 60.0,
    ) -> None:
        self._region = region
        self._frame_buffer = FrameBuffer(maxsize=30)
        self._capture = CaptureThread(region, self._frame_buffer, fps=fps)
        self._ocr = OCRPipeline(confidence_threshold=confidence_threshold)
        self._latest_state: Optional[BBState] = None
        self._state_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._process_thread: Optional[threading.Thread] = None
        self._overlay: Optional[OverlayLoop] = None

    def start(self) -> None:
        """Start all pipeline stages."""
        _log.info("Starting pipeline...")
        self._stop_event.clear()

        # Start capture thread
        self._capture.start()

        # Start processing thread
        self._process_thread = threading.Thread(
            target=self._process_loop, daemon=True
        )
        self._process_thread.start()

        # Start overlay
        self._overlay = OverlayLoop(
            self._region, self._get_latest_state, refresh_hz=15
        )
        self._overlay.start()

        _log.info("Pipeline running")

    def stop(self) -> None:
        """Stop all pipeline stages."""
        _log.info("Stopping pipeline...")
        self._stop_event.set()

        if self._overlay is not None:
            self._overlay.stop()
        if self._process_thread is not None:
            self._process_thread.join(timeout=3.0)
        self._capture.stop()

        _log.info("Pipeline stopped")

    @property
    def running(self) -> bool:
        return not self._stop_event.is_set()

    def _get_latest_state(self) -> Optional[BBState]:
        with self._state_lock:
            return self._latest_state

    def _process_loop(self) -> None:
        """Main processing loop: grab frame → OCR → parse → convert."""
        while not self._stop_event.is_set():
            frame = self._frame_buffer.get(timeout=0.1)
            if frame is None:
                continue

            # OCR
            ocr_result = self._ocr.process(frame)
            if ocr_result is None:
                continue

            # Parse
            try:
                table_state = assemble_table_state(ocr_result.text)
                table_state = sanitize(table_state)
            except ParserError:
                _log.debug("Parse failed for: %s", ocr_result.text[:80])
                continue

            # Convert
            bb_state = convert_table(table_state)

            with self._state_lock:
                self._latest_state = bb_state
