"""Tests for first-run setup wizard."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from bbs_converter.cli.setup_wizard import (
    load_saved_region,
    run_setup_wizard,
    save_region,
)
from bbs_converter.models import CaptureRegion


class TestSaveAndLoadRegion:
    def test_save_and_load(self, tmp_path: Path) -> None:
        setup_file = tmp_path / ".bbs_converter_setup.json"
        region = CaptureRegion(x=100, y=200, width=800, height=600)

        with patch(
            "bbs_converter.cli.setup_wizard._setup_path",
            return_value=setup_file,
        ):
            save_region(region)
            loaded = load_saved_region()

        assert loaded == region

    def test_load_missing_file(self, tmp_path: Path) -> None:
        setup_file = tmp_path / "nonexistent.json"
        with patch(
            "bbs_converter.cli.setup_wizard._setup_path",
            return_value=setup_file,
        ):
            assert load_saved_region() is None

    def test_load_corrupted_file(self, tmp_path: Path) -> None:
        setup_file = tmp_path / ".bbs_converter_setup.json"
        setup_file.write_text("not json")
        with patch(
            "bbs_converter.cli.setup_wizard._setup_path",
            return_value=setup_file,
        ):
            assert load_saved_region() is None


class TestRunSetupWizard:
    def test_returns_saved_region(self, tmp_path: Path) -> None:
        setup_file = tmp_path / ".bbs_converter_setup.json"
        region = CaptureRegion(x=10, y=20, width=300, height=400)
        setup_file.write_text(json.dumps({
            "x": 10, "y": 20, "width": 300, "height": 400,
        }))

        with patch(
            "bbs_converter.cli.setup_wizard._setup_path",
            return_value=setup_file,
        ):
            result = run_setup_wizard(force=False)

        assert result == region

    def test_force_runs_selector(self, tmp_path: Path) -> None:
        setup_file = tmp_path / ".bbs_converter_setup.json"
        new_region = CaptureRegion(x=50, y=50, width=500, height=500)

        with patch(
            "bbs_converter.cli.setup_wizard._setup_path",
            return_value=setup_file,
        ):
            with patch(
                "bbs_converter.cli.setup_wizard"
                ".select_region",
                return_value=new_region,
            ):
                result = run_setup_wizard(force=True)

        assert result == new_region
        # Verify it was saved
        with patch(
            "bbs_converter.cli.setup_wizard._setup_path",
            return_value=setup_file,
        ):
            loaded = load_saved_region()
        assert loaded == new_region
