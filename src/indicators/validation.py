import pandas as pd


def validate_is_series(variable: pd.Series, name: str) -> None:
    if not isinstance(variable, pd.Series):
        raise TypeError(f"{name} must be a series")


def validate_period(period: int, name: str = "Period") -> None:
    if not isinstance(period, int):
        raise TypeError(f"{name} must be an integer")
    if period < 1:
        raise ValueError(f"{name} can't be less than 1")


def validate_std_multiplier(std_multiplier: float | int) -> None:
    if not isinstance(std_multiplier, float | int):
        raise TypeError("Std multiplier must be a float or integer")
    if std_multiplier <= 0:
        raise ValueError("Std multiplier must be greater than 0")


def validate_signal_period(signal_period: int) -> None:
    if not isinstance(signal_period, int):
        raise TypeError("Signal period must be an integer")
    if signal_period < 1:
        raise ValueError("Signal period can't be less than 1")
