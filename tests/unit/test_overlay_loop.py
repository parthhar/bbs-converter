"""Tests for overlay refresh loop."""

from __future__ import annotations

import sys
import time
from unittest.mock import MagicMock, patch

from bbs_converter.models import BBState, CaptureRegion


class TestOverlayLoop:
    def _make_region(self) -> CaptureRegion:
        return CaptureRegion(x=0, y=0, width=400, height=300)

    def test_start_and_stop(self) -> None:
        cv2_mock = MagicMock()
        cv2_mock.WINDOW_NORMAL = 0
        cv2_mock.WND_PROP_TOPMOST = 5
        cv2_mock.FONT_HERSHEY_SIMPLEX = 0
        cv2_mock.getTextSize.return_value = ((100, 20), 5)

        state = BBState(pot_bb=3.5, stacks_bb={"Alice": 50.0})
        get_state = MagicMock(return_value=state)

        with patch.dict(sys.modules, {"cv2": cv2_mock}):
            from bbs_converter.overlay.loop import OverlayLoop
            loop = OverlayLoop(self._make_region(), get_state, refresh_hz=100)
            loop.start()
            assert loop.running is True
            time.sleep(0.05)
            loop.stop()
            assert loop.running is False

    def test_calls_get_state(self) -> None:
        cv2_mock = MagicMock()
        cv2_mock.WINDOW_NORMAL = 0
        cv2_mock.WND_PROP_TOPMOST = 5
        cv2_mock.FONT_HERSHEY_SIMPLEX = 0
        cv2_mock.getTextSize.return_value = ((100, 20), 5)

        get_state = MagicMock(return_value=None)

        with patch.dict(sys.modules, {"cv2": cv2_mock}):
            from bbs_converter.overlay.loop import OverlayLoop
            loop = OverlayLoop(self._make_region(), get_state, refresh_hz=100)
            loop.start()
            time.sleep(0.05)
            loop.stop()

        assert get_state.call_count > 0

    def test_handles_none_state(self) -> None:
        cv2_mock = MagicMock()
        cv2_mock.WINDOW_NORMAL = 0
        cv2_mock.WND_PROP_TOPMOST = 5

        get_state = MagicMock(return_value=None)

        with patch.dict(sys.modules, {"cv2": cv2_mock}):
            from bbs_converter.overlay.loop import OverlayLoop
            loop = OverlayLoop(self._make_region(), get_state, refresh_hz=100)
            loop.start()
            time.sleep(0.03)
            loop.stop()
            # Should not crash when state is None
