"""Tests for error recovery with retry."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from bbs_converter.pipeline.recovery import retry
from bbs_converter.utils.exceptions import PipelineError


class TestRetry:
    def test_succeeds_on_first_attempt(self) -> None:
        func = MagicMock(return_value=42)
        assert retry(func, max_attempts=3, delay=0) == 42
        assert func.call_count == 1

    def test_succeeds_after_retry(self) -> None:
        func = MagicMock(side_effect=[ValueError("fail"), 42])
        assert retry(func, max_attempts=3, delay=0) == 42
        assert func.call_count == 2

    def test_all_attempts_fail_raises(self) -> None:
        func = MagicMock(side_effect=ValueError("always fails"))
        with pytest.raises(PipelineError, match="All 3 attempts failed"):
            retry(func, max_attempts=3, delay=0)
        assert func.call_count == 3

    def test_on_error_callback(self) -> None:
        func = MagicMock(side_effect=[ValueError("err"), 42])
        on_error = MagicMock()
        retry(func, max_attempts=3, delay=0, on_error=on_error)
        on_error.assert_called_once()
        args = on_error.call_args[0]
        assert isinstance(args[0], ValueError)
        assert args[1] == 1  # first attempt

    def test_wraps_last_exception(self) -> None:
        func = MagicMock(side_effect=RuntimeError("boom"))
        with pytest.raises(PipelineError) as exc_info:
            retry(func, max_attempts=2, delay=0)
        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, RuntimeError)
