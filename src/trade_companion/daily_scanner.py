from pathlib import Path

from trade_companion.fetch_stock_data import fetch_stock_data
from trade_companion.filters import price_over_sma
from trade_companion.json_loader import json_loader
from trade_companion.ticker_parser import extract_tickers

TICKERS_FILE = Path(__file__).resolve().parents[2] / "data" / "tickers.json"
SCAN_PERIOD = "2y"
SCAN_INTERVAL = "1d"


def main() -> None:
    tickers = extract_tickers(json_loader(TICKERS_FILE))
    data = fetch_stock_data(tickers, SCAN_PERIOD, SCAN_INTERVAL)
    passed_tickers = []
    for ticker in tickers:
        if ticker not in data["Close"].columns:
            continue
        close = data["Close"][ticker].dropna()
        print(close)
        if not price_over_sma(close):
            continue
        passed_tickers.append(ticker)
    print(passed_tickers)


if __name__ == "__main__":
    main()
