"""Tests for the fiscal period utilities."""

import pandas as pd

from dataclean.fiscal import get_fiscal_quarter, assign_fiscal_quarters


class TestFiscal:
    def test_q1_february(self):
        date = pd.Timestamp("2024-02-15")
        assert get_fiscal_quarter(date) == "FY2025-Q1"

    def test_q1_april(self):
        date = pd.Timestamp("2024-04-30")
        assert get_fiscal_quarter(date) == "FY2025-Q1"

    def test_q2_may(self):
        date = pd.Timestamp("2024-05-01")
        assert get_fiscal_quarter(date) == "FY2025-Q2"

    def test_q3_august(self):
        date = pd.Timestamp("2024-08-15")
        assert get_fiscal_quarter(date) == "FY2025-Q3"

    def test_q4_november(self):
        date = pd.Timestamp("2024-11-01")
        assert get_fiscal_quarter(date) == "FY2025-Q4"

    def test_q4_january(self):
        date = pd.Timestamp("2025-01-31")
        assert get_fiscal_quarter(date) == "FY2025-Q4"

    def test_assign_fiscal_quarters(self):
        df = pd.DataFrame({
            "transaction_date": pd.to_datetime(["2024-08-15", "2024-11-10"]),
            "amount": [100, 200],
        })
        result = assign_fiscal_quarters(df)
        assert "fiscal_quarter" in result.columns
        assert result["fiscal_quarter"].iloc[0] == "FY2025-Q3"
        assert result["fiscal_quarter"].iloc[1] == "FY2025-Q4"
