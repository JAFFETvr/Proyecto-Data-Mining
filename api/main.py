"""
main.py — Composition Root / Entrypoint de la API

Inicia la aplicación FastAPI e inyecta las dependencias.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Puertos y adaptadores
from domain.ports import DataWarehousePort, MLModelPort
from adapters.duckdb_adapter import DuckDBAdapter
from adapters.ml_adapter import ScikitLearnAdapter
from adapters.api_adapter import create_health_router, create_olap_router, create_predict_router

# Servicios de aplicación
from application.services import OlapService, PredictionService


app = FastAPI(
    title="EA FC Players Analytics API",
    description="API para predicción de mercado y análisis OLAP de jugadores (Clean Architecture)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Dependency Injection (Composition Root) ─────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "pipeline", "warehouse.duckdb")
MODELS_DIR = os.path.join(BASE_DIR, "..", "pipeline", "models")

# 1. Instanciar Adaptadores (Infraestructura)
warehouse_adapter: DataWarehousePort = DuckDBAdapter(DB_PATH)
ml_adapter: MLModelPort = ScikitLearnAdapter(MODELS_DIR)

# 2. Instanciar Servicios (Casos de Uso) inyectando adaptadores
olap_service = OlapService(warehouse_adapter)
prediction_service = PredictionService(ml_adapter)

# 3. Registrar Routers (Presentación HTTP) inyectando servicios
app.include_router(create_health_router(DB_PATH))
app.include_router(create_olap_router(olap_service))
app.include_router(create_predict_router(prediction_service))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
