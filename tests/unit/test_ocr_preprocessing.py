"""Tests for OCR preprocessing chain (grayscale, threshold, denoise)."""

from __future__ import annotations

import numpy as np

from bbs_converter.ocr.denoise import reduce_noise
from bbs_converter.ocr.preprocessor import to_grayscale
from bbs_converter.ocr.threshold import adaptive_threshold


class TestToGrayscale:
    def test_bgr_to_gray(self) -> None:
        bgr = np.zeros((100, 100, 3), dtype=np.uint8)
        bgr[:, :, 2] = 255  # red channel
        gray = to_grayscale(bgr)
        assert gray.ndim == 2
        assert gray.shape == (100, 100)

    def test_bgra_to_gray(self) -> None:
        bgra = np.zeros((100, 100, 4), dtype=np.uint8)
        gray = to_grayscale(bgra)
        assert gray.ndim == 2

    def test_already_gray(self) -> None:
        gray = np.ones((50, 50), dtype=np.uint8) * 128
        result = to_grayscale(gray)
        assert result.ndim == 2
        assert np.array_equal(result, gray)


class TestAdaptiveThreshold:
    def test_output_is_binary(self) -> None:
        gray = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        binary = adaptive_threshold(gray)
        unique = set(np.unique(binary))
        assert unique.issubset({0, 255})

    def test_output_shape_matches_input(self) -> None:
        gray = np.zeros((80, 120), dtype=np.uint8)
        binary = adaptive_threshold(gray)
        assert binary.shape == (80, 120)


class TestReduceNoise:
    def test_output_shape_matches_input(self) -> None:
        image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
        result = reduce_noise(image)
        assert result.shape == image.shape

    def test_reduces_noise(self) -> None:
        # Create image with salt-and-pepper noise
        image = np.full((100, 100), 128, dtype=np.uint8)
        image[50, 50] = 255  # salt
        image[25, 25] = 0    # pepper
        result = reduce_noise(image, kernel_size=3)
        # The median filter should reduce extreme pixel values
        assert result[50, 50] == 128
        assert result[25, 25] == 128


class TestPreprocessingChain:
    def test_full_chain(self) -> None:
        """Verify the full preprocessing pipeline works end-to-end."""
        bgra = np.random.randint(0, 256, (100, 100, 4), dtype=np.uint8)
        gray = to_grayscale(bgra)
        binary = adaptive_threshold(gray)
        clean = reduce_noise(binary)
        assert clean.ndim == 2
        assert clean.shape == (100, 100)
        assert set(np.unique(clean)).issubset({0, 255})
