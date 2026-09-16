import pandas as pd

from indicators.validation import validate_is_series, validate_period


def calculate_sma(close: pd.Series, period: int) -> pd.Series:
    validate_is_series(close, "Close")
    validate_period(period)
    return close.rolling(period).mean()


def calculate_ema(close: pd.Series, period: int) -> pd.Series:
    validate_is_series(close, "Close")
    validate_period(period)
    return close.ewm(span=period).mean()
