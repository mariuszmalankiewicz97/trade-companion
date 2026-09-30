import pandas as pd
import pytest

from support_resistance import (
    concat_low_and_high_price_zones,
    find_pivot_high,
    find_pivot_lows,
    find_the_high_price_zones,
    find_the_low_price_zones,
    merge_price_zones,
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


###
# CONCAT LOW AND HIGH PRICE ZONES
###


def test_concat_low_and_high_price_zones_type_error_invalid_low_zone():
    with pytest.raises(TypeError):
        low_zone = []
        high_zone = pd.DataFrame()
        concat_low_and_high_price_zones(low_zone, high_zone)


def test_concat_low_and_high_price_zones_type_error_invalid_high_zone():
    with pytest.raises(TypeError):
        low_zone = pd.DataFrame()
        high_zone = []
        concat_low_and_high_price_zones(low_zone, high_zone)


def test_concat_low_and_high_price_zones_returns_correct_structure():
    low_zone = pd.DataFrame()
    high_zone = pd.DataFrame()
    result = concat_low_and_high_price_zones(low_zone, high_zone)
    assert isinstance(result, pd.DataFrame)


###
# MERGE PRICE ZONES
###


def test_merge_price_zones_type_error_invalid_all_zones():
    with pytest.raises(TypeError):
        all_zones = ""
        last_atr = 2.3
        merge_price_zones(all_zones, last_atr)


def test_merge_price_zones_type_error_invalid_last_atr():
    with pytest.raises(TypeError):
        all_zones = pd.DataFrame()
        last_atr = "30"
        merge_price_zones(all_zones, last_atr)


def test_merge_price_zones_value_error_invalid_last_atr():
    with pytest.raises(ValueError):
        all_zones = pd.DataFrame()
        last_atr = 0.0
        merge_price_zones(all_zones, last_atr)


def test_merge_price_zones_all_zones_is_empty_return_empty_data_frame():
    all_zones = pd.DataFrame()
    last_atr = 2.30
    result = merge_price_zones(all_zones, last_atr)
    expected = pd.DataFrame()
    assert pd.DataFrame.equals(result, expected)


def test_merge_price_zones_returns_correct_values():
    all_zones = pd.DataFrame(
        {
            "date": ["2025-10-22 00:00:00-04:00", "2025-10-10 00:00:00-04:00"],
            "type": ["low", "low"],
            "bottom": [100.00, 103.00],
            "top": [102.00, 104.00],
        }
    )
    last_atr = 5.00
    result = merge_price_zones(all_zones, last_atr)
    expected = pd.DataFrame(
        {
            "first_date": "2025-10-10 00:00:00-04:00",
            "last_date": "2025-10-22 00:00:00-04:00",
            "bottom": 100.0,
            "top": 104.0,
            "touch_count": 2,
        },
        index=[0],
    )
    assert pd.DataFrame.equals(result, expected)
