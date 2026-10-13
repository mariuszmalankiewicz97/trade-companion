import pandas as pd
import pytest

from trade_companion.fetch_stock_data import fetch_stock_data

tickers = ["PKO.WA", "AAPL"]
period = "1y"
interval = "1d"


def test_fetch_stock_data_invalid_tickers():
    with pytest.raises(TypeError):
        tickers = "PKO.WA"
        result = fetch_stock_data(tickers, period, interval)
        assert isinstance(result, pd.DataFrame)


def test_fetch_stock_data_invalid_period():
    with pytest.raises(TypeError):
        period = 1
        result = fetch_stock_data(tickers, period, interval)
        assert isinstance(result, pd.DataFrame)


def test_fetch_stock_data_invalid_interval():
    with pytest.raises(TypeError):
        interval = 10.1
        result = fetch_stock_data(tickers, period, interval)
        assert isinstance(result, pd.DataFrame)


def test_fetch_stock_data_returns_correct_structure():
    result = fetch_stock_data(tickers, period, interval)
    assert isinstance(result, pd.DataFrame)
