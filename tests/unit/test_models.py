"""Tests for core data models."""

from bbs_converter.models import (
    BBState,
    CaptureRegion,
    GameConfig,
    PlayerInfo,
    TableState,
)


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


class TestCaptureRegion:
    def test_create_region(self) -> None:
        region = CaptureRegion(x=100, y=200, width=800, height=600)
        assert region.x == 100
        assert region.y == 200
        assert region.width == 800
        assert region.height == 600

    def test_to_mss_monitor(self) -> None:
        region = CaptureRegion(x=10, y=20, width=300, height=400)
        monitor = region.to_mss_monitor()
        assert monitor == {"left": 10, "top": 20, "width": 300, "height": 400}

    def test_is_frozen(self) -> None:
        region = CaptureRegion(x=0, y=0, width=100, height=100)
        try:
            region.x = 50  # type: ignore[misc]
            raise AssertionError("Should have raised")
        except AttributeError:
            pass


class TestPlayerInfo:
    def test_create_player(self) -> None:
        player = PlayerInfo(name="Alice", seat=3, stack=1500.0)
        assert player.name == "Alice"
        assert player.seat == 3
        assert player.stack == 1500.0

    def test_is_frozen(self) -> None:
        player = PlayerInfo(name="Bob", seat=1, stack=1000.0)
        try:
            player.stack = 2000.0  # type: ignore[misc]
            raise AssertionError("Should have raised")
        except AttributeError:
            pass


class TestGameConfig:
    def test_create_config(self) -> None:
        config = GameConfig(big_blind=100.0, small_blind=50.0, ante=10.0)
        assert config.big_blind == 100.0
        assert config.small_blind == 50.0
        assert config.ante == 10.0

    def test_default_ante(self) -> None:
        config = GameConfig(big_blind=200.0, small_blind=100.0)
        assert config.ante == 0.0

    def test_is_frozen(self) -> None:
        config = GameConfig(big_blind=100.0, small_blind=50.0)
        try:
            config.big_blind = 200.0  # type: ignore[misc]
            raise AssertionError("Should have raised")
        except AttributeError:
            pass
