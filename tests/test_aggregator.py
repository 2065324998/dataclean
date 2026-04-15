"""Tests for the aggregator module."""

import pandas as pd

from dataclean.aggregator import (
    aggregate_by_region,
    aggregate_by_tier,
    aggregate_by_category,
    aggregate_by_month,
)


class TestAggregator:
    def test_aggregate_by_region(self):
        df = pd.DataFrame({
            "order_id": [1, 2, 3],
            "amount": [100, 200, 300],
            "region": ["Northeast", "West", "Northeast"],
        })
        result = aggregate_by_region(df)
        assert len(result) == 2
        ne = result[result["region"] == "Northeast"]
        assert ne["order_count"].iloc[0] == 2
        assert ne["total_amount"].iloc[0] == 400

    def test_aggregate_by_region_drops_null(self):
        df = pd.DataFrame({
            "order_id": [1, 2],
            "amount": [100, 200],
            "region": ["Northeast", None],
        })
        result = aggregate_by_region(df)
        assert len(result) == 1

    def test_aggregate_by_tier(self):
        df = pd.DataFrame({
            "order_id": [1, 2, 3],
            "amount": [100, 200, 300],
            "tier": ["Gold", "Silver", "Gold"],
        })
        result = aggregate_by_tier(df)
        gold = result[result["tier"] == "Gold"]
        assert gold["order_count"].iloc[0] == 2
        assert gold["avg_order_value"].iloc[0] == 200.0

    def test_aggregate_by_category(self):
        df = pd.DataFrame({
            "order_id": [1, 2, 3],
            "amount": [100, 200, 150],
            "product_category": ["Books", "Electronics", "Books"],
        })
        result = aggregate_by_category(df)
        assert len(result) == 2
        books = result[result["product_category"] == "Books"]
        assert books["total_amount"].iloc[0] == 250

    def test_aggregate_by_month(self):
        df = pd.DataFrame({
            "order_id": [1, 2, 3],
            "amount": [100, 200, 300],
            "order_date": pd.to_datetime([
                "2024-01-15", "2024-01-20", "2024-02-10"
            ]),
        })
        result = aggregate_by_month(df)
        assert len(result) == 2
        jan = result[result["month"] == "2024-01"]
        assert jan["order_count"].iloc[0] == 2
