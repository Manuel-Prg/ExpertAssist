class Feedback:
    def __init__(self):
        self.retroalimentacion = []

    def agregar_feedback(self, pregunta, respuesta, valoracion):
        self.retroalimentacion.append({"pregunta": pregunta, "respuesta": respuesta, "valoracion": valoracion})

    def obtener_feedback(self):
        return self.retroalimentacion

    def calcular_promedio_valoracion(self):
        if not self.retroalimentacion:
            return 0
        total = sum(item["valoracion"] for item in self.retroalimentacion)
        return total / len(self.retroalimentacion)
