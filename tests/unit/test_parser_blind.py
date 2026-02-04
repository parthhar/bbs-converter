"""Tests for blind level parser."""

from __future__ import annotations

from bbs_converter.parser.blind_parser import parse_blinds


class TestParseBlinds:
    def test_standard_format(self) -> None:
        assert parse_blinds("Blinds: 50/100") == (50.0, 100.0)

    def test_abbreviated(self) -> None:
        assert parse_blinds("BL 25/50") == (25.0, 50.0)

    def test_with_dollar_signs(self) -> None:
        assert parse_blinds("Blind $100/$200") == (100.0, 200.0)

    def test_with_commas(self) -> None:
        assert parse_blinds("Blinds: 1,000/2,000") == (1000.0, 2000.0)

    def test_with_decimals(self) -> None:
        assert parse_blinds("Blinds 0.50/1.00") == (0.50, 1.00)

    def test_backslash_separator(self) -> None:
        assert parse_blinds("Blinds 50\\100") == (50.0, 100.0)

    def test_pipe_separator(self) -> None:
        assert parse_blinds("Blinds 50|100") == (50.0, 100.0)

    def test_no_match(self) -> None:
        assert parse_blinds("no blind info here") is None

    def test_empty_text(self) -> None:
        assert parse_blinds("") is None

    def test_case_insensitive(self) -> None:
        assert parse_blinds("BLINDS: 50/100") == (50.0, 100.0)
