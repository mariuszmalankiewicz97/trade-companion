import pandas as pd
import pytest

from trade_companion import daily_scanner


@pytest.fixture
def dummy_dataframe() -> pd.DataFrame:
    """Tworzy przykładowy DataFrame na potrzeby mockowania zawartości słownika."""
    return pd.DataFrame({"Close": [100.0, 105.0]})


def test_main_executes_workflow_and_filters_tickers(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    expected_tickers = ["AAPL", "MSFT", "TSLA"]
    monkeypatch.setattr(daily_scanner, "load_tickers", lambda path: expected_tickers)

    df_aapl = pd.DataFrame({"Close": [150.0]})
    df_msft = pd.DataFrame({"Close": [300.0]})
    df_tsla = pd.DataFrame({"Close": [200.0]})

    calls = {}

    def fake_fetch(tickers, period, interval):
        calls["tickers"] = tickers
        calls["period"] = period
        calls["interval"] = interval
        return {"AAPL": df_aapl, "MSFT": df_msft, "TSLA": df_tsla}

    monkeypatch.setattr(daily_scanner, "fetch_stock_data", fake_fetch)

    def fake_strategy(df: pd.DataFrame) -> bool:
        return df is df_aapl or df is df_tsla

    monkeypatch.setattr(daily_scanner, "daily_trend_strategy", fake_strategy)

    daily_scanner.main()

    assert calls["tickers"] == expected_tickers
    assert calls["period"] == daily_scanner.SCAN_PERIOD
    assert calls["interval"] == daily_scanner.SCAN_INTERVAL

    captured = capsys.readouterr()
    assert "['AAPL', 'TSLA']" in captured.out
    assert "MSFT" not in captured.out


def test_main_handles_empty_market_data(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setattr(daily_scanner, "load_tickers", lambda _: ["AAPL"])
    monkeypatch.setattr(daily_scanner, "fetch_stock_data", lambda *args: {})

    daily_scanner.main()

    captured = capsys.readouterr()
    assert "[]" in captured.out


def test_main_handles_all_tickers_failing_strategy(
    dummy_dataframe: pd.DataFrame,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    monkeypatch.setattr(daily_scanner, "load_tickers", lambda _: ["AAPL", "MSFT"])
    monkeypatch.setattr(
        daily_scanner,
        "fetch_stock_data",
        lambda *args: {"AAPL": dummy_dataframe, "MSFT": dummy_dataframe},
    )
    monkeypatch.setattr(daily_scanner, "daily_trend_strategy", lambda df: False)

    daily_scanner.main()

    captured = capsys.readouterr()
    assert "[]" in captured.out
