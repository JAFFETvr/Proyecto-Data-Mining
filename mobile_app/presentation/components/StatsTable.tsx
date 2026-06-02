/**
 * presentation/components/StatsTable.tsx — Tabla de estadísticas reutilizable
 *
 * Muestra datos tabulares con headers configurables.
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

type Column = {
  key: string;
  header: string;
  flex?: number;
  format?: (val: any) => string;
  colorFn?: (val: any) => string;
};

type Props = {
  title: string;
  columns: Column[];
  data: Record<string, any>[];
};

export function StatsTable({ title, columns, data }: Props) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      <View style={styles.tableWrap}>
        {/* Header */}
        <View style={styles.headerRow}>
          {columns.map((col) => (
            <Text
              key={col.key}
              style={[styles.headerCell, { flex: col.flex ?? 1 }]}
            >
              {col.header}
            </Text>
          ))}
        </View>
        {/* Rows */}
        {data.map((row, i) => (
          <View
            key={i}
            style={[styles.row, i % 2 === 0 ? styles.rowEven : styles.rowOdd]}
          >
            {columns.map((col) => {
              const raw = row[col.key];
              const display = col.format ? col.format(raw) : String(raw ?? '–');
              const color = col.colorFn ? col.colorFn(raw) : '#c9d8e8';
              return (
                <Text
                  key={col.key}
                  style={[styles.cell, { flex: col.flex ?? 1, color }]}
                >
                  {display}
                </Text>
              );
            })}
          </View>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 24,
  },
  title: {
    color: '#e9f5e9',
    fontSize: 16,
    fontWeight: '700',
    marginTop: 20,
    marginBottom: 12,
  },
  tableWrap: {
    backgroundColor: '#133d29',
    borderRadius: 10,
    overflow: 'hidden',
  },
  headerRow: {
    flexDirection: 'row',
    backgroundColor: '#1b5e20',
    padding: 10,
  },
  headerCell: {
    color: '#fdd835',
    fontWeight: '700',
    fontSize: 11,
  },
  row: {
    flexDirection: 'row',
    paddingVertical: 10,
    paddingHorizontal: 10,
  },
  rowEven: {
    backgroundColor: '#133d29',
  },
  rowOdd: {
    backgroundColor: '#0f3323',
  },
  cell: {
    fontSize: 11,
    color: '#e9f5e9',
  },
});
