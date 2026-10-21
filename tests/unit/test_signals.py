import pytest

from trade_companion.indicators import SwingPoint
from trade_companion.signals import (
    is_fast_over_slow_sma,
    is_hh_hl_trend,
    is_price_over_sma,
)


@pytest.mark.parametrize(
    "current_close, current_sma, expected",
    [
        (105.0, 100.0, True),
        (95.0, 100.0, False),
        (
            100.0,
            100.0,
            False,
        ),
        (100.0001, 100.0, True),
        (100.0, 100.0001, False),
        (0.0, 0.0, False),
        (-5.0, -10.0, True),
        (-10.0, -5.0, False),
    ],
)
def test_is_price_over_sma(
    current_close: float, current_sma: float, expected: bool
) -> None:
    assert is_price_over_sma(current_close, current_sma) is expected


@pytest.mark.parametrize(
    "current_close, current_sma",
    [
        (float("nan"), 100.0),
        (100.0, float("nan")),
        (float("nan"), float("nan")),
    ],
)
def test_is_price_over_sma_handles_nan_as_false(
    current_close: float, current_sma: float
) -> None:
    assert is_price_over_sma(current_close, current_sma) is False


@pytest.mark.parametrize(
    "current_fast, current_slow, expected",
    [
        (
            150.0,
            140.0,
            True,
        ),
        (135.0, 140.0, False),
        (140.0, 140.0, False),
        (140.0001, 140.0, True),
        (140.0, 140.0001, False),
        (200, 180, True),
        (150, 160, False),
        (0.0, 0.0, False),
        (0.5, 0.0, True),
        (-10.0, -20.0, True),
        (-30.0, -15.0, False),
    ],
)
def test_is_fast_over_slow_sma(
    current_fast: float, current_slow: float, expected: bool
) -> None:
    assert is_fast_over_slow_sma(current_fast, current_slow) is expected


@pytest.mark.parametrize(
    "current_fast, current_slow",
    [
        (float("nan"), 100.0),
        (100.0, float("nan")),
        (float("nan"), float("nan")),
    ],
)
def test_is_fast_over_slow_sma_handles_nan(
    current_fast: float, current_slow: float
) -> None:
    assert is_fast_over_slow_sma(current_fast, current_slow) is False


def test_is_fast_over_slow_sma_handles_infinity() -> None:
    assert is_fast_over_slow_sma(float("inf"), 100.0) is True
    assert is_fast_over_slow_sma(100.0, float("inf")) is False
    assert is_fast_over_slow_sma(100.0, float("-inf")) is True


def test_is_hh_hl_trend_returns_true_for_valid_uptrend() -> None:
    swings = [
        SwingPoint(index=1, price=80.0, type="LOW"),
        SwingPoint(index=3, price=100.0, type="HIGH"),
        SwingPoint(index=5, price=85.0, type="LOW"),
        SwingPoint(index=7, price=110.0, type="HIGH"),
    ]
    assert is_hh_hl_trend(swings) is True


def test_is_hh_hl_trend_returns_false_for_downtrend() -> None:
    swings = [
        SwingPoint(index=1, price=120.0, type="HIGH"),
        SwingPoint(index=3, price=100.0, type="LOW"),
        SwingPoint(index=5, price=110.0, type="HIGH"),
        SwingPoint(index=7, price=90.0, type="LOW"),
    ]
    assert is_hh_hl_trend(swings) is False


def test_is_hh_hl_trend_returns_false_for_higher_high_but_lower_low() -> None:
    swings = [
        SwingPoint(index=1, price=80.0, type="LOW"),
        SwingPoint(index=3, price=100.0, type="HIGH"),
        SwingPoint(index=5, price=75.0, type="LOW"),
        SwingPoint(index=7, price=115.0, type="HIGH"),
    ]
    assert is_hh_hl_trend(swings) is False


def test_is_hh_hl_trend_returns_false_for_lower_high_but_higher_low() -> None:
    swings = [
        SwingPoint(index=1, price=80.0, type="LOW"),
        SwingPoint(index=3, price=120.0, type="HIGH"),
        SwingPoint(index=5, price=85.0, type="LOW"),
        SwingPoint(index=7, price=110.0, type="HIGH"),
    ]
    assert is_hh_hl_trend(swings) is False


def test_is_hh_hl_trend_returns_false_when_highs_are_equal() -> None:
    swings = [
        SwingPoint(index=1, price=80.0, type="LOW"),
        SwingPoint(index=3, price=100.0, type="HIGH"),
        SwingPoint(index=5, price=85.0, type="LOW"),
        SwingPoint(index=7, price=100.0, type="HIGH"),
    ]
    assert is_hh_hl_trend(swings) is False


def test_is_hh_hl_trend_returns_false_when_lows_are_equal() -> None:
    swings = [
        SwingPoint(index=1, price=80.0, type="LOW"),
        SwingPoint(index=3, price=100.0, type="HIGH"),
        SwingPoint(index=5, price=80.0, type="LOW"),
        SwingPoint(index=7, price=110.0, type="HIGH"),
    ]
    assert is_hh_hl_trend(swings) is False


def test_is_hh_hl_trend_evaluates_only_latest_two_highs_and_lows() -> None:
    swings = [
        SwingPoint(index=1, price=150.0, type="HIGH"),
        SwingPoint(index=2, price=130.0, type="LOW"),
        SwingPoint(index=3, price=100.0, type="HIGH"),
        SwingPoint(index=4, price=80.0, type="LOW"),
        SwingPoint(index=5, price=110.0, type="HIGH"),
        SwingPoint(index=6, price=90.0, type="LOW"),
    ]
    assert is_hh_hl_trend(swings) is True


@pytest.mark.parametrize(
    "insufficient_swings",
    [
        [],
        [SwingPoint(index=1, price=100.0, type="HIGH")],
        [
            SwingPoint(index=1, price=100.0, type="HIGH"),
            SwingPoint(index=2, price=80.0, type="LOW"),
        ],
        [
            SwingPoint(index=1, price=100.0, type="HIGH"),
            SwingPoint(index=3, price=110.0, type="HIGH"),
            SwingPoint(index=2, price=80.0, type="LOW"),
        ],
        [
            SwingPoint(index=1, price=80.0, type="LOW"),
            SwingPoint(index=3, price=85.0, type="LOW"),
            SwingPoint(index=2, price=100.0, type="HIGH"),
        ],
    ],
)
def test_is_hh_hl_trend_returns_false_for_insufficient_swings(
    insufficient_swings: list[SwingPoint],
) -> None:
    assert is_hh_hl_trend(insufficient_swings) is False
