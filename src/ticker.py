def valid_ticker(ticker):
    if not isinstance(ticker, str):
        return False
    if not ticker:
        return False
    if len(ticker) > 5:
        return False
    if not ticker.isalpha():
        return False
    return True
