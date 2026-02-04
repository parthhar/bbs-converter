"""Tests for capture thread lifecycle."""

from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import numpy as np

from bbs_converter.capture.frame_buffer import FrameBuffer
from bbs_converter.capture.thread import CaptureThread
from bbs_converter.models import CaptureRegion


class TestCaptureThread:
    def _make_region(self) -> CaptureRegion:
        return CaptureRegion(x=0, y=0, width=100, height=100)

    def _mock_grabber(self) -> MagicMock:
        fake_frame = np.zeros((100, 100, 4), dtype=np.uint8)
        mock = MagicMock()
        mock.grab.return_value = fake_frame
        mock.__enter__ = MagicMock(return_value=mock)
        mock.__exit__ = MagicMock(return_value=False)
        return mock

    def test_start_and_stop(self) -> None:
        buf = FrameBuffer(maxsize=5)
        with patch("bbs_converter.capture.thread.FrameGrabber", return_value=self._mock_grabber()):
            ct = CaptureThread(self._make_region(), buf, fps=100)
            ct.start()
            assert ct.running is True
            time.sleep(0.05)
            ct.stop()
            assert ct.running is False

    def test_produces_frames(self) -> None:
        buf = FrameBuffer(maxsize=10)
        with patch("bbs_converter.capture.thread.FrameGrabber", return_value=self._mock_grabber()):
            ct = CaptureThread(self._make_region(), buf, fps=100)
            ct.start()
            time.sleep(0.1)
            ct.stop()
        assert buf.size > 0

    def test_double_start_is_safe(self) -> None:
        buf = FrameBuffer(maxsize=5)
        with patch("bbs_converter.capture.thread.FrameGrabber", return_value=self._mock_grabber()):
            ct = CaptureThread(self._make_region(), buf, fps=100)
            ct.start()
            ct.start()  # should not create a second thread
            assert ct.running is True
            ct.stop()

    def test_stop_before_start_is_safe(self) -> None:
        buf = FrameBuffer(maxsize=5)
        ct = CaptureThread(self._make_region(), buf, fps=30)
        ct.stop()  # should not raise
        assert ct.running is False
