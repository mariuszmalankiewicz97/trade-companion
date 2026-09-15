import numpy as np
import pandas as pd
from validation import validate_is_series, validate_period


def calculate_rsi(close: pd.Series, period: int) -> pd.Series:
    validate_is_series(close, "Close")
    validate_period(period)
    diff: pd.Series = close.diff()
    gain: list | pd.Series = []
    loss: list | pd.Series = []
    for ele in diff:
        if pd.isna(ele):
            gain.append(np.nan)
            loss.append(np.nan)
        elif ele >= 0:
            gain.append(ele)
            loss.append(0)
        elif ele < 0:
            ele = ele * -1
            loss.append(ele)
            gain.append(0)
    gain: list | pd.Series = pd.Series(gain)
    loss: list | pd.Series = pd.Series(loss)
    avg_gain: pd.Series = gain.rolling(period).mean()
    avg_loss: pd.Series = loss.rolling(period).mean()
    rs: pd.Series = avg_gain / avg_loss
    rsi: pd.Series = 100 - (100 / (1 + rs))
    return rsi
