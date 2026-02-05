"""TOML configuration loader."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib
from pathlib import Path
from typing import Any

from bbs_converter.utils.constants import (
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEFAULT_CONFIG_FILENAME,
    DEFAULT_FPS,
)
from bbs_converter.utils.exceptions import ConfigError

_DEFAULTS: dict[str, Any] = {
    "capture": {
        "fps": DEFAULT_FPS,
    },
    "ocr": {
        "confidence_threshold": DEFAULT_CONFIDENCE_THRESHOLD,
    },
    "overlay": {
        "enabled": True,
    },
}


def _deep_merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge *overrides* into a copy of *base*."""
    merged = base.copy()
    for key, value in overrides.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(path: Path | None = None) -> dict[str, Any]:
    """Load configuration from a TOML file, merged with defaults.

    Parameters
    ----------
    path:
        Explicit path to a TOML file.  When *None*, looks for
        ``bbs_converter.toml`` in the current working directory.

    Returns
    -------
    dict
        Merged configuration dictionary.

    Raises
    ------
    ConfigError
        If the file exists but cannot be parsed.
    """
    if path is None:
        path = Path.cwd() / DEFAULT_CONFIG_FILENAME

    if not path.exists():
        return _DEFAULTS.copy()

    try:
        raw = path.read_bytes()
        user_config = tomllib.loads(raw.decode())
    except Exception as exc:
        raise ConfigError(f"Failed to parse config file {path}: {exc}") from exc

    return _deep_merge(_DEFAULTS, user_config)
