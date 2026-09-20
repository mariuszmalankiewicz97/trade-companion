import pandas as pd
import pytest

from indicators.atr import calculate_true_range


def test_calculate_true_range_type_error_invalid_data():
    with pytest.raises(TypeError):
        data = []
        calculate_true_range(data)


def test_calculate_true_range_return_correct_structure():
    data = pd.DataFrame()
    result = calculate_true_range(data)
    assert isinstance(result, pd.Series)


def test_calculate_true_range_return_correct_values():
    data = pd.DataFrame(
        {
            "High": [105, 108, 110, 107, 112],
            "Low": [100, 102, 104, 103, 106],
            "Close": [103, 107, 105, 106, 110],
        },
        index=[
            "2026-09-01",
            "2026-09-02",
            "2026-09-03",
            "2026-09-04",
            "2026-09-05",
        ],
    )
    result = calculate_true_range(data)
    expected = pd.Series(
        [5, 6, 6, 4, 6],
        index=["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04", "2026-09-05"],
    )
    assert pd.Series.equals(result, expected)
