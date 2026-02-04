"""Tests for the custom exception hierarchy."""

import pytest

from bbs_converter.utils.exceptions import (
    BBSConverterError,
    CaptureError,
    ConfigError,
    ConversionError,
    OCRError,
    OverlayError,
    ParserError,
    PipelineError,
)


class TestExceptionHierarchy:
    """All module exceptions inherit from BBSConverterError."""

    @pytest.mark.parametrize(
        "exc_class",
        [
            ConfigError,
            CaptureError,
            OCRError,
            ParserError,
            ConversionError,
            OverlayError,
            PipelineError,
        ],
    )
    def test_subclass_of_base(self, exc_class: type) -> None:
        assert issubclass(exc_class, BBSConverterError)

    @pytest.mark.parametrize(
        "exc_class",
        [
            ConfigError,
            CaptureError,
            OCRError,
            ParserError,
            ConversionError,
            OverlayError,
            PipelineError,
        ],
    )
    def test_catchable_as_base(self, exc_class: type) -> None:
        with pytest.raises(BBSConverterError):
            raise exc_class("test error")

    def test_base_is_exception(self) -> None:
        assert issubclass(BBSConverterError, Exception)

    def test_message_preserved(self) -> None:
        err = CaptureError("monitor not found")
        assert str(err) == "monitor not found"
