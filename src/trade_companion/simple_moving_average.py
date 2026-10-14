import pandas as pd


def simple_moving_average(close: pd.Series, period: int) -> pd.Series:
    if not isinstance(close, pd.Series):
        raise TypeError("Close must be a pandas series")
    if not pd.api.types.is_numeric_dtype(close):
        raise TypeError("Period must be an integer")
    if period <= 0:
        raise ValueError("Period must be greater than 0")
    if period > len(close):
        raise ValueError("Period can't be greater than length of close")
    return close.rolling(window=period).mean()
