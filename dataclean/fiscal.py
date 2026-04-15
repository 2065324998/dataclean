"""Fiscal period utilities.

The company's fiscal year starts on February 1.
FY2025 runs from February 2024 through January 2025.

Quarters:
    Q1: February - April
    Q2: May - July
    Q3: August - October
    Q4: November - January
"""

import pandas as pd

FISCAL_YEAR_START_MONTH = 2


def get_fiscal_quarter(date) -> str:
    """Get the fiscal quarter label for a given date.

    Returns a string like 'FY2025-Q3' indicating the fiscal year
    and quarter the date falls into.
    """
    month = date.month
    shifted = (month - FISCAL_YEAR_START_MONTH) % 12 + 1
    quarter = (shifted - 1) // 3 + 1
    if month >= FISCAL_YEAR_START_MONTH:
        fiscal_year = date.year + 1
    else:
        fiscal_year = date.year
    return f"FY{fiscal_year}-Q{quarter}"


def assign_fiscal_quarters(
    df: pd.DataFrame, date_col: str = "transaction_date"
) -> pd.DataFrame:
    """Add a fiscal_quarter column to a DataFrame based on transaction dates."""
    df = df.copy()
    df["fiscal_quarter"] = df[date_col].apply(get_fiscal_quarter)
    return df
