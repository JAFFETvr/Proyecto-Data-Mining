"""
domain/ports.py — Puertos (Interfaces Abstractas)

Define los contratos que los adaptadores deben implementar.
El dominio depende de estas abstracciones, NO de implementaciones concretas.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List


# ═══════════════════════════════════════════════════════════════════════════
# PUERTOS DE SALIDA (el dominio los NECESITA — implementados por adaptadores)
# ═══════════════════════════════════════════════════════════════════════════

class DataWarehousePort(ABC):
    """Puerto de acceso al Data Warehouse (DuckDB)."""

    @abstractmethod
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """Ejecuta una consulta SQL y retorna una lista de diccionarios."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Cierra la conexión al warehouse."""
        ...


class MLModelPort(ABC):
    """Puerto de acceso a los modelos de Machine Learning."""

    @abstractmethod
    def predict_value(self, features: List[Any]) -> float:
        """Predice el valor de mercado (regresión lineal)."""
        ...

    @abstractmethod
    def predict_elite_logistic(self, features: List[Any]) -> tuple[int, float]:
        """Predice si es élite con regresión logística. Retorna (clase, probabilidad)."""
        ...

    @abstractmethod
    def predict_elite_rf(self, features: List[Any]) -> tuple[int, float]:
        """Predice si es élite con random forest. Retorna (clase, probabilidad)."""
        ...

    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """Retorna las métricas de evaluación de los modelos."""
        ...

    @abstractmethod
    def get_feature_cols(self) -> List[str]:
        """Retorna la lista de columnas de features esperadas."""
        ...


# ═══════════════════════════════════════════════════════════════════════════
# PUERTOS DE ENTRADA (el mundo exterior los USA — implementados por la app)
# ═══════════════════════════════════════════════════════════════════════════

class OlapQueryPort(ABC):
    """Puerto para consultas OLAP."""

    @abstractmethod
    def get_kpis(self) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def get_por_liga(self) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def get_por_nacionalidad(self) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def get_por_posicion(self) -> List[Dict[str, Any]]:
        ...


class PredictionPort(ABC):
    """Puerto para predicciones ML."""

    @abstractmethod
    def predict(self, features: List[float]) -> Dict[str, Any]:
        ...
