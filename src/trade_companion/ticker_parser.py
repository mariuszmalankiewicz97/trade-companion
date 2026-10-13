from itertools import chain


def extract_tickers(tickers):
    if not isinstance(tickers, dict):
        raise TypeError("Type must be a dict")
    if len(tickers) == 0:
        raise ValueError("Missing tickers")
    unique_tickers = set(chain.from_iterable(tickers.values()))
    return list(unique_tickers)
