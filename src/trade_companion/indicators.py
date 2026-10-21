from dataclasses import dataclass
from typing import Literal

import pandas as pd


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


@dataclass(frozen=True)
class SwingPoint:
    index: int
    price: float
    type: Literal["HIGH", "LOW"]


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
