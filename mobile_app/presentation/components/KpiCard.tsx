/**
 * presentation/components/KpiCard.tsx — Componente de tarjeta KPI
 *
 * Componente visual reutilizable para mostrar una métrica.
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

type Props = {
  label: string;
  value: string;
  accent: string;
};

export function KpiCard({ label, value, accent }: Props) {
  return (
    <View style={[styles.card, { borderLeftColor: accent }]}>
      <Text style={styles.value}>{value}</Text>
      <Text style={styles.label}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#133d29',
    borderRadius: 10,
    padding: 14,
    width: '47%',
    borderLeftWidth: 3,
  },
  value: {
    color: '#e9f5e9',
    fontSize: 20,
    fontWeight: '800',
  },
  label: {
    color: '#b7d6c2',
    fontSize: 11,
    marginTop: 4,
  },
});
