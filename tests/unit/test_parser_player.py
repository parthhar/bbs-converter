"""Tests for player name/seat parser."""

from __future__ import annotations

from bbs_converter.parser.player_parser import parse_players


class TestParsePlayers:
    def test_single_player_with_stack(self) -> None:
        text = "Seat 3: Alice\nAlice 5000"
        players = parse_players(text)
        assert len(players) == 1
        assert players[0].name == "Alice"
        assert players[0].seat == 3
        assert players[0].stack == 5000.0

    def test_multiple_players(self) -> None:
        text = "Seat 1: Alice\nSeat 2: Bob\nAlice 5000\nBob 3200"
        players = parse_players(text)
        assert len(players) == 2
        names = {p.name for p in players}
        assert names == {"Alice", "Bob"}

    def test_seat_with_hash(self) -> None:
        text = "Seat #5: Carol\nCarol 1000"
        players = parse_players(text)
        assert len(players) == 1
        assert players[0].seat == 5

    def test_missing_stack_defaults_to_zero(self) -> None:
        text = "Seat 1: Alice"
        players = parse_players(text)
        assert len(players) == 1
        assert players[0].stack == 0.0

    def test_no_seat_info(self) -> None:
        text = "Alice 5000"
        players = parse_players(text)
        assert players == []

    def test_empty_text(self) -> None:
        assert parse_players("") == []
