"""Frame rate throttle to maintain a target FPS."""

from __future__ import annotations

import time

from bbs_converter.utils.constants import DEFAULT_FPS


class FPSController:
    """Throttle a loop to run at a target frames-per-second.

    Call :meth:`tick` at the end of each loop iteration. It will
    sleep for the remaining time to maintain the target FPS.

    Parameters
    ----------
    target_fps:
        Desired frames per second.
    """

    def __init__(self, target_fps: int = DEFAULT_FPS) -> None:
        self._target_fps = target_fps
        self._frame_time = 1.0 / target_fps
        self._last_time: float | None = None
        self._actual_fps: float = 0.0

    def tick(self) -> None:
        """Wait as needed to maintain the target frame rate."""
        now = time.perf_counter()
        if self._last_time is not None:
            elapsed = now - self._last_time
            remaining = self._frame_time - elapsed
            if remaining > 0:
                time.sleep(remaining)
            actual_elapsed = time.perf_counter() - self._last_time
            self._actual_fps = 1.0 / actual_elapsed if actual_elapsed > 0 else 0.0
        self._last_time = time.perf_counter()

    @property
    def actual_fps(self) -> float:
        """Return the measured FPS from the last tick interval."""
        return self._actual_fps

    @property
    def target_fps(self) -> int:
        return self._target_fps
