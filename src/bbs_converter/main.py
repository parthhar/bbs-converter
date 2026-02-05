"""Entry point for the BBS Converter application."""

from __future__ import annotations

import argparse
import signal
import sys

from bbs_converter.capture.region_selector import select_region
from bbs_converter.models import CaptureRegion
from bbs_converter.pipeline.orchestrator import PipelineOrchestrator
from bbs_converter.utils.config import load_config
from bbs_converter.utils.logger import get_logger

_log = get_logger("main")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Parameters
    ----------
    argv:
        Argument list (defaults to sys.argv[1:]).
    """
    parser = argparse.ArgumentParser(
        prog="bbs-converter",
        description="Real-time Poker HUD to Big Blinds converter",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=None,
        help="Target capture FPS (default: from config or 30)",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=None,
        help="OCR confidence threshold 0-100 (default: from config or 60)",
    )
    parser.add_argument(
        "--region",
        type=str,
        default=None,
        metavar="X,Y,W,H",
        help="Capture region as 'x,y,width,height' (skips interactive selector)",
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=5,
        metavar="SECONDS",
        help="Ignored with interactive UI (kept for backwards compatibility)",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to TOML config file",
    )
    return parser.parse_args(argv)


def _parse_region(region_str: str) -> CaptureRegion:
    """Parse a 'x,y,w,h' string into a CaptureRegion."""
    parts = [int(p.strip()) for p in region_str.split(",")]
    if len(parts) != 4:
        raise ValueError(f"Expected 4 values (x,y,w,h), got {len(parts)}")
    return CaptureRegion(x=parts[0], y=parts[1], width=parts[2], height=parts[3])


def main(argv: list[str] | None = None) -> None:
    """Run the BBS Converter pipeline."""
    args = parse_args(argv)

    # Load config
    config_path = None
    if args.config:
        from pathlib import Path
        config_path = Path(args.config)
    config = load_config(config_path)

    # Determine settings
    fps = args.fps or config["capture"]["fps"]
    confidence = args.confidence or config["ocr"]["confidence_threshold"]

    # Get capture region
    if args.region:
        region = _parse_region(args.region)
    else:
        region = select_region(delay=args.delay)

    _log.info(
        "Starting BBS Converter: region=%s fps=%d confidence=%.0f",
        region, fps, confidence,
    )

    # Run pipeline
    orchestrator = PipelineOrchestrator(
        region=region,
        fps=fps,
        confidence_threshold=confidence,
    )

    def shutdown(signum: int, frame: object) -> None:
        _log.info("Received signal %d, shutting down...", signum)
        orchestrator.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    orchestrator.start()

    # Wait for user to be ready before starting the overlay.
    print("\n  Pipeline is running (capture + OCR + conversion).")
    print("  Switch to your poker window, then come back and press Enter to start the HUD.")
    print("  Press Ctrl+C to quit.\n")

    try:
        input("  Press Enter to start overlay HUD...")
    except (KeyboardInterrupt, EOFError):
        _log.info("Interrupted before overlay, shutting down...")
        orchestrator.stop()
        return

    print("  HUD starting — switch to your poker window now.\n")

    # Run the overlay on the main thread (required on macOS for OpenCV GUI).
    # This blocks until the stop event is set via signal handler.
    try:
        orchestrator.run_overlay()
    except KeyboardInterrupt:
        _log.info("Interrupted, shutting down...")
        orchestrator.stop()


if __name__ == "__main__":
    main()
