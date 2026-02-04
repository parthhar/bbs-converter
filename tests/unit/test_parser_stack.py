"""Tests for stack parser."""

from __future__ import annotations

from bbs_converter.parser.stack_parser import parse_stacks


class TestParseStacks:
    def test_simple_stacks(self) -> None:
        text = "Alice 5000\nBob 3200"
        result = parse_stacks(text)
        assert result == {"Alice": 5000.0, "Bob": 3200.0}

    def test_with_commas(self) -> None:
        text = "Alice 5,000\nBob 3,200"
        result = parse_stacks(text)
        assert result == {"Alice": 5000.0, "Bob": 3200.0}

    def test_with_dollar_sign(self) -> None:
        text = "Alice $5000"
        result = parse_stacks(text)
        assert result == {"Alice": 5000.0}

    def test_with_colon(self) -> None:
        text = "Alice: 5000"
        result = parse_stacks(text)
        assert result == {"Alice": 5000.0}

    def test_decimal_amounts(self) -> None:
        text = "Alice 1234.56"
        result = parse_stacks(text)
        assert result == {"Alice": 1234.56}

    def test_empty_text(self) -> None:
        assert parse_stacks("") == {}

    def test_no_matches(self) -> None:
        assert parse_stacks("--- 123 ---") == {}

    def test_multiple_on_same_line(self) -> None:
        text = "Alice 5000 Bob 3200"
        result = parse_stacks(text)
        assert "Alice" in result
        assert "Bob" in result
