import math

import pandas as pd

from trade_companion.indicators import calculate_sma, clean_swings, find_raw_swings
from trade_companion.signals import (
    is_fast_over_slow_sma,
    is_hh_hl_trend,
    is_price_over_sma,
)


def daily_trend_strategy(df: pd.DataFrame) -> bool:
    close = df["Close"].dropna()
    highs = df["High"].dropna()
    lows = df["Low"].dropna()

    if len(close) < 200:
        return False

    current_close = df["Close"].iloc[-1]
    current_sma50 = calculate_sma(close, 50).iloc[-1]
    current_sma200 = calculate_sma(close, 200).iloc[-1]
    raw_swings = find_raw_swings(highs, lows, 3)
    swings = clean_swings(raw_swings)

    values_to_check = (current_close, current_sma50, current_sma200)
    if any(math.isnan(val) or math.isinf(val) for val in values_to_check):
        return False

    return (
        is_price_over_sma(current_close, current_sma200)
        and is_fast_over_slow_sma(current_sma50, current_sma200)
        and is_hh_hl_trend(swings)
    )
