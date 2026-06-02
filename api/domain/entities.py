"""
domain/entities.py — Entidades de Dominio

Define las estructuras de datos puras del negocio.
No debe tener dependencias externas (solo dataclasses, typing, etc.).
"""

from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class PlayerPredictionInput:
    """Atributos necesarios para predecir sobre un jugador."""
    age: int
    height_cm: int
    weight_kg: int
    pace: int
    shooting: int
    passing: int
    dribbling: int
    defending: int
    physic: int
    skill_moves: int
    weak_foot: int
    international_reputation: int
    preferred_foot: int
    work_rate: int
    body_type: int


@dataclass
class PredictionResult:
    """Resultado de la predicción de valor y categoría élite."""
    elite_logistic: int
    elite_logistic_proba: float
    elite_rf: int
    elite_rf_proba: float
    value_eur_pred: float
    model_metrics: Dict[str, Any]
