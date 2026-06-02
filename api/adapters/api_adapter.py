"""
adapters/api_adapter.py — Adaptador FastAPI (HTTP)

Contiene los routers de FastAPI.
Traduce: Requests HTTP → Servicios de Aplicación → Respuestas HTTP

Este adaptador es la "cara" HTTP del sistema.
No contiene lógica de negocio.
"""

from __future__ import annotations
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from application.services import OlapService, PredictionService


# ── Schemas de Request / Response (Pydantic) ────────────────────────────────

class PredictRequest(BaseModel):
    """Schema de entrada para predicción de valor y élite."""
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


class PredictResponse(BaseModel):
    """Schema de respuesta para predicción."""
    elite_logistic: int
    elite_logistic_proba: float
    elite_rf: int
    elite_rf_proba: float
    value_eur_pred: float
    model_metrics: Dict[str, Any]


# ── Factory de Routers ──────────────────────────────────────────────────────

def create_health_router(db_path: str) -> APIRouter:
    """Crea el router de health check."""
    router = APIRouter()

    @router.get("/health")
    def health():
        return {"status": "ok", "models_loaded": True, "db": db_path}

    return router


def create_olap_router(olap_service: OlapService) -> APIRouter:
    """Crea el router de endpoints OLAP."""
    router = APIRouter(prefix="/olap", tags=["OLAP"])

    @router.get("/kpis")
    def get_kpis():
        try:
            rows = olap_service.get_kpis()
            return {"view": "olap_kpis", "data": rows}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/liga")
    def get_liga():
        try:
            rows = olap_service.get_por_liga()
            return {"view": "olap_por_liga", "data": rows}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/nacionalidad")
    def get_nacionalidad():
        try:
            rows = olap_service.get_por_nacionalidad()
            return {"view": "olap_por_nacionalidad", "data": rows}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/posicion")
    def get_posicion():
        try:
            rows = olap_service.get_por_posicion()
            return {"view": "olap_por_posicion", "data": rows}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router


def create_predict_router(prediction_service: PredictionService) -> APIRouter:
    """Crea el router de predicción ML."""
    router = APIRouter(tags=["Predicción"])

    @router.post("/predict", response_model=PredictResponse)
    def predict(req: PredictRequest):
        try:
            features = [
                req.age,
                req.height_cm,
                req.weight_kg,
                req.pace,
                req.shooting,
                req.passing,
                req.dribbling,
                req.defending,
                req.physic,
                req.skill_moves,
                req.weak_foot,
                req.international_reputation,
                req.preferred_foot,
                req.work_rate,
                req.body_type,
            ]
            result = prediction_service.predict(features)
            # return as dict so Pydantic parses it
            return PredictResponse(
                elite_logistic=result.elite_logistic,
                elite_logistic_proba=result.elite_logistic_proba,
                elite_rf=result.elite_rf,
                elite_rf_proba=result.elite_rf_proba,
                value_eur_pred=result.value_eur_pred,
                model_metrics=result.model_metrics
            )
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

    return router
