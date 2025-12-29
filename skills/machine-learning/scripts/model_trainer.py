#!/usr/bin/env python3
"""
ML Model Trainer
Train and evaluate machine learning models.
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                            f1_score, roc_auc_score, confusion_matrix,
                            classification_report)
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib


class ModelTrainer:
    """Train and evaluate ML models."""

    def __init__(self, model, config: Dict = None):
        self.model = model
        self.config = config or {}
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = None

    def prepare_data(self, X, y, test_size: float = 0.2, random_state: int = 42
                    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Prepare and split data."""
        # Store feature names if DataFrame
        if hasattr(X, 'columns'):
            self.feature_names = X.columns.tolist()
            X = X.values

        # Encode labels if needed
        if not np.issubdtype(y.dtype, np.number):
            y = self.label_encoder.fit_transform(y)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        # Scale features
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)

        return X_train, X_test, y_train, y_test

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """Train the model."""
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """Evaluate model performance."""
        y_pred = self.model.predict(X_test)
        y_proba = None

        if hasattr(self.model, 'predict_proba'):
            y_proba = self.model.predict_proba(X_test)[:, 1]

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1': f1_score(y_test, y_pred, average='weighted'),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }

        if y_proba is not None:
            metrics['roc_auc'] = roc_auc_score(y_test, y_proba)

        return metrics

    def cross_validate(self, X: np.ndarray, y: np.ndarray,
                      cv: int = 5) -> Dict[str, float]:
        """Perform cross-validation."""
        scores = cross_val_score(self.model, X, y, cv=cv, scoring='accuracy')
        return {
            'cv_mean': float(np.mean(scores)),
            'cv_std': float(np.std(scores)),
            'cv_scores': scores.tolist()
        }

    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance if available."""
        if not hasattr(self.model, 'feature_importances_'):
            return {}

        importance = self.model.feature_importances_

        if self.feature_names:
            return dict(zip(self.feature_names, importance.tolist()))
        return {f'feature_{i}': imp for i, imp in enumerate(importance)}

    def save(self, path: str) -> None:
        """Save model and preprocessors."""
        save_path = Path(path)
        save_path.mkdir(parents=True, exist_ok=True)

        joblib.dump(self.model, save_path / 'model.joblib')
        joblib.dump(self.scaler, save_path / 'scaler.joblib')
        if hasattr(self.label_encoder, 'classes_'):
            joblib.dump(self.label_encoder, save_path / 'label_encoder.joblib')

        metadata = {
            'feature_names': self.feature_names,
            'config': self.config
        }
        with open(save_path / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)

    @classmethod
    def load(cls, path: str) -> 'ModelTrainer':
        """Load model and preprocessors."""
        load_path = Path(path)

        model = joblib.load(load_path / 'model.joblib')
        trainer = cls(model)
        trainer.scaler = joblib.load(load_path / 'scaler.joblib')

        le_path = load_path / 'label_encoder.joblib'
        if le_path.exists():
            trainer.label_encoder = joblib.load(le_path)

        with open(load_path / 'metadata.json') as f:
            metadata = json.load(f)
            trainer.feature_names = metadata.get('feature_names')
            trainer.config = metadata.get('config', {})

        return trainer

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions on new data."""
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)

        if hasattr(self.label_encoder, 'classes_'):
            predictions = self.label_encoder.inverse_transform(predictions)

        return predictions


def main():
    """Example usage."""
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier

    # Load sample data
    data = load_iris()
    X, y = data.data, data.target

    # Initialize trainer
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    trainer = ModelTrainer(model)

    # Prepare and train
    X_train, X_test, y_train, y_test = trainer.prepare_data(X, y)
    trainer.train(X_train, y_train)

    # Evaluate
    metrics = trainer.evaluate(X_test, y_test)
    print("Evaluation Metrics:")
    print(json.dumps({k: v for k, v in metrics.items()
                     if k != 'classification_report'}, indent=2))

    # Cross-validation
    cv_results = trainer.cross_validate(X, y)
    print(f"\nCross-validation: {cv_results['cv_mean']:.3f} (+/- {cv_results['cv_std']:.3f})")

    # Feature importance
    importance = trainer.get_feature_importance()
    print("\nFeature Importance:")
    for feat, imp in sorted(importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {feat}: {imp:.4f}")


if __name__ == "__main__":
    main()
