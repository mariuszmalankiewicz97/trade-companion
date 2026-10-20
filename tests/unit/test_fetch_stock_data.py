import numpy as np
import pandas as pd
from pytest_mock import MockerFixture

from trade_companion.fetch_stock_data import fetch_stock_data


def _create_sample_df() -> pd.DataFrame:
    """Tworzy standardowy DataFrame dla pojedynczego tickera."""
    return pd.DataFrame(
        {
            "Open": [150.0, 152.0],
            "High": [155.0, 156.0],
            "Low": [149.0, 151.0],
            "Close": [153.0, 155.0],
            "Volume": [1000, 1200],
        },
        index=pd.date_range("2026-01-01", periods=2),
    )


def test_fetch_stock_data_empty_tickers_list(mocker: MockerFixture) -> None:

    mock_download = mocker.patch(
        "trade_companion.fetch_stock_data.yf.download",
        return_value=pd.DataFrame(),
    )

    result = fetch_stock_data(tickers=[], period="1mo", interval="1d")

    assert result == {}
    mock_download.assert_called_once_with(
        tickers=[],
        period="1mo",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        progress=False,
    )


def test_fetch_stock_data_single_ticker_success(mocker: MockerFixture) -> None:
    sample_df = _create_sample_df()
    mock_download = mocker.patch(
        "trade_companion.fetch_stock_data.yf.download", return_value=sample_df
    )

    result = fetch_stock_data(tickers=["AAPL"], period="1mo", interval="1d")

    mock_download.assert_called_once()
    assert "AAPL" in result
    assert isinstance(result["AAPL"], pd.DataFrame)
    assert len(result["AAPL"]) == 2
    pd.testing.assert_frame_equal(result["AAPL"], sample_df)


def test_fetch_stock_data_single_ticker_empty_response(
    mocker: MockerFixture,
) -> None:
    empty_df = pd.DataFrame(
        {"Close": [np.nan, np.nan]},
        index=pd.date_range("2026-01-01", periods=2),
    )
    mocker.patch("trade_companion.fetch_stock_data.yf.download", return_value=empty_df)

    result = fetch_stock_data(tickers=["INVALID"], period="1mo", interval="1d")

    assert result == {}


def test_fetch_stock_data_multiple_tickers_success(
    mocker: MockerFixture,
) -> None:
    df_aapl = _create_sample_df()
    df_msft = _create_sample_df() * 2

    multi_df = pd.concat({"AAPL": df_aapl, "MSFT": df_msft}, axis=1)

    mocker.patch("trade_companion.fetch_stock_data.yf.download", return_value=multi_df)

    result = fetch_stock_data(tickers=["AAPL", "MSFT"], period="6mo", interval="1d")

    assert set(result.keys()) == {"AAPL", "MSFT"}
    pd.testing.assert_frame_equal(result["AAPL"], df_aapl)
    pd.testing.assert_frame_equal(result["MSFT"], df_msft)


def test_fetch_stock_data_multiple_tickers_with_missing_and_empty_ticker(
    mocker: MockerFixture,
) -> None:
    df_aapl = _create_sample_df()
    df_empty = pd.DataFrame(
        {"Open": [np.nan], "Close": [np.nan]},
        index=pd.date_range("2026-01-01", periods=1),
    )

    multi_df = pd.concat({"AAPL": df_aapl, "EMPTY_TICKER": df_empty}, axis=1)

    mocker.patch("trade_companion.fetch_stock_data.yf.download", return_value=multi_df)

    result = fetch_stock_data(
        tickers=["AAPL", "EMPTY_TICKER", "UNKNOWN_TICKER"],
        period="1mo",
        interval="1d",
    )

    assert list(result.keys()) == ["AAPL"]
    pd.testing.assert_frame_equal(result["AAPL"], df_aapl)
