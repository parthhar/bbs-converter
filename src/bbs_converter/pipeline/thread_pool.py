"""Thread pool manager for pipeline stages."""

from __future__ import annotations

import threading
from typing import Callable

from bbs_converter.utils.logger import get_logger

_log = get_logger("pipeline.thread_pool")


class ThreadPool:
    """Manage a pool of named daemon threads for pipeline stages.

    Parameters
    ----------
    workers:
        Mapping of worker name to callable target function.
    """

    def __init__(self, workers: dict[str, Callable[[], None]]) -> None:
        self._workers = workers
        self._threads: dict[str, threading.Thread] = {}
        self._stop_event = threading.Event()

    def start(self) -> None:
        """Start all worker threads."""
        self._stop_event.clear()
        for name, target in self._workers.items():
            thread = threading.Thread(target=target, name=name, daemon=True)
            self._threads[name] = thread
            thread.start()
            _log.info("Started worker thread: %s", name)

    def stop(self, timeout: float = 5.0) -> None:
        """Signal stop and join all threads."""
        self._stop_event.set()
        for name, thread in self._threads.items():
            thread.join(timeout=timeout)
            _log.info("Stopped worker thread: %s", name)
        self._threads.clear()

    @property
    def stop_event(self) -> threading.Event:
        """Return the shared stop event for workers to check."""
        return self._stop_event

    @property
    def alive_count(self) -> int:
        """Return the number of currently alive threads."""
        return sum(1 for t in self._threads.values() if t.is_alive())

    @property
    def worker_names(self) -> list[str]:
        return list(self._workers.keys())
