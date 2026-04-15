"""Merge order data with reference tables."""

import pandas as pd
from dataclean.cleaner import normalize_customer_id


def merge_with_customers(orders_df: pd.DataFrame,
                         customers_df: pd.DataFrame) -> pd.DataFrame:
    """Merge orders with customer reference data.

    Enriches order records with customer names, tiers, and signup dates.
    Uses a left join so all orders are preserved even if the customer
    is not found in the reference table.
    """
    # Normalize customer IDs in the reference table for merge compatibility
    customers_normalized = normalize_customer_id(customers_df)

    merged = pd.merge(orders_df, customers_normalized, on="customer_id", how="left")

    return merged


def merge_with_regions(orders_df: pd.DataFrame,
                       regions_df: pd.DataFrame) -> pd.DataFrame:
    """Merge orders with regional zip code mappings.

    Adds state and region information based on the order's zip code.
    Uses a left join so orders with unknown zip codes are preserved.
    """
    # Ensure zip_code types match for the merge
    orders_copy = orders_df.copy()
    orders_copy["zip_code"] = orders_copy["zip_code"].astype(str)

    merged = pd.merge(orders_copy, regions_df, on="zip_code", how="left")
    return merged
