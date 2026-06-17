import json
import os

cells = []

def add_md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [text]})

def add_code(text):
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [text]})

add_md("""# MINERÍA DE DATOS · UNIDAD 2 — DEL TEXTO AL SIGNIFICADO · UPCh 2026A
## Lab 1 — Pipeline de preprocesamiento de texto
De texto crudo a términos limpios · NLTK + spaCy (es_core_news_sm)""")

add_md("### 0 · Entorno")
add_code("""# !pip install -q nltk spacy && python -m spacy download es_core_news_sm
import re, unicodedata, json
from collections import Counter
import pandas as pd

import nltk
nltk.download('punkt', quiet=True)
from nltk.stem import SnowballStemmer

import spacy
try:
    nlp = spacy.load('es_core_news_sm')
except OSError:
    from spacy.cli import download; download('es_core_news_sm')
    nlp = spacy.load('es_core_news_sm')

print('Entorno listo.')""")

add_md("### Corpus")
add_code("""corpus_crudo = [
    {"id": "d01", "titulo": "Lluvias provocan inundaciones en Tuxtla",
     "texto": "Las  fuertes lluvias   provocaron inundaciones en varias colonias del sur de Tuxtla Gutierrez 😟. "
              "Proteccion Civil pidio a la poblacion no cruzar las calles anegadas. Mas info en https://chiapasparalelo.com/nota1 ."},
    {"id": "d02", "titulo": "Crisis hidrica golpea la region",
     "texto": "La crisis hidrica se agrava: el desabasto del liquido vital afecta a miles de familias en la zona alta. "
              "Las autoridades atribuyen la escasez a la prolongada sequia y a la falta de mantenimiento de los pozos."},
    {"id": "d03", "titulo": "Cafe de Chiapas rompe record de exportacion",
     "texto": "El cafe de Chiapas rompio su record historico de exportacion este ciclo, impulsado por la demanda en Europa y Asia. "
              "Los productores de la Sierra celebran precios al alza."},
    {"id": "d04", "titulo": "Sequia afecta cultivos de maiz",
     "texto": "La sequia afecta gravemente los cultivos de maiz y frijol en la region fronteriza. "
              "Los agricultores reportan perdidas de hasta el 40% y piden apoyos al gobierno estatal."},
    {"id": "d05", "titulo": "Turismo crece en el Canon del Sumidero",
     "texto": "El Canon del Sumidero recibio mas de 200 mil visitantes durante la temporada. "
              "Los recorridos en lancha y el avistamiento de fauna son los principales atractivos del parque nacional. #Chiapas"},
    {"id": "d06", "titulo": "Sismo de magnitud 5.1 frente a las costas",
     "texto": "Un sismo de magnitud 5.1 se registro frente a las costas de Chiapas la madrugada del martes. "
              "No se reportaron danos ni victimas, informo el Servicio Sismologico Nacional."},
    {"id": "d07", "titulo": "UPCh inaugura laboratorio de IA",
     "texto": "La Universidad Politecnica de Chiapas inauguro un nuevo laboratorio de inteligencia artificial "
              "equipado con GPUs para proyectos de aprendizaje automatico y vision por computadora. Visita https://upchiapas.edu.mx ."},
    {"id": "d08", "titulo": "Repunta la produccion de cacao",
     "texto": "La produccion de cacao en la region del Soconusco repunto este año tras varios ciclos a la baja. "
              "Cooperativas locales apuestan por el chocolate artesanal de origen para mercados premium."},
    {"id": "d09", "titulo": "San Cristobal, destino cultural",
     "texto": "San Cristobal de las Casas se consolida como destino cultural: sus mercados, iglesias y cafeterias "
              "atraen a viajeros de todo el mundo. La gastronomia y el textil artesanal son protagonistas."},
    {"id": "d10", "titulo": "Avanza obra de infraestructura carretera",
     "texto": "Avanza la rehabilitacion de la carretera que conecta Tuxtla con la costa. "
              "La obra busca reducir tiempos de traslado y mejorar la seguridad vial para miles de automovilistas."},
    {"id": "d11", "titulo": "Alertan por casos de dengue",
     "texto": "La Secretaria de Salud alerto por un repunte de casos de dengue en municipios de tierra caliente. "
              "Pide a la poblacion eliminar criaderos de mosco y acudir al medico ante fiebre alta. 🦟"},
    {"id": "d12", "titulo": "Feria celebra el cafe y el cacao",
     "texto": "La feria regional celebro el cafe y el cacao chiapaneco con catas, musica y venta directa de productores. "
              "Miles de asistentes recorrieron los stands durante el fin de semana."},
    {"id": "d13", "titulo": "Restablecen servicio de agua potable",
     "texto": "El servicio de agua potable se restablecera de forma escalonada en las colonias afectadas por la falla en la red. "
              "El organismo operador pidio a los usuarios almacenar agua de manera responsable."},
    {"id": "d14", "titulo": "Estudiantes ganan concurso de robotica",
     "texto": "Estudiantes de ingenieria de Tuxtla ganaron el primer lugar en un concurso nacional de robotica 🤖 "
              "con un brazo robotico de bajo costo. El equipo representara a Mexico en una competencia internacional."},
]
print(f"{len(corpus_crudo)} documentos cargados.")""")

add_code("""df = pd.DataFrame(corpus_crudo)
df['n_chars'] = df['texto'].str.len()
df[['id', 'titulo', 'n_chars']].head()""")

add_md("""### 1 · Cargar y explorar
Antes de limpiar, hay que mirar los datos. Una limpieza a ciegas destruye señal sin que se den cuenta.
**1.a Estadísticas de longitud.**""")

add_code("""num_docs = len(df)
media_caracteres = df['n_chars'].mean()
media_palabras = df['texto'].str.split().str.len().mean()

print(f"Numero de documentos: {num_docs}")
print(f"Longitud media en caracteres: {media_caracteres:.2f}")
print(f"Longitud media en palabras (split ingenuo): {media_palabras:.2f}")""")

add_md("**1.b Detección de ruido.** Completen los detectores de etiquetas HTML y de emojis, y reporten en qué documentos aparece cada tipo de ruido.")
add_code("""RE_URL  = re.compile(r'https?://\\S+')
RE_HTML = re.compile(r'<[^>]+>') 
RE_EMOJI = re.compile(r'[^\\w\\s.,:;/#%A-Za-z0-9áéíóúÁÉÍÓÚñÑ]+')

for fila in corpus_crudo:
    urls = RE_URL.findall(fila['texto'])
    if urls:
        print(fila['id'], '-> URL:', urls)
        
    htmls = RE_HTML.findall(fila['texto'])
    if htmls:
        print(fila['id'], '-> HTML:', htmls)
        
    emojis = [c for c in fila['texto'] if unicodedata.category(c) == 'So']
    if emojis:
        print(fila['id'], '-> Emoji:', emojis)""")

add_md("""**Pregunta (defensa): de los tres tipos de ruido, ¿cuál podría ser señal útil en algún dominio y por qué?**

**Su respuesta:** Los Emojis. En dominios como análisis de sentimiento en redes sociales, los emojis expresan directamente la polaridad o emoción del usuario, compensando la falta de entonación en el texto y actuando como un predictor importante.""")

add_md("""### 2 · Tokenizar y normalizar
**2.a Comparen el split ingenuo contra un tokenizador real (spaCy).**""")
add_code("""ejemplo = corpus_crudo[0]['texto']

ingenuo = ejemplo.split()
print('Ingenuo  :', ingenuo[:12])

doc = nlp(ejemplo)
spacy_tokens = [t.text for t in doc]
print('spaCy    :', spacy_tokens[:12])""")

add_md("""**Diferencias:** 
1. spaCy aísla los signos de puntuación ("Gutierrez", "😟", "."), mientras que el split ingenuo agrupa la puntuación a la palabra adyacente ("Gutierrez", "😟.").
2. spaCy colapsa los espacios múltiples intermedios automáticamente de manera más limpia.""")

add_md("""**2.b Función de normalización.**""")
add_code("""def normalizar(texto, quitar_acentos=False):
    texto = re.sub(r'<[^>]+>', ' ', texto)
    texto = re.sub(r'https?://\\S+', ' ', texto)
    texto = texto.lower()
    texto = unicodedata.normalize('NFC', texto)
    
    if quitar_acentos:
        texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
        
    texto = re.sub(r'\\s+', ' ', texto).strip()
    return texto

print(normalizar(corpus_crudo[2]['texto'], quitar_acentos=True))""")

add_md("""**Decisión documentada: ¿quitar acentos por defecto, sí o no?**

**Su decisión y justificación:** Sí, decidí quitarlos. 
*A favor:* Los usuarios en buscadores comúnmente omiten las tildes ("cafe" en vez de "café"). Quitar acentos aumenta el "Recall" porque unifica ambas grafías en el mismo término.
*En contra:* Podría generar polisemia al colapsar palabras distintas (ej: "inglés" vs "ingles").
*Conclusión:* Para este corpus de noticias, pesa más facilitar la búsqueda al usuario y tolerar faltas de ortografía que la pérdida marginal de precisión por palabras homónimas.""")

add_md("""### 3 · Stopwords con criterio""")
add_code("""stopwords_es = nlp.Defaults.stop_words
print('Total de stopwords de spaCy (es):', len(stopwords_es))
print(sorted(list(stopwords_es))[:30])""")

add_code("""CONSERVAR = {'no', 'sin', 'ni', 'pero'}

MIS_STOPWORDS = set(stopwords_es) - CONSERVAR
print(f"Se eliminaron {len(stopwords_es) - len(MIS_STOPWORDS)} stopwords de la lista original.")
print(f"¿'no' esta en stopwords? {'no' in MIS_STOPWORDS}")""")

add_md("""**Justifiquen qué conservaron y por qué (lo defenderán oralmente):**
Conservé las negaciones ('no', 'sin', 'ni'). Filtrar un "no" destruye completamente el sentido de oraciones informativas (ej. cambia de "No se reportaron daños" a "reportaron daños"). Mantener el contexto de negación es fundamental en un buscador.""")

add_md("""### 4 · Stemming vs. lemmatización""")
add_code("""stemmer = SnowballStemmer('spanish')

def tokens_stemming(texto):
    norm = normalizar(texto, quitar_acentos=True)
    tokens = re.findall(r'\\b\\w+\\b', norm)
    return [stemmer.stem(t) for t in tokens if t not in MIS_STOPWORDS]

def tokens_lemma(texto):
    norm = normalizar(texto, quitar_acentos=True)
    doc = nlp(norm)
    tokens = []
    for t in doc:
        if t.is_punct or t.is_space:
            continue
        lemma = t.lemma_.lower()
        lemma = ''.join(c for c in unicodedata.normalize('NFD', lemma) if unicodedata.category(c) != 'Mn')
        if lemma not in MIS_STOPWORDS:
            tokens.append(lemma)
    return tokens""")

add_md("""**4.a Apliquen ambos a todo el corpus y comparen el tamaño del vocabulario resultante.**""")
add_code("""vocab_stem = set()
vocab_lemma = set()

for f in corpus_crudo:
    txt = f['texto']
    vocab_stem.update(tokens_stemming(txt))
    vocab_lemma.update(tokens_lemma(txt))

print(f"|V_stemming|: {len(vocab_stem)} términos")
print(f"|V_lemma|   : {len(vocab_lemma)} términos")

print("\\nEjemplos en lemma que no están en stemming:")
print(list(vocab_lemma - vocab_stem)[:10])""")

add_md("""**Decisión final: ¿stemming o lemmatización para este corpus en español?**

**Su decisión y justificación:** Lematización. El Stemming en español a menudo trunca palabras salvajemente (sobre-stemming), agrupando raíces de formas que pierden sentido semántico. La lematización con spaCy respeta la morfología del idioma, reduciendo el vocabulario pero manteniendo términos que siguen siendo válidos lingüísticamente.""")

add_md("""### 5 · Pipeline final + persistencia""")
add_code("""def preprocesar(texto):
    \"\"\"Pipeline definitivo del equipo: texto crudo -> lista de terminos limpios.
    Debe reflejar TODAS sus decisiones (acentos, stopwords, stemming/lemma).\"\"\"
    return tokens_lemma(texto)

for fila in corpus_crudo[:3]:
    print(fila['id'], '->', preprocesar(fila['texto'])[:10])""")

add_code("""corpus_procesado = [{'id': f['id'], 'titulo': f['titulo'],
                     'tokens': preprocesar(f['texto'])} for f in corpus_crudo]

with open('corpus_crudo.json', 'w', encoding='utf-8') as fh:
    json.dump(corpus_crudo, fh, ensure_ascii=False, indent=2)
with open('corpus_procesado.json', 'w', encoding='utf-8') as fh:
    json.dump(corpus_procesado, fh, ensure_ascii=False, indent=2)

print('Guardados: corpus_crudo.json y corpus_procesado.json')""")

notebook = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("lap 1/Lab_1_Pipeline.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=2)
