import pandas as pd

from indicators.validation import validate_is_series, validate_period


def find_pivot_lows(low: pd.Series, period: int) -> pd.Series:
    validate_is_series(low, "Low")
    validate_period(period)
    pivots = pd.Series(dtype=float)
    for index, value in enumerate(low):
        count = 0
        if index >= period and index < len(low) - period:
            for inner_index, inner_value in enumerate(low):
                if (
                    inner_index >= index - period
                    and inner_index <= index + period
                    and inner_index != index
                ):
                    if value <= inner_value:
                        count += 1
                    if count == 2 * period:
                        pivots.at[index] = value
                        count = 0
    return pivots
