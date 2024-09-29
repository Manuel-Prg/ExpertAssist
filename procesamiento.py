import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Descargar recursos de NLTK
nltk.download('punkt')
nltk.download('wordnet')

# Inicializar el lematizador
lemmatizer = WordNetLemmatizer()

# Función para cargar el conocimiento desde el archivo JSON
def cargar_conocimiento():
    try:
        with open('knowledge.json', 'r', encoding='utf-8') as archivo:
            knowledge = json.load(archivo)
    except FileNotFoundError:
        knowledge = []
    return knowledge

# Función para lematizar una frase
def lematizar_frase(frase):
    tokens = word_tokenize(frase.lower())
    lematizado = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(lematizado)

# Función para buscar una respuesta en base a la pregunta
def buscar_respuesta(pregunta, knowledge):
    pregunta_lematizada = lematizar_frase(pregunta)
    for item in knowledge:
        if isinstance(item, dict) and 'pregunta' in item and 'respuesta' in item:
            pregunta_conocimiento_lematizada = lematizar_frase(item['pregunta'].strip().lower())
            if pregunta_conocimiento_lematizada == pregunta_lematizada:
                return item['respuesta'][0]
    return "Lo siento, no tengo una respuesta para eso. Puedes buscar ayuda específica en línea o consultar con un técnico especializado."
