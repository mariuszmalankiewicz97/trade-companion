import json
from unittest.mock import patch

import pandas as pd

from trade_companion.daily_scanner import run_daily_scanner


def test_daily_scanner_end_to_end(tmp_path):
    json_file = tmp_path / "tickers.json"
    tickers_data = {"wig20": ["PKO.WA", "PZU.WA"]}
    json_file.write_text(json.dumps(tickers_data), encoding="utf-8")

    fake_result = pd.DataFrame({"Close": [120.5, 245.0], "Volume": [1000000, 500000]})

    with patch(
        "trade_companion.daily_scanner.fetch_stock_data", return_value=fake_result
    ) as mock_fetch:
        result = run_daily_scanner(json_file, "1mo", "1d")

    mock_fetch.assert_called_once_with(["PKO.WA", "PZU.WA"], "1mo", "1d")

    assert isinstance(result, pd.DataFrame)
    assert result.equals(fake_result)
