"""Text rendering for the overlay display."""

from __future__ import annotations

import cv2
import numpy as np

from bbs_converter.models import BBState


def render_bb_values(
    canvas: np.ndarray,
    bb_state: BBState,
    positions: dict[str, tuple[int, int]],
    font_scale: float = 0.6,
    color: tuple[int, int, int, int] = (0, 255, 0, 255),
    thickness: int = 1,
) -> None:
    """Draw BB values onto the overlay canvas.

    Parameters
    ----------
    canvas:
        BGRA canvas to draw on (modified in place).
    bb_state:
        Converted BB values.
    positions:
        Mapping of player names to (x, y) pixel coordinates.
    font_scale:
        OpenCV font scale.
    color:
        BGRA color tuple.
    thickness:
        Text stroke thickness.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX

    for name, bb_val in bb_state.stacks_bb.items():
        if name not in positions:
            continue
        x, y = positions[name]
        text = f"{bb_val:.1f}bb"
        cv2.putText(canvas, text, (x, y), font, font_scale, color, thickness)

    # Render pot BB at top-center if there's space
    if bb_state.pot_bb > 0:
        pot_text = f"Pot: {bb_state.pot_bb:.1f}bb"
        text_size = cv2.getTextSize(pot_text, font, font_scale, thickness)[0]
        px = (canvas.shape[1] - text_size[0]) // 2
        py = 25
        cv2.putText(canvas, pot_text, (px, py), font, font_scale, color, thickness)
