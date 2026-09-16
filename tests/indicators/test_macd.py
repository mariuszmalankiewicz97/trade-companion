import pandas as pd
import pytest

from indicators.macd import calculate_histogram, calculate_macd, calculate_signal
from indicators.moving_averages import calculate_ema


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


def test_calculate_macd_raises_value_error_for_invalid_fast_period():
    with pytest.raises(ValueError):
        close = pd.Series([10, 12, 14, 11, 15])
        fast_period = -1
        slow_period = 3
        calculate_macd(close, fast_period, slow_period)


def test_calculate_macd_raises_value_error_for_invalid_slow_period():
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
