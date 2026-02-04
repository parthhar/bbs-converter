"""Tests for overlay coordinate positioning."""

from __future__ import annotations

from bbs_converter.models import CaptureRegion
from bbs_converter.overlay.positioning import compute_positions


class TestComputePositions:
    def test_single_player(self) -> None:
        region = CaptureRegion(x=0, y=0, width=400, height=300)
        positions = compute_positions(region, ["Alice"])
        assert "Alice" in positions
        x, y = positions["Alice"]
        assert x == 10
        assert 0 < y < 300

    def test_multiple_players(self) -> None:
        region = CaptureRegion(x=0, y=0, width=400, height=300)
        positions = compute_positions(region, ["Alice", "Bob", "Carol"])
        assert len(positions) == 3
        # y values should increase
        ys = [positions[n][1] for n in ["Alice", "Bob", "Carol"]]
        assert ys == sorted(ys)

    def test_empty_players(self) -> None:
        region = CaptureRegion(x=0, y=0, width=400, height=300)
        assert compute_positions(region, []) == {}

    def test_positions_within_region(self) -> None:
        region = CaptureRegion(x=0, y=0, width=400, height=300)
        names = [f"P{i}" for i in range(6)]
        positions = compute_positions(region, names)
        for name, (x, y) in positions.items():
            assert 0 <= x < region.width
            assert 0 < y < region.height
