"""Basic pipeline smoke tests."""

import pytest
from pathlib import Path

from dataclean.pipeline import Pipeline

DATA_DIR = Path(__file__).parent.parent / "data"


class TestPipeline:
    def test_pipeline_produces_report(self):
        pipeline = Pipeline(
            transactions_path=DATA_DIR / "transactions.csv",
            salespeople_path=DATA_DIR / "salespeople.csv",
        )
        report = pipeline.run()
        assert report is not None
        assert report.by_quarter is not None
        assert report.by_salesperson is not None

    def test_pipeline_report_has_all_salespeople(self):
        pipeline = Pipeline(
            transactions_path=DATA_DIR / "transactions.csv",
            salespeople_path=DATA_DIR / "salespeople.csv",
        )
        report = pipeline.run()
        sp_ids = set(report.by_salesperson["salesperson_id"])
        assert sp_ids == {"S001", "S002", "S003"}

    def test_pipeline_s003_commission(self):
        """S003 only has tier-1 sales ($5K total), commission should be $250."""
        pipeline = Pipeline(
            transactions_path=DATA_DIR / "transactions.csv",
            salespeople_path=DATA_DIR / "salespeople.csv",
        )
        report = pipeline.run()
        s003_total = report.get_total_commission("S003")
        assert s003_total == pytest.approx(250.0, abs=1.0)

    def test_pipeline_report_summary(self):
        pipeline = Pipeline(
            transactions_path=DATA_DIR / "transactions.csv",
            salespeople_path=DATA_DIR / "salespeople.csv",
        )
        report = pipeline.run()
        summary = report.summary()
        assert "Commission Report" in summary
        assert "Alice Chen" in summary
