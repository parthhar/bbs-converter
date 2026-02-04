"""Performance timing utilities."""

from __future__ import annotations

import functools
import time
from typing import Any, Callable, TypeVar

from bbs_converter.utils.logger import get_logger

_log = get_logger("timer")

F = TypeVar("F", bound=Callable[..., Any])


def timed(func: F) -> F:
    """Decorator that logs the wall-clock duration of *func*."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            _log.debug("%s took %.1f ms", func.__qualname__, elapsed_ms)

    return wrapper  # type: ignore[return-value]
