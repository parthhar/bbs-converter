"""Color-code BB values by stack depth."""

from __future__ import annotations


def stack_color(bb_value: float) -> tuple[int, int, int, int]:
    """Return a BGRA color based on stack depth in big blinds.

    - < 20 BB: red (short stack, danger)
    - 20-50 BB: yellow (medium stack)
    - > 50 BB: green (deep stack)

    Parameters
    ----------
    bb_value:
        Stack size in big blinds.

    Returns
    -------
    tuple
        BGRA color tuple.
    """
    if bb_value < 20:
        return (0, 0, 255, 255)     # red
    if bb_value <= 50:
        return (0, 255, 255, 255)   # yellow
    return (0, 255, 0, 255)         # green


def colorize_stacks(
    stacks_bb: dict[str, float],
) -> dict[str, tuple[int, int, int, int]]:
    """Assign colors to each player based on their stack depth.

    Parameters
    ----------
    stacks_bb:
        Player name to BB value mapping.

    Returns
    -------
    dict
        Player name to BGRA color mapping.
    """
    return {name: stack_color(bb) for name, bb in stacks_bb.items()}
