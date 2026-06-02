/**
 * app/predict.tsx — Formulario de Predicción (EA Sports FC Players)
 *
 * Permite al usuario ingresar atributos de un jugador de fútbol
 * y obtener predicción de valor de mercado (regresión) y
 * clasificación élite (overall >= 80).
 *
 * Sigue Clean Architecture: consume hooks y componentes de presentación.
 */

import React, { useState } from 'react';
import {
  View, Text, ScrollView, StyleSheet,
  TouchableOpacity, ActivityIndicator,
} from 'react-native';

import { PredictionInput } from '../domain/entities';
import { usePrediction } from '../presentation/hooks/usePrediction';
import { ResultCard } from '../presentation/components/ResultCard';

// ── Form State ──
type FormState = {
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
  preferred_foot: number;
  work_rate: number;
  body_type: number;
};

const DEFAULT_FORM: FormState = {
  age: 25,
  height_cm: 180,
  weight_kg: 75,
  pace: 70,
  shooting: 65,
  passing: 65,
  dribbling: 68,
  defending: 55,
  physic: 65,
  skill_moves: 3,
  weak_foot: 3,
  international_reputation: 2,
  preferred_foot: 1,   // Right
  work_rate: 0,
  body_type: 0,
};

export default function Predict() {
  const [form, setForm] = useState<FormState>(DEFAULT_FORM);
  const { result, loading, error, predict } = usePrediction();

  const set = (key: keyof FormState, val: number) =>
    setForm(prev => ({ ...prev, [key]: val }));

  const handlePredict = () => {
    const input: PredictionInput = { ...form };
    predict(input);
  };

  return (
    <ScrollView style={styles.container} keyboardShouldPersistTaps="handled">
      <Text style={styles.header}>🔮 Predicción de Jugador</Text>
      <Text style={styles.subHeader}>
        Ingresa los atributos del jugador para predecir su valor de mercado y si es élite
      </Text>

      {/* ── Datos Físicos ── */}
      <Text style={styles.sectionLabel}>📏 Datos Físicos</Text>
      <Field label={`Edad: ${form.age} años`}>
        <ChipRow
          values={[18, 20, 23, 25, 28, 30, 33, 36]}
          selected={form.age}
          onChange={v => set('age', v)}
        />
      </Field>
      <Field label={`Altura: ${form.height_cm} cm`}>
        <ChipRow
          values={[165, 170, 175, 180, 185, 190, 195]}
          selected={form.height_cm}
          onChange={v => set('height_cm', v)}
        />
      </Field>
      <Field label={`Peso: ${form.weight_kg} kg`}>
        <ChipRow
          values={[60, 65, 70, 75, 80, 85, 90]}
          selected={form.weight_kg}
          onChange={v => set('weight_kg', v)}
        />
      </Field>

      {/* ── Pie Preferido ── */}
      <Field label="Pie Preferido">
        <SegmentedControl
          options={['Izquierdo', 'Derecho']}
          value={form.preferred_foot}
          onChange={v => set('preferred_foot', v)}
        />
      </Field>

      {/* ── Atributos de Rendimiento ── */}
      <Text style={styles.sectionLabel}>⚡ Atributos de Rendimiento</Text>
      {[
        { key: 'pace' as const, label: '🏃 Velocidad (PAC)' },
        { key: 'shooting' as const, label: '🎯 Tiro (SHO)' },
        { key: 'passing' as const, label: '📬 Pase (PAS)' },
        { key: 'dribbling' as const, label: '⚽ Regate (DRI)' },
        { key: 'defending' as const, label: '🛡 Defensa (DEF)' },
        { key: 'physic' as const, label: '💪 Físico (PHY)' },
      ].map(attr => (
        <Field key={attr.key} label={`${attr.label}: ${form[attr.key]}`}>
          <ChipRow
            values={[30, 45, 55, 65, 75, 85, 95]}
            selected={form[attr.key]}
            onChange={v => set(attr.key, v)}
          />
        </Field>
      ))}

      {/* ── Skills ── */}
      <Text style={styles.sectionLabel}>🌟 Habilidades</Text>
      <Field label={`Skill Moves: ${form.skill_moves}⭐`}>
        <SegmentedControl
          options={['1⭐', '2⭐', '3⭐', '4⭐', '5⭐']}
          value={form.skill_moves - 1}
          onChange={v => set('skill_moves', v + 1)}
        />
      </Field>
      <Field label={`Pie Débil: ${form.weak_foot}⭐`}>
        <SegmentedControl
          options={['1⭐', '2⭐', '3⭐', '4⭐', '5⭐']}
          value={form.weak_foot - 1}
          onChange={v => set('weak_foot', v + 1)}
        />
      </Field>
      <Field label={`Reputación Int.: ${form.international_reputation}⭐`}>
        <SegmentedControl
          options={['1⭐', '2⭐', '3⭐', '4⭐', '5⭐']}
          value={form.international_reputation - 1}
          onChange={v => set('international_reputation', v + 1)}
        />
      </Field>

      {/* ── Botón Predecir ── */}
      <TouchableOpacity style={styles.predictBtn} onPress={handlePredict} disabled={loading}>
        {loading
          ? <ActivityIndicator color="#0b2f1e" />
          : <Text style={styles.predictBtnText}>⚡ Predecir Jugador</Text>
        }
      </TouchableOpacity>

      {/* ── Error ── */}
      {error && (
        <View style={styles.errorBox}>
          <Text style={styles.errorText}>❌ {error}</Text>
        </View>
      )}

      {/* ── Resultados ── */}
      {result && <ResultCard result={result} />}

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

// ── Sub-componentes ──

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <View style={fieldStyles.container}>
      <Text style={fieldStyles.label}>{label}</Text>
      {children}
    </View>
  );
}
const fieldStyles = StyleSheet.create({
  container: { marginBottom: 16 },
  label: { color: '#b7d6c2', fontSize: 12, marginBottom: 6, fontWeight: '600' },
});

function SegmentedControl(
  { options, value, onChange }: { options: string[]; value: number; onChange: (v: number) => void }
) {
  return (
    <View style={segStyles.container}>
      {options.map((opt, i) => (
        <TouchableOpacity
          key={i}
          style={[segStyles.btn, value === i && segStyles.btnActive]}
          onPress={() => onChange(i)}
        >
          <Text style={[segStyles.text, value === i && segStyles.textActive]}>
            {opt}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}
const segStyles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: '#0f3323',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#1b5e20',
    overflow: 'hidden',
  },
  btn: { flex: 1, paddingVertical: 8, alignItems: 'center' },
  btnActive: { backgroundColor: '#fdd835' },
  text: { color: '#b7d6c2', fontSize: 12 },
  textActive: { color: '#0b2f1e', fontWeight: '700' },
});

function ChipRow(
  { values, selected, onChange }: { values: number[]; selected: number; onChange: (v: number) => void }
) {
  return (
    <View style={chipStyles.row}>
      {values.map(v => (
        <TouchableOpacity
          key={v}
          style={[chipStyles.chip, selected === v && chipStyles.chipActive]}
          onPress={() => onChange(v)}
        >
          <Text style={[chipStyles.text, selected === v && chipStyles.textActive]}>
            {v}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}
const chipStyles = StyleSheet.create({
  row: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  chip: {
    backgroundColor: '#0f3323',
    borderRadius: 6,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderWidth: 1,
    borderColor: '#1b5e20',
  },
  chipActive: { backgroundColor: '#fdd835', borderColor: '#fdd835' },
  text: { color: '#b7d6c2', fontSize: 12 },
  textActive: { color: '#0b2f1e', fontWeight: '700' },
});

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0b2f1e', padding: 16 },
  header: { color: '#e9f5e9', fontSize: 22, fontWeight: '800', marginBottom: 4 },
  subHeader: { color: '#b7d6c2', fontSize: 13, marginBottom: 24 },
  sectionLabel: {
    color: '#fdd835',
    fontSize: 14,
    fontWeight: '700',
    marginTop: 16,
    marginBottom: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#1b5e20',
    paddingBottom: 6,
  },
  predictBtn: {
    backgroundColor: '#fdd835',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 16,
    marginBottom: 16,
  },
  predictBtnText: { color: '#0b2f1e', fontWeight: '800', fontSize: 16 },
  errorBox: {
    backgroundColor: '#3b0d0d',
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
  },
  errorText: { color: '#ef5350', fontSize: 13 },
});
