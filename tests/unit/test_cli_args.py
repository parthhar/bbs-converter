"""Tests for CLI argument parser."""

from __future__ import annotations

import pytest

from bbs_converter.main import _parse_region, parse_args
from bbs_converter.models import CaptureRegion


class TestParseArgs:
    def test_defaults(self) -> None:
        args = parse_args([])
        assert args.fps is None
        assert args.confidence is None
        assert args.region is None
        assert args.config is None

    def test_fps_flag(self) -> None:
        args = parse_args(["--fps", "60"])
        assert args.fps == 60

    def test_confidence_flag(self) -> None:
        args = parse_args(["--confidence", "80.5"])
        assert args.confidence == 80.5

    def test_region_flag(self) -> None:
        args = parse_args(["--region", "100,200,800,600"])
        assert args.region == "100,200,800,600"

    def test_config_flag(self) -> None:
        args = parse_args(["--config", "/path/to/config.toml"])
        assert args.config == "/path/to/config.toml"

    def test_all_flags(self) -> None:
        args = parse_args([
            "--fps", "60",
            "--confidence", "75",
            "--region", "0,0,1920,1080",
            "--config", "my.toml",
        ])
        assert args.fps == 60
        assert args.confidence == 75.0
        assert args.region == "0,0,1920,1080"
        assert args.config == "my.toml"


class TestParseRegion:
    def test_valid_region(self) -> None:
        region = _parse_region("100,200,800,600")
        assert region == CaptureRegion(x=100, y=200, width=800, height=600)

    def test_with_spaces(self) -> None:
        region = _parse_region("100, 200, 800, 600")
        assert region == CaptureRegion(x=100, y=200, width=800, height=600)

    def test_invalid_count(self) -> None:
        with pytest.raises(ValueError, match="Expected 4"):
            _parse_region("100,200,800")
