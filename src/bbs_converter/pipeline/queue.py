"""Inter-stage thread-safe queues for pipeline data flow."""

from __future__ import annotations

import queue
from typing import Generic, Optional, TypeVar

from bbs_converter.utils.constants import DEFAULT_QUEUE_MAXSIZE

T = TypeVar("T")


class StageQueue(Generic[T]):
    """Thread-safe bounded queue for passing data between pipeline stages.

    Uses a drop-oldest policy when the queue is full to prevent the
    pipeline from stalling.

    Parameters
    ----------
    maxsize:
        Maximum number of items in the queue.
    name:
        Optional name for logging/debugging.
    """

    def __init__(self, maxsize: int = DEFAULT_QUEUE_MAXSIZE, name: str = "") -> None:
        self._queue: queue.Queue[T] = queue.Queue(maxsize=maxsize)
        self._name = name

    def put(self, item: T) -> None:
        """Add an item, dropping the oldest if full."""
        try:
            self._queue.put_nowait(item)
        except queue.Full:
            try:
                self._queue.get_nowait()
            except queue.Empty:
                pass
            self._queue.put_nowait(item)

    def get(self, timeout: float | None = None) -> Optional[T]:
        """Retrieve the next item, or None on timeout."""
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    @property
    def size(self) -> int:
        return self._queue.qsize()

    @property
    def empty(self) -> bool:
        return self._queue.empty()

    @property
    def name(self) -> str:
        return self._name
