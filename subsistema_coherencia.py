from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

class SubsistemaCoherencia:
    def __init__(self, base_conocimiento):
        self.base_conocimiento = base_conocimiento

    def verificar_coherencia(self, pregunta):
        conocimiento = self.base_conocimiento.cargar_conocimiento()
        pregunta_lematizada = self.lematizar_frase(pregunta)
        for item in conocimiento:
            pregunta_conocimiento_lematizada = self.lematizar_frase(item['pregunta'].strip().lower())
            if pregunta_conocimiento_lematizada == pregunta_lematizada:
                return False  # La pregunta ya existe
        return True

    def lematizar_frase(self, frase):
        tokens = word_tokenize(frase.lower())
        lematizado = [lemmatizer.lemmatize(token) for token in tokens]
        return ' '.join(lematizado)
