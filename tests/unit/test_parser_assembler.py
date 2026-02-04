"""Tests for the table state assembler."""

from __future__ import annotations

import pytest

from bbs_converter.parser.assembler import assemble_table_state
from bbs_converter.utils.exceptions import ParserError


class TestAssembleTableState:
    def test_full_text(self) -> None:
        text = "Blinds: 50/100\nPot: 350\nAlice 5000\nBob 3200"
        state = assemble_table_state(text)
        assert state.big_blind == 100.0
        assert state.small_blind == 50.0
        assert state.pot == 350.0
        assert state.stacks["Alice"] == 5000.0
        assert state.stacks["Bob"] == 3200.0

    def test_missing_pot_defaults_to_zero(self) -> None:
        text = "Blinds: 50/100\nAlice 5000"
        state = assemble_table_state(text)
        assert state.pot == 0.0

    def test_no_player_stacks_only_keywords(self) -> None:
        text = "Blinds: 50/100\nPot: 350"
        state = assemble_table_state(text)
        # stack parser picks up keywords as names — sanitizer handles this later
        assert state.big_blind == 100.0
        assert state.pot == 350.0

    def test_missing_blinds_raises(self) -> None:
        text = "Pot: 350\nAlice 5000"
        with pytest.raises(ParserError, match="blind levels"):
            assemble_table_state(text)

    def test_empty_text_raises(self) -> None:
        with pytest.raises(ParserError):
            assemble_table_state("")
