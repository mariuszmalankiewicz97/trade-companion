import json
from pathlib import Path

import pytest

from trade_companion.daily_trend import DailySetup
from trade_companion.storage import load_h1_watchlist, save_h1_watchlist


@pytest.fixture
def sample_setups() -> list[DailySetup]:
    return [
        DailySetup(
            ticker="ALE.WA",
            current_close=36.50,
            stop_loss=32.00,
            fib_50=36.80,
            fib_618=35.40,
            peak_high=41.00,
        ),
        DailySetup(
            ticker="BDX.WA",
            current_close=610.0,
            stop_loss=550.0,
            fib_50=615.0,
            fib_618=595.0,
            peak_high=680.0,
        ),
    ]


def test_save_h1_watchlist_creates_directory_and_writes_json(
    tmp_path: Path, sample_setups: list[DailySetup]
) -> None:
    target_file = tmp_path / "subfolder" / "h1_watchlist.json"

    save_h1_watchlist(sample_setups, target_file)

    assert target_file.exists()
    content = json.loads(target_file.read_text(encoding="utf-8"))

    assert content["count"] == 2
    assert len(content["candidates"]) == 2
    assert content["candidates"][0]["ticker"] == "ALE.WA"
    assert content["candidates"][0]["fib_50"] == 36.80


def test_load_h1_watchlist_reconstructs_daily_setup_objects(
    tmp_path: Path, sample_setups: list[DailySetup]
) -> None:
    target_file = tmp_path / "h1_watchlist.json"
    save_h1_watchlist(sample_setups, target_file)

    loaded_setups = load_h1_watchlist(target_file)

    assert len(loaded_setups) == 2
    assert loaded_setups == sample_setups
    assert isinstance(loaded_setups[0], DailySetup)
    assert loaded_setups[0].ticker == "ALE.WA"
    assert loaded_setups[0].stop_loss == 32.00


def test_load_h1_watchlist_returns_empty_list_for_missing_file(
    tmp_path: Path,
) -> None:
    non_existent = tmp_path / "does_not_exist.json"
    assert load_h1_watchlist(non_existent) == []


def test_load_h1_watchlist_handles_empty_candidates_payload(
    tmp_path: Path,
) -> None:
    target_file = tmp_path / "empty_watchlist.json"
    target_file.write_text(json.dumps({"count": 0, "candidates": []}), encoding="utf-8")

    assert load_h1_watchlist(target_file) == []
