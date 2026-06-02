/**
 * domain/repositories.ts — Puertos (Interfaces) de Dominio
 *
 * Define los contratos que deben cumplir las capas de infraestructura
 * para comunicarse con fuentes de datos externas.
 */

import {
  PlayerKPI,
  LeagueStats,
  NationalityStats,
  PositionStats,
  PredictionInput,
  PredictionResult,
} from './entities';

/**
 * Puerto para obtener datos analíticos agregados (OLAP).
 */
export interface IOlapRepository {
  getKpis(): Promise<PlayerKPI[]>;
  getByLeague(): Promise<LeagueStats[]>;
  getByNationality(): Promise<NationalityStats[]>;
  getByPosition(): Promise<PositionStats[]>;
}

/**
 * Puerto para invocar modelos predictivos (ML).
 */
export interface IPredictionRepository {
  predictPlayer(input: PredictionInput): Promise<PredictionResult>;
}
