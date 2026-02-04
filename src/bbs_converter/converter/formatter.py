"""BB value display formatting."""

from __future__ import annotations

from bbs_converter.utils.constants import (
    BB_DECIMAL_PLACES,
    COMPACT_THRESHOLD_BB,
    DisplayMode,
)


def format_bb(value: float, mode: DisplayMode = DisplayMode.DECIMAL) -> str:
    """Format a BB value for display in the overlay.

    Parameters
    ----------
    value:
        The BB value to format.
    mode:
        Display style — DECIMAL (``2.5bb``), INTEGER (``3bb``),
        or COMPACT (``100+`` for large values).
    """
    if mode == DisplayMode.COMPACT and value >= COMPACT_THRESHOLD_BB:
        return f"{int(COMPACT_THRESHOLD_BB)}+bb"

    if mode == DisplayMode.INTEGER:
        return f"{round(value)}bb"

    return f"{value:.{BB_DECIMAL_PLACES}f}bb"
