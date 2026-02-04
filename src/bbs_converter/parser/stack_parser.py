"""Extract player stack amounts from OCR text."""

from __future__ import annotations

import re

_STACK_PATTERN = re.compile(
    r"(?P<name>[A-Za-z]\w*)\s*[\$:]?\s*(?P<amount>[\d,]+(?:\.\d{1,2})?)",
)


def parse_stacks(text: str) -> dict[str, float]:
    """Extract player-name → chip-stack mappings from raw OCR text.

    Looks for patterns like ``Alice 5,000``, ``Bob: $3200``,
    or ``Carol 1234.56``.

    Parameters
    ----------
    text:
        Raw OCR output containing player stack information.

    Returns
    -------
    dict
        Mapping of player names to chip amounts.
    """
    stacks: dict[str, float] = {}
    for match in _STACK_PATTERN.finditer(text):
        name = match.group("name")
        raw_amount = match.group("amount").replace(",", "")
        stacks[name] = float(raw_amount)
    return stacks
