"""Custom exception hierarchy for BBS Converter."""

from __future__ import annotations


class BBSConverterError(Exception):
    """Base exception for all BBS Converter errors."""


class ConfigError(BBSConverterError):
    """Raised when configuration loading or validation fails."""


class CaptureError(BBSConverterError):
    """Raised when screen capture operations fail."""


class OCRError(BBSConverterError):
    """Raised when OCR text extraction fails."""


class ParserError(BBSConverterError):
    """Raised when parsing extracted text fails."""


class ConversionError(BBSConverterError):
    """Raised when chip-to-BB conversion fails."""


class OverlayError(BBSConverterError):
    """Raised when the overlay display encounters an error."""


class PipelineError(BBSConverterError):
    """Raised when the processing pipeline encounters an error."""
