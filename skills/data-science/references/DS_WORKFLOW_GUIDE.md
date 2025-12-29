# Data Science Workflow Guide

## CRISP-DM Process

1. **Business Understanding** - Define objectives
2. **Data Understanding** - EDA, quality assessment
3. **Data Preparation** - Cleaning, feature engineering
4. **Modeling** - Algorithm selection, training
5. **Evaluation** - Metrics, validation
6. **Deployment** - Production integration

## Feature Engineering

| Technique | Use Case |
|-----------|----------|
| One-hot | Categorical |
| Target encoding | High cardinality |
| Binning | Continuous → Categorical |
| Log transform | Skewed distributions |
| Polynomial | Non-linear relationships |

## Model Selection

```
Classification → Logistic, RF, XGBoost
Regression → Linear, RF, XGBoost
Clustering → K-Means, DBSCAN
Time Series → ARIMA, Prophet
```

## Evaluation Metrics

### Classification
- Accuracy, Precision, Recall, F1
- AUC-ROC, PR-AUC
- Confusion Matrix

### Regression
- MAE, MSE, RMSE, R²
- MAPE, SMAPE
