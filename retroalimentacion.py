import json

class Feedback:
    def __init__(self):
        self.retroalimentacion = self.cargar_feedback()  # Cargar retroalimentación existente

    def agregar_feedback(self, pregunta, respuesta, valoracion):
        # Agregar la retroalimentación
        self.retroalimentacion.append({"pregunta": pregunta, "respuesta": respuesta, "valoracion": valoracion})
        self.guardar_feedback()  # Guardar en el archivo

    def cargar_feedback(self):
        try:
            with open('feedback.json', 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return []  # Si no existe el archivo, retornar una lista vacía

    def guardar_feedback(self):
        with open('feedback.json', 'w', encoding='utf-8') as archivo:
            json.dump(self.retroalimentacion, archivo, ensure_ascii=False, indent=2)

    def obtener_feedback(self):
        return self.retroalimentacion

    def calcular_promedio_valoracion(self):
        if not self.retroalimentacion:
            return 0
        total = sum(item["valoracion"] for item in self.retroalimentacion)
        return total / len(self.retroalimentacion)
