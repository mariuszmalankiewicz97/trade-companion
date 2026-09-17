import pandas as pd
import pytest

from support_resistance import find_pivot_lows


def test_find_pivot_lows_raises_type_error_for_invalid_low():
    with pytest.raises(TypeError):
        low = [10, 12, 14]
        period = 2
        find_pivot_lows(low, period)


def test_find_pivot_lows_raises_type_error_for_invalid_period():
    with pytest.raises(TypeError):
        low = pd.Series([10, 12, 14])
        period = "2"
        find_pivot_lows(low, period)


def test_find_pivot_lows_raises_value_error_for_invalid_period():
    with pytest.raises(ValueError):
        low = pd.Series([10, 12, 14])
        period = 0
        find_pivot_lows(low, period)


def test_find_pivot_lows_returns_correct_structure():
    low = pd.Series([10, 12, 14])
    period = 2
    result = find_pivot_lows(low, period)
    assert isinstance(result, pd.Series)


def test_find_pivot_lows_returns_correct_values():
    low = pd.Series([10.0, 8.0, 4.0, 5.0, 4.0, 3.0, 9.0, 11.0])
    period = 2
    result = find_pivot_lows(low, period)
    expected = pd.Series([4.0, 3.0], index=[2, 5])
    assert pd.Series.equals(result, expected)
