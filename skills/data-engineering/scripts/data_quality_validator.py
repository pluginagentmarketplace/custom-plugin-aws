#!/usr/bin/env python3
"""Data quality validation framework."""

import pandas as pd
from typing import Dict, List

class DataValidator:
    """Validate data quality."""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.results = []

    def check_nulls(self, columns: List[str], threshold: float = 0.1) -> bool:
        """Check null percentage threshold."""
        for col in columns:
            null_pct = self.df[col].isnull().mean()
            passed = null_pct <= threshold
            self.results.append({
                "check": "null_check",
                "column": col,
                "value": null_pct,
                "passed": passed
            })
        return all(r["passed"] for r in self.results if r["check"] == "null_check")

    def check_unique(self, columns: List[str]) -> bool:
        """Check uniqueness constraint."""
        for col in columns:
            is_unique = self.df[col].is_unique
            self.results.append({
                "check": "unique_check",
                "column": col,
                "passed": is_unique
            })
        return all(r["passed"] for r in self.results if r["check"] == "unique_check")

    def check_range(self, column: str, min_val: float, max_val: float) -> bool:
        """Check value range."""
        in_range = self.df[column].between(min_val, max_val).all()
        self.results.append({
            "check": "range_check",
            "column": column,
            "passed": in_range
        })
        return in_range

    def report(self) -> Dict:
        """Generate validation report."""
        passed = sum(1 for r in self.results if r["passed"])
        return {
            "total_checks": len(self.results),
            "passed": passed,
            "failed": len(self.results) - passed,
            "details": self.results
        }

if __name__ == "__main__":
    df = pd.DataFrame({"id": [1, 2, 3], "value": [10, 20, 30]})
    validator = DataValidator(df)
    validator.check_nulls(["id", "value"])
    validator.check_unique(["id"])
    print(validator.report())
