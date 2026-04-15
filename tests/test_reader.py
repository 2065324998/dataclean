"""Tests for the data reader module."""

import pandas as pd
from pathlib import Path

from dataclean.reader import read_transactions, read_salespeople

DATA_DIR = Path(__file__).parent.parent / "data"


class TestReader:
    def test_read_transactions_shape(self):
        df = read_transactions(DATA_DIR / "transactions.csv")
        assert len(df) == 15
        assert "transaction_id" in df.columns
        assert "salesperson_id" in df.columns

    def test_read_transactions_date_parsing(self):
        df = read_transactions(DATA_DIR / "transactions.csv")
        assert pd.api.types.is_datetime64_any_dtype(df["transaction_date"])

    def test_read_transactions_columns(self):
        df = read_transactions(DATA_DIR / "transactions.csv")
        expected = {"transaction_id", "salesperson_id", "transaction_date",
                    "amount", "product_category"}
        assert expected == set(df.columns)

    def test_read_transactions_has_returns(self):
        df = read_transactions(DATA_DIR / "transactions.csv")
        assert (df["amount"] < 0).any()

    def test_read_salespeople_shape(self):
        df = read_salespeople(DATA_DIR / "salespeople.csv")
        assert len(df) == 3

    def test_read_salespeople_date_parsing(self):
        df = read_salespeople(DATA_DIR / "salespeople.csv")
        assert pd.api.types.is_datetime64_any_dtype(df["hire_date"])
