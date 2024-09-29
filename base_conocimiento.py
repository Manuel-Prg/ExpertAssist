import json

class BaseConocimiento:
    def __init__(self, archivo='knowledge.json'):
        self.archivo = archivo

    def cargar_conocimiento(self):
        try:
            with open(self.archivo, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return []

    def guardar_conocimiento(self, conocimiento):
        with open(self.archivo, 'w', encoding='utf-8') as archivo:
            json.dump(conocimiento, archivo, ensure_ascii=False, indent=2)
