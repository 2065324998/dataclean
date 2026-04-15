"""Read CSV data files into DataFrames."""

import pandas as pd
from pathlib import Path


def read_orders(path: str | Path) -> pd.DataFrame:
    """Read the orders CSV file.

    Parses order data including order IDs, customer IDs, dates, amounts,
    zip codes, and product categories.
    """
    df = pd.read_csv(path, parse_dates=["order_date"])
    return df


def read_customers(path: str | Path) -> pd.DataFrame:
    """Read the customer reference CSV file.

    Contains customer names, tiers, and signup dates.
    """
    df = pd.read_csv(path, parse_dates=["signup_date"])
    return df


def read_regions(path: str | Path) -> pd.DataFrame:
    """Read the regional zip code mapping CSV file.

    Maps zip codes to states and regions for geographic analysis.
    """
    df = pd.read_csv(path, dtype={"zip_code": str})
    return df
