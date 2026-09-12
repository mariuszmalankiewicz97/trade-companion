import numpy as np
import pandas as pd
import pytest

from indicators import calculate_ema, calculate_rsi, calculate_sma


def test_calculate_sma_returns_series():
    test_data = [10, 12, 14, 16, 18, 20]
    period = 5
    close = pd.Series(test_data)
    result = calculate_sma(close, period)
    assert isinstance(result, pd.Series)


def test_calculate_sma_return_correct_period():
    test_data = [10, 12, 14, 16, 18, 20]
    period = 5
    close = pd.Series(test_data)
    result = calculate_sma(close, period)
    expected = pd.Series([np.nan, np.nan, np.nan, np.nan, 14.0, 16.0])
    assert pd.Series.equals(result, expected)


def test_calculate_sma_return_incorrect_type_period():
    with pytest.raises(TypeError):
        test_data = [10, 12, 14, 16, 18, 20]
        period = 5.5
        close = pd.Series(test_data)
        calculate_sma(close, period)


def test_calculate_sma_return_incorrect_period():
    with pytest.raises(ValueError):
        test_data = [10, 12, 14, 16, 18, 20]
        period = -5
        close = pd.Series(test_data)
        calculate_sma(close, period)


def test_calculate_sma_with_period_longer_than_data():
    test_data = [10, 12, 14]
    period = 5
    close = pd.Series(test_data)
    result = calculate_sma(close, period)
    expected = pd.Series([np.nan, np.nan, np.nan])
    assert pd.Series.equals(result, expected)


def test_calculate_sma_with_close_is_not_series():
    with pytest.raises(TypeError):
        close = [10, 12, 14, 16, 18, 20]
        period = 5
        calculate_sma(close, period)


def test_calculate_ema_returns_series():
    test_data = [10, 12, 14, 16, 18, 20]
    period = 5
    close = pd.Series(test_data)
    result = calculate_ema(close, period)
    assert isinstance(result, pd.Series)


def test_calculate_ema_returns_correct_values():
    test_data = [10, 12, 14, 16, 18, 20]
    period = 5
    close = pd.Series(test_data)
    expected = pd.Series([10.00, 11.20, 12.53, 13.97, 15.52, 17.15])
    result = calculate_ema(close, period)
    assert pd.Series.equals(round(result, 2), round(expected, 2))


def test_calculate_ema_with_close_is_not_series():
    with pytest.raises(TypeError):
        close = [10, 12, 14, 16, 18, 20]
        period = 5
        calculate_ema(close, period)


def test_calculate_ema_incorrect_period():
    with pytest.raises(ValueError):
        test_data = [10, 12, 14, 16, 18, 20]
        period = -5
        close = pd.Series(test_data)
        calculate_ema(close, period)


def test_calculate_incorrect_type_period():
    with pytest.raises(TypeError):
        test_data = [10, 12, 14, 16, 18, 20]
        period = "5"
        close = pd.Series(test_data)
        calculate_ema(close, period)


def test_calculate_rsi_returns_series():
    close = pd.Series([10, 12, 14, 11, 15])
    period = 3
    result = calculate_rsi(close, period)
    assert isinstance(result, pd.Series)


def test_calculate_rsi_returns_correct_values():
    close = pd.Series([10, 12, 14, 11, 15])
    period = 2
    result = calculate_rsi(close, period)
    expected = pd.Series([np.nan, np.nan, 100.00, 40.00, 57.14])
    assert pd.Series.equals(round(result, 2), expected)


def test_calculate_rsi_raises_type_error_for_invalid_close():
    with pytest.raises(TypeError):
        close = [10, 12, 14, 11, 15]
        period = 2
        calculate_rsi(close, period)


def test_calculate_rsi_raises_type_error_for_invalid_period():
    with pytest.raises(TypeError):
        close = pd.Series([10, 12, 14, 11, 15])
        period = 2.5
        calculate_rsi(close, period)


def test_calculate_rsi_raises_value_error_for_invalid_period():
    with pytest.raises(ValueError):
        close = pd.Series([10, 12, 14, 11, 15])
        period = -2
        calculate_rsi(close, period)


def test_calculate_rsi_returns_nan_before_enough_data():
    close = pd.Series([10, 12])
    period = 3
    result = calculate_rsi(close, period)
    expected = pd.Series([np.nan, np.nan])
    assert pd.Series.equals(result, expected)
