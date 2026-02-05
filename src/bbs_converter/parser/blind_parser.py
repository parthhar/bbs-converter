"""Extract blind levels from OCR text."""

from __future__ import annotations

import re

_BLIND_PATTERN = re.compile(
    r"(?:blinds?|bl)\s*:?\s*"
    r"[\$]?(?P<sb>[\d,]+(?:\.\d{1,2})?)"
    r"\s*[/\\|]\s*"
    r"[\$]?(?P<bb>[\d,]+(?:\.\d{1,2})?)",
    re.IGNORECASE,
)


def parse_blinds(text: str) -> tuple[float, float] | None:
    """Extract small blind and big blind from raw OCR text.

    Looks for patterns like ``Blinds: 50/100``, ``BL 25/50``,
    or ``Blind $100/$200``.

    Parameters
    ----------
    text:
        Raw OCR output containing blind level information.

    Returns
    -------
    tuple or None
        ``(small_blind, big_blind)`` if found, otherwise ``None``.
    """
    match = _BLIND_PATTERN.search(text)
    if match is None:
        return None
    sb = float(match.group("sb").replace(",", ""))
    bb = float(match.group("bb").replace(",", ""))
    return (sb, bb)
