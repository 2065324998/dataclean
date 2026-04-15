"""Read CSV data files into DataFrames."""

import pandas as pd
from pathlib import Path


def read_transactions(path: str | Path) -> pd.DataFrame:
    """Read the transactions CSV file.

    Contains sales and return records with transaction IDs, salesperson
    IDs, dates, amounts, and product categories.
    """
    df = pd.read_csv(path, parse_dates=["transaction_date"])
    return df


def read_salespeople(path: str | Path) -> pd.DataFrame:
    """Read the salespeople reference CSV file.

    Contains salesperson names, teams, hire dates, and regions.
    """
    df = pd.read_csv(path, parse_dates=["hire_date"])
    return df
