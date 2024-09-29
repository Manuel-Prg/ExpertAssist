# entrenamiento.py
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

def cargar_datos(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def entrenar_modelo(data):
    preguntas = [item['pregunta'] for item in data]
    respuestas = [item['respuesta'] for item in data]

    modelo = make_pipeline(CountVectorizer(), LogisticRegression())
    modelo.fit(preguntas, respuestas)

    return modelo
