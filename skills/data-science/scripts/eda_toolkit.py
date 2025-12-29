#!/usr/bin/env python3
"""Exploratory Data Analysis toolkit."""
import pandas as pd
import numpy as np

def quick_eda(df: pd.DataFrame) -> dict:
    """Generate quick EDA summary."""
    return {
        "shape": df.shape,
        "dtypes": df.dtypes.value_counts().to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "numeric_stats": df.describe().to_dict(),
        "categorical_unique": {col: df[col].nunique()
                              for col in df.select_dtypes(include='object').columns}
    }

def detect_outliers(df: pd.DataFrame, columns: list, method: str = 'iqr') -> dict:
    """Detect outliers using IQR method."""
    outliers = {}
    for col in columns:
        if method == 'iqr':
            Q1, Q3 = df[col].quantile([0.25, 0.75])
            IQR = Q3 - Q1
            outlier_mask = (df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)
            outliers[col] = outlier_mask.sum()
    return outliers

if __name__ == "__main__":
    df = pd.DataFrame({"a": [1, 2, 3, 100], "b": ["x", "y", None, "z"]})
    print(quick_eda(df))
