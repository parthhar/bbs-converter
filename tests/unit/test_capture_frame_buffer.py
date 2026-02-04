"""Tests for thread-safe frame buffer."""

from __future__ import annotations

import numpy as np

from bbs_converter.capture.frame_buffer import FrameBuffer


class TestFrameBuffer:
    def _frame(self, value: int = 0) -> np.ndarray:
        f = np.zeros((10, 10, 4), dtype=np.uint8)
        f[0, 0, 0] = value
        return f

    def test_put_and_get(self) -> None:
        buf = FrameBuffer(maxsize=5)
        frame = self._frame(42)
        buf.put(frame)
        result = buf.get(timeout=1.0)
        assert result is not None
        assert result[0, 0, 0] == 42

    def test_empty_get_returns_none(self) -> None:
        buf = FrameBuffer(maxsize=5)
        assert buf.get(timeout=0.01) is None

    def test_drop_oldest_when_full(self) -> None:
        buf = FrameBuffer(maxsize=2)
        buf.put(self._frame(1))
        buf.put(self._frame(2))
        buf.put(self._frame(3))  # should drop frame 1
        assert buf.size == 2
        first = buf.get(timeout=1.0)
        assert first is not None
        assert first[0, 0, 0] == 2

    def test_size_property(self) -> None:
        buf = FrameBuffer(maxsize=10)
        assert buf.size == 0
        buf.put(self._frame())
        assert buf.size == 1

    def test_empty_property(self) -> None:
        buf = FrameBuffer(maxsize=10)
        assert buf.empty is True
        buf.put(self._frame())
        assert buf.empty is False
