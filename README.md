# DataClean

A CSV data pipeline for processing customer order data, enriching it with
reference data, and generating summary reports.

## Features

- Read and validate CSV order data
- Clean and normalize customer identifiers
- Merge with customer reference data and regional zip code mappings
- Aggregate order data by region, customer tier, and time period
- Generate formatted summary reports

## Usage

```python
from dataclean import Pipeline

pipeline = Pipeline(
    orders_path="data/orders.csv",
    customers_path="data/customers.csv",
    regions_path="data/regions.csv",
)
report = pipeline.run()
print(report.summary())
```

## Installation

```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest -v
```
