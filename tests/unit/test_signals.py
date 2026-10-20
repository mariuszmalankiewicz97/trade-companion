import pytest

from trade_companion.signals import is_fast_over_slow_sma, is_price_over_sma


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
