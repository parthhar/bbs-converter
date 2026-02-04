"""Assemble sub-parser results into a unified TableState."""

from __future__ import annotations

from bbs_converter.models import TableState
from bbs_converter.parser.blind_parser import parse_blinds
from bbs_converter.parser.pot_parser import parse_pot
from bbs_converter.parser.stack_parser import parse_stacks
from bbs_converter.utils.exceptions import ParserError


def assemble_table_state(text: str) -> TableState:
    """Combine all sub-parsers to build a complete TableState.

    Parameters
    ----------
    text:
        Raw OCR output from a single frame.

    Returns
    -------
    TableState
        Fully populated table state.

    Raises
    ------
    ParserError
        If required fields (blinds) cannot be extracted.
    """
    blinds = parse_blinds(text)
    if blinds is None:
        raise ParserError("Could not extract blind levels from text")

    small_blind, big_blind = blinds
    pot = parse_pot(text) or 0.0
    stacks = parse_stacks(text)

    return TableState(
        big_blind=big_blind,
        small_blind=small_blind,
        pot=pot,
        stacks=stacks,
    )
