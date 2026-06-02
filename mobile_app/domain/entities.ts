/**
 * domain/entities.ts — Entidades de Dominio
 * 
 * Contiene los tipos puros de la aplicación, sin dependencias de React
 * o de librerías de infraestructura como axios.
 */

// ── Modelos de Análisis OLAP ─────────────────────────────────────────────

export interface PlayerKPI {
  total_jugadores: number;
  avg_overall: number;
  avg_potential: number;
  avg_value_eur: number;
  avg_wage_eur: number;
  total_value_eur: number;
}

export interface LeagueStats {
  league_name: string;
  total_jugadores: number;
  avg_overall: number;
  avg_value: number;
  top_value: number;
}

export interface NationalityStats {
  nationality_name: string;
  total_jugadores: number;
  avg_overall: number;
  avg_potential: number;
  total_value: number;
}

export interface PositionStats {
  club_position: string;
  total_jugadores: number;
  avg_overall: number;
  avg_value: number;
  avg_wage: number;
}

// ── Modelos de Predicción Machine Learning ────────────────────────────────

export interface PredictionInput {
  age: number;
  height_cm: number;
  weight_kg: number;
  pace: number;
  shooting: number;
  passing: number;
  dribbling: number;
  defending: number;
  physic: number;
  skill_moves: number;
  weak_foot: number;
  international_reputation: number;
  preferred_foot: number; // 0 = Izquierdo, 1 = Derecho
  work_rate: number;      // 0 a 8
  body_type: number;      // 0 a 9
}

export interface PredictionResult {
  elite_logistic: number;
  elite_logistic_proba: number;
  elite_rf: number;
  elite_rf_proba: number;
  value_eur_pred: number;
  model_metrics: {
    linear_regression: { rmse: number; r2: number };
    logistic_regression: { accuracy: number; auc: number };
    random_forest: { accuracy: number; auc: number };
  };
}

// ── Envoltorios de Respuestas de la API ───────────────────────────────────

export interface ApiResponse<T> {
  view: string;
  data: T[];
}
