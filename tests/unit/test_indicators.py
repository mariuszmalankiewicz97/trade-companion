import pandas as pd
import pytest

from trade_companion.indicators import calculate_sma


def test_calculate_sma_raises_type_error_for_non_series() -> None:
    with pytest.raises(TypeError, match="Close must be a pandas series"):
        calculate_sma([10.0, 20.0, 30.0], period=2)


def test_calculate_sma_raises_type_error_for_non_numeric_series() -> None:
    text_series = pd.Series(["10", "20", "30"])
    with pytest.raises(TypeError, match="Close series must contain numeric data"):
        calculate_sma(text_series, period=2)


@pytest.mark.parametrize("invalid_period", [2.5, "3", [2], None, True, False])
def test_calculate_sma_raises_type_error_for_non_integer_period(
    invalid_period: object,
) -> None:
    prices = pd.Series([10.0, 20.0, 30.0])
    with pytest.raises(TypeError, match="Period must be an integer"):
        calculate_sma(prices, period=invalid_period)


@pytest.mark.parametrize("invalid_period", [0, -1, -50])
def test_calculate_sma_raises_value_error_for_non_positive_period(
    invalid_period: int,
) -> None:
    prices = pd.Series([10.0, 20.0, 30.0])
    with pytest.raises(ValueError, match="Period must be greater than 0"):
        calculate_sma(prices, period=invalid_period)


def test_calculate_sma_raises_value_error_when_period_exceeds_length() -> None:
    prices = pd.Series([10.0, 20.0])
    with pytest.raises(
        ValueError, match="Period can't be greater than length of close"
    ):
        calculate_sma(prices, period=3)
