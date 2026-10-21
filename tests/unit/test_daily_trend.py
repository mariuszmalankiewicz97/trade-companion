from dataclasses import FrozenInstanceError

import numpy as np
import pandas as pd
import pytest

from trade_companion.daily_trend import DailySetup, evaluate_daily_trend_setup


def test_daily_setup_immutability() -> None:
    setup = DailySetup(
        ticker="ALE.WA",
        current_close=36.0,
        stop_loss=32.0,
        fib_50=36.5,
        fib_618=35.0,
        peak_high=40.0,
    )
    with pytest.raises(FrozenInstanceError):
        setup.current_close = 37.0


def test_daily_setup_to_dict() -> None:
    setup = DailySetup(
        ticker="ALE.WA",
        current_close=36.0,
        stop_loss=32.0,
        fib_50=36.5,
        fib_618=35.0,
        peak_high=40.0,
    )
    expected = {
        "ticker": "ALE.WA",
        "current_close": 36.0,
        "stop_loss": 32.0,
        "fib_50": 36.5,
        "fib_618": 35.0,
        "peak_high": 40.0,
    }
    assert setup.to_dict() == expected


@pytest.fixture
def valid_trend_dataframe() -> pd.DataFrame:
    length = 210
    dates = pd.date_range("2025-01-01", periods=length, freq="D")

    prices = np.linspace(80.0, 130.0, length)
    close = pd.Series(prices, index=dates)
    high = close + 2.0
    low = close - 2.0

    df = pd.DataFrame({"Close": close, "High": high, "Low": low}, index=dates)

    df.loc[df.index[180], "Low"] = 80.0
    df.loc[df.index[188], "High"] = 135.0
    df.loc[df.index[196], "Low"] = 100.0
    df.loc[df.index[204], "High"] = 150.0

    df.loc[df.index[-1], "Low"] = 122.0
    df.loc[df.index[-1], "Close"] = 124.0
    df.loc[df.index[-1], "High"] = 126.0

    return df


def test_evaluate_daily_trend_setup_success(
    valid_trend_dataframe: pd.DataFrame,
) -> None:
    setup = evaluate_daily_trend_setup("ALE.WA", valid_trend_dataframe)

    assert setup is not None
    assert isinstance(setup, DailySetup)
    assert setup.ticker == "ALE.WA"
    assert setup.current_close == 124.0
    assert setup.stop_loss == 100.0
    assert setup.peak_high == 150.0
    assert setup.fib_50 == 125.0
    assert setup.fib_618 == 119.1


def test_evaluate_daily_trend_setup_empty_dataframe() -> None:
    assert evaluate_daily_trend_setup("ALE.WA", pd.DataFrame()) is None


@pytest.mark.parametrize(
    "missing_cols",
    [
        {"High", "Low"},
        {"Close", "Low"},
        {"Close", "High"},
    ],
)
def test_evaluate_daily_trend_setup_missing_columns(
    missing_cols: set[str],
) -> None:
    df = pd.DataFrame(
        {col: [100.0] * 205 for col in missing_cols},
        index=pd.date_range("2025-01-01", periods=205),
    )
    assert evaluate_daily_trend_setup("ALE.WA", df) is None


def test_evaluate_daily_trend_setup_insufficient_rows(
    valid_trend_dataframe: pd.DataFrame,
) -> None:
    df_short = valid_trend_dataframe.iloc[-199:]
    assert evaluate_daily_trend_setup("ALE.WA", df_short) is None


def test_evaluate_daily_trend_setup_rejects_nan_in_latest_candle(
    valid_trend_dataframe: pd.DataFrame,
) -> None:
    df = valid_trend_dataframe.copy()
    df.loc[df.index[-1], "Close"] = np.nan
    assert evaluate_daily_trend_setup("ALE.WA", df) is None


def test_evaluate_daily_trend_setup_rejects_when_sma_condition_fails(
    valid_trend_dataframe: pd.DataFrame,
) -> None:
    df = valid_trend_dataframe.copy()
    df.loc[df.index[-1], "Close"] = 50.0
    df.loc[df.index[-1], "Low"] = 49.0
    assert evaluate_daily_trend_setup("ALE.WA", df) is None


def test_evaluate_daily_trend_setup_rejects_when_hh_hl_fails(
    valid_trend_dataframe: pd.DataFrame,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "trade_companion.daily_trend.is_hh_hl_trend", lambda swings: False
    )
    assert evaluate_daily_trend_setup("ALE.WA", valid_trend_dataframe) is None


def test_evaluate_daily_trend_setup_rejects_when_fib_range_none(
    valid_trend_dataframe: pd.DataFrame,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "trade_companion.daily_trend.get_active_trading_range",
        lambda swings: None,
    )
    assert evaluate_daily_trend_setup("ALE.WA", valid_trend_dataframe) is None


def test_evaluate_daily_trend_setup_rejects_when_price_not_in_fib_zone(
    valid_trend_dataframe: pd.DataFrame,
) -> None:
    df = valid_trend_dataframe.copy()
    df.loc[df.index[-1], "Low"] = 128.0
    df.loc[df.index[-1], "Close"] = 130.0
    assert evaluate_daily_trend_setup("ALE.WA", df) is None


def test_evaluate_daily_trend_setup_rejects_when_fib_zone_broken(
    valid_trend_dataframe: pd.DataFrame,
) -> None:
    df = valid_trend_dataframe.copy()
    df.loc[df.index[-1], "Low"] = 114.0
    df.loc[df.index[-1], "Close"] = 115.0
    assert evaluate_daily_trend_setup("ALE.WA", df) is None
