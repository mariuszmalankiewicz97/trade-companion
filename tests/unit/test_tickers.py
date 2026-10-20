import json
from pathlib import Path

import pytest

from trade_companion.tickers import extract_tickers, load_tickers


def test_extract_tickers_single_category() -> None:
    data = {"watchlist": ["AAPL", "MSFT", "NVDA"]}
    assert extract_tickers(data) == ["AAPL", "MSFT", "NVDA"]


def test_extract_tickers_multiple_categories() -> None:
    data = {
        "tech": ["AAPL", "GOOGL"],
        "finance": ["JPM", "BAC"],
    }
    assert extract_tickers(data) == ["AAPL", "GOOGL", "JPM", "BAC"]


def test_extract_tickers_removes_duplicates_and_preserves_order() -> None:

    data = {
        "group1": ["AAPL", "MSFT", "TSLA"],
        "group2": ["NVDA", "AAPL", "MSFT", "AMZN"],
    }
    expected = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
    assert extract_tickers(data) == expected


def test_extract_tickers_empty_sublists() -> None:
    data = {"empty_group": [], "active_group": ["AMD"]}
    assert extract_tickers(data) == ["AMD"]


@pytest.mark.parametrize(
    "invalid_input",
    [
        ["AAPL", "MSFT"],
        "AAPL,MSFT",
        123,
        None,
    ],
)
def test_extract_tickers_raises_type_error_for_non_dict(
    invalid_input: object,
) -> None:
    with pytest.raises(TypeError, match="Type must be a dict"):
        extract_tickers(invalid_input)


def test_extract_tickers_raises_value_error_for_empty_dict() -> None:
    with pytest.raises(ValueError, match="Missing tickers"):
        extract_tickers({})


def test_load_tickers_valid_json_file(tmp_path: Path) -> None:
    file_path = tmp_path / "tickers.json"
    file_path.write_text(
        json.dumps({"watchlist": ["AAPL", "MSFT", "AAPL"]}),
        encoding="utf-8",
    )

    result = load_tickers(file_path)

    assert result == ["AAPL", "MSFT"]


def test_load_tickers_accepts_string_path(tmp_path: Path) -> None:
    file_path = tmp_path / "tickers.json"
    file_path.write_text(json.dumps({"watchlist": ["NVDA"]}), encoding="utf-8")

    result = load_tickers(str(file_path))

    assert result == ["NVDA"]


@pytest.mark.parametrize(
    "filename",
    [
        "tickers.txt",
        "tickers.csv",
        "tickers.yaml",
        "tickers",
    ],
)
def test_load_tickers_raises_value_error_for_invalid_extension(
    tmp_path: Path, filename: str
) -> None:
    file_path = tmp_path / filename
    file_path.touch()

    with pytest.raises(ValueError, match="File must have .json extension"):
        load_tickers(file_path)


def test_load_tickers_raises_file_not_found_error_for_missing_file(
    tmp_path: Path,
) -> None:
    non_existent_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_tickers(non_existent_file)


def test_load_tickers_raises_json_decode_error_for_malformed_json(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "corrupt.json"
    file_path.write_text("{invalid_json: true,", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_tickers(file_path)
