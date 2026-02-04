"""Enumerate available monitors/screens."""

from __future__ import annotations

from dataclasses import dataclass

from bbs_converter.utils.exceptions import CaptureError


@dataclass(frozen=True)
class MonitorInfo:
    """Information about a detected monitor."""

    index: int
    left: int
    top: int
    width: int
    height: int


def list_monitors() -> list[MonitorInfo]:
    """Return information about all available monitors.

    Uses ``mss`` to enumerate monitors. The first entry in the mss
    monitor list is the virtual "all monitors" aggregate, so we skip it.

    Raises
    ------
    CaptureError
        If no monitors can be detected.
    """
    try:
        import mss
    except ImportError as exc:
        raise CaptureError("mss library is required for screen capture") from exc

    with mss.mss() as sct:
        # sct.monitors[0] is the "all monitors" aggregate — skip it
        monitors = [
            MonitorInfo(
                index=i,
                left=m["left"],
                top=m["top"],
                width=m["width"],
                height=m["height"],
            )
            for i, m in enumerate(sct.monitors[1:], start=1)
        ]

    if not monitors:
        raise CaptureError("No monitors detected")

    return monitors
