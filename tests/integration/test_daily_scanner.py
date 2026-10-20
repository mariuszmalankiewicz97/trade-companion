import json

import pandas as pd

from trade_companion import daily_scanner


def test_main_scans_configured_tickers_with_fetched_close_data(
    tmp_path, monkeypatch, capsys
):
    tickers_file = tmp_path / "tickers.json"
    tickers_file.write_text(
        json.dumps({"watchlist": ["AAA", "BBB", "AAA", "NO_DATA"]}),
        encoding="utf-8",
    )
    monkeypatch.setattr(daily_scanner, "TICKERS_FILE", tickers_file)

    dates = pd.date_range("2025-01-01", periods=202)
    df_aaa = pd.DataFrame({"Close": [None] + [100.0] * 200 + [110.0]}, index=dates)
    df_bbb = pd.DataFrame({"Close": [100.0] * 201 + [90.0]}, index=dates)

    mock_market_data = {
        "AAA": df_aaa,
        "BBB": df_bbb,
    }

    fetch_calls = []

    def fake_fetch_stock_data(tickers, period, interval):
        fetch_calls.append((tickers, period, interval))
        return mock_market_data

    monkeypatch.setattr(daily_scanner, "fetch_stock_data", fake_fetch_stock_data)

    strategy_calls = []
    real_strategy = daily_scanner.daily_trend_strategy

    def spy_strategy(ticker_df):
        result = real_strategy(ticker_df)
        strategy_calls.append(result)
        return result

    monkeypatch.setattr(daily_scanner, "daily_trend_strategy", spy_strategy)

    daily_scanner.main()

    assert len(fetch_calls) == 1
    assert set(fetch_calls[0][0]) == {"AAA", "BBB", "NO_DATA"}

    captured = capsys.readouterr()
    assert "AAA" in captured.out
    assert "BBB" not in captured.out
