from pathlib import Path

from trade_companion.daily_trend import daily_trend_strategy
from trade_companion.fetch_stock_data import fetch_stock_data
from trade_companion.tickers import load_tickers

TICKERS_FILE = Path(__file__).resolve().parents[2] / "data" / "tickers.json"
SCAN_PERIOD = "2y"
SCAN_INTERVAL = "1d"


def main() -> None:
    tickers = load_tickers(TICKERS_FILE)
    market_data = fetch_stock_data(tickers, SCAN_PERIOD, SCAN_INTERVAL)

    passed_tickers = []
    for ticker, ticker_df in market_data.items():
        if not daily_trend_strategy(ticker_df):
            continue
        passed_tickers.append(ticker)

    print(passed_tickers)


if __name__ == "__main__":
    main()
