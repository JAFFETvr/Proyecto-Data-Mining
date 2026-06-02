"""
adapters/ml_adapter.py — Adaptador para Modelos Machine Learning

Implementa el MLModelPort utilizando Scikit-Learn y Joblib.
Carga los modelos entrenados por el pipeline y expone el método de predicción.
"""

import os
import json
import joblib
import numpy as np
from typing import List, Dict, Any, Tuple

from domain.ports import MLModelPort

class ScikitLearnAdapter(MLModelPort):
    def __init__(self, models_dir: str):
        self.models_dir = models_dir
        
        # Cargar artefactos de Machine Learning
        self.lr_model = joblib.load(os.path.join(models_dir, "linear_regression.joblib"))
        self.log_model = joblib.load(os.path.join(models_dir, "logistic_regression.joblib"))
        self.rf_model = joblib.load(os.path.join(models_dir, "random_forest.joblib"))
        
        self.scaler = joblib.load(os.path.join(models_dir, "scaler.joblib"))
        
        with open(os.path.join(models_dir, "model_meta.json"), "r") as f:
            self.meta = json.load(f)

    def _scale(self, features: List[Any]) -> np.ndarray:
        X_num = np.array([features]).astype(float)
        return self.scaler.transform(X_num)

    def predict_value(self, features: List[Any]) -> float:
        X_scaled = self._scale(features)
        return float(self.lr_model.predict(X_scaled)[0])

    def predict_elite_logistic(self, features: List[Any]) -> Tuple[int, float]:
        X_scaled = self._scale(features)
        log_pred = int(self.log_model.predict(X_scaled)[0])
        log_proba = float(self.log_model.predict_proba(X_scaled)[0][1])
        return log_pred, log_proba

    def predict_elite_rf(self, features: List[Any]) -> Tuple[int, float]:
        X_scaled = self._scale(features)
        rf_pred = int(self.rf_model.predict(X_scaled)[0])
        rf_proba = float(self.rf_model.predict_proba(X_scaled)[0][1])
        return rf_pred, rf_proba

    def get_metrics(self) -> Dict[str, Any]:
        return self.meta.get("metrics", {})

    def get_feature_cols(self) -> List[str]:
        return self.meta.get("feature_cols", [])
