"""Tests for pipeline orchestrator."""

from __future__ import annotations

import sys
import time
from unittest.mock import MagicMock, patch

import numpy as np

from bbs_converter.models import BBState, CaptureRegion


class TestPipelineOrchestrator:
    def _make_region(self) -> CaptureRegion:
        return CaptureRegion(x=0, y=0, width=100, height=100)

    def test_start_and_stop(self) -> None:
        cv2_mock = MagicMock()
        cv2_mock.WINDOW_NORMAL = 0
        cv2_mock.WND_PROP_TOPMOST = 5
        cv2_mock.FONT_HERSHEY_SIMPLEX = 0
        cv2_mock.getTextSize.return_value = ((100, 20), 5)

        fake_frame = np.zeros((100, 100, 4), dtype=np.uint8)
        mock_grabber = MagicMock()
        mock_grabber.grab.return_value = fake_frame
        mock_grabber.__enter__ = MagicMock(return_value=mock_grabber)
        mock_grabber.__exit__ = MagicMock(return_value=False)

        with patch.dict(sys.modules, {"cv2": cv2_mock}):
            with patch("bbs_converter.capture.thread.FrameGrabber", return_value=mock_grabber):
                from bbs_converter.pipeline.orchestrator import PipelineOrchestrator
                orch = PipelineOrchestrator(self._make_region(), fps=100)
                orch.start()
                assert orch.running is True
                time.sleep(0.1)
                orch.stop()
                assert orch.running is False

    def test_get_latest_state_initially_none(self) -> None:
        from bbs_converter.pipeline.orchestrator import PipelineOrchestrator
        orch = PipelineOrchestrator(self._make_region())
        assert orch._get_latest_state() is None

    def test_state_updates_thread_safe(self) -> None:
        from bbs_converter.pipeline.orchestrator import PipelineOrchestrator
        orch = PipelineOrchestrator(self._make_region())
        state = BBState(pot_bb=3.5, stacks_bb={"A": 50.0})
        with orch._state_lock:
            orch._latest_state = state
        assert orch._get_latest_state() == state
