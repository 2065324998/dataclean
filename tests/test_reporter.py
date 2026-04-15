"""Tests for the reporter module."""

import pandas as pd

from dataclean.reporter import Report, generate_report


class TestReporter:
    def _make_report(self):
        by_region = pd.DataFrame({
            "region": ["Northeast", "West"],
            "order_count": [5, 3],
            "total_amount": [1000.0, 800.0],
        })
        by_tier = pd.DataFrame({
            "tier": ["Gold", "Silver"],
            "order_count": [4, 4],
            "total_amount": [1200.0, 600.0],
            "avg_order_value": [300.0, 150.0],
        })
        by_category = pd.DataFrame({
            "product_category": ["Electronics", "Books"],
            "order_count": [3, 5],
            "total_amount": [900.0, 400.0],
        })
        by_month = pd.DataFrame({
            "month": ["2024-01"],
            "order_count": [8],
            "total_amount": [1800.0],
        })
        enriched = pd.DataFrame({
            "order_id": [1],
            "zip_code": ["07102"],
        })
        return generate_report(by_region, by_tier, by_category, by_month, enriched)

    def test_summary_contains_regions(self):
        report = self._make_report()
        text = report.summary()
        assert "Northeast" in text
        assert "West" in text

    def test_get_region_total(self):
        report = self._make_report()
        assert report.get_region_total("Northeast") == 1000.0
        assert report.get_region_total("Nonexistent") == 0.0

    def test_get_region_count(self):
        report = self._make_report()
        assert report.get_region_count("West") == 3

    def test_zip_code_validity(self):
        report = self._make_report()
        validity = report.get_zip_code_validity()
        assert validity["07102"] is True
