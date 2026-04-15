"""Tests for the commission calculation module."""

import pandas as pd

from dataclean.commission import (
    compute_commissions,
    calculate_total_commission,
    get_commission_rate,
    COMMISSION_TIERS,
    ACCELERATED_TIERS,
    CATEGORY_MULTIPLIERS,
    QUOTA_MULTIPLIERS,
    TENURE_THRESHOLD_DAYS,
)


def _make_transactions(entries):
    """Helper to create a transactions DataFrame.

    entries: list of (salesperson_id, date_str, amount) tuples
    """
    records = []
    for i, (sp_id, date, amount) in enumerate(entries):
        records.append({
            "transaction_id": f"T{i + 1:03d}",
            "salesperson_id": sp_id,
            "transaction_date": pd.Timestamp(date),
            "amount": amount,
            "product_category": "Test",
        })
    return pd.DataFrame(records)


class TestCommissionRates:
    def test_tier_structure(self):
        """Commission tiers should be defined."""
        assert len(COMMISSION_TIERS) == 3
        assert COMMISSION_TIERS[0][2] == 0.05
        assert COMMISSION_TIERS[1][2] == 0.08
        assert COMMISSION_TIERS[2][2] == 0.12

    def test_accelerated_tier_structure(self):
        """Accelerated tiers should have tighter boundaries."""
        assert len(ACCELERATED_TIERS) == 3
        assert ACCELERATED_TIERS[0][1] == 8_000
        assert ACCELERATED_TIERS[1][1] == 20_000
        assert ACCELERATED_TIERS[0][2] == 0.05

    def test_rate_tier1(self):
        """Amounts in tier 1 should get 5% rate."""
        assert get_commission_rate(5000) == 0.05
        assert get_commission_rate(9999) == 0.05

    def test_rate_at_boundary(self):
        """$10,000 exactly should be tier 1 (5%)."""
        assert get_commission_rate(10000) == 0.05

    def test_category_multipliers(self):
        """Category multipliers should be defined."""
        assert CATEGORY_MULTIPLIERS["Enterprise"] == 1.5
        assert CATEGORY_MULTIPLIERS["SMB"] == 1.0

    def test_quota_multipliers(self):
        """Quota multipliers should be defined."""
        assert QUOTA_MULTIPLIERS["exceeds"] == 1.2
        assert QUOTA_MULTIPLIERS["meets"] == 1.0
        assert QUOTA_MULTIPLIERS["below"] == 0.8

    def test_tenure_threshold(self):
        """Tenure threshold should be 365 days."""
        assert TENURE_THRESHOLD_DAYS == 365


class TestCommissionCalculation:
    def test_single_sale_tier1(self):
        """A single $5,000 sale should earn $250 (5%)."""
        txns = _make_transactions([("S001", "2024-08-15", 5000.0)])
        result = compute_commissions(txns)
        assert result["commission"].iloc[0] == 250.0

    def test_two_sales_within_tier1(self):
        """Two sales totaling $9,000 should earn $450."""
        txns = _make_transactions([
            ("S001", "2024-08-15", 5000.0),
            ("S001", "2024-08-20", 4000.0),
        ])
        result = compute_commissions(txns)
        assert result["commission"].sum() == 450.0
        assert result["commission"].iloc[0] == 250.0
        assert result["commission"].iloc[1] == 200.0

    def test_exact_tier_boundary(self):
        """$10,000 exactly should earn $500."""
        txns = _make_transactions([("S001", "2024-08-15", 10000.0)])
        result = compute_commissions(txns)
        assert result["commission"].iloc[0] == 500.0

    def test_return_within_tier1(self):
        """A return keeping cumulative in tier 1 should reduce commission."""
        txns = _make_transactions([
            ("S001", "2024-08-15", 8000.0),
            ("S001", "2024-08-20", -3000.0),
        ])
        result = compute_commissions(txns)
        assert result["commission"].iloc[0] == 400.0
        assert result["commission"].iloc[1] == -150.0

    def test_multiple_salespeople(self):
        """Each salesperson's commission is independent."""
        txns = _make_transactions([
            ("S001", "2024-08-15", 5000.0),
            ("S002", "2024-08-16", 3000.0),
        ])
        result = compute_commissions(txns)
        s001 = result[result["salesperson_id"] == "S001"]
        s002 = result[result["salesperson_id"] == "S002"]
        assert s001["commission"].iloc[0] == 250.0
        assert s002["commission"].iloc[0] == 150.0

    def test_cumulative_tracking(self):
        """Commission should track cumulative sales correctly."""
        txns = _make_transactions([
            ("S001", "2024-08-15", 3000.0),
            ("S001", "2024-08-20", 3000.0),
            ("S001", "2024-08-25", 3000.0),
        ])
        result = compute_commissions(txns)
        assert result["commission"].tolist() == [150.0, 150.0, 150.0]
