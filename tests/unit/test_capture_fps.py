"""Tests for FPS controller."""

from __future__ import annotations

import time

from bbs_converter.capture.fps_controller import FPSController


class TestFPSController:
    def test_initial_fps_is_zero(self) -> None:
        ctrl = FPSController(target_fps=30)
        assert ctrl.actual_fps == 0.0

    def test_target_fps_property(self) -> None:
        ctrl = FPSController(target_fps=60)
        assert ctrl.target_fps == 60

    def test_tick_throttles_to_target(self) -> None:
        ctrl = FPSController(target_fps=100)
        ctrl.tick()
        start = time.perf_counter()
        ctrl.tick()
        elapsed = time.perf_counter() - start
        # should be at least ~10ms (1/100) but allow tolerance
        assert elapsed >= 0.005

    def test_actual_fps_updates_after_tick(self) -> None:
        ctrl = FPSController(target_fps=100)
        ctrl.tick()
        ctrl.tick()
        # FPS should be in a reasonable range
        assert ctrl.actual_fps > 0

    def test_first_tick_does_not_sleep(self) -> None:
        ctrl = FPSController(target_fps=10)
        start = time.perf_counter()
        ctrl.tick()
        elapsed = time.perf_counter() - start
        # first tick should return immediately (no previous reference)
        assert elapsed < 0.05
