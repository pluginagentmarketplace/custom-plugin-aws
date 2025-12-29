# Machine Learning Algorithms Guide

Quick reference for ML algorithm selection and implementation.

## Algorithm Selection Flowchart

```
What type of output?
│
├── Continuous value → Regression
│   ├── Linear relationship → Linear Regression
│   ├── Non-linear → Random Forest, XGBoost, Neural Network
│   └── Time series → ARIMA, Prophet, LSTM
│
├── Category/Class → Classification
│   ├── Binary → Logistic Regression, SVM, XGBoost
│   ├── Multi-class → Random Forest, Neural Network
│   └── Multi-label → Multi-label classifiers
│
├── Groups/Clusters → Clustering
│   ├── Known k → K-Means
│   ├── Unknown k → DBSCAN, Hierarchical
│   └── Density-based → DBSCAN, OPTICS
│
└── Pattern/Anomaly → Anomaly Detection
    ├── Statistical → Isolation Forest
    └── Distance-based → LOF, One-Class SVM
```

## Supervised Learning

### Linear Models

| Algorithm | Use Case | Pros | Cons |
|-----------|----------|------|------|
| Linear Regression | Continuous prediction | Fast, interpretable | Assumes linearity |
| Logistic Regression | Binary classification | Probabilistic, fast | Linear boundaries |
| Ridge/Lasso | Regularized regression | Prevents overfitting | Requires scaling |

### Tree-Based

| Algorithm | Use Case | Pros | Cons |
|-----------|----------|------|------|
| Decision Tree | Classification/Regression | Interpretable | Overfits easily |
| Random Forest | General purpose | Robust, parallel | Memory intensive |
| XGBoost | Competition winner | High accuracy | Complex tuning |
| LightGBM | Large datasets | Fast, low memory | Sensitive to params |

### Support Vector Machines

```python
from sklearn.svm import SVC

# Classification
svc = SVC(kernel='rbf', C=1.0, gamma='scale')
svc.fit(X_train, y_train)

# Probability estimates
svc_proba = SVC(kernel='rbf', probability=True)
```

## Unsupervised Learning

### Clustering

```python
from sklearn.cluster import KMeans, DBSCAN

# K-Means (known k)
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# DBSCAN (unknown k)
dbscan = DBSCAN(eps=0.5, min_samples=5)
clusters = dbscan.fit_predict(X)
```

### Dimensionality Reduction

| Method | Use Case | Preserves |
|--------|----------|-----------|
| PCA | Linear reduction | Variance |
| t-SNE | Visualization | Local structure |
| UMAP | Fast visualization | Global + local |

## Model Evaluation Metrics

### Classification

| Metric | Formula | When to Use |
|--------|---------|-------------|
| Accuracy | (TP+TN)/(All) | Balanced classes |
| Precision | TP/(TP+FP) | Minimize false positives |
| Recall | TP/(TP+FN) | Minimize false negatives |
| F1 Score | 2×(P×R)/(P+R) | Balance P and R |
| AUC-ROC | Area under curve | Ranking quality |

### Regression

| Metric | Description |
|--------|-------------|
| MAE | Mean Absolute Error |
| MSE | Mean Squared Error |
| RMSE | Root MSE |
| R² | Explained variance |
| MAPE | Mean Absolute Percentage Error |

## Hyperparameter Tuning

### Grid Search

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
```

### Bayesian Optimization

```python
from optuna import create_study

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3)
    }
    model = XGBClassifier(**params)
    return cross_val_score(model, X, y, cv=5).mean()

study = create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```

## Feature Engineering

### Scaling

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Standardization (mean=0, std=1)
scaler = StandardScaler()

# Normalization (0-1 range)
normalizer = MinMaxScaler()
```

### Encoding

```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Label encoding
le = LabelEncoder()
encoded = le.fit_transform(categories)

# One-hot encoding
ohe = OneHotEncoder(sparse=False)
encoded = ohe.fit_transform(categories.reshape(-1, 1))
```

## Common Pitfalls

| Problem | Solution |
|---------|----------|
| Data leakage | Split before preprocessing |
| Imbalanced classes | SMOTE, class weights |
| Overfitting | Regularization, more data |
| Feature scaling | StandardScaler for most algorithms |
| Missing values | Imputation, tree-based models |
