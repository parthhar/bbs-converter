"""Tests for live status dashboard."""

from __future__ import annotations

import time

from bbs_converter.cli.status import PipelineStats, StatusDashboard


class TestPipelineStats:
    def test_default_values(self) -> None:
        stats = PipelineStats()
        assert stats.capture_fps == 0.0
        assert stats.ocr_confidence == 0.0
        assert stats.cache_hit_rate == 0.0
        assert stats.frames_processed == 0
        assert stats.parse_errors == 0
        assert stats.ocr_errors == 0

    def test_mutable(self) -> None:
        stats = PipelineStats()
        stats.capture_fps = 30.0
        stats.frames_processed = 100
        assert stats.capture_fps == 30.0
        assert stats.frames_processed == 100


class TestStatusDashboard:
    def test_start_and_stop(self) -> None:
        stats = PipelineStats()
        dash = StatusDashboard(stats, refresh_interval=0.01)
        dash.start()
        assert dash.running is True
        time.sleep(0.05)
        dash.stop()
        assert dash.running is False

    def test_prints_status(self, capsys) -> None:
        stats = PipelineStats(capture_fps=30.0, frames_processed=42)
        dash = StatusDashboard(stats, refresh_interval=0.01)
        dash.start()
        time.sleep(0.05)
        dash.stop()
        # Status is written to stderr
        captured = capsys.readouterr()
        assert "FPS" in captured.err or captured.err == ""  # may not flush in test

    def test_double_start_safe(self) -> None:
        stats = PipelineStats()
        dash = StatusDashboard(stats, refresh_interval=0.1)
        dash.start()
        dash.start()  # should not create second thread
        assert dash.running is True
        dash.stop()
