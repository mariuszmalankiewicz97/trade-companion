import pandas as pd

from src.indicators.validation import validate_is_series, validate_period


def calculate_average_volume(volume: pd.Series, period: int) -> float:
    validate_is_series(volume, "Volume")
    validate_period(period)
    if period > len(volume):
        raise ValueError("Volume length can't be less than period")
    volume_without_last = volume.iloc[:-1]
    average_volume = sum(volume_without_last.tail(period)) / period
    return float(average_volume)
