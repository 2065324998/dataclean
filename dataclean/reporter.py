"""Report generation from aggregated data."""

import pandas as pd
from dataclean.validators import validate_zip_code


class Report:
    """Container for pipeline output report."""

    def __init__(self, by_region: pd.DataFrame, by_tier: pd.DataFrame,
                 by_category: pd.DataFrame, by_month: pd.DataFrame,
                 enriched_orders: pd.DataFrame):
        self.by_region = by_region
        self.by_tier = by_tier
        self.by_category = by_category
        self.by_month = by_month
        self.enriched_orders = enriched_orders

    def summary(self) -> str:
        """Generate a text summary of the report."""
        lines = ["=== Order Summary Report ===", ""]

        lines.append("--- By Region ---")
        for _, row in self.by_region.iterrows():
            lines.append(
                f"  {row['region']}: {row['order_count']} orders, "
                f"${row['total_amount']:,.2f}"
            )

        lines.append("")
        lines.append("--- By Customer Tier ---")
        for _, row in self.by_tier.iterrows():
            lines.append(
                f"  {row['tier']}: {row['order_count']} orders, "
                f"${row['total_amount']:,.2f} "
                f"(avg ${row['avg_order_value']:,.2f})"
            )

        lines.append("")
        lines.append("--- By Category ---")
        for _, row in self.by_category.iterrows():
            lines.append(
                f"  {row['product_category']}: {row['order_count']} orders, "
                f"${row['total_amount']:,.2f}"
            )

        return "\n".join(lines)

    def get_region_total(self, region: str) -> float:
        """Get total order amount for a specific region."""
        match = self.by_region[self.by_region["region"] == region]
        if match.empty:
            return 0.0
        return float(match["total_amount"].iloc[0])

    def get_region_count(self, region: str) -> int:
        """Get order count for a specific region."""
        match = self.by_region[self.by_region["region"] == region]
        if match.empty:
            return 0
        return int(match["order_count"].iloc[0])

    def get_zip_code_validity(self) -> dict[str, bool]:
        """Check zip code validity across all orders."""
        result = {}
        for zip_code in self.enriched_orders["zip_code"].unique():
            result[str(zip_code)] = validate_zip_code(str(zip_code))
        return result


def generate_report(by_region: pd.DataFrame, by_tier: pd.DataFrame,
                    by_category: pd.DataFrame, by_month: pd.DataFrame,
                    enriched_orders: pd.DataFrame) -> Report:
    """Create a Report from aggregated DataFrames."""
    return Report(by_region, by_tier, by_category, by_month, enriched_orders)
