"""Tests for stack-depth color coding."""

from __future__ import annotations

from bbs_converter.overlay.colorizer import colorize_stacks, stack_color


class TestStackColor:
    def test_short_stack_red(self) -> None:
        assert stack_color(10.0) == (0, 0, 255, 255)

    def test_medium_stack_yellow(self) -> None:
        assert stack_color(35.0) == (0, 255, 255, 255)

    def test_deep_stack_green(self) -> None:
        assert stack_color(100.0) == (0, 255, 0, 255)

    def test_boundary_20bb(self) -> None:
        assert stack_color(20.0) == (0, 255, 255, 255)  # yellow

    def test_boundary_50bb(self) -> None:
        assert stack_color(50.0) == (0, 255, 255, 255)  # yellow

    def test_zero_bb(self) -> None:
        assert stack_color(0.0) == (0, 0, 255, 255)  # red


class TestColorizeStacks:
    def test_mixed_stacks(self) -> None:
        stacks = {"Short": 10.0, "Medium": 30.0, "Deep": 100.0}
        colors = colorize_stacks(stacks)
        assert colors["Short"] == (0, 0, 255, 255)
        assert colors["Medium"] == (0, 255, 255, 255)
        assert colors["Deep"] == (0, 255, 0, 255)

    def test_empty(self) -> None:
        assert colorize_stacks({}) == {}
