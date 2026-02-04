"""Tests for inter-stage pipeline queues."""

from __future__ import annotations

from bbs_converter.pipeline.queue import StageQueue


class TestStageQueue:
    def test_put_and_get(self) -> None:
        q: StageQueue[str] = StageQueue(maxsize=5, name="test")
        q.put("hello")
        assert q.get(timeout=1.0) == "hello"

    def test_empty_get_returns_none(self) -> None:
        q: StageQueue[int] = StageQueue(maxsize=5)
        assert q.get(timeout=0.01) is None

    def test_drop_oldest_when_full(self) -> None:
        q: StageQueue[int] = StageQueue(maxsize=2)
        q.put(1)
        q.put(2)
        q.put(3)  # should drop 1
        assert q.size == 2
        assert q.get(timeout=0.1) == 2

    def test_size_and_empty(self) -> None:
        q: StageQueue[int] = StageQueue(maxsize=10)
        assert q.empty is True
        assert q.size == 0
        q.put(42)
        assert q.empty is False
        assert q.size == 1

    def test_name_property(self) -> None:
        q: StageQueue[int] = StageQueue(name="ocr_output")
        assert q.name == "ocr_output"
