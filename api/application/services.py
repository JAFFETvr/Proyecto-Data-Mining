"""
application/services.py — Servicios de Aplicación

Contiene los casos de uso principales:
1. Consultas OLAP (kpis, ligas, nacionalidades)
2. Predicción de Machine Learning

Actúan como orquestadores. Toman dependencias inyectadas (Ports) para
no acoplarse a tecnologías concretas (como DuckDB o Scikit-Learn).
"""

from typing import List, Dict, Any

from domain.ports import DataWarehousePort, MLModelPort
from domain.entities import PredictionResult

class OlapService:
    def __init__(self, dw_port: DataWarehousePort):
        self.dw = dw_port

    def get_kpis(self) -> List[Dict[str, Any]]:
        return self.dw.query("SELECT * FROM olap_kpis")

    def get_por_liga(self) -> List[Dict[str, Any]]:
        return self.dw.query("SELECT * FROM olap_por_liga")

    def get_por_nacionalidad(self) -> List[Dict[str, Any]]:
        return self.dw.query("SELECT * FROM olap_por_nacionalidad")

    def get_por_posicion(self) -> List[Dict[str, Any]]:
        return self.dw.query("SELECT * FROM olap_por_posicion")


class PredictionService:
    def __init__(self, ml_port: MLModelPort):
        self.ml_port = ml_port

    def predict(self, features: List[Any]) -> PredictionResult:
        """
        Orquesta el caso de uso de predicción combinando múltiples modelos.
        """
        if len(features) != 15:
            raise ValueError(f"Se esperaban 15 características, se recibieron {len(features)}")
            
        val_pred = self.ml_port.predict_value(features)
        log_pred, log_proba = self.ml_port.predict_elite_logistic(features)
        rf_pred, rf_proba = self.ml_port.predict_elite_rf(features)
        metrics = self.ml_port.get_metrics()
        
        # Validaciones de negocio: un jugador no puede tener un valor negativo
        if val_pred < 0:
            val_pred = 0.0
            
        return PredictionResult(
            elite_logistic=log_pred,
            elite_logistic_proba=log_proba,
            elite_rf=rf_pred,
            elite_rf_proba=rf_proba,
            value_eur_pred=val_pred,
            model_metrics=metrics
        )
