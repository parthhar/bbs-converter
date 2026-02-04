"""Tests for BB display formatter."""

from __future__ import annotations

from bbs_converter.converter.formatter import format_bb
from bbs_converter.utils.constants import DisplayMode


class TestFormatBB:
    def test_decimal_mode(self) -> None:
        assert format_bb(2.5) == "2.5bb"

    def test_decimal_mode_whole_number(self) -> None:
        assert format_bb(10.0) == "10.0bb"

    def test_integer_mode(self) -> None:
        assert format_bb(2.5, DisplayMode.INTEGER) == "2bb"

    def test_integer_mode_rounds_up(self) -> None:
        assert format_bb(2.6, DisplayMode.INTEGER) == "3bb"

    def test_compact_mode_below_threshold(self) -> None:
        assert format_bb(50.0, DisplayMode.COMPACT) == "50.0bb"

    def test_compact_mode_at_threshold(self) -> None:
        assert format_bb(100.0, DisplayMode.COMPACT) == "100+bb"

    def test_compact_mode_above_threshold(self) -> None:
        assert format_bb(250.0, DisplayMode.COMPACT) == "100+bb"

    def test_zero_value(self) -> None:
        assert format_bb(0.0) == "0.0bb"
