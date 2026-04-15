"""Main pipeline orchestration."""

from pathlib import Path
import pandas as pd

from dataclean.reader import read_transactions, read_salespeople
from dataclean.cleaner import clean_amounts, standardize_dates
from dataclean.commission import compute_commissions
from dataclean.fiscal import assign_fiscal_quarters
from dataclean.reporter import generate_report, CommissionReport


class Pipeline:
    """End-to-end sales commission processing pipeline.

    Reads transaction and salesperson CSV files, cleans the data,
    calculates commissions, and produces a quarterly commission report.
    """

    def __init__(self, transactions_path: str | Path,
                 salespeople_path: str | Path):
        self.transactions_path = Path(transactions_path)
        self.salespeople_path = Path(salespeople_path)

    def run(self) -> CommissionReport:
        """Execute the full pipeline and return a commission report."""
        # Step 1: Read data
        transactions = read_transactions(self.transactions_path)
        salespeople = read_salespeople(self.salespeople_path)

        # Step 2: Clean transaction data
        transactions = clean_amounts(transactions)
        transactions = standardize_dates(transactions)

        # Step 3: Calculate commissions
        commission_details = compute_commissions(transactions)

        # Step 4: Assign fiscal quarters
        commission_details = assign_fiscal_quarters(commission_details)

        # Step 5: Merge with salesperson info
        enriched = pd.merge(
            commission_details, salespeople,
            on="salesperson_id", how="left"
        )

        # Step 6: Aggregate
        by_quarter = self._aggregate_by_quarter(enriched)
        by_salesperson = self._aggregate_by_salesperson(enriched)
        by_sp_quarter = self._aggregate_by_sp_quarter(enriched)

        return generate_report(by_quarter, by_salesperson, by_sp_quarter,
                               enriched)

    def _aggregate_by_quarter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate commissions by fiscal quarter."""
        return (
            df.groupby("fiscal_quarter")
            .agg(
                transaction_count=("transaction_id", "count"),
                total_sales=("amount", "sum"),
                total_commission=("commission", "sum"),
            )
            .reset_index()
            .sort_values("fiscal_quarter")
        )

    def _aggregate_by_salesperson(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate commissions by salesperson."""
        return (
            df.groupby(["salesperson_id", "name"])
            .agg(
                transaction_count=("transaction_id", "count"),
                total_sales=("amount", "sum"),
                total_commission=("commission", "sum"),
            )
            .reset_index()
            .sort_values("total_commission", ascending=False)
        )

    def _aggregate_by_sp_quarter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate commissions by salesperson and fiscal quarter."""
        return (
            df.groupby(["salesperson_id", "name", "fiscal_quarter"])
            .agg(
                transaction_count=("transaction_id", "count"),
                total_sales=("amount", "sum"),
                total_commission=("commission", "sum"),
            )
            .reset_index()
            .sort_values(["fiscal_quarter", "total_commission"],
                         ascending=[True, False])
        )
