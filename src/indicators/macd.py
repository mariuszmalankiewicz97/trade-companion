import pandas as pd

from indicators.moving_averages import calculate_ema
from indicators.validation import (
    validate_is_series,
    validate_period,
    validate_signal_period,
)


def calculate_macd(close: pd.Series, fast_period: int, slow_period: int) -> pd.Series:
    validate_is_series(close, "Close")
    validate_period(fast_period, "Fast period")
    validate_period(slow_period, "Slow period")
    if fast_period > slow_period:
        raise ValueError("Fast period can't be greater than slow period")
    ema_fast: pd.Series = calculate_ema(close, fast_period)
    ema_slow: pd.Series = calculate_ema(close, slow_period)
    macd: pd.Series = ema_fast - ema_slow
    return macd


def calculate_signal(macd: pd.Series, signal_period: int) -> pd.Series:
    validate_is_series(macd, "MACD")
    validate_signal_period(signal_period)
    signal: pd.Series = calculate_ema(macd, signal_period)
    return signal


def calculate_histogram(macd: pd.Series, signal: pd.Series) -> pd.Series:
    validate_is_series(macd, "MACD")
    validate_is_series(signal, "Signal")
    histogram: pd.Series = macd - signal
    return histogram
