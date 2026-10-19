from trade_companion.fetch_stock_data import fetch_stock_data
from trade_companion.filters import price_over_sma
from trade_companion.json_loader import json_loader
from trade_companion.ticker_parser import extract_tickers

from ...config import SCAN_INTERVAL, SCAN_PERIOD, SMA_LONG_TREND_PERIOD, TICKERS_FILE


def main() -> None:
    tickers = extract_tickers(json_loader(TICKERS_FILE))
    data = fetch_stock_data(tickers, SCAN_PERIOD, SCAN_INTERVAL)
    passed_tickers = []
    for ticker in tickers:
        close = data["Close"][ticker].dropna()
        print(close)
        if not price_over_sma(close, SMA_LONG_TREND_PERIOD):
            continue
        passed_tickers.append(ticker)
    print(passed_tickers)


if __name__ == "__main__":
    main()
