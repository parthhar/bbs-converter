"""Extract pot size from OCR text."""

from __future__ import annotations

import re

_POT_PATTERN = re.compile(
    r"(?:pot|total)\s*:?\s*[\$]?(?P<amount>[\d,]+(?:\.\d{1,2})?)",
    re.IGNORECASE,
)


def parse_pot(text: str) -> float | None:
    """Extract the pot size from raw OCR text.

    Looks for patterns like ``Pot: 350``, ``Total $1,200``,
    or ``Pot 500.50``.

    Parameters
    ----------
    text:
        Raw OCR output containing pot information.

    Returns
    -------
    float or None
        The pot size if found, otherwise ``None``.
    """
    match = _POT_PATTERN.search(text)
    if match is None:
        return None
    return float(match.group("amount").replace(",", ""))
