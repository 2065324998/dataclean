"""Tests for the reporter module."""

import pandas as pd

from dataclean.reporter import CommissionReport, generate_report


class TestReporter:
    def _make_report(self):
        by_quarter = pd.DataFrame({
            "fiscal_quarter": ["FY2025-Q3"],
            "transaction_count": [5],
            "total_sales": [30000.0],
            "total_commission": [1500.0],
        })
        by_salesperson = pd.DataFrame({
            "salesperson_id": ["S001"],
            "name": ["Alice Chen"],
            "transaction_count": [5],
            "total_sales": [30000.0],
            "total_commission": [1500.0],
        })
        by_sp_quarter = pd.DataFrame({
            "salesperson_id": ["S001"],
            "name": ["Alice Chen"],
            "fiscal_quarter": ["FY2025-Q3"],
            "transaction_count": [5],
            "total_sales": [30000.0],
            "total_commission": [1500.0],
        })
        details = pd.DataFrame({
            "transaction_id": ["T001"],
            "salesperson_id": ["S001"],
            "amount": [5000.0],
            "commission": [250.0],
            "fiscal_quarter": ["FY2025-Q3"],
        })
        return generate_report(by_quarter, by_salesperson,
                               by_sp_quarter, details)

    def test_summary_contains_quarter(self):
        report = self._make_report()
        text = report.summary()
        assert "FY2025-Q3" in text

    def test_summary_contains_salesperson(self):
        report = self._make_report()
        text = report.summary()
        assert "Alice Chen" in text

    def test_get_quarterly_commission(self):
        report = self._make_report()
        assert report.get_quarterly_commission("S001", "FY2025-Q3") == 1500.0
        assert report.get_quarterly_commission("S001", "FY2025-Q4") == 0.0

    def test_get_total_commission(self):
        report = self._make_report()
        assert report.get_total_commission("S001") == 1500.0
        assert report.get_total_commission("S999") == 0.0

    def test_get_quarter_total(self):
        report = self._make_report()
        assert report.get_quarter_total("FY2025-Q3") == 1500.0

    def test_get_transaction_details(self):
        report = self._make_report()
        details = report.get_transaction_details("S001")
        assert len(details) == 1
        assert details["commission"].iloc[0] == 250.0
