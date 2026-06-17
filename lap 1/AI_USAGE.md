# Declaración de uso de IA - Lab 1

De acuerdo con las reglas de entrega de la Unidad 2, declaro el siguiente uso de asistentes de inteligencia artificial:

* **Herramienta:** ChatGPT / Claude
* **Uso (Sección 1.b):** Se le solicitó la estructura base (boilerplate) para armar una Expresión Regular (`re.compile`) que limpiara las etiquetas HTML y se consultó cómo extraer Emojis usando la librería `unicodedata` (`category 'So'`). Yo integré esa lógica a mi bucle `for` para imprimir los documentos afectados.
* **Uso (Sección 4):** Se le pidió la sintaxis para invocar la librería de NLTK (`SnowballStemmer`) y para iterar sobre los tokens de `spaCy`. 
* **Qué cambié/decidí yo:** El código generado por la IA para filtrar *Stopwords* fue modificado manualmente por mí para evitar que borrara las negaciones (`"no"`, `"sin"`, `"ni"`), ya que en las noticias (ej. "No se reportaron daños") esto arruina completamente el contexto. Asimismo, la decisión final de utilizar Lematización y eliminar los acentos para maximizar el *Recall* en búsquedas es de mi autoría.
