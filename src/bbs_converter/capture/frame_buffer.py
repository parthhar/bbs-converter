"""Thread-safe frame buffer for passing frames between threads."""

from __future__ import annotations

import queue

import numpy as np

from bbs_converter.utils.constants import DEFAULT_QUEUE_MAXSIZE


class FrameBuffer:
    """Thread-safe bounded buffer for captured frames.

    When the buffer is full, the oldest frame is discarded to make
    room for the new one (drop-oldest policy).

    Parameters
    ----------
    maxsize:
        Maximum number of frames to hold.
    """

    def __init__(self, maxsize: int = DEFAULT_QUEUE_MAXSIZE) -> None:
        self._queue: queue.Queue[np.ndarray] = queue.Queue(maxsize=maxsize)

    def put(self, frame: np.ndarray) -> None:
        """Add a frame, dropping the oldest if full."""
        try:
            self._queue.put_nowait(frame)
        except queue.Full:
            try:
                self._queue.get_nowait()
            except queue.Empty:
                pass
            self._queue.put_nowait(frame)

    def get(self, timeout: float | None = None) -> np.ndarray | None:
        """Retrieve the next frame, blocking up to *timeout* seconds.

        Returns ``None`` if no frame is available within the timeout.
        """
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    @property
    def size(self) -> int:
        """Current number of frames in the buffer."""
        return self._queue.qsize()

    @property
    def empty(self) -> bool:
        return self._queue.empty()
