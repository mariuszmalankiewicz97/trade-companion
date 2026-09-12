import numpy as np
import pandas as pd
import pytest

from indicators import (
    calculate_bollinger_bands,
    calculate_ema,
    calculate_histogram,
    calculate_macd,
    calculate_rsi,
    calculate_signal,
    calculate_sma,
)


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


def test_calculate_macd_returns_series():
    close = pd.Series([10, 12, 14, 11, 15])
    fast_period = 2
    slow_period = 3
    result = calculate_macd(close, fast_period, slow_period)
    assert isinstance(result, pd.Series)


def test_calculate_macd_returns_correct_values():
    close = pd.Series([10, 12, 14, 11, 15])
    fast_period = 2
    slow_period = 3
    ema_fast = calculate_ema(close, fast_period)
    ema_slow = calculate_ema(close, slow_period)
    macd = ema_fast - ema_slow
    result = calculate_macd(close, fast_period, slow_period)
    assert pd.Series.equals(round(result, 2), round(macd, 2))


def test_calculate_macd_raises_type_error_for_invalid_fast_period():
    with pytest.raises(TypeError):
        close = pd.Series([10, 12, 14, 11, 15])
        fast_period = 2.5
        slow_period = 3
        calculate_macd(close, fast_period, slow_period)


def test_calculate_macd_raises_type_error_for_invalid_slow_period():
    with pytest.raises(TypeError):
        close = pd.Series([10, 12, 14, 11, 15])
        fast_period = 2
        slow_period = 3.5
        calculate_macd(close, fast_period, slow_period)


def test_calculate_macd_raises_value_error_forinvalid_fast_period():
    with pytest.raises(ValueError):
        close = pd.Series([10, 12, 14, 11, 15])
        fast_period = -1
        slow_period = 3
        calculate_macd(close, fast_period, slow_period)


def test_calculate_macd_raises_value_error_forinvalid_slow_period():
    with pytest.raises(ValueError):
        close = pd.Series([10, 12, 14, 11, 15])
        fast_period = 2
        slow_period = -1
        calculate_macd(close, fast_period, slow_period)


def test_calculate_macd_raises_value_error_when_fast_period_is_greater_that_slow_period():
    with pytest.raises(ValueError):
        close = pd.Series([10, 12, 14, 11, 15])
        fast_period = 3
        slow_period = 2
        calculate_macd(close, fast_period, slow_period)


def test_calculate_signal_returns_series():
    close = pd.Series([10, 12, 14, 11, 15])
    fast_period = 2
    slow_period = 3
    macd = calculate_macd(close, fast_period, slow_period)
    signal_period = 2
    assert isinstance(calculate_signal(macd, signal_period), pd.Series)


def test_calculate_signal_returns_correct_values():
    close = pd.Series([10, 12, 14, 11, 15])
    fast_period = 2
    slow_period = 3
    macd = calculate_macd(close, fast_period, slow_period)
    signal_period = 2
    expected = calculate_ema(macd, signal_period)
    result = calculate_signal(macd, signal_period)
    assert pd.Series.equals(result, expected)


def test_calculate_signal_invalid_macd_type():
    with pytest.raises(TypeError):
        macd = [12, 13, 14, 16]
        signal_period = 2
        calculate_signal(macd, signal_period)


def test_calculate_signal_invalid_signal_period_type():
    with pytest.raises(TypeError):
        close = pd.Series([10, 12, 14, 11, 15])
        fast_period = 2
        slow_period = 3
        macd = calculate_macd(close, fast_period, slow_period)
        signal_period = 2.5
        calculate_signal(macd, signal_period)


def test_calculate_signal_invalid_signal_period_value():
    with pytest.raises(ValueError):
        close = pd.Series([10, 12, 14, 11, 15])
        fast_period = 2
        slow_period = 3
        macd = calculate_macd(close, fast_period, slow_period)
        signal_period = -5
        calculate_signal(macd, signal_period)


def test_calculate_histogram_macd_returns_series():
    close = pd.Series([10, 12, 14, 11, 15])
    fast_period = 2
    slow_period = 3
    macd = calculate_macd(close, fast_period, slow_period)
    signal_period = 2
    signal = calculate_signal(macd, signal_period)
    result = calculate_histogram(macd, signal)
    assert isinstance(result, pd.Series)


def test_calculate_histogram_returns_correct_values():
    close = pd.Series([10, 12, 14, 11, 15])
    fast_period = 2
    slow_period = 3
    macd = calculate_macd(close, fast_period, slow_period)
    signal_period = 2
    signal = calculate_signal(macd, signal_period)
    result = calculate_histogram(macd, signal)
    excepted = macd - signal
    assert pd.Series.equals(result, excepted)


def test_calculate_histogram_invalid_macd_type():
    with pytest.raises(TypeError):
        macd = 1
        signal = pd.Series([0.12, 0.3, 0.1])
        calculate_histogram(macd, signal)


def test_calculate_histogram_invalid_signal_type():
    with pytest.raises(TypeError):
        close = pd.Series([10, 12, 14, 11, 15])
        fast_period = 2
        slow_period = 3
        macd = calculate_macd(close, fast_period, slow_period)
        signal = 1
        calculate_histogram(macd, signal)


def test_calculate_bollinger_bands_returns_dict():
    close = pd.Series([10, 12, 14, 16, 18])
    period = 3
    std_multiplier = 2
    result = calculate_bollinger_bands(close, period, std_multiplier)
    assert isinstance(result, dict)


def test_calculate_bollinger_bands_returns_three_series():
    close = pd.Series([10, 12, 14, 16, 18])
    period = 3
    std_multiplier = 2.0
    result = calculate_bollinger_bands(close, period, std_multiplier)
    assert isinstance(result["middle"], pd.Series)
    assert isinstance(result["upper"], pd.Series)
    assert isinstance(result["lower"], pd.Series)


def test_calculate_bollinger_bands_returns_correct_values():
    close = pd.Series([10, 12, 14, 16, 18])
    period = 3
    std_multiplier = 2.0
    result = calculate_bollinger_bands(close, period, std_multiplier)
    assert pd.Series.equals(
        result["middle"], pd.Series([np.nan, np.nan, 12.0, 14.0, 16.0])
    )
    assert pd.Series.equals(
        result["upper"], pd.Series([np.nan, np.nan, 16.0, 18.0, 20.0])
    )
    assert pd.Series.equals(
        result["lower"], pd.Series([np.nan, np.nan, 8.0, 10.0, 12.0])
    )


def test_calculate_bollinger_bands_invalid_type_error_close():
    with pytest.raises(TypeError):
        close = 10
        period = 3
        std_multiplier = 2.0
        calculate_bollinger_bands(close, period, std_multiplier)


def test_calculate_bollinger_bands_invalid_type_error_period():
    with pytest.raises(TypeError):
        close = pd.Series([10, 12, 14, 16, 18])
        period = "3"
        std_multiplier = 2.0
        calculate_bollinger_bands(close, period, std_multiplier)


def test_calculate_bollinger_bands_invalid_value_error_period():
    with pytest.raises(ValueError):
        close = pd.Series([10, 12, 14, 16, 18])
        period = -1
        std_multiplier = 2.0
        calculate_bollinger_bands(close, period, std_multiplier)


def test_calculate_bollinger_bands_invalid_type_error_std_multiplier():
    with pytest.raises(TypeError):
        close = pd.Series([10, 12, 14, 16, 18])
        period = 3
        std_multiplier = "2"
        calculate_bollinger_bands(close, period, std_multiplier)


def test_calculate_bollinger_bands_invalid_value_error_std_multiplier():
    with pytest.raises(ValueError):
        close = pd.Series([10, 12, 14, 16, 18])
        period = 3
        std_multiplier = 0
        calculate_bollinger_bands(close, period, std_multiplier)
