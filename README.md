# Trade Companion

A modular Python application for scanning and analyzing stock market data for swing trading opportunities.

## Project Goal

The goal of this project is to build an automated, reliable stock scanner that analyzes market data and identifies potential long setups based on technical indicators, market structure, and Fibonacci retracement zones.

The project follows clean architecture principles and is developed using Test-Driven Development (TDD).

## Architecture & Design

The application follows a **4-tier layered architecture** ensuring separation of concerns:

1. **Indicators (`indicators.py`):** Pure numerical calculations (e.g., SMA, EMA), structural swing point detection (`find_raw_swings`, `clean_swings`), and Fibonacci retracement zone calculation (`calculate_fib_zone`, `get_active_trading_range`).
2. **Signals (`signals.py`):** Atomic market criteria evaluation returning boolean values (`is_price_over_sma`, `is_fast_over_slow_sma`, `is_hh_hl_trend`, `is_price_in_fib_zone`).
3. **Strategies (`daily_trend.py`):** Composition of multiple signals into complete trading rules for specific timeframes, returning structured setup models (`DailySetup`).
4. **Storage & Orchestration (`storage.py`, `daily_scanner.py`):** Persistence of qualified candidates to `h1_watchlist.json` and end-to-end workflow handling ticker ingestion, API fetching, and terminal reporting.

## Technologies

- Python 3.14+
- pandas
- NumPy
- yfinance
- pytest
- Ruff
- Visual Studio Code

## Project Structure

```text
trade-companion/
├── data/
│   ├── h1_watchlist.json         # Qualified setups for H1 execution
│   └── tickers.json              # Watchlist configuration
├── src/
│   └── trade_companion/
│       ├── __init__.py
│       ├── daily_scanner.py      # Entry point / Orchestration
│       ├── daily_trend.py        # Strategy definition (SMA + HH/HL + Fib)
│       ├── fetch_stock_data.py   # Market data fetching (yfinance adapter)
│       ├── indicators.py         # Pure indicators, swing points & Fibonacci
│       ├── signals.py            # Boolean market signals
│       ├── storage.py            # H1 watchlist persistence & JSON serialization
│       └── tickers.py            # Watchlist loader, parser & deduplicator
├── tests/
│   ├── integration/
│   │   └── test_daily_scanner.py # Workflow integration tests
│   └── unit/
│       ├── test_daily_scanner.py
│       ├── test_daily_trend.py
│       ├── test_fetch_stock_data.py
│       ├── test_indicators.py
│       ├── test_signals.py
│       ├── test_storage.py
│       └── test_tickers.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Installation
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/mariuszmalankiewicz97/trade-companion.git
cd trade-companion
```

### Create and activate a virtual environment:

#### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```
#### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```
#### Install the project in editable mode with development dependencies:
```bash
pip install -e .
```
## Running the Scanner
Configure your ticker list in data/tickers.json:
```json
{
   "wig20": [
     "ALE.WA",
     "ALR.WA",
     "BDX.WA"
   ]
}
```
Run the daily trend scanner:
```bash
python -m trade_companion.daily_scanner
```
## Running Tests
Run all unit and integration tests:
```bash
pytest
```
Run tests with verbose output:
```bash
pytest -v
```
## Code Quality & Formatting
Ruff is used for linting and code formatting.

Check the project for issues:
```bash
ruff check .
```
Automatically fix issues:
```bash
ruff check . --fix
```
Format code:
```bash
ruff format .
```
### VS Code Integration
To format and lint automatically on save, add the following to .vscode/settings.json:
```json
{
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.fixAll.ruff": "explicit"
        }
    }
}
```
## Features
### Completed
- [x] 4-layer modular architecture (Indicators -> Signals -> Strategy -> Scanner).

- [x] Ticker loader with deduplication, string cleaning, and order preservation (tickers.py).

- [x] Batch data downloading with MultiIndex mapping to individual stock DataFrames (fetch_stock_data.py).

- [x] Robust SMA computation with parameter and type validation (indicators.py).

- [x] Pivot detection and swing point normalization (find_raw_swings, clean_swings).

- [x] Market structure trend evaluation (is_hh_hl_trend).

- [x] Active trading range detection and Fibonacci 0.50 – 0.618 retracement zones (calculate_fib_zone, is_price_in_fib_zone).

- [x] Candidate persistence and deserialization for H1 timeframe (storage.py -> h1_watchlist.json).

- [x] Comprehensive unit and integration test suite with high coverage using pytest.

### In Progress / Planned
- [ ] Hourly timeframe trigger scanner (hourly_scanner.py using h1_watchlist.json).

- [ ] Volume confirmation filters (e.g., volume spike, volume > SMA 20).

- [ ] Support and resistance zone detection.

- [ ] Risk/Reward ratio calculation and dynamic stop-loss placement.

- [ ] Telegram / Discord trade notifications.

## Status
🚧 Work in progress.

## Author
Mariusz Malankiewicz