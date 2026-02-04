"""Tests for interactive region selector."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from bbs_converter.capture.monitor import MonitorInfo
from bbs_converter.models import CaptureRegion
from bbs_converter.utils.exceptions import CaptureError


def _setup_cv2_mock(roi: tuple = (100, 200, 300, 400)):
    """Create a mock cv2 module."""
    mock_cv2 = MagicMock()
    mock_cv2.cvtColor.return_value = np.zeros((1080, 1920, 3), dtype=np.uint8)
    mock_cv2.selectROI.return_value = roi
    mock_cv2.COLOR_BGRA2BGR = 0
    return mock_cv2


def _setup_mss_mock():
    """Create a mock mss module."""
    fake_screenshot = np.zeros((1080, 1920, 4), dtype=np.uint8)
    mock_sct = MagicMock()
    mock_sct.grab.return_value = fake_screenshot
    mock_mss = MagicMock()
    mock_mss.mss.return_value.__enter__ = MagicMock(return_value=mock_sct)
    mock_mss.mss.return_value.__exit__ = MagicMock(return_value=False)
    return mock_mss


class TestSelectRegion:
    def test_returns_capture_region(self) -> None:
        monitors_patch = patch(
            "bbs_converter.capture.region_selector.list_monitors",
            return_value=[MonitorInfo(index=1, left=0, top=0, width=1920, height=1080)],
        )
        cv2_mock = _setup_cv2_mock(roi=(100, 200, 300, 400))
        mss_mock = _setup_mss_mock()

        with monitors_patch, patch.dict(sys.modules, {"cv2": cv2_mock, "mss": mss_mock}):
            # Force re-import with mocked modules
            from bbs_converter.capture.region_selector import select_region
            region = select_region()

        assert isinstance(region, CaptureRegion)
        assert region.x == 100
        assert region.y == 200
        assert region.width == 300
        assert region.height == 400

    def test_empty_selection_raises(self) -> None:
        monitors_patch = patch(
            "bbs_converter.capture.region_selector.list_monitors",
            return_value=[MonitorInfo(index=1, left=0, top=0, width=1920, height=1080)],
        )
        cv2_mock = _setup_cv2_mock(roi=(100, 200, 0, 0))
        mss_mock = _setup_mss_mock()

        with monitors_patch, patch.dict(sys.modules, {"cv2": cv2_mock, "mss": mss_mock}):
            from bbs_converter.capture.region_selector import select_region
            with pytest.raises(CaptureError, match="No region selected"):
                select_region()

    def test_on_frame_callback(self) -> None:
        callback = MagicMock()
        monitors_patch = patch(
            "bbs_converter.capture.region_selector.list_monitors",
            return_value=[MonitorInfo(index=1, left=0, top=0, width=1920, height=1080)],
        )
        cv2_mock = _setup_cv2_mock(roi=(10, 10, 50, 50))
        mss_mock = _setup_mss_mock()

        with monitors_patch, patch.dict(sys.modules, {"cv2": cv2_mock, "mss": mss_mock}):
            from bbs_converter.capture.region_selector import select_region
            select_region(on_frame=callback)

        callback.assert_called_once()
