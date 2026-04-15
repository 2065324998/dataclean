"""Tests for the data reader module."""

import pandas as pd
from pathlib import Path

from dataclean.reader import read_orders, read_customers, read_regions

DATA_DIR = Path(__file__).parent.parent / "data"


class TestReader:
    def test_read_orders_shape(self):
        df = read_orders(DATA_DIR / "orders.csv")
        assert len(df) == 20
        assert "order_id" in df.columns
        assert "customer_id" in df.columns

    def test_read_orders_date_parsing(self):
        df = read_orders(DATA_DIR / "orders.csv")
        assert pd.api.types.is_datetime64_any_dtype(df["order_date"])

    def test_read_orders_columns(self):
        df = read_orders(DATA_DIR / "orders.csv")
        expected = {"order_id", "customer_id", "order_date", "amount",
                    "zip_code", "product_category"}
        assert expected == set(df.columns)

    def test_read_customers_shape(self):
        df = read_customers(DATA_DIR / "customers.csv")
        assert len(df) == 10

    def test_read_customers_date_parsing(self):
        df = read_customers(DATA_DIR / "customers.csv")
        assert pd.api.types.is_datetime64_any_dtype(df["signup_date"])

    def test_read_regions_shape(self):
        df = read_regions(DATA_DIR / "regions.csv")
        assert len(df) == 10

    def test_read_regions_zip_as_string(self):
        df = read_regions(DATA_DIR / "regions.csv")
        # Zip codes should be read as strings (not int)
        assert not pd.api.types.is_integer_dtype(df["zip_code"])
        assert "07102" in df["zip_code"].values
