import pandas as pd

from trade_companion.simple_moving_average import simple_moving_average


def price_over_sma(close: pd.Series, period: int = 200) -> bool:
    if not isinstance(close, pd.Series):
        raise TypeError("Close must be an pandas series")
    if not isinstance(period, int):
        raise TypeError("SMA period must be a integer")
    if len(close) < period:
        return False
    sma = simple_moving_average(close, period)
    return bool(close.iloc[-1] > sma.iloc[-1])
