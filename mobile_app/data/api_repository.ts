/**
 * data/api_repository.ts — Adaptadores de Infraestructura
 *
 * Implementación de los puertos definidos en el dominio.
 * Utiliza fetch para comunicarse con la API de FastAPI.
 */

import {
  IOlapRepository,
  IPredictionRepository,
} from '../domain/repositories';
import {
  PlayerKPI,
  LeagueStats,
  NationalityStats,
  PositionStats,
  PredictionInput,
  PredictionResult,
  ApiResponse,
} from '../domain/entities';

// Cambia esto a la IP de tu máquina si pruebas en un dispositivo físico
const API_BASE_URL = 'http://127.0.0.1:8000';

export class ApiOlapRepository implements IOlapRepository {
  private async fetch<T>(endpoint: string): Promise<T[]> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!response.ok) {
      throw new Error(`Error en API: ${response.status} ${response.statusText}`);
    }
    const json: ApiResponse<T> = await response.json();
    return json.data;
  }

  async getKpis(): Promise<PlayerKPI[]> {
    return this.fetch<PlayerKPI>('/olap/kpis');
  }

  async getByLeague(): Promise<LeagueStats[]> {
    return this.fetch<LeagueStats>('/olap/liga');
  }

  async getByNationality(): Promise<NationalityStats[]> {
    return this.fetch<NationalityStats>('/olap/nacionalidad');
  }

  async getByPosition(): Promise<PositionStats[]> {
    return this.fetch<PositionStats>('/olap/posicion');
  }
}

export class ApiPredictionRepository implements IPredictionRepository {
  async predictPlayer(input: PredictionInput): Promise<PredictionResult> {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(input),
    });

    if (!response.ok) {
      throw new Error(`Error en API: ${response.status} ${response.statusText}`);
    }

    const data: PredictionResult = await response.json();
    return data;
  }
}
