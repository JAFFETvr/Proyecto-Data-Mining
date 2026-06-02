#!/usr/bin/env python3
"""
generar_pipeline.py
Pipeline completo: EDA → DuckDB Warehouse → Modelos ML
Dataset: EA Sports FC Players (male_players.csv)
"""

import os, warnings
import numpy as np
import pandas as pd
import duckdb
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    mean_squared_error, r2_score,
    accuracy_score, classification_report, roc_auc_score,
)

warnings.filterwarnings("ignore")

# ── Rutas ──────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
DB_PATH    = os.path.join(BASE_DIR, "warehouse.duckdb")
CSV_PATH   = os.path.join(DATA_DIR, "male_players.csv")

os.makedirs(DATA_DIR,   exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════
# 1. CARGA
# ═══════════════════════════════════════════════════════════════════════════
print("\n[1/5] Cargando dataset...")
df = pd.read_csv(CSV_PATH, low_memory=False)
print(f"    Shape original: {df.shape}")

# ═══════════════════════════════════════════════════════════════════════════
# 2. EDA — Limpieza, Outliers, Imputación
# ═══════════════════════════════════════════════════════════════════════════
print("\n[2/5] EDA: limpieza y preparación...")

# Filtrar jugadores sin valor o salario
df = df.dropna(subset=['value_eur', 'wage_eur', 'overall']).copy()

# Rellenar stats físicos si faltan (porteros no tienen pace, shooting, etc.)
stats_cols = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
for c in stats_cols:
    df[c] = df[c].fillna(df[c].median())

# Target binario para clasificación: Elite si overall >= 80
df['elite'] = (df['overall'] >= 80).astype(int)

# ═══════════════════════════════════════════════════════════════════════════
# 3. DATA WAREHOUSE — DuckDB (Esquema Estrella)
# ═══════════════════════════════════════════════════════════════════════════
print("\n[3/5] Construyendo Data Warehouse en DuckDB...")

con = duckdb.connect(DB_PATH)

# Asegurar limpieza de NaN en columnas texto para DuckDB
df['club_name'] = df['club_name'].fillna('Unknown')
df['league_name'] = df['league_name'].fillna('Unknown')
df['club_position'] = df['club_position'].fillna('RES')
df['nationality_name'] = df['nationality_name'].fillna('Unknown')

# Dimension Jugador
con.execute("""
    CREATE OR REPLACE TABLE dim_jugador AS
    SELECT DISTINCT
        player_id,
        short_name,
        age,
        nationality_name,
        club_name,
        league_name,
        club_position
    FROM df
""")

# Tabla de Hechos
con.execute("""
    CREATE OR REPLACE TABLE fact_stats AS
    SELECT
        player_id,
        overall,
        potential,
        value_eur,
        wage_eur,
        pace,
        shooting,
        passing,
        dribbling,
        defending,
        physic,
        elite
    FROM df
""")

# Vista OLAP — KPIs globales
con.execute("""
    CREATE OR REPLACE VIEW olap_kpis AS
    SELECT
        COUNT(*) AS total_jugadores,
        ROUND(AVG(overall), 2) AS avg_overall,
        ROUND(AVG(potential), 2) AS avg_potential,
        ROUND(AVG(value_eur), 2) AS avg_value_eur,
        ROUND(AVG(wage_eur), 2) AS avg_wage_eur,
        SUM(value_eur) AS total_value_eur
    FROM fact_stats
""")

# Vista OLAP — Por Liga
con.execute("""
    CREATE OR REPLACE VIEW olap_por_liga AS
    SELECT
        d.league_name,
        COUNT(*) AS total_jugadores,
        ROUND(AVG(f.overall), 2) AS avg_overall,
        ROUND(AVG(f.value_eur), 2) AS avg_value,
        MAX(f.value_eur) AS top_value
    FROM fact_stats f
    JOIN dim_jugador d USING (player_id)
    GROUP BY d.league_name
    ORDER BY avg_value DESC
""")

# Vista OLAP — Por Nacionalidad
con.execute("""
    CREATE OR REPLACE VIEW olap_por_nacionalidad AS
    SELECT
        d.nationality_name,
        COUNT(*) AS total_jugadores,
        ROUND(AVG(f.overall), 2) AS avg_overall,
        ROUND(AVG(f.potential), 2) AS avg_potential,
        SUM(f.value_eur) AS total_value
    FROM fact_stats f
    JOIN dim_jugador d USING (player_id)
    GROUP BY d.nationality_name
    ORDER BY total_value DESC
""")

# Vista OLAP — Por Posición
con.execute("""
    CREATE OR REPLACE VIEW olap_por_posicion AS
    SELECT
        d.club_position,
        COUNT(*) AS total_jugadores,
        ROUND(AVG(f.overall), 2) AS avg_overall,
        ROUND(AVG(f.value_eur), 2) AS avg_value,
        ROUND(AVG(f.wage_eur), 2) AS avg_wage
    FROM fact_stats f
    JOIN dim_jugador d USING (player_id)
    GROUP BY d.club_position
    ORDER BY avg_wage DESC
""")

con.close()
print(f"    DuckDB warehouse → {DB_PATH}")

# ═══════════════════════════════════════════════════════════════════════════
# 4. MACHINE LEARNING (PREVENCIÓN DE DATA LEAKAGE)
# ═══════════════════════════════════════════════════════════════════════════
print("\n[4/5] Entrenando modelos ML...")

FEATURE_COLS = [
    'age', 'height_cm', 'weight_kg', 'pace', 'shooting', 
    'passing', 'dribbling', 'defending', 'physic', 
    'skill_moves', 'weak_foot', 'international_reputation', 
    'preferred_foot', 'work_rate', 'body_type'
]

# Imputar Nans en features categóricas/numéricas antes del split (o dropearlas)
df = df.dropna(subset=FEATURE_COLS).copy()

# Codificar categorías (preferred_foot, work_rate, body_type) para que sean numéricas
# Hacemos el encoding básico de las variables string
df['preferred_foot'] = LabelEncoder().fit_transform(df['preferred_foot'].astype(str))
df['work_rate'] = LabelEncoder().fit_transform(df['work_rate'].astype(str))
df['body_type'] = LabelEncoder().fit_transform(df['body_type'].astype(str))

X = df[FEATURE_COLS].copy()
y_value = df['value_eur'].copy()
y_elite = df['elite'].copy()

# 1. Train-Test Split (Sin Data Leakage)
X_train, X_test, yv_train, yv_test, ye_train, ye_test = train_test_split(
    X, y_value, y_elite, test_size=0.2, random_state=42, stratify=y_elite
)

X_train = X_train.copy()
X_test = X_test.copy()

# 2. Scaling (Fit SOLO en Train)
print("    Escalando variables numéricas...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.joblib"))

# Generamos un dummy encoder dict para no romper código que espere encoders.joblib (aunque no lo usemos en predict)
joblib.dump({}, os.path.join(MODELS_DIR, "encoders.joblib"))

# ── 4a. Regresión Lineal (Predecir Valor de Mercado) ─────────────────────
lr = LinearRegression()
lr.fit(X_train_scaled, yv_train)
yv_pred = lr.predict(X_test_scaled)
rmse = np.sqrt(mean_squared_error(yv_test, yv_pred))
r2 = r2_score(yv_test, yv_pred)
print(f"    [LinearRegression] RMSE={rmse:,.2f}  R²={r2:.4f}")
joblib.dump(lr, os.path.join(MODELS_DIR, "linear_regression.joblib"))

# ── 4b. Regresión Logística (Predecir Elite) ─────────────────────────────
log_clf = LogisticRegression(max_iter=1000, random_state=42)
log_clf.fit(X_train_scaled, ye_train)
ye_pred_log = log_clf.predict(X_test_scaled)
acc_log = accuracy_score(ye_test, ye_pred_log)
auc_log = roc_auc_score(ye_test, log_clf.predict_proba(X_test_scaled)[:, 1])
print(f"    [LogisticRegression] Accuracy={acc_log:.4f}  AUC={auc_log:.4f}")
joblib.dump(log_clf, os.path.join(MODELS_DIR, "logistic_regression.joblib"))

# ── 4c. Random Forest (Predecir Elite) ───────────────────────────────────
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_clf.fit(X_train_scaled, ye_train)
ye_pred_rf = rf_clf.predict(X_test_scaled)
acc_rf = accuracy_score(ye_test, ye_pred_rf)
auc_rf = roc_auc_score(ye_test, rf_clf.predict_proba(X_test_scaled)[:, 1])
print(f"    [RandomForest]       Accuracy={acc_rf:.4f}  AUC={auc_rf:.4f}")
joblib.dump(rf_clf, os.path.join(MODELS_DIR, "random_forest.joblib"))

# Metadata
meta = {
    "feature_cols": FEATURE_COLS,
    "metrics": {
        "linear_regression": {"rmse": float(rmse), "r2": float(r2)},
        "logistic_regression": {"accuracy": float(acc_log), "auc": float(auc_log)},
        "random_forest": {"accuracy": float(acc_rf), "auc": float(auc_rf)},
    }
}
with open(os.path.join(MODELS_DIR, "model_meta.json"), "w") as f:
    json.dump(meta, f, indent=2)

print(f"    Modelos guardados en {MODELS_DIR}/")

# ═══════════════════════════════════════════════════════════════════════════
# 5. REPORTE FINAL
# ═══════════════════════════════════════════════════════════════════════════
print("\n[5/5] ✅ Pipeline completado exitosamente.")
print("─" * 60)
print(f"  DuckDB         : {DB_PATH}")
print(f"  Modelos        : {MODELS_DIR}/")
print("─" * 60)
print("  Próximo paso: cd ../api && uvicorn main:app --reload")
