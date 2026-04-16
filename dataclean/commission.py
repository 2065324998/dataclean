"""Sales commission calculation.

Commission is calculated using a progressive tiered rate structure.
Each tier's rate applies only to the portion of sales falling within
that range, similar to marginal tax brackets. The tiers are based on
cumulative sales volume within each fiscal quarter:

    Tier 1: $0 - $10,000          5%
    Tier 2: $10,001 - $25,000     8%
    Tier 3: $25,001+              12%

Tenured salespeople — those who have been with the company for at
least one year as of the transaction date — qualify for accelerated
tier advancement. Their tier 1 covers only the first $8,000 (rather
than $10,000), tier 2 runs from $8,001 to $20,000 (rather than
$25,000), and tier 3 begins at $20,001. The rates themselves are
unchanged.

Product category multipliers scale the above-tier-1 (tier 2+) portion
of each transaction's commission. Tier 1 earnings always use the
standard rate regardless of product category:

    Enterprise: 1.5x on Tier 2+ commission
    SMB:        1.0x (standard rate on all tiers)

A quarterly performance bonus rewards salespeople who exceed their
quota target. The bonus is 20% of the base tier 2+ commission — the
commission amount computed at tier rates before category multipliers
are applied — added to each transaction's total. This supplements
the category-scaled commission rather than scaling it further. For
salespeople between 50% and 100% of quota, no adjustment is made.
Those below 50% have a penalty of 20% of base tier 2+ commission
deducted from each transaction.

Commission tiers reset at the start of each fiscal quarter.
Cumulative sales from prior quarters do not carry over.
"""

import pandas as pd


COMMISSION_TIERS = [
    (0, 10_000, 0.05),
    (10_000, 25_000, 0.08),
    (25_000, None, 0.12),
]

CATEGORY_MULTIPLIERS = {
    "Enterprise": 1.5,
    "SMB": 1.0,
}


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
