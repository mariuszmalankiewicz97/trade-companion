import pandas as pd
import pytest

from stock_data import fetch_stock_data


def test_fetch_stock_data_returns_dataframe():
    data = fetch_stock_data("AAPL")
    assert data is not None
    assert isinstance(data, pd.DataFrame)


def test_fetch_stock_data_has_required_column():
    data = fetch_stock_data("AAPL")

    required_columns = ["Open", "High", "Low", "Close", "Volume"]

    for element in required_columns:
        if element not in data.columns:
            assert False, f"Missing required column: {element}"


def test_fetch_stock_data_dataframe_is_not_empty():
    data = fetch_stock_data("AAPL")
    assert data.empty is False


def test_fetch_stock_data_invalid_ticker_and_value_error():
    with pytest.raises(ValueError):
        fetch_stock_data("ABCDEFG")
