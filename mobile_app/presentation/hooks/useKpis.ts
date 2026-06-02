/**
 * presentation/hooks/useKpis.ts
 *
 * Hook de React para inyectar y usar el repositorio de OLAP.
 */

import { useState, useEffect } from 'react';
import { ApiOlapRepository } from '../../data/api_repository';
import {
  PlayerKPI,
  LeagueStats,
  NationalityStats,
  PositionStats,
} from '../../domain/entities';

// Inyección de dependencias simple
const repository = new ApiOlapRepository();

export function useKpis() {
  const [kpis, setKpis] = useState<PlayerKPI[]>([]);
  const [leagues, setLeagues] = useState<LeagueStats[]>([]);
  const [nationalities, setNationalities] = useState<NationalityStats[]>([]);
  const [positions, setPositions] = useState<PositionStats[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [k, l, n, p] = await Promise.all([
        repository.getKpis(),
        repository.getByLeague(),
        repository.getByNationality(),
        repository.getByPosition(),
      ]);

      setKpis(k);
      setLeagues(l);
      setNationalities(n);
      setPositions(p);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return {
    kpis,
    leagues,
    nationalities,
    positions,
    loading,
    error,
    refetch: fetchData,
  };
}
