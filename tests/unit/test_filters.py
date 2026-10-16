from unittest.mock import patch

import pandas as pd
import pytest

from trade_companion.filters import price_over_sma


def test_price_over_sma_invalid_close_type():
    with pytest.raises(TypeError, match="Close must be an pandas series"):
        price_over_sma([100.0, 105.0, 110.0], period=3)


def test_price_over_sma_invalid_period_type():
    close = pd.Series([10.0, 20.0, 30.0])
    with pytest.raises(TypeError, match="SMA period must be a integer"):
        price_over_sma(close, period="200")


def test_price_over_sma_series_shorter_than_period():
    close = pd.Series([100.0, 102.0, 101.0])
    assert price_over_sma(close, period=5) is False


def test_price_over_sma_empty_series():
    close = pd.Series([], dtype=float)
    assert price_over_sma(close, period=10) is False


@patch("trade_companion.filters.simple_moving_average")
def test_price_over_sma_returns_true_when_price_higher(mock_sma):
    close = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0])
    mock_sma.return_value = pd.Series([10.0, 15.0, 20.0, 25.0, 45.0])

    result = price_over_sma(close, period=5)

    assert result is True
    mock_sma.assert_called_once_with(close, 5)


@patch("trade_companion.filters.simple_moving_average")
def test_price_over_sma_returns_false_when_price_lower(mock_sma):
    close = pd.Series([50.0, 40.0, 30.0, 20.0, 10.0])
    mock_sma.return_value = pd.Series([50.0, 45.0, 40.0, 35.0, 15.0])

    result = price_over_sma(close, period=5)

    assert result is False
    mock_sma.assert_called_once_with(close, 5)


@patch("trade_companion.filters.simple_moving_average")
def test_price_over_sma_returns_false_when_price_equal_to_sma(mock_sma):
    close = pd.Series([100.0, 100.0, 100.0])
    mock_sma.return_value = pd.Series([100.0, 100.0, 100.0])

    result = price_over_sma(close, period=3)

    assert result is False


@pytest.mark.parametrize(
    "last_price, last_sma, expected",
    [
        (105.5, 100.0, True),
        (99.9, 100.0, False),
        (100.0, 100.0, False),
    ],
)
@patch("trade_companion.filters.simple_moving_average")
def test_price_over_sma_scenarios(mock_sma, last_price, last_sma, expected):
    close = pd.Series([100.0, 100.0, last_price])
    mock_sma.return_value = pd.Series([100.0, 100.0, last_sma])

    assert price_over_sma(close, period=3) is expected
