from pathlib import Path

from trade_companion.daily_trend import DailySetup, evaluate_daily_trend_setup
from trade_companion.fetch_stock_data import fetch_stock_data
from trade_companion.storage import save_h1_watchlist
from trade_companion.tickers import load_tickers

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
TICKERS_FILE = DATA_DIR / "tickers.json"
H1_WATCHLIST_FILE = DATA_DIR / "h1_watchlist.json"

SCAN_PERIOD = "2y"
SCAN_INTERVAL = "1d"


def main() -> None:
    tickers = load_tickers(TICKERS_FILE)
    market_data = fetch_stock_data(tickers, SCAN_PERIOD, SCAN_INTERVAL)

    qualified_setups: list[DailySetup] = []

    for ticker, ticker_df in market_data.items():
        setup = evaluate_daily_trend_setup(ticker, ticker_df)
        if setup is not None:
            qualified_setups.append(setup)

    save_h1_watchlist(qualified_setups, H1_WATCHLIST_FILE)

    print(f"Zapisano {len(qualified_setups)} setupów do: {H1_WATCHLIST_FILE.name}")
    for s in qualified_setups:
        print(
            f"  - {s.ticker}: Close={s.current_close}, "
            f"Strefa=[{s.fib_618} - {s.fib_50}], SL={s.stop_loss}"
        )


if __name__ == "__main__":
    main()
