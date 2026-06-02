/**
 * presentation/hooks/usePrediction.ts — Hook para predicción ML
 *
 * Custom hook que encapsula la lógica de envío de predicciones.
 * Maneja estados: loading, error, result.
 */

import { useState } from 'react';
import { PredictionInput, PredictionResult } from '../../domain/entities';
import { ApiPredictionRepository } from '../../data/api_repository';

const repository = new ApiPredictionRepository();

type PredictionState = {
  result: PredictionResult | null;
  loading: boolean;
  error: string | null;
  predict: (input: PredictionInput) => Promise<void>;
  reset: () => void;
};

export function usePrediction(): PredictionState {
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const predict = async (input: PredictionInput) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await repository.predictPlayer(input);
      setResult(data);
    } catch (e: any) {
      setError(e.message || 'Error al predecir');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
  };

  return { result, loading, error, predict, reset };
}
