"""Tests for monitor enumeration."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from bbs_converter.capture.monitor import MonitorInfo, list_monitors
from bbs_converter.utils.exceptions import CaptureError


class TestListMonitors:
    def test_returns_monitors(self) -> None:
        mock_sct = MagicMock()
        mock_sct.monitors = [
            {"left": 0, "top": 0, "width": 3840, "height": 2160},  # aggregate
            {"left": 0, "top": 0, "width": 1920, "height": 1080},  # monitor 1
            {"left": 1920, "top": 0, "width": 1920, "height": 1080},  # monitor 2
        ]
        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_sct)
        mock_ctx.__exit__ = MagicMock(return_value=False)

        with patch("bbs_converter.capture.monitor.mss.mss", return_value=mock_ctx):
            monitors = list_monitors()

        assert len(monitors) == 2
        assert monitors[0] == MonitorInfo(index=1, left=0, top=0, width=1920, height=1080)
        assert monitors[1].left == 1920

    def test_no_monitors_raises(self) -> None:
        mock_sct = MagicMock()
        mock_sct.monitors = [
            {"left": 0, "top": 0, "width": 0, "height": 0},  # aggregate only
        ]
        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_sct)
        mock_ctx.__exit__ = MagicMock(return_value=False)

        with patch("bbs_converter.capture.monitor.mss.mss", return_value=mock_ctx):
            with pytest.raises(CaptureError, match="No monitors"):
                list_monitors()

    def test_monitor_info_is_frozen(self) -> None:
        info = MonitorInfo(index=1, left=0, top=0, width=1920, height=1080)
        with pytest.raises(AttributeError):
            info.width = 800  # type: ignore[misc]
