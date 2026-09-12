import numpy as np
import pandas as pd


def validate_indicator_inputs(close: pd.Series, period: int) -> None:
    if not isinstance(close, pd.Series):
        raise TypeError("Close must be a series")
    if not isinstance(period, int):
        raise TypeError("Period must be an integer")
    if period < 1:
        raise ValueError("Period can't be less than 1")


def calculate_sma(close: pd.Series, period: int) -> pd.Series:
    validate_indicator_inputs(close, period)
    return close.rolling(period).mean()


def calculate_ema(close: pd.Series, period: int) -> pd.Series:
    validate_indicator_inputs(close, period)
    return close.ewm(span=period).mean()


def calculate_rsi(close: pd.Series, period: int) -> pd.Series:
    validate_indicator_inputs(close, period)
    diff: pd.Series = close.diff()
    gain: list | pd.Series = []
    loss: list | pd.Series = []
    for ele in diff:
        if pd.isna(ele):
            gain.append(np.nan)
            loss.append(np.nan)
        elif ele >= 0:
            gain.append(ele)
            loss.append(0)
        elif ele < 0:
            ele = ele * -1
            loss.append(ele)
            gain.append(0)
    gain: list | pd.Series = pd.Series(gain)
    loss: list | pd.Series = pd.Series(loss)
    avg_gain: pd.Series = gain.rolling(period).mean()
    avg_loss: pd.Series = loss.rolling(period).mean()
    rs: pd.Series = avg_gain / avg_loss
    rsi: pd.Series = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(close: pd.Series, fast_period: int, slow_period: int) -> pd.Series:
    if not isinstance(fast_period, int):
        raise TypeError("Fast period must be an integer")
    if not isinstance(fast_period, int):
        raise TypeError("Slow period must be an integer")
    if fast_period < 1:
        raise ValueError("Fast peroid can't be less than 1")
    if slow_period < 1:
        raise ValueError("Slow peroid can't be less than 1")
    if fast_period > slow_period:
        raise ValueError("Fast period can't be less that slow period")
    ema_fast: pd.Series = calculate_ema(close, fast_period)
    ema_slow: pd.Series = calculate_ema(close, slow_period)
    macd: pd.Series = ema_fast - ema_slow
    return macd


def calculate_signal(macd: pd.Series, signal_period: int) -> pd.Series:
    if not isinstance(macd, pd.Series):
        raise TypeError("MACD must be a Series")
    if not isinstance(signal_period, int):
        raise TypeError("Signal period must be an integer")
    if signal_period < 1:
        raise ValueError("Signal period can't be less that 1")
    signal: pd.Series = calculate_ema(macd, signal_period)
    return signal


def calculate_histogram(macd: pd.Series, signal: pd.Series) -> pd.Series:
    if not isinstance(macd, pd.Series):
        raise TypeError("MACD must be a Series")
    if not isinstance(signal, pd.Series):
        raise TypeError("Signal must be a Series")
    histogram: pd.Series = macd - signal
    return histogram
