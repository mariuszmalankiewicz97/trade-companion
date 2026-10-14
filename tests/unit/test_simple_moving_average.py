import numpy as np
import pandas as pd
import pytest

from trade_companion.simple_moving_average import simple_moving_average


def test_simple_moving_average_return_correct_values():
    close = pd.Series([10, 20, 30, 40, 50], dtype=float)
    period = 3
    result = simple_moving_average(close, period)
    expected = pd.Series(
        [np.nan, np.nan, 20.0, 30.0, 40.0], index=[0, 1, 2, 3, 4], dtype=float
    )
    assert isinstance(result, pd.Series)
    pd.testing.assert_series_equal(result, expected)


def test_simple_moving_average_invalid_type_close():
    with pytest.raises(TypeError):
        close = [10, 20, 30, 40, 50]
        period = 3
        simple_moving_average(close, period)


def test_simple_moving_average_invalid_type_period():
    with pytest.raises(TypeError):
        close = pd.Series([10, 20, 30, 40, 50], dtype=float)
        period = "3"
        simple_moving_average(close, period)


def test_simple_moving_average_invalid_value_period():
    with pytest.raises(ValueError):
        close = pd.Series([10, 20, 30, 40, 50], dtype=float)
        period = 0
        simple_moving_average(close, period)
    with pytest.raises(ValueError):
        close = pd.Series([10, 20, 30, 40, 50], dtype=float)
        period = -1
        simple_moving_average(close, period)


def test_simple_moving_average_invalid_period_greater_that_lenght_close():
    with pytest.raises(ValueError):
        close = pd.Series([10, 20], dtype=float)
        period = 3
        simple_moving_average(close, period)


def test_simple_moving_average_only_nan_values_in_close():
    with pytest.raises(ValueError):
        close = pd.Series([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan], dtype=float)
        period = 3
        expected = pd.Series(
            [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            index=[1, 2, 3, 4, 5],
            dtype=float,
        )
        result = simple_moving_average(close, period)
        pd.testing.assert_series_equal(result, expected)


def test_simple_moving_average_nan_value_in_middle_values():
    with pytest.raises(ValueError):
        close = pd.Series([10.0, 20.0, np.nan, 40.0, 50.0, 60.0], dtype=float)
        period = 3
        expected = pd.Series(
            [np.nan, np.nan, np.nan, np.nan, np.nan, 50.0],
            index=[1, 2, 3, 4, 5],
            dtype=float,
        )
        result = simple_moving_average(close, period)
        pd.testing.assert_series_equal(result, expected)
