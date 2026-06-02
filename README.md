# EA Sports FC Players Analytics - Pipeline Full Stack

Este repositorio contiene la entrega del **Proyecto Data Mining — Corte 1** (Curso Minería de Datos, Ingeniería de Software, 9.º semestre, UPCh, 2026A).

El proyecto implementa un pipeline de datos end-to-end, un Data Warehouse dimensional, una API RESTful con Clean Architecture (FastAPI), y un producto frontend funcional (Aplicación Móvil en React Native/Expo) que opera sobre datos de jugadores de EA Sports FC (`male_players.csv`).

## 1. Justificación del Dataset
Se eligió el dataset de **EA Sports FC (`male_players.csv`)** por ser un conjunto de datos real, robusto (más de 90 MB) e imperfecto, que requiere limpieza (imputación de nulos) y transformaciones. 
Permite responder dos preguntas complejas y de mucho interés en la gestión de clubes deportivos:
1. **Regresión:** ¿Cuál es el valor estimado de mercado (`value_eur`) de un jugador dadas sus características físicas y técnicas?
2. **Clasificación:** ¿El jugador pertenece a la "Élite" mundial (Overall $\ge$ 80) según sus estadísticas?

## 2. Arquitectura del Proyecto

El sistema está dividido en 4 capas principales:

1. **Capa de Análisis (EDA) y Preprocesamiento:** `pipeline/generar_pipeline.py`. Realiza limpieza, imputación de nulos, eliminación de registros inválidos y la separación limpia de datos (*train_test_split*) sin fuga de datos.
2. **Capa de Datos (Data Warehouse en DuckDB):** Se construye un modelo dimensional en esquema estrella con una tabla de hechos (`fact_stats`), dimensiones (`dim_jugador`) y vistas OLAP precalculadas por liga, nacionalidad y posición.
3. **Capa de Modelado:** Se entrenan algoritmos de Machine Learning (Regresión Lineal para valor; Regresión Logística y Random Forest para Élite) evaluados rigurosamente con RMSE, Accuracy y AUC-ROC.
4. **Capa de Presentación (FastAPI + React Native):** Una API con Arquitectura Hexagonal (Puertos y Adaptadores) que inyecta la conexión de DuckDB y Scikit-Learn. Es consumida por una aplicación móvil que funge como interfaz de producto final.

## 3. Instrucciones de Reproducción

Es imprescindible **ejecutar primero el pipeline** para que se genere el Data Warehouse y los artefactos `.joblib` en tu entorno local. Sin esto, la API no podrá levantar.

### Paso 1: Ejecutar el Pipeline de Machine Learning
Asegúrate de tener un entorno virtual (venv) con `pandas`, `numpy`, `scikit-learn` y `duckdb` instalados.
```bash
cd pipeline
pip install -r requirements.txt
python3 generar_pipeline.py
```
Esto creará el archivo `warehouse.duckdb` y llenará la carpeta `models/` con los codificadores y algoritmos entrenados.

### Paso 2: Iniciar la API REST
En el mismo entorno virtual:
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
La API estará viva en `http://127.0.0.1:8000`. Puedes verificar los modelos explorando `http://127.0.0.1:8000/docs`.

### Paso 3: Iniciar la Aplicación Móvil
En una nueva terminal, instala las dependencias de Node e inicia el *bundler* de Expo.
```bash
cd mobile_app
npm install
npm run start
```
Con la app levantada, presiona `w` para ver la web o escanea el QR con la app **Expo Go** en tu dispositivo físico para ver los Dashboards OLAP y el formulario de predicciones de mercado en tiempo real.

## Rigor Metodológico
- **Cero Fuga de Datos (Data Leakage):** La estandarización de las variables numéricas (`StandardScaler`) se calculó (`fit`) estrictamente sobre el conjunto de entrenamiento de forma aislada, aplicándose de manera estática al set de prueba (`transform`).
- **Clean Architecture:** Desacoplamiento total entre infraestructura (Scikit-Learn, DuckDB) y las entidades de negocio.
