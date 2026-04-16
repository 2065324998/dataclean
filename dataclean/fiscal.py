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

# Maps calendar month to fiscal quarter.
_QUARTER_FOR_MONTH = {
    2: 1, 3: 1, 4: 1,           # Q1: Feb - Apr
    5: 2, 6: 2, 7: 2,           # Q2: May - Jul
    8: 3, 9: 3,                  # Q3: Aug - Sep
    10: 4, 11: 4, 12: 4, 1: 4,  # Q4: Oct - Jan
}


def get_fiscal_quarter(date) -> str:
    """Get the fiscal quarter label for a given date.

    Returns a string like 'FY2025-Q3' indicating the fiscal year
    and quarter the date falls into.
    """
    month = date.month
    quarter = _QUARTER_FOR_MONTH[month]
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
