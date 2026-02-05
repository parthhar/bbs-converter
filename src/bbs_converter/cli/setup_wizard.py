"""First-run setup wizard for region selection and OCR verification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from bbs_converter.capture.region_selector import select_region
from bbs_converter.models import CaptureRegion
from bbs_converter.utils.logger import get_logger

_log = get_logger("cli.setup")

_SETUP_FILE = ".bbs_converter_setup.json"


def _setup_path() -> Path:
    """Return the path to the persisted setup file."""
    return Path.home() / _SETUP_FILE


def load_saved_region() -> Optional[CaptureRegion]:
    """Load a previously saved capture region, or None if not found."""
    path = _setup_path()
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        return CaptureRegion(
            x=data["x"], y=data["y"],
            width=data["width"], height=data["height"],
        )
    except (json.JSONDecodeError, KeyError):
        _log.warning("Corrupted setup file, ignoring")
        return None


def save_region(region: CaptureRegion) -> None:
    """Persist a capture region for future runs."""
    data = {
        "x": region.x,
        "y": region.y,
        "width": region.width,
        "height": region.height,
    }
    _setup_path().write_text(json.dumps(data))
    _log.info("Saved capture region to %s", _setup_path())


def run_setup_wizard(force: bool = False) -> CaptureRegion:
    """Run the first-run setup wizard.

    If a saved region exists and *force* is False, returns the saved
    region. Otherwise launches the interactive selector and saves the
    result.

    Parameters
    ----------
    force:
        If True, always run the interactive selector.

    Returns
    -------
    CaptureRegion
        The selected capture region.
    """
    if not force:
        saved = load_saved_region()
        if saved is not None:
            _log.info("Using saved capture region: %s", saved)
            return saved

    _log.info("Running first-time setup — please select the capture region")
    region = select_region()
    save_region(region)
    return region
