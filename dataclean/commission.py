"""Sales commission calculation.

Commission is calculated using a tiered rate structure based on
cumulative sales volume within each fiscal quarter:

    Tier 1: $0 - $10,000          5%
    Tier 2: $10,001 - $25,000     8%
    Tier 3: $25,001+              12%

Tenured salespeople (1+ year with the company as of the transaction
date) use accelerated tier thresholds that reward loyalty:

    Tier 1: $0 - $8,000           5%
    Tier 2: $8,001 - $20,000      8%
    Tier 3: $20,001+              12%

Product category multipliers adjust the tier-2-and-above portion of
each transaction's commission. Tier 1 earnings always use the base
rate:

    Enterprise: 1.5x on Tier 2+ commission
    SMB:        1.0x (standard rate on all tiers)

After computing all transaction-level commissions for a quarter, a
performance multiplier is applied based on quota attainment:

    Below 50% of quota:   0.8x
    50% - 100% of quota:  1.0x
    Above 100% of quota:  1.2x

Commission tiers reset at the start of each fiscal quarter.
Cumulative sales from prior quarters do not carry over.
"""

import pandas as pd


COMMISSION_TIERS = [
    (0, 10_000, 0.05),
    (10_000, 25_000, 0.08),
    (25_000, None, 0.12),
]

ACCELERATED_TIERS = [
    (0, 8_000, 0.05),
    (8_000, 20_000, 0.08),
    (20_000, None, 0.12),
]

CATEGORY_MULTIPLIERS = {
    "Enterprise": 1.5,
    "SMB": 1.0,
}

QUOTA_MULTIPLIERS = {
    "exceeds": 1.2,   # > 100% of quota
    "meets": 1.0,     # 50-100% of quota
    "below": 0.8,     # < 50% of quota
}

TENURE_THRESHOLD_DAYS = 365


def get_commission_rate(cumulative_sales: float) -> float:
    """Determine the commission rate for a given cumulative sales amount.

    Returns the rate of the tier that the cumulative total falls into.
    """
    rate = COMMISSION_TIERS[0][2]
    for lower, upper, tier_rate in COMMISSION_TIERS:
        if cumulative_sales > lower:
            rate = tier_rate
    return rate


def calculate_total_commission(cumulative_sales: float) -> float:
    """Calculate total commission earned on cumulative sales volume.

    Uses the tiered rate structure to determine the commission amount.
    """
    rate = get_commission_rate(cumulative_sales)
    return round(cumulative_sales * rate, 2)


def compute_commissions(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-transaction commission for each salesperson.

    Processes transactions in chronological order, tracking cumulative
    sales to determine the correct commission tier. Each transaction's
    commission is the incremental change in total commission.
    """
    results = []

    for sp_id in transactions_df["salesperson_id"].unique():
        sp_txns = transactions_df[
            transactions_df["salesperson_id"] == sp_id
        ].copy()
        sp_txns = sp_txns.sort_values("transaction_date")

        cumulative = 0.0
        prev_total_commission = 0.0

        for _, txn in sp_txns.iterrows():
            cumulative += txn["amount"]
            total_commission = calculate_total_commission(cumulative)
            commission_delta = total_commission - prev_total_commission
            prev_total_commission = total_commission

            results.append({
                "transaction_id": txn["transaction_id"],
                "salesperson_id": sp_id,
                "transaction_date": txn["transaction_date"],
                "amount": txn["amount"],
                "cumulative_sales": cumulative,
                "commission": round(commission_delta, 2),
            })

    return pd.DataFrame(results)
