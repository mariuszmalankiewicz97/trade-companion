from trade_companion.indicators import SwingPoint


def is_price_over_sma(current_close: float, current_sma: float) -> bool:
    return current_close > current_sma


def is_fast_over_slow_sma(current_fast: float, current_slow: float) -> bool:
    return current_fast > current_slow


def is_hh_hl_trend(cleaned_swings: list[SwingPoint]) -> bool:
    highs = [s.price for s in cleaned_swings if s.type == "HIGH"]
    lows = [s.price for s in cleaned_swings if s.type == "LOW"]

    if len(highs) < 2 or len(lows) < 2:
        return False

    latest_high, previous_high = highs[-1], highs[-2]
    latest_low, previous_low = lows[-1], lows[-2]

    has_higher_high = latest_high > previous_high
    has_higher_low = latest_low > previous_low

    return has_higher_high and has_higher_low
