"""Tests for BB history tracker."""

from __future__ import annotations

from bbs_converter.converter.history import BBHistory


class TestBBHistory:
    def test_empty_history(self) -> None:
        history = BBHistory()
        assert len(history) == 0
        assert history.latest is None
        assert history.snapshots == []

    def test_record_and_retrieve(self) -> None:
        history = BBHistory()
        history.record({"Alice": 50.0}, pot_bb=3.5)
        assert len(history) == 1
        assert history.latest is not None
        assert history.latest.stacks_bb["Alice"] == 50.0
        assert history.latest.pot_bb == 3.5

    def test_multiple_records(self) -> None:
        history = BBHistory()
        history.record({"A": 10.0}, pot_bb=1.0)
        history.record({"A": 20.0}, pot_bb=2.0)
        assert len(history) == 2
        assert history.snapshots[0].stacks_bb["A"] == 10.0
        assert history.latest is not None
        assert history.latest.stacks_bb["A"] == 20.0

    def test_max_size_eviction(self) -> None:
        history = BBHistory(max_size=3)
        for i in range(5):
            history.record({"P": float(i)}, pot_bb=0.0)
        assert len(history) == 3
        # oldest entries (0, 1) should be evicted
        assert history.snapshots[0].stacks_bb["P"] == 2.0

    def test_timestamps_increase(self) -> None:
        history = BBHistory()
        history.record({"X": 1.0}, pot_bb=0.0)
        history.record({"X": 2.0}, pot_bb=0.0)
        t0 = history.snapshots[0].timestamp
        t1 = history.snapshots[1].timestamp
        assert t1 >= t0

    def test_snapshot_copies_dict(self) -> None:
        """Mutating the input dict after recording must not affect history."""
        stacks = {"A": 10.0}
        history = BBHistory()
        history.record(stacks, pot_bb=0.0)
        stacks["A"] = 999.0
        assert history.latest is not None
        assert history.latest.stacks_bb["A"] == 10.0
