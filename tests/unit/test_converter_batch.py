"""Tests for batch multi-player conversion."""

from __future__ import annotations

import pytest

from bbs_converter.converter.batch import convert_table
from bbs_converter.models import TableState


class TestConvertTable:
    def test_converts_pot_and_stacks(self) -> None:
        state = TableState(
            big_blind=100.0,
            small_blind=50.0,
            pot=350.0,
            stacks={"Alice": 5000.0, "Bob": 3200.0},
        )
        result = convert_table(state)
        assert result.pot_bb == pytest.approx(3.5)
        assert result.stacks_bb["Alice"] == pytest.approx(50.0)
        assert result.stacks_bb["Bob"] == pytest.approx(32.0)

    def test_empty_stacks(self) -> None:
        state = TableState(big_blind=100.0, small_blind=50.0, pot=0.0)
        result = convert_table(state)
        assert result.pot_bb == 0.0
        assert result.stacks_bb == {}

    def test_single_player(self) -> None:
        state = TableState(
            big_blind=200.0,
            small_blind=100.0,
            pot=600.0,
            stacks={"Solo": 10000.0},
        )
        result = convert_table(state)
        assert result.pot_bb == pytest.approx(3.0)
        assert result.stacks_bb["Solo"] == pytest.approx(50.0)

    def test_zero_big_blind_returns_zeroed_state(self) -> None:
        """Regression: zero BB between hands must not crash."""
        state = TableState(
            big_blind=0.0,
            small_blind=0.0,
            pot=500.0,
            stacks={"Alice": 3000.0},
        )
        result = convert_table(state)
        assert result.pot_bb == 0.0
        assert result.stacks_bb["Alice"] == 0.0
