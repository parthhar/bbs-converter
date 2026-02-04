"""Tests for parsed value sanitizer."""

from __future__ import annotations

import pytest

from bbs_converter.models import TableState
from bbs_converter.parser.sanitizer import sanitize
from bbs_converter.utils.exceptions import ParserError


class TestSanitize:
    def test_removes_keyword_names(self) -> None:
        state = TableState(
            big_blind=100.0,
            small_blind=50.0,
            pot=350.0,
            stacks={"Alice": 5000.0, "Pot": 350.0, "Blinds": 50.0},
        )
        cleaned = sanitize(state)
        assert "Alice" in cleaned.stacks
        assert "Pot" not in cleaned.stacks
        assert "Blinds" not in cleaned.stacks

    def test_case_insensitive_keyword_removal(self) -> None:
        state = TableState(
            big_blind=100.0,
            small_blind=50.0,
            pot=0.0,
            stacks={"Fold": 100.0, "Bob": 2000.0},
        )
        cleaned = sanitize(state)
        assert "Fold" not in cleaned.stacks
        assert "Bob" in cleaned.stacks

    def test_drops_negative_stacks(self) -> None:
        state = TableState(
            big_blind=100.0,
            small_blind=50.0,
            pot=0.0,
            stacks={"Alice": 5000.0, "Bob": -100.0},
        )
        cleaned = sanitize(state)
        assert "Alice" in cleaned.stacks
        assert "Bob" not in cleaned.stacks

    def test_negative_big_blind_raises(self) -> None:
        state = TableState(big_blind=-100.0, small_blind=50.0, pot=0.0)
        with pytest.raises(ParserError, match="Negative blind"):
            sanitize(state)

    def test_negative_pot_raises(self) -> None:
        state = TableState(big_blind=100.0, small_blind=50.0, pot=-50.0)
        with pytest.raises(ParserError, match="Negative pot"):
            sanitize(state)

    def test_valid_state_passes_through(self) -> None:
        state = TableState(
            big_blind=100.0,
            small_blind=50.0,
            pot=350.0,
            stacks={"Alice": 5000.0},
        )
        cleaned = sanitize(state)
        assert cleaned.big_blind == 100.0
        assert cleaned.pot == 350.0
        assert cleaned.stacks == {"Alice": 5000.0}
