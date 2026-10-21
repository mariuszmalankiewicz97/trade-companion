import json
from pathlib import Path

import pytest

from trade_companion.tickers import extract_tickers, load_tickers


def test_extract_tickers_cleans_whitespace_and_uppercases() -> None:
    data = {"watchlist": [" ale.wa ", "bdx.wa\t", "\ncdr.wa\n"]}
    assert extract_tickers(data) == ["ALE.WA", "BDX.WA", "CDR.WA"]


def test_extract_tickers_removes_duplicates_and_preserves_order() -> None:
    data = {
        "group_a": ["ALE.WA", "BDX.WA"],
        "group_b": ["bdx.wa", "PKN.WA", "ale.wa"],
    }
    assert extract_tickers(data) == ["ALE.WA", "BDX.WA", "PKN.WA"]


def test_extract_tickers_skips_empty_strings_and_non_strings() -> None:
    data = {"watchlist": ["ALE.WA", "", "   ", None, 123, "BDX.WA"]}
    assert extract_tickers(data) == ["ALE.WA", "BDX.WA"]


def test_extract_tickers_raises_type_error_for_non_dict() -> None:
    with pytest.raises(TypeError, match="Type must be a dict"):
        extract_tickers(["ALE.WA", "BDX.WA"])


def test_extract_tickers_raises_value_error_for_empty_dict() -> None:
    with pytest.raises(ValueError, match="Missing tickers"):
        extract_tickers({})


def test_extract_tickers_raises_value_error_when_all_sublists_empty() -> None:
    data = {"group_a": [], "group_b": ["   ", ""]}
    with pytest.raises(ValueError, match="No valid tickers found in data"):
        extract_tickers(data)


def test_load_tickers_reads_valid_file(tmp_path: Path) -> None:
    file_path = tmp_path / "tickers.json"
    file_path.write_text(
        json.dumps({"wig20": [" ale.wa ", "BDX.WA"]}), encoding="utf-8"
    )

    result = load_tickers(file_path)
    assert result == ["ALE.WA", "BDX.WA"]


def test_load_tickers_raises_value_error_for_wrong_extension(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "tickers.txt"
    file_path.touch()

    with pytest.raises(ValueError, match="File must have .json extension"):
        load_tickers(file_path)


def test_load_tickers_raises_file_not_found(tmp_path: Path) -> None:
    non_existent = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        load_tickers(non_existent)
