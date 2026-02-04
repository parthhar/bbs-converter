"""Tests for pot size parser."""

from __future__ import annotations

from bbs_converter.parser.pot_parser import parse_pot


class TestParsePot:
    def test_standard_format(self) -> None:
        assert parse_pot("Pot: 350") == 350.0

    def test_total_keyword(self) -> None:
        assert parse_pot("Total 1200") == 1200.0

    def test_with_dollar_sign(self) -> None:
        assert parse_pot("Pot: $500") == 500.0

    def test_with_commas(self) -> None:
        assert parse_pot("Pot: 1,200") == 1200.0

    def test_with_decimals(self) -> None:
        assert parse_pot("Pot 500.50") == 500.50

    def test_no_match(self) -> None:
        assert parse_pot("no pot info") is None

    def test_empty_text(self) -> None:
        assert parse_pot("") is None

    def test_case_insensitive(self) -> None:
        assert parse_pot("POT: 999") == 999.0
