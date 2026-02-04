"""Tests for ROI extraction."""

from __future__ import annotations

import numpy as np

from bbs_converter.models import CaptureRegion
from bbs_converter.ocr.roi import extract_roi


class TestExtractROI:
    def test_basic_extraction(self) -> None:
        frame = np.arange(100 * 200, dtype=np.uint8).reshape(100, 200)
        region = CaptureRegion(x=10, y=20, width=50, height=30)
        roi = extract_roi(frame, region)
        assert roi.shape == (30, 50)

    def test_with_frame_origin(self) -> None:
        frame = np.zeros((100, 200), dtype=np.uint8)
        region = CaptureRegion(x=110, y=120, width=50, height=30)
        roi = extract_roi(frame, region, frame_origin_x=100, frame_origin_y=100)
        assert roi.shape == (30, 50)

    def test_clips_to_frame_boundary(self) -> None:
        frame = np.zeros((100, 200), dtype=np.uint8)
        # Region extends beyond frame
        region = CaptureRegion(x=180, y=80, width=50, height=50)
        roi = extract_roi(frame, region)
        assert roi.shape[1] <= 20  # clipped at width boundary
        assert roi.shape[0] <= 20  # clipped at height boundary

    def test_returns_copy(self) -> None:
        frame = np.ones((100, 200), dtype=np.uint8) * 42
        region = CaptureRegion(x=0, y=0, width=10, height=10)
        roi = extract_roi(frame, region)
        roi[:] = 0
        assert frame[0, 0] == 42  # original unchanged

    def test_multi_channel(self) -> None:
        frame = np.zeros((100, 200, 3), dtype=np.uint8)
        region = CaptureRegion(x=0, y=0, width=50, height=50)
        roi = extract_roi(frame, region)
        assert roi.shape == (50, 50, 3)
