"""Main pipeline orchestration."""

from pathlib import Path
import pandas as pd

from dataclean.reader import read_orders, read_customers, read_regions
from dataclean.cleaner import clean_amounts, standardize_dates
from dataclean.merger import merge_with_customers, merge_with_regions
from dataclean.aggregator import (
    aggregate_by_region,
    aggregate_by_tier,
    aggregate_by_category,
    aggregate_by_month,
)
from dataclean.reporter import generate_report, Report


class Pipeline:
    """End-to-end data processing pipeline.

    Reads CSV files, cleans and merges data, aggregates results,
    and produces a summary report.
    """

    def __init__(self, orders_path: str | Path,
                 customers_path: str | Path,
                 regions_path: str | Path):
        self.orders_path = Path(orders_path)
        self.customers_path = Path(customers_path)
        self.regions_path = Path(regions_path)

    def run(self) -> Report:
        """Execute the full pipeline and return a report."""
        # Step 1: Read data
        orders = read_orders(self.orders_path)
        customers = read_customers(self.customers_path)
        regions = read_regions(self.regions_path)

        # Step 2: Clean order data
        orders = clean_amounts(orders)
        orders = standardize_dates(orders)

        # Step 3: Merge with reference data
        enriched = merge_with_customers(orders, customers)
        enriched = merge_with_regions(enriched, regions)

        # Step 4: Aggregate
        by_region = aggregate_by_region(enriched)
        by_tier = aggregate_by_tier(enriched)
        by_category = aggregate_by_category(enriched)
        by_month = aggregate_by_month(enriched)

        # Step 5: Generate report
        return generate_report(
            by_region, by_tier, by_category, by_month, enriched
        )
