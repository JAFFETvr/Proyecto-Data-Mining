/**
 * app/index.tsx — Dashboard (EA Sports FC Analytics)
 *
 * Pantalla principal. Muestra los KPIs y las tablas OLAP.
 * Usa Clean Architecture consumiendo el hook useKpis().
 */

import React from 'react';
import { View, Text, ScrollView, StyleSheet, ActivityIndicator, TouchableOpacity } from 'react-native';
import { useKpis } from '../presentation/hooks/useKpis';

export default function Dashboard() {
  const { kpis, leagues, nationalities, positions, loading, error, refetch } = useKpis();

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#fdd835" />
        <Text style={{ color: '#e9f5e9', marginTop: 12 }}>Cargando Data Warehouse...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.center}>
        <Text style={{ color: '#ef5350', fontSize: 16 }}>❌ {error}</Text>
        <TouchableOpacity onPress={refetch} style={styles.retryBtn}>
          <Text style={{ color: '#0b2f1e', fontWeight: 'bold' }}>Reintentar</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const mainKpi = kpis[0];

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.header}>⚽ EA FC Analytics</Text>
      
      {mainKpi && (
        <View style={styles.kpiGrid}>
          <KpiCard title="Total Jugadores" value={mainKpi.total_jugadores.toLocaleString()} />
          <KpiCard title="OVR Promedio" value={mainKpi.avg_overall.toFixed(1)} />
          <KpiCard title="Valor Promedio" value={`€${(mainKpi.avg_value_eur / 1e6).toFixed(2)}M`} />
          <KpiCard title="Salario Prom." value={`€${(mainKpi.avg_wage_eur / 1000).toFixed(1)}K`} />
        </View>
      )}

      {/* Ligas Top */}
      <Text style={styles.sectionTitle}>🏆 Top Ligas por Valor</Text>
      <View style={styles.table}>
        <View style={styles.tableHeader}>
          <Text style={[styles.cellH, { flex: 2 }]}>Liga</Text>
          <Text style={styles.cellH}>OVR</Text>
          <Text style={styles.cellH}>Valor Prom.</Text>
        </View>
        {leagues.slice(0, 5).map((l, i) => (
          <View key={i} style={styles.tableRow}>
            <Text style={[styles.cell, { flex: 2 }]} numberOfLines={1}>{l.league_name}</Text>
            <Text style={styles.cell}>{l.avg_overall.toFixed(1)}</Text>
            <Text style={styles.cell}>€{(l.avg_value / 1e6).toFixed(1)}M</Text>
          </View>
        ))}
      </View>

      {/* Posiciones */}
      <Text style={styles.sectionTitle}>👕 Posiciones Mejor Pagadas</Text>
      <View style={styles.table}>
        <View style={styles.tableHeader}>
          <Text style={[styles.cellH, { flex: 2 }]}>Posición</Text>
          <Text style={styles.cellH}>Jugadores</Text>
          <Text style={styles.cellH}>Salario</Text>
        </View>
        {positions.slice(0, 5).map((p, i) => (
          <View key={i} style={styles.tableRow}>
            <Text style={[styles.cell, { flex: 2 }]}>{p.club_position}</Text>
            <Text style={styles.cell}>{p.total_jugadores}</Text>
            <Text style={styles.cell}>€{(p.avg_wage / 1000).toFixed(1)}K</Text>
          </View>
        ))}
      </View>
      
      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

// ── Componentes de UI ──────────────────────────────────────────────────────

function KpiCard({ title, value }: { title: string; value: string | number }) {
  return (
    <View style={styles.kpiCard}>
      <Text style={styles.kpiTitle}>{title}</Text>
      <Text style={styles.kpiValue}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0b2f1e', padding: 16 },
  center: { flex: 1, backgroundColor: '#0b2f1e', justifyContent: 'center', alignItems: 'center' },
  header: { color: '#e9f5e9', fontSize: 24, fontWeight: '900', marginBottom: 20 },
  retryBtn: { marginTop: 16, backgroundColor: '#fdd835', padding: 12, borderRadius: 8 },
  
  kpiGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between' },
  kpiCard: {
    backgroundColor: '#0f3323',
    width: '48%',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#1b5e20',
  },
  kpiTitle: { color: '#b7d6c2', fontSize: 12, marginBottom: 8, fontWeight: '600' },
  kpiValue: { color: '#fdd835', fontSize: 20, fontWeight: '800' },

  sectionTitle: { color: '#e9f5e9', fontSize: 18, fontWeight: '700', marginTop: 16, marginBottom: 12 },
  
  table: { backgroundColor: '#0f3323', borderRadius: 12, overflow: 'hidden', borderWidth: 1, borderColor: '#1b5e20' },
  tableHeader: { flexDirection: 'row', backgroundColor: '#1b5e20', padding: 12 },
  tableRow: { flexDirection: 'row', padding: 12, borderBottomWidth: 1, borderBottomColor: '#1b5e20' },
  cellH: { flex: 1, color: '#fdd835', fontSize: 12, fontWeight: '700' },
  cell: { flex: 1, color: '#e9f5e9', fontSize: 12 },
});
