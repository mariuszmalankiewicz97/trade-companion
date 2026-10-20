def is_price_over_sma(current_close: float, current_sma: float) -> bool:
    return current_close > current_sma


def is_fast_over_slow_sma(current_fast: float, current_slow: float) -> bool:
    return current_fast > current_slow
