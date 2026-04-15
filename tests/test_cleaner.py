"""Tests for the data cleaner module."""

import pandas as pd

from dataclean.cleaner import clean_amounts, standardize_dates, remove_duplicates


class TestCleaner:
    def test_clean_amounts_string(self):
        df = pd.DataFrame({"amount": ["$1,234.56", "$789.00"]})
        result = clean_amounts(df)
        assert result["amount"].iloc[0] == 1234.56
        assert result["amount"].iloc[1] == 789.00

    def test_clean_amounts_already_numeric(self):
        df = pd.DataFrame({"amount": [100.0, 200.0]})
        result = clean_amounts(df)
        assert result["amount"].iloc[0] == 100.0

    def test_standardize_dates(self):
        df = pd.DataFrame({"transaction_date": ["2024-01-15", "2024-02-20"]})
        result = standardize_dates(df)
        assert pd.api.types.is_datetime64_any_dtype(result["transaction_date"])

    def test_remove_duplicates(self):
        df = pd.DataFrame({
            "transaction_id": [1, 2, 1],
            "amount": [100, 200, 100],
        })
        result = remove_duplicates(df, subset=["transaction_id"])
        assert len(result) == 2

    def test_clean_does_not_mutate_original(self):
        df = pd.DataFrame({"amount": ["$500"]})
        _ = clean_amounts(df)
        assert df["amount"].iloc[0] == "$500"
