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


def concat_low_and_high_price_zones(
    low_zone: pd.DataFrame, high_zone: pd.DataFrame
) -> pd.DataFrame:
    if not isinstance(low_zone, pd.DataFrame):
        raise TypeError("Low zone name must be a data frame")
    if not isinstance(high_zone, pd.DataFrame):
        raise TypeError("High zone name must be a data frame")
    all_zones = pd.concat([low_zone, high_zone])
    return all_zones


def merge_price_zones(all_zones: pd.DataFrame, last_atr: float) -> pd.DataFrame:
    if not isinstance(all_zones, pd.DataFrame):
        raise TypeError("Zones name must be a data frame")
    if not isinstance(last_atr, float):
        raise TypeError("Last ATR name must be a float")
    if last_atr <= 0:
        raise ValueError("Last ATR can't be less or equal 0")
    if all_zones.empty:
        return pd.DataFrame([])
    length = len(all_zones)
    start = 0
    stop = length
    sorted_by_bottom = all_zones.sort_values(by="top").reset_index(drop=True)
    merged_zones = []
    touch_count = 1
    tolerance = 0.3 * last_atr
    max_width = 1.5 * last_atr
    for index in range(start, stop):
        current_date = sorted_by_bottom.iloc[index]["date"]
        current_bottom = sorted_by_bottom.iloc[index]["bottom"]
        current_top = sorted_by_bottom.iloc[index]["top"]
        if not merged_zones:
            merged_zones.append(
                {
                    "first_date": current_date,
                    "last_date": current_date,
                    "bottom": current_bottom,
                    "top": current_top,
                    "touch_count": touch_count,
                }
            )
        else:
            last_zone = merged_zones[-1]
            if (
                last_zone["bottom"] <= current_top
                and last_zone["top"] + tolerance >= current_bottom
                and max_width
                >= max(last_zone["top"], current_top) - last_zone["bottom"]
            ):
                last_zone["last_date"] = max(last_zone["last_date"], current_date)
                last_zone["first_date"] = min(last_zone["first_date"], current_date)
                last_zone["top"] = max(current_top, last_zone["top"])
                last_zone["bottom"] = min(current_bottom, last_zone["bottom"])
                last_zone["touch_count"] = last_zone["touch_count"] + 1
            else:
                merged_zones.append(
                    {
                        "first_date": current_date,
                        "last_date": current_date,
                        "bottom": current_bottom,
                        "top": current_top,
                        "touch_count": touch_count,
                    }
                )

    return pd.DataFrame(merged_zones)
