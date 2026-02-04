"""Constants, enums, and default values for BBS Converter."""

from __future__ import annotations

from enum import Enum, auto


class CaptureBackend(Enum):
    """Supported screen capture backends."""

    MSS = auto()


class OCREngine(Enum):
    """Supported OCR engines."""

    TESSERACT = auto()


class DisplayMode(Enum):
    """How BB values are displayed in the overlay."""

    DECIMAL = auto()   # e.g. 2.5bb
    INTEGER = auto()   # e.g. 3bb (rounded)
    COMPACT = auto()   # e.g. 100+ (for large stacks)


# --- Capture defaults ---
DEFAULT_FPS = 30
MIN_FPS = 1
MAX_FPS = 120

# --- OCR defaults ---
DEFAULT_OCR_ENGINE = OCREngine.TESSERACT
DEFAULT_CONFIDENCE_THRESHOLD = 60.0  # minimum OCR confidence (0-100)

# --- Converter defaults ---
DEFAULT_DISPLAY_MODE = DisplayMode.DECIMAL
BB_DECIMAL_PLACES = 1
COMPACT_THRESHOLD_BB = 100.0  # stacks above this show as "100+"

# --- Config defaults ---
DEFAULT_CONFIG_FILENAME = "bbs_converter.toml"

# --- Pipeline defaults ---
DEFAULT_QUEUE_MAXSIZE = 30
DEFAULT_RETRY_LIMIT = 3
DEFAULT_RETRY_DELAY_SECONDS = 1.0
