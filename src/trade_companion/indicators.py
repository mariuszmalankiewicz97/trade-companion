from dataclasses import dataclass
from typing import Literal

import pandas as pd


@dataclass(frozen=True)
class SwingPoint:
    index: int
    price: float
    type: Literal["HIGH", "LOW"]


@dataclass(frozen=True)
class FibZone:
    base_low: float
    peak_high: float
    fib_50: float
    fib_618: float


def calculate_sma(close: pd.Series, period: int) -> pd.Series:
    if not isinstance(close, pd.Series):
        raise TypeError("Close must be a pandas series")

    if not pd.api.types.is_numeric_dtype(close):
        raise TypeError("Close series must contain numeric data")

    if not isinstance(period, int) or isinstance(period, bool):
        raise TypeError("Period must be an integer")

    if period <= 0:
        raise ValueError("Period must be greater than 0")

    if period > len(close):
        raise ValueError("Period can't be greater than length of close")

    return close.rolling(window=period).mean()


def find_raw_swings(
    high: pd.Series, low: pd.Series, window: int = 3
) -> list[SwingPoint]:
    if len(high) != len(low) or len(high) < (2 * window + 1):
        return []

    raw_swings: list[SwingPoint] = []
    total_len = len(high)

    for i in range(window, total_len - window):
        current_high = high.iloc[i]
        left_highs = high.iloc[i - window : i]
        right_highs = high.iloc[i + 1 : i + window + 1]

        if (current_high > left_highs).all() and (current_high >= right_highs).all():
            raw_swings.append(
                SwingPoint(index=i, price=float(current_high), type="HIGH")
            )

        current_low = low.iloc[i]
        left_lows = low.iloc[i - window : i]
        right_lows = low.iloc[i + 1 : i + window + 1]

        if (current_low < left_lows).all() and (current_low <= right_lows).all():
            raw_swings.append(SwingPoint(index=i, price=float(current_low), type="LOW"))

    raw_swings.sort(key=lambda s: s.index)
    return raw_swings


def clean_swings(raw_swings: list[SwingPoint]) -> list[SwingPoint]:
    if not raw_swings:
        return []

    cleaned: list[SwingPoint] = [raw_swings[0]]

    for current in raw_swings[1:]:
        previous = cleaned[-1]

        if current.type == previous.type:
            if (
                current.type == "HIGH"
                and current.price > previous.price
                or current.type == "LOW"
                and current.price < previous.price
            ):
                cleaned[-1] = current
        else:
            cleaned.append(current)

    return cleaned


def calculate_fib_zone(base_low: float, peak_high: float) -> FibZone:
    impulse = peak_high - base_low
    return FibZone(
        base_low=base_low,
        peak_high=peak_high,
        fib_50=round(peak_high - 0.50 * impulse, 4),
        fib_618=round(peak_high - 0.618 * impulse, 4),
    )


def get_active_trading_range(
    cleaned_swings: list[SwingPoint],
) -> FibZone | None:
    highs = [s for s in cleaned_swings if s.type == "HIGH"]
    lows = [s for s in cleaned_swings if s.type == "LOW"]

    if len(highs) < 2 or len(lows) < 2:
        return None

    latest_high = highs[-1]
    prior_lows = [l for l in lows if l.index < latest_high.index]
    if not prior_lows:
        return None

    base_low = prior_lows[-1]
    return calculate_fib_zone(base_low=base_low.price, peak_high=latest_high.price)
