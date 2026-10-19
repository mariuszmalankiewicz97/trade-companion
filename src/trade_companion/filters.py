import pandas as pd

from trade_companion.simple_moving_average import simple_moving_average


def price_over_sma(close: pd.Series, period: int) -> bool:
    if len(close) < period:
        return False
    sma = simple_moving_average(close, period)
    last_sma = sma.iloc[-1]
    last_close = close.iloc[-1]
    return bool(last_close > last_sma)
