import pytest

from trade_companion.ticker_parser import extract_tickers


def test_extract_tickers_invalid_type():
    with pytest.raises(TypeError):
        tickers = []
        extract_tickers(tickers)


def test_extract_tickers_empty_input_data():
    with pytest.raises(ValueError):
        tickers = {}
        extract_tickers(tickers)


def test_extract_tickers_returns_correct_values():
    tickers = {"wig20": ["PKO.WA", "PZU.WA"]}
    result = extract_tickers(tickers)
    expected = ["PKO.WA", "PZU.WA"]
    assert isinstance(result, list)
    assert result == expected


def test_extract_tickers_remove_duplication():
    tickers = {"wig20": ["PKO.WA", "PZU.WA", "PKO.WA"]}
    result = extract_tickers(tickers)
    expected = ["PKO.WA", "PZU.WA"]
    assert set(result) == set(expected)
