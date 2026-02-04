"""Map player positions to overlay coordinates."""

from __future__ import annotations

from bbs_converter.models import CaptureRegion


def compute_positions(
    region: CaptureRegion,
    player_names: list[str],
    max_seats: int = 9,
) -> dict[str, tuple[int, int]]:
    """Compute overlay pixel positions for each player.

    Distributes player labels vertically within the capture region,
    with a left margin offset.

    Parameters
    ----------
    region:
        The overlay display region.
    player_names:
        Ordered list of player names.
    max_seats:
        Maximum number of seat slots to allocate space for.

    Returns
    -------
    dict
        Mapping of player name to ``(x, y)`` pixel coordinates
        relative to the overlay canvas.
    """
    if not player_names:
        return {}

    slot_count = max(len(player_names), 1)
    slot_height = region.height // (slot_count + 1)
    x_offset = 10

    positions: dict[str, tuple[int, int]] = {}
    for i, name in enumerate(player_names):
        y = slot_height * (i + 1)
        positions[name] = (x_offset, y)

    return positions
