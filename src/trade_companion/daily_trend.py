import math
from dataclasses import asdict, dataclass

import pandas as pd

from trade_companion.indicators import (
    calculate_sma,
    clean_swings,
    find_raw_swings,
    get_active_trading_range,
)
from trade_companion.signals import (
    is_fast_over_slow_sma,
    is_hh_hl_trend,
    is_price_in_fib_zone,
    is_price_over_sma,
)


@dataclass(frozen=True)
class DailySetup:
    ticker: str
    current_close: float
    stop_loss: float
    fib_50: float
    fib_618: float
    peak_high: float

    def to_dict(self) -> dict:
        return asdict(self)


def evaluate_daily_trend_setup(ticker: str, df: pd.DataFrame) -> DailySetup | None:
    if df.empty or not {"Close", "High", "Low"}.issubset(df.columns):
        return None

    valid_df = df[["Close", "High", "Low"]].dropna()
    close = valid_df["Close"]
    highs = valid_df["High"]
    lows = valid_df["Low"]

    if len(close) < 200:
        return None

    current_close = float(close.iloc[-1])
    current_low = float(lows.iloc[-1])
    current_sma50 = float(calculate_sma(close, 50).iloc[-1])
    current_sma200 = float(calculate_sma(close, 200).iloc[-1])

    values_to_check = (
        current_close,
        current_low,
        current_sma50,
        current_sma200,
    )
    if any(math.isnan(val) or math.isinf(val) for val in values_to_check):
        return None

    if not (
        is_price_over_sma(current_close, current_sma200)
        and is_fast_over_slow_sma(current_sma50, current_sma200)
    ):
        return None

    raw_swings = find_raw_swings(highs, lows, window=3)
    swings = clean_swings(raw_swings)
    if not is_hh_hl_trend(swings):
        return None

    fib = get_active_trading_range(swings)
    if fib is None:
        return None

    if not is_price_in_fib_zone(current_low, current_close, fib):
        return None

    return DailySetup(
        ticker=ticker,
        current_close=current_close,
        stop_loss=fib.base_low,
        fib_50=fib.fib_50,
        fib_618=fib.fib_618,
        peak_high=fib.peak_high,
    )
