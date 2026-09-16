import numpy as np
import pandas as pd
import pytest

from indicators.volatility import calculate_bollinger_bands


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
