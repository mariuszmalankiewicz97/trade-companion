import pandas as pd
import pytest

from support_resistance import (
    find_pivot_high,
    find_pivot_lows,
    find_the_high_price_zones,
    find_the_low_price_zones,
)

###
# FIND PIVOTS LOWS
###


def test_find_pivot_lows_type_error_invalid_low():
    with pytest.raises(TypeError):
        low = []
        period = 2
        find_pivot_lows(low, period)


def test_find_pivot_lows_type_error_invalid_period():
    with pytest.raises(TypeError):
        low = pd.Series()
        period = "2"
        find_pivot_lows(low, period)


def test_find_pivot_lows_value_error_invalid_period():
    with pytest.raises(ValueError):
        low = pd.Series()
        period = 0
        find_pivot_lows(low, period)


def test_find_pivot_lows_value_returns_correct_structure():
    low = pd.Series()
    period = 2
    result = find_pivot_lows(low, period)
    assert isinstance(result, pd.Series)


def test_find_pivot_lows_value_returns_correct_values():
    low = pd.Series(
        [100, 90, 80, 90, 100],
        index=[
            "2025-10-15 00:00:00-04:00",
            "2025-10-16 00:00:00-04:00",
            "2025-10-17 00:00:00-04:00",
            "2025-10-20 00:00:00-04:00",
            "2025-10-21 00:00:00-04:00",
        ],
    )
    period = 2
    result = find_pivot_lows(low, period)
    expected = pd.Series([80.0], index=["2025-10-17 00:00:00-04:00"])
    assert pd.Series.equals(result, expected)


###
# FIND THE LOW PRICE ZONES
###


def test_find_the_low_price_zones_type_error_invalid_low_pivots():
    with pytest.raises(TypeError):
        low_pivots = []
        atr = pd.Series()
        find_the_low_price_zones(low_pivots, atr)


def test_find_the_low_price_zones_type_error_invalid_atr():
    with pytest.raises(TypeError):
        low_pivots = pd.Series()
        atr = []
        find_the_low_price_zones(low_pivots, atr)


def test_find_the_low_price_zones_returns_correct_structure():
    low_pivots = pd.Series(
        [200, 190],
        index=[
            "2025-11-11 00:00:00-05:00",
            "2025-11-21 00:00:00-05:00",
        ],
    )
    atr = pd.Series(
        [5, 4],
        index=[
            "2025-11-11 00:00:00-05:00",
            "2025-11-21 00:00:00-05:00",
        ],
    )
    result = find_the_low_price_zones(low_pivots, atr)
    expected = pd.DataFrame(
        {
            "date": ["2025-11-11 00:00:00-05:00", "2025-11-21 00:00:00-05:00"],
            "type": ["low", "low"],
            "bottom": [200, 190],
            "top": [201.5, 191.2],
        }
    )
    assert pd.DataFrame.equals(result, expected)


###
# FIND PIVOTS HIGHS
###


def test_find_pivot_high_type_error_invalid_low():
    with pytest.raises(TypeError):
        low = []
        period = 2
        find_pivot_high(low, period)


def test_find_pivot_high_type_error_invalid_period():
    with pytest.raises(TypeError):
        low = pd.Series()
        period = "2"
        find_pivot_high(low, period)


def test_find_pivot_high_value_error_invalid_period():
    with pytest.raises(ValueError):
        low = pd.Series()
        period = 0
        find_pivot_high(low, period)


def test_find_pivot_high_value_returns_correct_structure():
    low = pd.Series()
    period = 2
    result = find_pivot_high(low, period)
    assert isinstance(result, pd.Series)


def test_find_pivot_high_value_returns_correct_values():
    low = pd.Series(
        [80, 90, 100, 90, 80],
        index=[
            "2025-10-15 00:00:00-04:00",
            "2025-10-16 00:00:00-04:00",
            "2025-10-17 00:00:00-04:00",
            "2025-10-20 00:00:00-04:00",
            "2025-10-21 00:00:00-04:00",
        ],
    )
    period = 2
    result = find_pivot_high(low, period)
    expected = pd.Series([100.0], index=["2025-10-17 00:00:00-04:00"])
    assert pd.Series.equals(result, expected)


###
# FIND THE LOW PRICE ZONES
###


def test_find_the_high_price_zones_type_error_invalid_low_pivots():
    with pytest.raises(TypeError):
        low_pivots = []
        atr = pd.Series()
        find_the_high_price_zones(low_pivots, atr)


def test_find_the_high_price_zones_type_error_invalid_atr():
    with pytest.raises(TypeError):
        low_pivots = pd.Series()
        atr = []
        find_the_high_price_zones(low_pivots, atr)


def test_find_the_high_price_zones_returns_correct_structure():
    low_pivots = pd.Series(
        [200, 190],
        index=[
            "2025-11-11 00:00:00-05:00",
            "2025-11-21 00:00:00-05:00",
        ],
    )
    atr = pd.Series(
        [5, 4],
        index=[
            "2025-11-11 00:00:00-05:00",
            "2025-11-21 00:00:00-05:00",
        ],
    )
    result = find_the_high_price_zones(low_pivots, atr)
    expected = pd.DataFrame(
        {
            "date": ["2025-11-11 00:00:00-05:00", "2025-11-21 00:00:00-05:00"],
            "type": ["high", "high"],
            "top": [200, 190],
            "bottom": [
                198.5,
                188.8,
            ],
        }
    )
    assert pd.DataFrame.equals(result, expected)
