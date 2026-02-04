"""Tests for frame grabber."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from bbs_converter.capture.grabber import FrameGrabber
from bbs_converter.models import CaptureRegion
from bbs_converter.utils.exceptions import CaptureError


class TestFrameGrabber:
    def _make_region(self) -> CaptureRegion:
        return CaptureRegion(x=0, y=0, width=100, height=100)

    def test_grab_without_open_raises(self) -> None:
        grabber = FrameGrabber(self._make_region())
        with pytest.raises(CaptureError, match="not open"):
            grabber.grab()

    def test_grab_returns_numpy_array(self) -> None:
        fake_frame = np.zeros((100, 100, 4), dtype=np.uint8)
        mock_sct = MagicMock()
        mock_sct.grab.return_value = fake_frame

        with patch("bbs_converter.capture.grabber.mss.mss", return_value=mock_sct):
            grabber = FrameGrabber(self._make_region())
            grabber.open()
            frame = grabber.grab()
            grabber.close()

        assert isinstance(frame, np.ndarray)
        assert frame.shape == (100, 100, 4)

    def test_context_manager(self) -> None:
        fake_frame = np.zeros((100, 100, 4), dtype=np.uint8)
        mock_sct = MagicMock()
        mock_sct.grab.return_value = fake_frame

        with patch("bbs_converter.capture.grabber.mss.mss", return_value=mock_sct):
            with FrameGrabber(self._make_region()) as grabber:
                frame = grabber.grab()

        assert isinstance(frame, np.ndarray)

    def test_close_releases_resources(self) -> None:
        mock_sct = MagicMock()

        with patch("bbs_converter.capture.grabber.mss.mss", return_value=mock_sct):
            grabber = FrameGrabber(self._make_region())
            grabber.open()
            grabber.close()

        mock_sct.close.assert_called_once()
