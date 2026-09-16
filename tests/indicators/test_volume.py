import pandas as pd
import pytest

from indicators.volume import calculate_average_volume


def test_calculate_average_volume_returns_values_float():
    volume = pd.Series([100, 200, 300])
    period = 2
    result = calculate_average_volume(volume, period)
    assert isinstance(result, float)


def test_calculate_average_volume_arg_volume_is_series():
    with pytest.raises(TypeError):
        volume = [100, 200, 300]
        period = 2
        calculate_average_volume(volume, period)


def test_calculate_average_volume_arg_period_is_integer():
    with pytest.raises(TypeError):
        volume = pd.Series()
        period = "2"
        calculate_average_volume(volume, period)


def test_calculate_average_volume_period_cant_be_less_than_one():
    with pytest.raises(ValueError):
        volume = pd.Series([100, 200, 300, 400])
        period = 0
        calculate_average_volume(volume, period)


def test_calculate_average_volume_volume_length_cant_be_less_than_period():
    with pytest.raises(ValueError):
        volume = pd.Series([100, 200, 300, 400])
        period = 20
        calculate_average_volume(volume, period)


def test_calculate_average_volume_excludes_last_day():
    volume = pd.Series([100, 200, 300, 400, 1000])
    period = 4
    result = calculate_average_volume(volume, period)
    expected = 250.0
    assert result == expected
