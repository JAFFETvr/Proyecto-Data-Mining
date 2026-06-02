"""
adapters/duckdb_adapter.py — Adaptador DuckDB

Implementación concreta del puerto DataWarehousePort.
Toda la lógica de conexión y queries a DuckDB está aislada aquí.
"""

from __future__ import annotations
from typing import Any, Dict, List

import duckdb

from domain.ports import DataWarehousePort


class DuckDBAdapter(DataWarehousePort):
    """Adaptador que conecta con la base de datos DuckDB."""

    def __init__(self, db_path: str):
        self._db_path = db_path

    def query(self, sql: str) -> List[Dict[str, Any]]:
        """Ejecuta una consulta SQL en DuckDB y retorna registros como dicts."""
        con = duckdb.connect(self._db_path, read_only=True)
        try:
            result = con.execute(sql).fetchdf()
            return result.to_dict(orient="records")
        finally:
            con.close()

    def close(self) -> None:
        """No-op: las conexiones se abren y cierran por query."""
        pass
