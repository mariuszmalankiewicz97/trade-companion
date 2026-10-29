from unittest.mock import patch

import pandas as pd
import pytest

from trade_companion.providers import YFinanceProvider


@pytest.fixture
def provider():
    return YFinanceProvider()


@pytest.fixture
def sample_dataframe():
    dates = pd.date_range("2026-01-01", periods=2, freq="D")
    data = {
        "Open": [150.0, 152.5],
        "High": [155.0, 157.0],
        "Low": [149.0, 151.0],
        "Close": [153.0, 156.0],
        "Volume": [1000000, 1200000],
    }
    return pd.DataFrame(data, index=dates)


def test_fetch_data_success(provider, sample_dataframe):
    with patch("yfinance.download", return_value=sample_dataframe) as mock_download:
        ticker = "AAPL"
        period = "1mo"
        interval = "1d"

        candles = provider.fetch_data(ticker=ticker, period=period, interval=interval)

        mock_download.assert_called_once_with(ticker, period=period, interval=interval)

        assert len(candles) == 2

        first_candle = candles[0]
        assert first_candle.open == 150.0
        assert first_candle.high == 155.0
        assert first_candle.low == 149.0
        assert first_candle.close == 153.0
        assert first_candle.volume == 1000000
        assert first_candle.timestamp == sample_dataframe.index[0]


def test_fetch_data_empty_dataframe(provider):
    empty_df = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])

    with patch("yfinance.download", return_value=empty_df):
        candles = provider.fetch_data("UNKNOWN", period="1d", interval="1m")

        assert isinstance(candles, list)
        assert len(candles) == 0


def test_fetch_data_propagates_exception(provider):
    with patch("yfinance.download", side_effect=Exception("Network error")):
        with pytest.raises(Exception) as exc_info:
            provider.fetch_data("AAPL", period="1d", interval="1m")

        assert "Network error" in str(exc_info.value)
