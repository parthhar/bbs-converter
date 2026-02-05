"""Error recovery with retry logic for pipeline stages."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

from bbs_converter.utils.constants import (
    DEFAULT_RETRY_DELAY_SECONDS,
    DEFAULT_RETRY_LIMIT,
)
from bbs_converter.utils.exceptions import PipelineError
from bbs_converter.utils.logger import get_logger

_log = get_logger("pipeline.recovery")

T = TypeVar("T")


def retry(
    func: Callable[[], T],
    max_attempts: int = DEFAULT_RETRY_LIMIT,
    delay: float = DEFAULT_RETRY_DELAY_SECONDS,
    on_error: Callable[[Exception, int], None] | None = None,
) -> T:
    """Execute *func* with retry on failure.

    Parameters
    ----------
    func:
        Callable to execute.
    max_attempts:
        Maximum number of attempts before giving up.
    delay:
        Seconds to wait between attempts.
    on_error:
        Optional callback invoked with (exception, attempt_number).

    Returns
    -------
    T
        The return value of *func* on success.

    Raises
    ------
    PipelineError
        If all attempts fail, wrapping the last exception.
    """
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as exc:
            last_exc = exc
            _log.warning(
                "Attempt %d/%d failed: %s", attempt, max_attempts, exc
            )
            if on_error is not None:
                on_error(exc, attempt)
            if attempt < max_attempts:
                time.sleep(delay)

    raise PipelineError(
        f"All {max_attempts} attempts failed"
    ) from last_exc
