"""Tests for core chip-to-BB conversion."""

from __future__ import annotations

import pytest

from bbs_converter.converter.core import chips_to_bb
from bbs_converter.utils.exceptions import ConversionError


class TestChipsToBB:
    def test_exact_division(self) -> None:
        assert chips_to_bb(1000.0, 100.0) == 10.0

    def test_fractional_result(self) -> None:
        result = chips_to_bb(250.0, 100.0)
        assert result == pytest.approx(2.5)

    def test_small_stack(self) -> None:
        assert chips_to_bb(50.0, 100.0) == pytest.approx(0.5)

    def test_large_stack(self) -> None:
        assert chips_to_bb(50000.0, 100.0) == 500.0

    def test_zero_chips(self) -> None:
        assert chips_to_bb(0.0, 100.0) == 0.0

    def test_zero_big_blind_raises(self) -> None:
        with pytest.raises(ConversionError, match="positive"):
            chips_to_bb(1000.0, 0.0)

    def test_negative_big_blind_raises(self) -> None:
        with pytest.raises(ConversionError, match="positive"):
            chips_to_bb(1000.0, -50.0)
