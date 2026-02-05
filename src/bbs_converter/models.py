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


@dataclass(frozen=True)
class CaptureRegion:
    """Screen region to capture, defined by top-left corner and size."""

    x: int
    y: int
    width: int
    height: int

    def to_mss_monitor(self) -> dict[str, int]:
        """Convert to the dict format expected by mss."""
        return {
            "left": self.x,
            "top": self.y,
            "width": self.width,
            "height": self.height,
        }


@dataclass(frozen=True)
class PlayerInfo:
    """Information about a single player at the table."""

    name: str
    seat: int
    stack: float


@dataclass(frozen=True)
class GameConfig:
    """Blind structure and ante configuration for the current game."""

    big_blind: float
    small_blind: float
    ante: float = 0.0
