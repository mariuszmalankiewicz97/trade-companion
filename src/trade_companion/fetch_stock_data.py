import pandas as pd
import yfinance as yf


def fetch_stock_data(tickers: list, period: str, interval: str) -> pd.DataFrame:
    if not isinstance(tickers, list):
        raise TypeError("Tickers must be a list")
    if not isinstance(period, str):
        raise TypeError("Period must be a string")
    if not isinstance(interval, str):
        raise TypeError("Interval must be a string")
    data = yf.download(
        tickers,
        period=period,
        interval=interval,
        group_by="ticker",
        threads=True,
        auto_adjust=True,
        actions=False,
        ignore_tz=True,
        progress=False,
    )
    return data
