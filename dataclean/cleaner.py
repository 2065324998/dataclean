"""Data cleaning and normalization utilities."""

import pandas as pd


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


def standardize_dates(
    df: pd.DataFrame, date_col: str = "transaction_date"
) -> pd.DataFrame:
    """Ensure date column is datetime type."""
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])
    return df


def remove_duplicates(
    df: pd.DataFrame, subset: list[str] | None = None
) -> pd.DataFrame:
    """Remove duplicate rows based on subset columns."""
    return df.drop_duplicates(subset=subset).reset_index(drop=True)
