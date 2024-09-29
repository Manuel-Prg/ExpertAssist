import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

class MotorInferencia:
    def __init__(self, base_conocimiento):
        self.base_conocimiento = base_conocimiento

    def buscar_respuesta(self, pregunta):
        pregunta_lematizada = self.lematizar_frase(pregunta)
        conocimiento = self.base_conocimiento.cargar_conocimiento()
        for item in conocimiento:
            pregunta_conocimiento_lematizada = self.lematizar_frase(item['pregunta'].strip().lower())
            if pregunta_conocimiento_lematizada == pregunta_lematizada:
                return item['respuesta'][0]
        return "Lo siento, no tengo una respuesta para eso."

    def lematizar_frase(self, frase):
        tokens = word_tokenize(frase.lower())
        lematizado = [lemmatizer.lemmatize(token) for token in tokens]
        return ' '.join(lematizado)
