from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import json
class ModeloAprendizaje:
    def __init__(self):
        self.vectorizador = TfidfVectorizer()
        self.modelo = LogisticRegression()
    
    def entrenar(self, preguntas, respuestas):
        X = self.vectorizador.fit_transform(preguntas)
        y = respuestas
        self.modelo.fit(X, y)
        joblib.dump(self.modelo, 'modelo.pkl')  # Guardar el modelo entrenado

    def predecir(self, pregunta):
        modelo = joblib.load('modelo.pkl')  # Cargar el modelo guardado
        X = self.vectorizador.transform([pregunta])
        return modelo.predict(X)[0]
