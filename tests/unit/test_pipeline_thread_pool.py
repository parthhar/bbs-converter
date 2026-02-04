"""Tests for pipeline thread pool manager."""

from __future__ import annotations

import time
import threading

from bbs_converter.pipeline.thread_pool import ThreadPool


class TestThreadPool:
    def test_start_and_stop(self) -> None:
        ran = threading.Event()

        def worker() -> None:
            ran.set()
            while True:
                time.sleep(0.01)

        pool = ThreadPool({"w1": worker})
        pool.start()
        ran.wait(timeout=1.0)
        assert pool.alive_count == 1
        pool.stop()
        time.sleep(0.1)  # allow thread to die
        assert pool.alive_count == 0

    def test_multiple_workers(self) -> None:
        events = {"a": threading.Event(), "b": threading.Event()}

        def make_worker(name: str):
            def worker() -> None:
                events[name].set()
                while True:
                    time.sleep(0.01)
            return worker

        pool = ThreadPool({"a": make_worker("a"), "b": make_worker("b")})
        pool.start()
        events["a"].wait(timeout=1.0)
        events["b"].wait(timeout=1.0)
        assert pool.alive_count == 2
        pool.stop()

    def test_worker_names(self) -> None:
        pool = ThreadPool({"capture": lambda: None, "ocr": lambda: None})
        assert sorted(pool.worker_names) == ["capture", "ocr"]

    def test_stop_event_shared(self) -> None:
        stopped = threading.Event()

        def worker() -> None:
            pool.stop_event.wait()
            stopped.set()

        pool = ThreadPool({"w1": worker})
        pool.start()
        pool.stop()
        stopped.wait(timeout=1.0)
        assert stopped.is_set()
