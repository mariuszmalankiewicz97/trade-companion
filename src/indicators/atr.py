import numpy as np
import pandas as pd

from indicators.validation import validate_is_series, validate_period


def calculate_true_range(data: pd.DataFrame) -> pd.Series:
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Data must be an DataFrame")
    previus_close = np.nan
    trs = pd.Series()
    for index, row in data.iterrows():
        tr_max = max(
            row["High"] - row["Low"],
            row["High"] - previus_close,
            abs(row["Low"] - previus_close),
        )
        trs.loc[index] = tr_max
        previus_close = row["Close"]
    return trs


def calculate_atr(tr: pd.Series, period: int) -> pd.Series:
    validate_is_series(tr, "True range")
    validate_period(period)
    atr = pd.Series(dtype=float)
    for index, value in enumerate(tr):
        temp_atr = 0
        count = 0
        if index >= period - 1:
            for index_inner, value_inner in enumerate(tr):
                if index_inner <= index and index_inner >= index - period + 1:
                    temp_atr += value_inner
                    count += 1
                    if count == period:
                        temp_atr = temp_atr / period
                        atr[tr.index[index]] = temp_atr
                        count = 0
                        temp_atr = 0
        else:
            atr[tr.index[index]] = np.nan
    return atr
