"""Tests for interactive region selector."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from bbs_converter.models import CaptureRegion
from bbs_converter.utils.exceptions import CaptureError


class TestSelectRegion:
    def test_returns_capture_region(self) -> None:
        expected = CaptureRegion(x=100, y=200, width=300, height=400)
        mock_app = MagicMock()
        mock_app.run.return_value = expected

        with patch(
            "bbs_converter.capture.region_selector._RegionSelectorApp",
            return_value=mock_app,
        ):
            from bbs_converter.capture.region_selector import select_region

            region = select_region()

        assert region is expected
        assert region.x == 100
        assert region.y == 200
        assert region.width == 300
        assert region.height == 400

    def test_cancel_raises(self) -> None:
        mock_app = MagicMock()
        mock_app.run.return_value = None

        with patch(
            "bbs_converter.capture.region_selector._RegionSelectorApp",
            return_value=mock_app,
        ):
            from bbs_converter.capture.region_selector import select_region

            with pytest.raises(CaptureError, match="No region selected"):
                select_region()

    def test_on_frame_callback(self) -> None:
        callback = MagicMock()
        expected = CaptureRegion(x=10, y=10, width=50, height=50)
        mock_app = MagicMock()
        mock_app.run.return_value = expected

        with patch(
            "bbs_converter.capture.region_selector._RegionSelectorApp",
            return_value=mock_app,
        ) as mock_cls:
            from bbs_converter.capture.region_selector import select_region

            select_region(on_frame=callback)

        mock_cls.assert_called_once_with(on_frame=callback)
