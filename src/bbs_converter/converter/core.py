"""Core chip-to-BB conversion logic."""

from __future__ import annotations

from bbs_converter.utils.exceptions import ConversionError


def chips_to_bb(chips: float, big_blind: float) -> float:
    """Convert a chip amount to big blind units.

    Parameters
    ----------
    chips:
        The chip amount to convert.
    big_blind:
        The current big blind value.

    Returns
    -------
    float
        The chip amount expressed in big blinds.

    Raises
    ------
    ConversionError
        If *big_blind* is zero or negative.
    """
    if big_blind <= 0:
        raise ConversionError(
            f"Big blind must be positive, got {big_blind}"
        )
    return chips / big_blind
