"""Extract player names and seat numbers from OCR text."""

from __future__ import annotations

import re

from bbs_converter.models import PlayerInfo
from bbs_converter.parser.stack_parser import parse_stacks

_SEAT_PATTERN = re.compile(
    r"[Ss]eat\s*#?(?P<seat>\d+)\s*:?\s*(?P<name>[A-Za-z]\w*)",
)


def parse_players(text: str) -> list[PlayerInfo]:
    """Extract player information from raw OCR text.

    Combines seat assignments (``Seat 3: Alice``) with stack amounts
    extracted by the stack parser to produce full PlayerInfo records.

    Parameters
    ----------
    text:
        Raw OCR output containing player and stack information.

    Returns
    -------
    list
        PlayerInfo records for each matched player.
    """
    stacks = parse_stacks(text)
    players: list[PlayerInfo] = []

    for match in _SEAT_PATTERN.finditer(text):
        seat = int(match.group("seat"))
        name = match.group("name")
        stack = stacks.get(name, 0.0)
        players.append(PlayerInfo(name=name, seat=seat, stack=stack))

    return players
