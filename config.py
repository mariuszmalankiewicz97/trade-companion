from pathlib import Path

TICKERS_FILE = Path(__file__).resolve().parents[2] / "data" / "tickers.json"
SCAN_PERIOD = "2y"
SCAN_INTERVAL = "1d"
SMA_LONG_TREND_PERIOD = 200
