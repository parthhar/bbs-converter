"""Core data models used across modules."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TableState:
    """Parsed state of the poker table from OCR output."""

    big_blind: float
    small_blind: float
    pot: float
    stacks: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class BBState:
    """Table state converted to big blind units."""

    pot_bb: float
    stacks_bb: dict[str, float] = field(default_factory=dict)
