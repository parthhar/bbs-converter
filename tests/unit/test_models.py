"""Tests for core data models."""

from bbs_converter.models import BBState, TableState


class TestTableState:
    def test_create_table_state(self) -> None:
        state = TableState(
            big_blind=100.0,
            small_blind=50.0,
            pot=350.0,
            stacks={"Player1": 5000.0, "Player2": 3200.0},
        )
        assert state.big_blind == 100.0
        assert state.small_blind == 50.0
        assert state.pot == 350.0
        assert state.stacks["Player1"] == 5000.0

    def test_table_state_default_stacks(self) -> None:
        state = TableState(big_blind=100.0, small_blind=50.0, pot=0.0)
        assert state.stacks == {}

    def test_table_state_is_frozen(self) -> None:
        state = TableState(big_blind=100.0, small_blind=50.0, pot=0.0)
        try:
            state.big_blind = 200.0  # type: ignore[misc]
            assert False, "Should have raised FrozenInstanceError"
        except AttributeError:
            pass


class TestBBState:
    def test_create_bb_state(self) -> None:
        state = BBState(
            pot_bb=3.5,
            stacks_bb={"Player1": 50.0, "Player2": 32.0},
        )
        assert state.pot_bb == 3.5
        assert state.stacks_bb["Player1"] == 50.0

    def test_bb_state_default_stacks(self) -> None:
        state = BBState(pot_bb=0.0)
        assert state.stacks_bb == {}
