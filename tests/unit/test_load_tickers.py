import json

import pytest

from trade_companion.json_loader import json_loader


def test_json_loader_file_not_found():
    with pytest.raises(FileNotFoundError):
        json_loader("invalid_file.json")


def test_json_loader_invalid_extenction():
    with pytest.raises(ValueError):
        json_loader("invalid_extenction.txt")


def test_json_loader_invalid_json_content(tmp_path):
    bad_file = tmp_path / "broken.json"
    bad_file.write_text("invalid json content")

    with pytest.raises(json.JSONDecodeError):
        json_loader(bad_file)


def test_json_loader_success(tmp_path):
    test_data = {"wig20": ["PKO.WA", "KGH.WA"], "nasdaq100": ["AAPL", "NVDA"]}
    valid_file = tmp_path / "ticker.json"
    valid_file.write_text(json.dumps(test_data))
    result = json_loader(valid_file)

    assert isinstance(result, dict)
    assert result == test_data
    assert result["wig20"][0] == "PKO.WA"
