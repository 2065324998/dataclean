"""Data cleaning and normalization utilities."""

import pandas as pd


def normalize_customer_id(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize customer IDs by stripping the 'C' prefix and converting to int.

    The customer reference file uses 'C'-prefixed IDs (e.g., 'C1001') while
    the orders file uses plain integers (e.g., 1001). This function strips
    the prefix for merge compatibility.
    """
    df = df.copy()
    if hasattr(df["customer_id"], "str"):
        try:
            df["customer_id"] = (
                df["customer_id"]
                .astype(str)
                .str.replace("C", "", regex=False)
                .astype(int)
            )
        except (ValueError, TypeError):
            pass
    return df


def clean_amounts(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure amount column is numeric, handling currency symbols."""
    df = df.copy()
    if not pd.api.types.is_numeric_dtype(df["amount"]):
        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(float)
        )
    return df


def standardize_dates(df: pd.DataFrame, date_col: str = "order_date") -> pd.DataFrame:
    """Ensure date column is datetime type."""
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])
    return df


def remove_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """Remove duplicate rows based on subset columns."""
    return df.drop_duplicates(subset=subset).reset_index(drop=True)
