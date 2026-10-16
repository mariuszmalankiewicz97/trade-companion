import json

import pandas as pd
from pandas.testing import assert_series_equal

from trade_companion import daily_scanner


def test_main_scans_configured_tickers_with_fetched_close_data(tmp_path, monkeypatch):
    tickers_file = tmp_path / "tickers.json"
    tickers_file.write_text(
        json.dumps({"watchlist": ["AAA", "BBB", "AAA", "NO_DATA"]}),
        encoding="utf-8",
    )
    monkeypatch.setattr(daily_scanner, "TICKERS_FILE", tickers_file)

    close_data = pd.DataFrame(
        {
            "AAA": [None] + [100.0] * 200 + [110.0],
            "BBB": [100.0] * 201 + [90.0],
        },
        index=pd.date_range("2025-01-01", periods=202),
    )
    market_data = pd.concat({"Close": close_data}, axis=1)
    fetch_calls = []

    def fake_fetch_stock_data(tickers, period, interval):
        fetch_calls.append((tickers, period, interval))
        return market_data

    monkeypatch.setattr(daily_scanner, "fetch_stock_data", fake_fetch_stock_data)

    original_filter = daily_scanner.price_over_sma
    filter_results = {}
    filtered_closes = {}

    def record_filter_result(close):
        filtered_closes[close.name] = close.copy()
        result = original_filter(close)
        filter_results[close.name] = result
        return result

    monkeypatch.setattr(daily_scanner, "price_over_sma", record_filter_result)

    daily_scanner.main()

    assert len(fetch_calls) == 1
    fetched_tickers, period, interval = fetch_calls[0]
    assert set(fetched_tickers) == {"AAA", "BBB", "NO_DATA"}
    assert len(fetched_tickers) == 3
    assert period == daily_scanner.SCAN_PERIOD
    assert interval == daily_scanner.SCAN_INTERVAL

    assert set(filtered_closes) == {"AAA", "BBB"}
    assert_series_equal(filtered_closes["AAA"], close_data["AAA"].dropna())
    assert_series_equal(filtered_closes["BBB"], close_data["BBB"].dropna())
    assert filter_results == {"AAA": True, "BBB": False}
