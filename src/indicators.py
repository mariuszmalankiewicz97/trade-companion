import pandas as pd


def calculate_sma(close, period):
    if not isinstance(close, pd.Series):
        raise TypeError("Close must by a series")
    if not isinstance(period, int):
        raise TypeError("Period must be an integer")
    if period < 1:
        raise ValueError("Period can't be less than 1")
    return close.rolling(period).mean()


def calculate_ema(close, period):
    if not isinstance(close, pd.Series):
        raise TypeError("Close must by a series")
    if period < 1:
        raise ValueError("Period can't be less than 1")
    if not isinstance(period, int):
        raise TypeError("Period must be an integer")
    return close.ewm(period).mean()
