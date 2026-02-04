"""Batch conversion of multi-player chip stacks to BB units."""

from __future__ import annotations

from bbs_converter.converter.core import chips_to_bb
from bbs_converter.models import BBState, TableState


def convert_table(state: TableState) -> BBState:
    """Convert all chip values in a TableState to big blind units.

    Parameters
    ----------
    state:
        Parsed table state with chip values.

    Returns
    -------
    BBState
        All values expressed in big blinds.  Returns zeroed-out
        BBState when big_blind is zero (e.g. between hands).
    """
    if state.big_blind <= 0:
        return BBState(
            pot_bb=0.0,
            stacks_bb={name: 0.0 for name in state.stacks},
        )

    pot_bb = chips_to_bb(state.pot, state.big_blind)
    stacks_bb = {
        name: chips_to_bb(stack, state.big_blind)
        for name, stack in state.stacks.items()
    }
    return BBState(pot_bb=pot_bb, stacks_bb=stacks_bb)
