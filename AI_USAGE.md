# Uso de Inteligencia Artificial Generativa

Tal y como lo solicita la rúbrica del proyecto, este documento declara de manera transparente y honesta el uso de herramientas de Inteligencia Artificial Generativa durante el desarrollo del "Pipeline Full Stack de Minería de Datos".

## ¿Qué partes se desarrollaron con IA?

1. **Andamiaje (Boilerplate) de React Native y UI:**
   Se utilizó IA para agilizar la creación de los componentes visuales del frontend en la carpeta `mobile_app/`. La IA generó el código base de Expo, los estilos de CSS *in-js*, y los componentes reutilizables como los `SegmentedControl` y `ChipRow` que conforman el formulario interactivo para capturar las habilidades del jugador.
   
2. **Estructuración de FastAPI (Arquitectura Limpia):**
   La IA fue fundamental para organizar las interfaces (puertos) y las implementaciones (adaptadores) en la carpeta `api/`. En vez de poner todo el código de Machine Learning y Base de Datos en un solo archivo, se le solicitó a la IA generar un esqueleto de Arquitectura Hexagonal donde el servidor REST simplemente orquesta las peticiones HTTP.

## ¿Qué partes son de autoría propia y dominio profundo?

El núcleo de la asignatura, el cual comprendo a la perfección y no se delegó a ciegas, consistió en:

1. **Diseño del Data Warehouse (DuckDB):**
   La decisión de utilizar un esquema dimensional para aislar `dim_jugador` y centralizar las métricas en `fact_stats`, así como el diseño de las vistas OLAP de pre-agregación, fue una decisión consciente para que el motor de DuckDB sirviera las consultas del Dashboard en milisegundos.

2. **Manejo Estricto de Fuga de Datos (Data Leakage):**
   Se estructuró de manera rigurosa el pipeline en `generar_pipeline.py` para asegurar que el `StandardScaler` hiciera su ajuste (`fit`) única y exclusivamente sobre los datos de entrenamiento (*X_train*) ANTES de aplicarse a los datos de evaluación, preservando la validez metodológica del proyecto.

3. **Definición de las Tareas y Elección del Dataset:**
   La investigación de qué variables eran óptimas (tiro, defensa, regate) para poder aplicar Regresión (predicting `value_eur`) y Clasificación (predicting `elite` en base al Overall) fue un proceso analítico realizado sobre `male_players.csv`, el cual aporta la riqueza y volumen ideal (96MB de datos) exigido por el proyecto.
