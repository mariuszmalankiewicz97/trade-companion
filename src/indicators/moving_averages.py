import pandas as pd
from validation import validate_close, validate_period


def calculate_sma(close: pd.Series, period: int) -> pd.Series:
    validate_close(close)
    validate_period(period)
    return close.rolling(period).mean()


def calculate_ema(close: pd.Series, period: int) -> pd.Series:
    validate_close(close)
    validate_period(period)
    return close.ewm(span=period).mean()
