import pandas as pd

from indicators.moving_averages import calculate_sma
from indicators.validation import (
    validate_is_series,
    validate_period,
    validate_std_multiplier,
)


def calculate_bollinger_bands(
    close: pd.Series, period: int, std_multiplier: float | int
) -> dict:
    validate_is_series(close, "Close")
    validate_period(period)
    validate_std_multiplier(std_multiplier)
    middle: pd.Series = calculate_sma(close, period)
    std: pd.Series = close.rolling(period).std()
    upper: pd.Series = middle + std_multiplier * std
    lower: pd.Series = middle - std_multiplier * std
    return {"middle": middle, "upper": upper, "lower": lower}
