import numpy as np
import pandas as pd


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
