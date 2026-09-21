import numpy as np
import pandas as pd
import pytest

from indicators.atr import calculate_atr, calculate_true_range


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


def test_calculate_atr_type_error_invalid_tr():
    with pytest.raises(TypeError):
        tr = []
        period = 2
        calculate_atr(tr, period)


def test_calculate_atr_type_error_invalid_period():
    with pytest.raises(TypeError):
        tr = pd.Series([10, 20, 30])
        period = "2"
        calculate_atr(tr, period)


def test_calculate_atr_type_value_invalid_period():
    with pytest.raises(ValueError):
        tr = pd.Series([10, 20, 30])
        period = 0
        calculate_atr(tr, period)


def test_calculate_atr_returns_correct_structure():
    tr = pd.Series([10, 20, 30])
    period = 2
    calculate_atr(tr, period)
    assert isinstance(calculate_atr(tr, period), pd.Series)


def test_calculate_atr_returns_correct_values():
    tr = pd.Series(
        [5, 6, 6, 4, 4],
        index=["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04", "2026-09-05"],
    )
    period = 3
    result = calculate_atr(tr, period)
    excepted = pd.Series(
        [np.nan, np.nan, 5.666667, 5.333333, 4.666667],
        index=["2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04", "2026-09-05"],
    )
    assert pd.Series.equals(round(result, 2), round(excepted, 2))
