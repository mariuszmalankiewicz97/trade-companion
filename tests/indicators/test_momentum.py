import numpy as np
import pandas as pd
import pytest

from src.indicators.momentum import calculate_rsi


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
