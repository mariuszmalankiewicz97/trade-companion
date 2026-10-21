import json

import pandas as pd

from trade_companion import daily_scanner


def test_main_scans_configured_tickers_with_fetched_close_data(
    tmp_path, monkeypatch, capsys
) -> None:
    tickers_file = tmp_path / "tickers.json"
    tickers_file.write_text(
        json.dumps({"watchlist": ["AAA", "BBB", "AAA", "NO_DATA"]}),
        encoding="utf-8",
    )
    monkeypatch.setattr(daily_scanner, "TICKERS_FILE", tickers_file)

    dates = pd.date_range("2025-01-01", periods=205)

    df_aaa = pd.DataFrame(
        {
            "Close": [100.0] * 204 + [110.0],
            "High": [102.0] * 204 + [112.0],
            "Low": [98.0] * 204 + [108.0],
        },
        index=dates,
    )

    df_bbb = pd.DataFrame(
        {
            "Close": [100.0] * 204 + [90.0],
            "High": [102.0] * 204 + [92.0],
            "Low": [98.0] * 204 + [88.0],
        },
        index=dates,
    )

    mock_market_data = {
        "AAA": df_aaa,
        "BBB": df_bbb,
    }

    fetch_calls = []

    def fake_fetch_stock_data(tickers, period, interval):
        fetch_calls.append((tickers, period, interval))
        return mock_market_data

    monkeypatch.setattr(daily_scanner, "fetch_stock_data", fake_fetch_stock_data)

    def fake_strategy(df: pd.DataFrame) -> bool:
        return df is df_aaa

    monkeypatch.setattr(daily_scanner, "daily_trend_strategy", fake_strategy)

    daily_scanner.main()

    assert len(fetch_calls) == 1
    assert set(fetch_calls[0][0]) == {"AAA", "BBB", "NO_DATA"}

    captured = capsys.readouterr()
    assert "AAA" in captured.out
    assert "BBB" not in captured.out
