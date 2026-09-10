import pandas as pd


def validate_indicator_inputs(close, period):
    if not isinstance(close, pd.Series):
        raise TypeError("Close must be a series")
    if not isinstance(period, int):
        raise TypeError("Period must be an integer")
    if period < 1:
        raise ValueError("Period can't be less than 1")


def calculate_sma(close, period):
    validate_indicator_inputs(close, period)
    return close.rolling(period).mean()


def calculate_ema(close, period):
    validate_indicator_inputs(close, period)
    return close.ewm(span=period).mean()
