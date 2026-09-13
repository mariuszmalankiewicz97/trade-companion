import numpy as np
import pandas as pd


def validate_indicator_inputs(close: pd.Series, period: int) -> None:
    if not isinstance(close, pd.Series):
        raise TypeError("Close must be a series")
    if not isinstance(period, int):
        raise TypeError("Period must be an integer")
    if period < 1:
        raise ValueError("Period can't be less than 1")


def validate_std_multiplier(std_multiplier: float | int) -> None:
    if not isinstance(std_multiplier, float | int):
        raise TypeError("Std multiplier must be a float or integer")
    if std_multiplier <= 0:
        raise ValueError("Std multiplier must be greater than 0")


def validate_macd_inputs(close: pd.Series, fast_period: int, slow_period: int) -> None:
    if not isinstance(close, pd.Series):
        raise TypeError("Close must be a series")
    if not isinstance(fast_period, int):
        raise TypeError("Fast period must be an integer")
    if not isinstance(slow_period, int):
        raise TypeError("Slow period must be an integer")
    if slow_period < 1:
        raise ValueError("Slow period can't be less than 1")
    if fast_period < 1:
        raise ValueError("Fast period can't be less than 1")
    if fast_period > slow_period:
        raise ValueError("Fast period can't be greater than slow period")


def validate_macd(macd) -> None:
    if not isinstance(macd, pd.Series):
        raise TypeError("MACD must be a Series")


def validate_signal_period(signal_period: int) -> None:
    if not isinstance(signal_period, int):
        raise TypeError("Signal period must be an integer")
    if signal_period < 1:
        raise ValueError("Signal period can't be less than 1")


def validate_signal(signal: pd.Series) -> None:
    if not isinstance(signal, pd.Series):
        raise TypeError("Signal must be a Series")


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
    validate_macd_inputs(close, fast_period, slow_period)
    ema_fast: pd.Series = calculate_ema(close, fast_period)
    ema_slow: pd.Series = calculate_ema(close, slow_period)
    macd: pd.Series = ema_fast - ema_slow
    return macd


def calculate_signal(macd: pd.Series, signal_period: int) -> pd.Series:
    validate_macd(macd)
    validate_signal_period(signal_period)
    signal: pd.Series = calculate_ema(macd, signal_period)
    return signal


def calculate_histogram(macd: pd.Series, signal: pd.Series) -> pd.Series:
    validate_macd(macd)
    validate_signal(signal)
    histogram: pd.Series = macd - signal
    return histogram


def calculate_bollinger_bands(
    close: pd.Series, period: int, std_multiplier: float | int
) -> dict:
    validate_indicator_inputs(close, period)
    validate_std_multiplier(std_multiplier)
    middle: pd.Series = calculate_sma(close, period)
    std: pd.Series = close.rolling(period).std()
    upper: pd.Series = middle + std_multiplier * std
    lower: pd.Series = middle - std_multiplier * std
    return {"middle": middle, "upper": upper, "lower": lower}
