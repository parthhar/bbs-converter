"""Tests for overlay window lifecycle."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from bbs_converter.models import CaptureRegion
from bbs_converter.utils.exceptions import OverlayError


class TestOverlayWindow:
    def _make_region(self) -> CaptureRegion:
        return CaptureRegion(x=100, y=200, width=400, height=300)

    def _mock_cv2(self) -> MagicMock:
        mock = MagicMock()
        mock.WINDOW_NORMAL = 0
        mock.WND_PROP_TOPMOST = 5
        return mock

    def test_open_creates_canvas(self) -> None:
        cv2_mock = self._mock_cv2()
        with patch.dict(sys.modules, {"cv2": cv2_mock}):
            from bbs_converter.overlay.window import OverlayWindow
            win = OverlayWindow(self._make_region())
            win.open()
            assert win.is_open is True
            assert win.canvas.shape == (300, 400, 4)
            win.close()

    def test_close_sets_not_open(self) -> None:
        cv2_mock = self._mock_cv2()
        with patch.dict(sys.modules, {"cv2": cv2_mock}):
            from bbs_converter.overlay.window import OverlayWindow
            win = OverlayWindow(self._make_region())
            win.open()
            win.close()
            assert win.is_open is False

    def test_canvas_before_open_raises(self) -> None:
        from bbs_converter.overlay.window import OverlayWindow
        win = OverlayWindow(self._make_region())
        with pytest.raises(OverlayError, match="not open"):
            _ = win.canvas

    def test_clear_resets_canvas(self) -> None:
        cv2_mock = self._mock_cv2()
        with patch.dict(sys.modules, {"cv2": cv2_mock}):
            from bbs_converter.overlay.window import OverlayWindow
            win = OverlayWindow(self._make_region())
            win.open()
            win.canvas[10, 10] = [255, 255, 255, 255]
            win.clear()
            assert np.all(win.canvas == 0)
            win.close()

    def test_context_manager(self) -> None:
        cv2_mock = self._mock_cv2()
        with patch.dict(sys.modules, {"cv2": cv2_mock}):
            from bbs_converter.overlay.window import OverlayWindow
            with OverlayWindow(self._make_region()) as win:
                assert win.is_open is True
            assert win.is_open is False
