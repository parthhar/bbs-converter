"""Tests for overlay text renderer."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np

from bbs_converter.models import BBState
from bbs_converter.overlay.renderer import render_bb_values


class TestRenderBBValues:
    def test_renders_player_stacks(self) -> None:
        cv2_mock = MagicMock()
        cv2_mock.FONT_HERSHEY_SIMPLEX = 0
        cv2_mock.getTextSize.return_value = ((100, 20), 5)

        with patch("bbs_converter.overlay.renderer.cv2", cv2_mock):
            canvas = np.zeros((300, 400, 4), dtype=np.uint8)
            bb_state = BBState(pot_bb=3.5, stacks_bb={"Alice": 50.0, "Bob": 32.0})
            positions = {"Alice": (10, 100), "Bob": (10, 200)}
            render_bb_values(canvas, bb_state, positions)

        # putText called for Alice, Bob, and pot
        assert cv2_mock.putText.call_count == 3

    def test_skips_missing_positions(self) -> None:
        cv2_mock = MagicMock()
        cv2_mock.FONT_HERSHEY_SIMPLEX = 0
        cv2_mock.getTextSize.return_value = ((100, 20), 5)

        with patch("bbs_converter.overlay.renderer.cv2", cv2_mock):
            canvas = np.zeros((300, 400, 4), dtype=np.uint8)
            bb_state = BBState(pot_bb=0.0, stacks_bb={"Alice": 50.0})
            positions = {}  # no positions
            render_bb_values(canvas, bb_state, positions)

        assert cv2_mock.putText.call_count == 0

    def test_renders_pot_when_positive(self) -> None:
        cv2_mock = MagicMock()
        cv2_mock.FONT_HERSHEY_SIMPLEX = 0
        cv2_mock.getTextSize.return_value = ((100, 20), 5)

        with patch("bbs_converter.overlay.renderer.cv2", cv2_mock):
            canvas = np.zeros((300, 400, 4), dtype=np.uint8)
            bb_state = BBState(pot_bb=5.0, stacks_bb={})
            render_bb_values(canvas, bb_state, {})

        assert cv2_mock.putText.call_count == 1  # pot only
