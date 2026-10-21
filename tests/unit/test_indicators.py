from dataclasses import FrozenInstanceError

import pandas as pd
import pytest

from trade_companion.indicators import (
    FibZone,
    SwingPoint,
    calculate_fib_zone,
    calculate_sma,
    clean_swings,
    find_raw_swings,
    get_active_trading_range,
)


def test_calculate_sma_raises_type_error_for_non_series() -> None:
    with pytest.raises(TypeError, match="Close must be a pandas series"):
        calculate_sma([10.0, 20.0, 30.0], period=2)


def test_calculate_sma_raises_type_error_for_non_numeric_series() -> None:
    text_series = pd.Series(["10", "20", "30"])
    with pytest.raises(TypeError, match="Close series must contain numeric data"):
        calculate_sma(text_series, period=2)


@pytest.mark.parametrize("invalid_period", [2.5, "3", [2], None, True, False])
def test_calculate_sma_raises_type_error_for_non_integer_period(
    invalid_period: object,
) -> None:
    prices = pd.Series([10.0, 20.0, 30.0])
    with pytest.raises(TypeError, match="Period must be an integer"):
        calculate_sma(prices, period=invalid_period)


@pytest.mark.parametrize("invalid_period", [0, -1, -50])
def test_calculate_sma_raises_value_error_for_non_positive_period(
    invalid_period: int,
) -> None:
    prices = pd.Series([10.0, 20.0, 30.0])
    with pytest.raises(ValueError, match="Period must be greater than 0"):
        calculate_sma(prices, period=invalid_period)


def test_calculate_sma_raises_value_error_when_period_exceeds_length() -> None:
    prices = pd.Series([10.0, 20.0])
    with pytest.raises(
        ValueError, match="Period can't be greater than length of close"
    ):
        calculate_sma(prices, period=3)


def test_swing_point_immutability() -> None:
    point = SwingPoint(index=5, price=100.0, type="HIGH")
    with pytest.raises(FrozenInstanceError):
        point.price = 105.0


def test_swing_point_equality() -> None:
    p1 = SwingPoint(index=2, price=50.0, type="LOW")
    p2 = SwingPoint(index=2, price=50.0, type="LOW")
    assert p1 == p2


def test_find_raw_swings_detects_isolated_peak_and_trough() -> None:
    highs = pd.Series([100.0, 110.0, 120.0, 110.0, 100.0, 90.0, 95.0, 100.0])
    lows = pd.Series([90.0, 95.0, 105.0, 95.0, 85.0, 80.0, 85.0, 90.0])

    result = find_raw_swings(highs, lows, window=2)

    assert result == [
        SwingPoint(index=2, price=120.0, type="HIGH"),
        SwingPoint(index=5, price=80.0, type="LOW"),
    ]


def test_find_raw_swings_returns_empty_when_series_lengths_differ() -> None:
    highs = pd.Series([10.0, 20.0, 30.0, 20.0, 10.0])
    lows = pd.Series([5.0, 10.0, 15.0])

    assert find_raw_swings(highs, lows, window=2) == []


def test_find_raw_swings_returns_empty_when_data_too_short() -> None:
    highs = pd.Series([10.0, 20.0, 30.0, 20.0, 10.0, 5.0])
    lows = pd.Series([5.0, 10.0, 15.0, 10.0, 5.0, 2.0])

    assert find_raw_swings(highs, lows, window=3) == []


def test_find_raw_swings_no_extrema_in_flat_market() -> None:
    highs = pd.Series([100.0] * 10)
    lows = pd.Series([90.0] * 10)

    assert find_raw_swings(highs, lows, window=2) == []


def test_find_raw_swings_results_are_sorted_by_index() -> None:
    highs = pd.Series([10.0, 12.0, 15.0, 11.0, 10.0, 8.0, 6.0, 9.0, 14.0, 11.0, 10.0])
    lows = pd.Series([8.0, 9.0, 11.0, 9.0, 7.0, 5.0, 4.0, 6.0, 10.0, 8.0, 7.0])

    result = find_raw_swings(highs, lows, window=2)
    indices = [point.index for point in result]

    assert indices == sorted(indices)


def test_clean_swings_empty_input() -> None:
    assert clean_swings([]) == []


def test_clean_swings_single_element() -> None:
    single = [SwingPoint(index=1, price=100.0, type="HIGH")]
    assert clean_swings(single) == single


def test_clean_swings_already_alternating() -> None:
    swings = [
        SwingPoint(index=2, price=120.0, type="HIGH"),
        SwingPoint(index=5, price=90.0, type="LOW"),
        SwingPoint(index=8, price=130.0, type="HIGH"),
        SwingPoint(index=11, price=95.0, type="LOW"),
    ]
    assert clean_swings(swings) == swings


def test_clean_swings_replaces_consecutive_highs_with_highest() -> None:
    swings = [
        SwingPoint(index=2, price=110.0, type="HIGH"),
        SwingPoint(index=4, price=125.0, type="HIGH"),
        SwingPoint(index=6, price=90.0, type="LOW"),
    ]

    result = clean_swings(swings)

    assert result == [
        SwingPoint(index=4, price=125.0, type="HIGH"),
        SwingPoint(index=6, price=90.0, type="LOW"),
    ]


def test_clean_swings_ignores_lower_consecutive_high() -> None:
    swings = [
        SwingPoint(index=2, price=130.0, type="HIGH"),
        SwingPoint(index=4, price=120.0, type="HIGH"),
        SwingPoint(index=6, price=85.0, type="LOW"),
    ]

    result = clean_swings(swings)

    assert result == [
        SwingPoint(index=2, price=130.0, type="HIGH"),
        SwingPoint(index=6, price=85.0, type="LOW"),
    ]


def test_clean_swings_replaces_consecutive_lows_with_lowest() -> None:
    swings = [
        SwingPoint(index=2, price=120.0, type="HIGH"),
        SwingPoint(index=5, price=95.0, type="LOW"),
        SwingPoint(index=7, price=85.0, type="LOW"),
    ]

    result = clean_swings(swings)

    assert result == [
        SwingPoint(index=2, price=120.0, type="HIGH"),
        SwingPoint(index=7, price=85.0, type="LOW"),
    ]


def test_clean_swings_multiple_consecutive_same_type() -> None:
    swings = [
        SwingPoint(index=1, price=100.0, type="HIGH"),
        SwingPoint(index=3, price=90.0, type="LOW"),
        SwingPoint(index=5, price=80.0, type="LOW"),
        SwingPoint(index=7, price=85.0, type="LOW"),
        SwingPoint(index=9, price=115.0, type="HIGH"),
    ]

    result = clean_swings(swings)

    assert result == [
        SwingPoint(index=1, price=100.0, type="HIGH"),
        SwingPoint(index=5, price=80.0, type="LOW"),
        SwingPoint(index=9, price=115.0, type="HIGH"),
    ]


def test_fib_zone_immutability() -> None:
    zone = FibZone(base_low=100.0, peak_high=150.0, fib_50=125.0, fib_618=119.1)
    with pytest.raises(FrozenInstanceError):
        zone.fib_50 = 130.0


def test_fib_zone_equality() -> None:
    z1 = FibZone(base_low=100.0, peak_high=150.0, fib_50=125.0, fib_618=119.1)
    z2 = FibZone(base_low=100.0, peak_high=150.0, fib_50=125.0, fib_618=119.1)
    assert z1 == z2


def test_calculate_fib_zone_standard_values() -> None:
    zone = calculate_fib_zone(base_low=100.0, peak_high=150.0)

    assert zone.base_low == 100.0
    assert zone.peak_high == 150.0
    assert zone.fib_50 == 125.0
    assert zone.fib_618 == 119.1


def test_calculate_fib_zone_precision_rounding() -> None:
    zone = calculate_fib_zone(base_low=10.1111, peak_high=33.3333)

    assert zone.fib_50 == 21.7222
    assert zone.fib_618 == 18.982


def test_calculate_fib_zone_small_impulse() -> None:
    zone = calculate_fib_zone(base_low=1.0, peak_high=2.0)
    assert zone.fib_50 == 1.5
    assert zone.fib_618 == 1.382


def test_get_active_trading_range_standard_uptrend() -> None:
    swings = [
        SwingPoint(index=10, price=80.0, type="LOW"),
        SwingPoint(index=20, price=120.0, type="HIGH"),
        SwingPoint(index=30, price=100.0, type="LOW"),
        SwingPoint(index=40, price=150.0, type="HIGH"),
    ]

    zone = get_active_trading_range(swings)

    assert zone is not None
    assert zone.base_low == 100.0
    assert zone.peak_high == 150.0
    assert zone.fib_50 == 125.0
    assert zone.fib_618 == 119.1


def test_get_active_trading_range_ignores_new_low_formed_after_peak() -> None:
    swings = [
        SwingPoint(index=10, price=80.0, type="LOW"),
        SwingPoint(index=20, price=120.0, type="HIGH"),
        SwingPoint(index=30, price=100.0, type="LOW"),
        SwingPoint(index=40, price=150.0, type="HIGH"),
        SwingPoint(index=55, price=122.0, type="LOW"),
    ]

    zone = get_active_trading_range(swings)

    assert zone is not None
    assert zone.base_low == 100.0
    assert zone.peak_high == 150.0
    assert zone.fib_50 == 125.0
    assert zone.fib_618 == 119.1


def test_get_active_trading_range_returns_none_when_insufficient_points() -> None:
    too_few_swings = [
        SwingPoint(index=10, price=100.0, type="LOW"),
        SwingPoint(index=20, price=150.0, type="HIGH"),
        SwingPoint(index=30, price=120.0, type="LOW"),
    ]
    assert get_active_trading_range(too_few_swings) is None
    assert get_active_trading_range([]) is None


def test_get_active_trading_range_returns_none_when_no_low_before_latest_high() -> None:
    corrupted_sequence = [
        SwingPoint(index=5, price=150.0, type="HIGH"),
        SwingPoint(index=10, price=160.0, type="HIGH"),
        SwingPoint(index=20, price=100.0, type="LOW"),
        SwingPoint(index=30, price=110.0, type="LOW"),
    ]
    assert get_active_trading_range(corrupted_sequence) is None
