---
name: data-science
description: Master data analysis, visualization, statistics, and storytelling techniques to extract insights from data.
---

# Data Science

## Quick Start

Analyze data and extract actionable insights using statistics and visualization.

## Exploratory Data Analysis (EDA)

### Data Exploration

**First Steps**
```python
import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())
```

**Distribution Analysis**
- Histograms (frequency distribution)
- Box plots (quartiles, outliers)
- Density plots (smooth distribution)
- KDE plots (kernel density estimation)

### Statistical Summary

- **Mean** - Average value
- **Median** - Middle value
- **Mode** - Most frequent
- **Std Dev** - Spread around mean
- **Variance** - Squared standard deviation
- **Skewness** - Asymmetry
- **Kurtosis** - Tail heaviness

## Statistical Concepts

### Hypothesis Testing

```python
from scipy import stats

# T-test: compare two groups
t_stat, p_value = stats.ttest_ind(group1, group2)

# P-value interpretation
if p_value < 0.05:
    print("Reject null hypothesis")
```

**Common Tests**
- T-test (two groups)
- ANOVA (multiple groups)
- Chi-square (categorical)
- Mann-Whitney (non-parametric)

### Correlation & Causation

**Correlation Coefficient**
- Pearson: Linear relationships
- Spearman: Rank-based
- Kendall: Robust to outliers

**Causal Inference**
- Correlation ≠ Causation
- Confounding variables
- Randomized experiments needed

## Data Visualization

### Visualization Types

**Categorical Data**
- Bar charts (comparisons)
- Pie charts (proportions)
- Count plots (frequencies)

**Numerical Data**
- Line plots (trends)
- Scatter plots (relationships)
- Histograms (distributions)
- Box plots (outliers)

**Relationships**
- Heatmaps (correlations)
- Pair plots (pairwise relationships)
- Bubble charts (3 dimensions)

### Visualization Tools

```python
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Matplotlib: Low-level, flexible
plt.figure(figsize=(10, 6))
plt.hist(data, bins=30)
plt.show()

# Seaborn: High-level, statistical
sns.heatmap(corr_matrix, annot=True)
plt.show()

# Plotly: Interactive, web-ready
fig = px.scatter(df, x='x', y='y', color='category')
fig.show()
```

## Time Series Analysis

**Components**
- Trend (long-term direction)
- Seasonality (regular pattern)
- Cyclicity (irregular pattern)
- Noise (random fluctuation)

**Decomposition**
```python
from statsmodels.tsa.seasonal import seasonal_decompose

result = seasonal_decompose(series, model='additive', period=12)
result.plot()
```

**Forecasting**
- ARIMA (autoregressive)
- Exponential Smoothing
- Prophet (Facebook)
- Neural networks (LSTM)

## A/B Testing

### Test Setup

```python
from scipy.stats import chi2_contingency

contingency_table = [[control_success, control_fail],
                     [test_success, test_fail]]

chi2, p_value, dof, expected = chi2_contingency(contingency_table)
```

**Key Metrics**
- Statistical significance (p < 0.05)
- Effect size (practical significance)
- Confidence interval
- Power (probability of detecting effect)

## Storytelling with Data

### Narrative Structure

1. **Context** - Why this analysis matters
2. **Data** - Show relevant evidence
3. **Insight** - Key finding
4. **Action** - Recommended next step

### Visualization Best Practices

- Simple, uncluttered
- Use color strategically
- Avoid misleading scales
- Include titles and labels
- Provide context

## Roadmaps Covered

- Data Analyst (https://roadmap.sh/data-analyst)
- AI and Data Scientist (https://roadmap.sh/ai-data-scientist)
