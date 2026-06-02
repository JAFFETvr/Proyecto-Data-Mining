/**
 * presentation/components/ResultCard.tsx
 *
 * Componente puro (UI) para mostrar el resultado de la predicción.
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { PredictionResult } from '../../domain/entities';

export function ResultCard({ result }: { result: PredictionResult }) {
  // Formatear a millones si es muy grande
  const val = result.value_eur_pred;
  const formattedVal = val >= 1e6 
    ? `€${(val / 1e6).toFixed(2)}M` 
    : `€${val.toLocaleString()}`;

  const rf_prob = (result.elite_rf_proba * 100).toFixed(1);
  const isElite = result.elite_rf === 1;

  return (
    <View style={styles.card}>
      <Text style={styles.title}>🏆 Resultado de Predicción</Text>
      
      <View style={styles.row}>
        <View style={styles.col}>
          <Text style={styles.label}>Valor Estimado</Text>
          <Text style={styles.value}>{formattedVal}</Text>
        </View>
        <View style={styles.col}>
          <Text style={styles.label}>Clasificación</Text>
          <Text style={[styles.eliteText, { color: isElite ? '#4caf50' : '#ff9800' }]}>
            {isElite ? '⭐ Élite' : 'Promedio'}
          </Text>
        </View>
      </View>

      <View style={styles.probBox}>
        <Text style={styles.probText}>
          Probabilidad de ser Élite (Random Forest): {rf_prob}%
        </Text>
      </View>

      <Text style={styles.metricsTitle}>Métricas de Modelos en Test</Text>
      <View style={styles.metricsGrid}>
        <View style={styles.metricItem}>
          <Text style={styles.mLabel}>LR RMSE:</Text>
          <Text style={styles.mValue}>€{(result.model_metrics.linear_regression.rmse / 1e6).toFixed(2)}M</Text>
        </View>
        <View style={styles.metricItem}>
          <Text style={styles.mLabel}>RF Acc:</Text>
          <Text style={styles.mValue}>{(result.model_metrics.random_forest.accuracy * 100).toFixed(1)}%</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#0f3323',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: '#fdd835',
    marginTop: 8,
  },
  title: {
    color: '#fdd835',
    fontSize: 18,
    fontWeight: '800',
    marginBottom: 16,
    textAlign: 'center',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  col: {
    alignItems: 'center',
    flex: 1,
  },
  label: {
    color: '#b7d6c2',
    fontSize: 12,
    marginBottom: 4,
    fontWeight: '600',
  },
  value: {
    color: '#e9f5e9',
    fontSize: 24,
    fontWeight: '900',
  },
  eliteText: {
    fontSize: 22,
    fontWeight: '900',
  },
  probBox: {
    backgroundColor: '#1b5e20',
    padding: 10,
    borderRadius: 8,
    marginBottom: 16,
    alignItems: 'center',
  },
  probText: {
    color: '#e9f5e9',
    fontSize: 13,
    fontWeight: '600',
  },
  metricsTitle: {
    color: '#b7d6c2',
    fontSize: 12,
    fontWeight: '700',
    marginBottom: 8,
    textAlign: 'center',
  },
  metricsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    borderTopWidth: 1,
    borderTopColor: '#1b5e20',
    paddingTop: 12,
  },
  metricItem: {
    alignItems: 'center',
  },
  mLabel: {
    color: '#81c784',
    fontSize: 10,
    marginBottom: 2,
  },
  mValue: {
    color: '#e9f5e9',
    fontSize: 12,
    fontWeight: '700',
  },
});
