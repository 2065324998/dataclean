"""Report generation from commission data."""

import pandas as pd


class CommissionReport:
    """Container for commission pipeline output."""

    def __init__(self, by_quarter: pd.DataFrame, by_salesperson: pd.DataFrame,
                 by_sp_quarter: pd.DataFrame, details: pd.DataFrame):
        self.by_quarter = by_quarter
        self.by_salesperson = by_salesperson
        self.by_sp_quarter = by_sp_quarter
        self.details = details

    def get_quarterly_commission(self, salesperson_id: str,
                                fiscal_quarter: str) -> float:
        """Get total commission for a salesperson in a specific quarter."""
        match = self.by_sp_quarter[
            (self.by_sp_quarter["salesperson_id"] == salesperson_id) &
            (self.by_sp_quarter["fiscal_quarter"] == fiscal_quarter)
        ]
        if match.empty:
            return 0.0
        return float(match["total_commission"].iloc[0])

    def get_total_commission(self, salesperson_id: str) -> float:
        """Get total commission for a salesperson across all quarters."""
        match = self.by_salesperson[
            self.by_salesperson["salesperson_id"] == salesperson_id
        ]
        if match.empty:
            return 0.0
        return float(match["total_commission"].iloc[0])

    def get_quarter_total(self, fiscal_quarter: str) -> float:
        """Get total commission for all salespeople in a quarter."""
        match = self.by_quarter[
            self.by_quarter["fiscal_quarter"] == fiscal_quarter
        ]
        if match.empty:
            return 0.0
        return float(match["total_commission"].iloc[0])

    def get_transaction_details(self, salesperson_id: str) -> pd.DataFrame:
        """Get detailed transaction-level commission data for a salesperson."""
        return self.details[
            self.details["salesperson_id"] == salesperson_id
        ].copy()

    def summary(self) -> str:
        """Generate a text summary of the commission report."""
        lines = ["=== Commission Report ===", ""]

        lines.append("--- By Fiscal Quarter ---")
        for _, row in self.by_quarter.iterrows():
            lines.append(
                f"  {row['fiscal_quarter']}: "
                f"{row['transaction_count']} transactions, "
                f"${row['total_sales']:,.2f} sales, "
                f"${row['total_commission']:,.2f} commission"
            )

        lines.append("")
        lines.append("--- By Salesperson ---")
        for _, row in self.by_salesperson.iterrows():
            lines.append(
                f"  {row['name']} ({row['salesperson_id']}): "
                f"${row['total_commission']:,.2f} commission on "
                f"${row['total_sales']:,.2f} sales"
            )

        return "\n".join(lines)


def generate_report(by_quarter: pd.DataFrame, by_salesperson: pd.DataFrame,
                    by_sp_quarter: pd.DataFrame,
                    details: pd.DataFrame) -> CommissionReport:
    """Create a CommissionReport from aggregated DataFrames."""
    return CommissionReport(by_quarter, by_salesperson, by_sp_quarter, details)
