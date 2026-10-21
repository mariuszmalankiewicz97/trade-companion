import json
from pathlib import Path

import pandas as pd
import pytest

from trade_companion import daily_scanner
from trade_companion.daily_trend import DailySetup
from trade_companion.storage import load_h1_watchlist


def test_daily_scanner_end_to_end_flow(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    tickers_file = tmp_path / "tickers.json"
    h1_watchlist_file = tmp_path / "h1_watchlist.json"

    tickers_file.write_text(
        json.dumps({"watchlist": ["ALE.WA", "BDX.WA", "ALE.WA", "NO_DATA"]}),
        encoding="utf-8",
    )

    monkeypatch.setattr(daily_scanner, "TICKERS_FILE", tickers_file)
    monkeypatch.setattr(daily_scanner, "H1_WATCHLIST_FILE", h1_watchlist_file)

    dates = pd.date_range("2025-01-01", periods=205)
    df_ale = pd.DataFrame(
        {
            "Close": [100.0] * 204 + [110.0],
            "High": [102.0] * 204 + [112.0],
            "Low": [98.0] * 204 + [108.0],
        },
        index=dates,
    )
    df_bdx = pd.DataFrame(
        {
            "Close": [100.0] * 204 + [90.0],
            "High": [102.0] * 204 + [92.0],
            "Low": [98.0] * 204 + [88.0],
        },
        index=dates,
    )

    mock_market_data = {
        "ALE.WA": df_ale,
        "BDX.WA": df_bdx,
    }

    monkeypatch.setattr(
        daily_scanner, "fetch_stock_data", lambda tickers, p, i: mock_market_data
    )

    expected_setup = DailySetup(
        ticker="ALE.WA",
        current_close=110.0,
        stop_loss=98.0,
        fib_50=105.0,
        fib_618=103.0,
        peak_high=112.0,
    )

    def fake_eval(ticker: str, df: pd.DataFrame) -> DailySetup | None:
        if ticker == "ALE.WA":
            return expected_setup
        return None

    monkeypatch.setattr(daily_scanner, "evaluate_daily_trend_setup", fake_eval)

    daily_scanner.main()

    assert h1_watchlist_file.exists()
    saved_setups = load_h1_watchlist(h1_watchlist_file)

    assert len(saved_setups) == 1
    assert saved_setups[0] == expected_setup
    assert saved_setups[0].ticker == "ALE.WA"
    assert saved_setups[0].fib_50 == 105.0

    captured = capsys.readouterr()
    assert "Zapisano 1 setupów do: h1_watchlist.json" in captured.out
    assert "ALE.WA" in captured.out
    assert "BDX.WA" not in captured.out
