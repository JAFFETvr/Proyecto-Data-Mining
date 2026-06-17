import json
import os

cells = []

def add_md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [text]})

def add_code(text):
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [text]})

add_md("""# MINERÍA DE DATOS · UNIDAD 2 — DEL TEXTO AL SIGNIFICADO · UPCh 2026A
## Lab 2 — Su primer motor de búsqueda
TF-IDF + similitud coseno, implementados desde cero · sin librerías de NLP""")

add_md("### 0 · Cargar el corpus procesado del Lab 1")
add_code("""import json, math, re, unicodedata
import spacy
try:
    nlp = spacy.load('es_core_news_sm')
except OSError:
    from spacy.cli import download; download('es_core_news_sm')
    nlp = spacy.load('es_core_news_sm')

with open('../lap 1/corpus_procesado.json', encoding='utf-8') as fh:
    corpus = json.load(fh)

documentos = [d['tokens'] for d in corpus]
print(f'{len(corpus)} documentos.  Ejemplo {corpus[0]["id"]}:', documentos[0][:8])""")

add_md("Reutilicen su preprocesar. Péguenla aquí idéntica a la del Lab 1.")
add_code("""stopwords_es = nlp.Defaults.stop_words
CONSERVAR = {'no', 'sin', 'ni', 'pero'}
MIS_STOPWORDS = set(stopwords_es) - CONSERVAR

def normalizar(texto, quitar_acentos=False):
    texto = re.sub(r'<[^>]+>', ' ', texto)
    texto = re.sub(r'https?://\\S+', ' ', texto)
    texto = texto.lower()
    texto = unicodedata.normalize('NFC', texto)
    if quitar_acentos:
        texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'\\s+', ' ', texto).strip()
    return texto

def preprocesar(texto):
    norm = normalizar(texto, quitar_acentos=True)
    doc = nlp(norm)
    tokens = []
    for t in doc:
        if t.is_punct or t.is_space: continue
        lemma = t.lemma_.lower()
        lemma = ''.join(c for c in unicodedata.normalize('NFD', lemma) if unicodedata.category(c) != 'Mn')
        if lemma not in MIS_STOPWORDS:
            tokens.append(lemma)
    return tokens""")

add_md("### 1 · Indexar — TF, IDF y TF-IDF desde cero")
add_code("""from collections import Counter

def tf(doc):
    counts = Counter(doc)
    total = len(doc)
    if total == 0: return {}
    return {t: count/total for t, count in counts.items()}

def idf(corpus):
    N = len(corpus)
    df = Counter()
    for doc in corpus:
        df.update(set(doc))
    return {t: math.log(N / count) for t, count in df.items()}

def tfidf(doc, idf_):
    tf_doc = tf(doc)
    return {t: tf_val * idf_.get(t, 0) for t, tf_val in tf_doc.items()}""")

add_code("""IDF = idf(documentos)
INDICE = [tfidf(doc, IDF) for doc in documentos]

import operator
top = sorted(INDICE[3].items(), key=operator.itemgetter(1), reverse=True)[:5]
print('Terminos top de', corpus[3]['id'], '->', top)""")

add_md("### 2 · Procesar la consulta")
add_code("""def vectorizar_consulta(texto):
    tokens = preprocesar(texto)
    return tfidf(tokens, IDF)

print(vectorizar_consulta('sequia en los cultivos'))""")

add_md("### 3 · Ranquear — similitud coseno")
add_code("""def coseno(v1, v2):
    interseccion = set(v1.keys()) & set(v2.keys())
    dot = sum(v1[t] * v2[t] for t in interseccion)
    
    norm1 = math.sqrt(sum(val**2 for val in v1.values()))
    norm2 = math.sqrt(sum(val**2 for val in v2.values()))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
        
    return dot / (norm1 * norm2)

def buscar(consulta, k=5):
    q = vectorizar_consulta(consulta)
    scores = []
    for i, doc_vector in enumerate(INDICE):
        score = coseno(q, doc_vector)
        scores.append((corpus[i]['id'], corpus[i]['titulo'], score))
        
    scores.sort(key=lambda x: x[2], reverse=True)
    return scores[:k]""")

add_code("""for id_, titulo, score in buscar('sequia y cultivos de maiz'):
    print(f'{score:.3f}  {id_}  {titulo}')""")

add_md("### 4 · Rómpanlo")
add_code("""print('Consulta: "problemas de agua"')
for id_, titulo, score in buscar('problemas de agua'):
    print(f'{score:.3f}  {id_}  {titulo}')""")

add_code("""print('\\nConsulta fallida 1: "ausencia de precipitaciones"')
for id_, titulo, score in buscar('ausencia de precipitaciones'):
    print(f'{score:.3f}  {id_}  {titulo}')""")

add_md("""**Causa de la falla 1:** 
Esta consulta es un **sinónimo semántico** de "sequía" (documentos d02 y d04). Sin embargo, TF-IDF se basa en correspondencia léxica exacta. Al no compartir exactamente la misma raíz ("ausencia" vs "falta", "precipitaciones" vs "lluvias"), el producto punto es 0, y el motor ignora los documentos a pesar de ser los correctos para esa intención.""")

add_code("""print('\\nConsulta fallida 2: "bajas por sismo en la costa"')
for id_, titulo, score in buscar('bajas por sismo en la costa'):
    print(f'{score:.3f}  {id_}  {titulo}')""")

add_md("""**Causa de la falla 2:** 
Este es un fallo por **falta de comprensión de negaciones y relaciones**. La consulta busca muertes (bajas) provocadas por el sismo. El buscador indexa alto el documento d06 por las palabras "sismo" y "costas", pero no entiende que dentro del documento d06 dice "No se reportaron bajas". TF-IDF puntúa alto los tokens individuales pero ignora totalmente el sentido opuesto de la oración.""")

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

with open("lap 2/Lab_2_Buscador.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=2)
