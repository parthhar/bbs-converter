"""Tests for TOML config loader."""

from __future__ import annotations

from pathlib import Path

import pytest

from bbs_converter.utils.config import load_config
from bbs_converter.utils.constants import DEFAULT_CONFIDENCE_THRESHOLD, DEFAULT_FPS
from bbs_converter.utils.exceptions import ConfigError


class TestLoadConfig:
    def test_defaults_when_no_file(self, tmp_path: Path) -> None:
        config = load_config(tmp_path / "nonexistent.toml")
        assert config["capture"]["fps"] == DEFAULT_FPS
        assert config["ocr"]["confidence_threshold"] == DEFAULT_CONFIDENCE_THRESHOLD
        assert config["overlay"]["enabled"] is True

    def test_user_values_override_defaults(self, tmp_path: Path) -> None:
        toml_path = tmp_path / "config.toml"
        toml_path.write_text('[capture]\nfps = 60\n')
        config = load_config(toml_path)
        assert config["capture"]["fps"] == 60
        # other defaults still present
        assert config["ocr"]["confidence_threshold"] == DEFAULT_CONFIDENCE_THRESHOLD

    def test_deep_merge_preserves_nested_defaults(self, tmp_path: Path) -> None:
        toml_path = tmp_path / "config.toml"
        toml_path.write_text('[ocr]\nlanguage = "eng"\n')
        config = load_config(toml_path)
        # user key added
        assert config["ocr"]["language"] == "eng"
        # default key preserved
        assert config["ocr"]["confidence_threshold"] == DEFAULT_CONFIDENCE_THRESHOLD

    def test_invalid_toml_raises_config_error(self, tmp_path: Path) -> None:
        toml_path = tmp_path / "bad.toml"
        toml_path.write_text("not = [valid toml")
        with pytest.raises(ConfigError, match="Failed to parse"):
            load_config(toml_path)

    def test_extra_sections_pass_through(self, tmp_path: Path) -> None:
        toml_path = tmp_path / "config.toml"
        toml_path.write_text('[custom]\nkey = "value"\n')
        config = load_config(toml_path)
        assert config["custom"]["key"] == "value"
