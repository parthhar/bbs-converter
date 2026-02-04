"""Tests for the performance timer decorator."""

from __future__ import annotations

import logging

from bbs_converter.utils.timer import timed


class TestTimed:
    def test_returns_original_value(self) -> None:
        @timed
        def add(a: int, b: int) -> int:
            return a + b

        assert add(2, 3) == 5

    def test_preserves_function_name(self) -> None:
        @timed
        def my_func() -> None:
            pass

        assert my_func.__name__ == "my_func"

    def test_logs_duration(self, caplog: logging.LogCaptureFixture) -> None:
        @timed
        def noop() -> None:
            pass

        with caplog.at_level(logging.DEBUG, logger="bbs_converter.timer"):
            noop()

        assert any("noop" in record.message and "ms" in record.message for record in caplog.records)

    def test_propagates_exceptions(self) -> None:
        @timed
        def fail() -> None:
            raise ValueError("boom")

        try:
            fail()
        except ValueError as exc:
            assert str(exc) == "boom"
        else:
            raise AssertionError("Expected ValueError")
