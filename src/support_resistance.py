import pandas as pd

from indicators.validation import validate_is_series, validate_period


def find_pivot_lows(low: pd.Series, period: int = 2) -> pd.Series:
    validate_is_series(low, "Low")
    validate_period(period)
    pivots = {}
    length = len(low)
    start = period
    stop = length - period
    for index in range(start, stop):
        if (
            low.iloc[index] < low.iloc[index - period + 1] < low.iloc[index - period]
            and low.iloc[index]
            < low.iloc[index + period - 1]
            < low.iloc[index + period]
        ):
            pivots[low.index[index]] = low.iloc[index]
    return pd.Series(pivots, dtype=float)


def find_the_low_price_zones(low_pivots: pd.Series, atr: pd.Series) -> pd.DataFrame:
    validate_is_series(low_pivots, "Pivots")
    validate_is_series(atr, "ATR")
    length = len(low_pivots)
    start = 0
    stop = length
    groups = []
    for index in range(start, stop):
        date = low_pivots.index[index]
        bottom_value = low_pivots.iloc[index]
        atr_value = atr[date]
        top_value = 0.3 * atr_value + bottom_value
        groups.append(
            {"date": date, "type": "low", "bottom": bottom_value, "top": top_value}
        )
    return pd.DataFrame(groups)


def find_pivot_high(high: pd.Series, period: int = 2) -> pd.Series:
    validate_is_series(high, "High")
    validate_period(period)
    pivots = {}
    length = len(high)
    start = period
    stop = length - period
    for index in range(start, stop):
        if (
            high.iloc[index] > high.iloc[index - period + 1] > high.iloc[index - period]
            and high.iloc[index]
            > high.iloc[index + period - 1]
            > high.iloc[index + period]
        ):
            pivots[high.index[index]] = high.iloc[index]
    return pd.Series(pivots, dtype=float)


def find_the_high_price_zones(high_pivots: pd.Series, atr: pd.Series) -> pd.DataFrame:
    validate_is_series(high_pivots, "Pivots")
    validate_is_series(atr, "ATR")
    length = len(high_pivots)
    start = 0
    stop = length
    groups = []
    for index in range(start, stop):
        date = high_pivots.index[index]
        top_value = high_pivots.iloc[index]
        atr_value = atr[date]
        bottom_value = top_value - 0.3 * atr_value
        groups.append(
            {"date": date, "type": "high", "top": top_value, "bottom": bottom_value}
        )
    return pd.DataFrame(groups)
