"""Validate and clean parsed values before conversion."""

from __future__ import annotations

from bbs_converter.models import TableState
from bbs_converter.utils.exceptions import ParserError

_KEYWORD_NAMES = frozenset({
    "blinds", "blind", "pot", "total", "seat", "bl",
    "dealer", "button", "fold", "check", "call", "raise", "bet",
})


def sanitize(state: TableState) -> TableState:
    """Validate and clean a parsed TableState.

    Removes stacks whose player names are actually parser keywords
    and ensures numeric values are non-negative.

    Parameters
    ----------
    state:
        Raw parsed table state.

    Returns
    -------
    TableState
        Cleaned table state.

    Raises
    ------
    ParserError
        If values are invalid (e.g. negative blinds).
    """
    if state.big_blind < 0 or state.small_blind < 0:
        raise ParserError(
            f"Negative blind values: sb={state.small_blind}, bb={state.big_blind}"
        )

    if state.pot < 0:
        raise ParserError(f"Negative pot value: {state.pot}")

    cleaned_stacks = {
        name: stack
        for name, stack in state.stacks.items()
        if name.lower() not in _KEYWORD_NAMES and stack >= 0
    }

    return TableState(
        big_blind=state.big_blind,
        small_blind=state.small_blind,
        pot=state.pot,
        stacks=cleaned_stacks,
    )
