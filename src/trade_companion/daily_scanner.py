from pathlib import Path

import pandas as pd

from trade_companion.fetch_stock_data import fetch_stock_data
from trade_companion.json_loader import json_loader
from trade_companion.ticker_parser import extract_tickers


def run_daily_scanner(tickers_path: Path, period: str, interval: str) -> pd.DataFrame:
    json_tickers = json_loader(tickers_path)
    tickers = extract_tickers(json_tickers)
    return fetch_stock_data(tickers, period, interval)


def main() -> None:
    tickers_path = Path(__file__).parent.parent.parent / "data" / "tickers.json"
    period = "1y"
    interval = "1d"
    run_daily_scanner(tickers_path, period, interval)


if __name__ == "__main__":
    main()
