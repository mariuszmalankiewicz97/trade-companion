# trade_companion/fetch_stock_data.py
import pandas as pd
import yfinance as yf


def fetch_stock_data(
    tickers: list[str], period: str, interval: str
) -> dict[str, pd.DataFrame]:
    raw_data = yf.download(
        tickers=tickers,
        period=period,
        interval=interval,
        group_by="ticker",
        auto_adjust=True,
        progress=False,
    )

    result: dict[str, pd.DataFrame] = {}

    if len(tickers) == 1:
        ticker = tickers[0]
        cleaned = raw_data.dropna(how="all")
        if not cleaned.empty:
            result[ticker] = cleaned
        return result

    for ticker in tickers:
        try:
            df = raw_data[ticker].dropna(how="all")
            if not df.empty:
                result[ticker] = df
        except KeyError:
            continue

    return result
