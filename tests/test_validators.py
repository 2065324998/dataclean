"""Tests for the validators module."""

import pandas as pd

from dataclean.validators import (
    validate_zip_code,
    validate_order_amounts,
    validate_required_columns,
    get_null_counts,
)


class TestValidators:
    def test_valid_zip_code(self):
        assert validate_zip_code("07102") is True
        assert validate_zip_code("10001") is True

    def test_invalid_zip_code(self):
        assert validate_zip_code("7102") is False  # 4 digits
        assert validate_zip_code("ABCDE") is False
        assert validate_zip_code("") is False

    def test_zip_code_non_string(self):
        assert validate_zip_code(7102) is False
        assert validate_zip_code(None) is False

    def test_validate_order_amounts(self):
        df = pd.DataFrame({"amount": [100, -50, 0, 200]})
        result = validate_order_amounts(df)
        assert result["amount_valid"].tolist() == [True, False, False, True]

    def test_validate_required_columns(self):
        df = pd.DataFrame({"a": [1], "b": [2]})
        missing = validate_required_columns(df, ["a", "b", "c"])
        assert missing == ["c"]

    def test_validate_required_columns_all_present(self):
        df = pd.DataFrame({"a": [1], "b": [2]})
        missing = validate_required_columns(df, ["a", "b"])
        assert missing == []

    def test_get_null_counts(self):
        df = pd.DataFrame({"a": [1, None, 3], "b": [None, None, 3]})
        counts = get_null_counts(df)
        assert counts["a"] == 1
        assert counts["b"] == 2
