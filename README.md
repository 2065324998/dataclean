# DataClean — Sales Commission Pipeline

A data pipeline for processing sales transactions and calculating
quarterly commissions for a sales team.

## Features

- Read and validate CSV transaction data
- Clean and normalize amounts and dates
- Calculate tiered commissions based on cumulative sales volume
- Assign fiscal quarters (fiscal year starts February)
- Generate quarterly commission reports per salesperson

## Usage

```python
from dataclean import Pipeline

pipeline = Pipeline(
    transactions_path="data/transactions.csv",
    salespeople_path="data/salespeople.csv",
)
report = pipeline.run()
print(report.summary())
```

## Commission Tiers

| Tier | Sales Range       | Rate |
|------|-------------------|------|
| 1    | $0 - $10,000      | 5%   |
| 2    | $10,001 - $25,000 | 8%   |
| 3    | $25,001+          | 12%  |

## Installation

```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest -v
```
