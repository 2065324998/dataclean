"""Data validation utilities."""

import pandas as pd
import re


def validate_zip_code(zip_code: str) -> bool:
    """Check if a zip code is in valid 5-digit format."""
    if not isinstance(zip_code, str):
        return False
    return bool(re.match(r"^\d{5}$", zip_code))


def validate_order_amounts(df: pd.DataFrame) -> pd.DataFrame:
    """Flag orders with invalid amounts (negative or zero)."""
    df = df.copy()
    df["amount_valid"] = df["amount"] > 0
    return df


def validate_required_columns(df: pd.DataFrame,
                              required: list[str]) -> list[str]:
    """Check that all required columns exist in the DataFrame."""
    missing = [col for col in required if col not in df.columns]
    return missing


def get_null_counts(df: pd.DataFrame) -> dict[str, int]:
    """Get count of null values per column."""
    return df.isnull().sum().to_dict()
