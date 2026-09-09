import yfinance as yf

from ticker import valid_ticker


def fetch_stock_data(ticker):
    if not valid_ticker(ticker):
        raise ValueError("Ticker is invalid!")
    stock = yf.Ticker(ticker)
    return stock.history(period="6mo", interval="1d")
