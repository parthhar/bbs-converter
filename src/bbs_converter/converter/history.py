"""Track BB values over time for trend analysis."""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class BBSnapshot:
    """A single point-in-time record of BB values."""

    timestamp: float
    stacks_bb: dict[str, float]
    pot_bb: float


class BBHistory:
    """Rolling history of BB snapshots.

    Parameters
    ----------
    max_size:
        Maximum number of snapshots to retain.  Oldest entries are
        discarded when the limit is reached.
    """

    def __init__(self, max_size: int = 100) -> None:
        self._max_size = max_size
        self._snapshots: list[BBSnapshot] = []

    def record(self, stacks_bb: dict[str, float], pot_bb: float) -> None:
        """Append a new snapshot with the current timestamp."""
        snapshot = BBSnapshot(
            timestamp=time.monotonic(),
            stacks_bb=dict(stacks_bb),
            pot_bb=pot_bb,
        )
        self._snapshots.append(snapshot)
        if len(self._snapshots) > self._max_size:
            self._snapshots.pop(0)

    @property
    def snapshots(self) -> list[BBSnapshot]:
        """Return all stored snapshots (oldest first)."""
        return list(self._snapshots)

    @property
    def latest(self) -> BBSnapshot | None:
        """Return the most recent snapshot, or None if empty."""
        return self._snapshots[-1] if self._snapshots else None

    def __len__(self) -> int:
        return len(self._snapshots)
