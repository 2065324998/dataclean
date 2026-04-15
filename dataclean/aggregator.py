"""Aggregate order data for reporting."""

import pandas as pd


def aggregate_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate order totals by region.

    Returns a DataFrame with columns: region, order_count, total_amount.
    Only includes rows that have a valid region mapping.
    """
    regional = df.dropna(subset=["region"]).copy()
    result = (
        regional
        .groupby("region")
        .agg(
            order_count=("order_id", "count"),
            total_amount=("amount", "sum"),
        )
        .reset_index()
        .sort_values("total_amount", ascending=False)
    )
    return result


def aggregate_by_tier(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate order totals by customer tier.

    Returns a DataFrame with columns: tier, order_count, total_amount,
    avg_order_value.
    """
    tiered = df.dropna(subset=["tier"]).copy()
    result = (
        tiered
        .groupby("tier")
        .agg(
            order_count=("order_id", "count"),
            total_amount=("amount", "sum"),
        )
        .reset_index()
    )
    result["avg_order_value"] = (result["total_amount"] / result["order_count"]).round(2)
    return result.sort_values("total_amount", ascending=False)


def aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate order totals by product category."""
    result = (
        df
        .groupby("product_category")
        .agg(
            order_count=("order_id", "count"),
            total_amount=("amount", "sum"),
        )
        .reset_index()
        .sort_values("total_amount", ascending=False)
    )
    return result


def aggregate_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate order totals by month."""
    df = df.copy()
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    result = (
        df
        .groupby("month")
        .agg(
            order_count=("order_id", "count"),
            total_amount=("amount", "sum"),
        )
        .reset_index()
        .sort_values("month")
    )
    return result
