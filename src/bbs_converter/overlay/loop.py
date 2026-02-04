"""Overlay refresh loop synchronized with the processing pipeline."""

from __future__ import annotations

import threading
import time
from typing import Callable, Optional

from bbs_converter.models import BBState, CaptureRegion
from bbs_converter.overlay.colorizer import colorize_stacks
from bbs_converter.overlay.positioning import compute_positions
from bbs_converter.overlay.renderer import render_bb_values
from bbs_converter.overlay.window import OverlayWindow
from bbs_converter.utils.logger import get_logger

_log = get_logger("overlay.loop")


class OverlayLoop:
    """Refresh loop that updates the overlay display.

    Parameters
    ----------
    region:
        Screen region for the overlay window.
    get_state:
        Callable that returns the latest BBState (or None if not ready).
    refresh_hz:
        Target refresh rate in Hz.
    """

    def __init__(
        self,
        region: CaptureRegion,
        get_state: Callable[[], Optional[BBState]],
        refresh_hz: int = 15,
    ) -> None:
        self._region = region
        self._get_state = get_state
        self._refresh_interval = 1.0 / refresh_hz
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._player_names: list[str] = []

    def start(self) -> None:
        """Start the overlay refresh loop in a background thread."""
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        _log.info("Overlay loop started at %.0f Hz", 1.0 / self._refresh_interval)

    def stop(self, timeout: float = 2.0) -> None:
        """Stop the overlay refresh loop."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=timeout)
            self._thread = None
        _log.info("Overlay loop stopped")

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def _run(self) -> None:
        """Main loop: fetch state → clear → render → show → sleep."""
        with OverlayWindow(self._region) as window:
            while not self._stop_event.is_set():
                state = self._get_state()
                if state is not None:
                    # Update player name list if changed
                    new_names = sorted(state.stacks_bb.keys())
                    if new_names != self._player_names:
                        self._player_names = new_names

                    positions = compute_positions(self._region, self._player_names)
                    colors = colorize_stacks(state.stacks_bb)

                    window.clear()
                    # Render each player with their stack-depth color
                    for name in self._player_names:
                        if name in positions:
                            color = colors.get(name, (0, 255, 0, 255))
                            single_state = BBState(
                                pot_bb=0.0,
                                stacks_bb={name: state.stacks_bb[name]},
                            )
                            render_bb_values(
                                window.canvas,
                                single_state,
                                {name: positions[name]},
                                color=color,
                            )
                    # Render pot
                    if state.pot_bb > 0:
                        pot_state = BBState(pot_bb=state.pot_bb, stacks_bb={})
                        render_bb_values(window.canvas, pot_state, {})

                    window.show()

                time.sleep(self._refresh_interval)
