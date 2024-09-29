import json
from procesamiento import cargar_conocimiento

# Función para agregar una nueva pregunta y respuesta al archivo
def agregar_respuesta(pregunta, respuesta):
    knowledge = cargar_conocimiento()
    nuevo_conocimiento = {
        "pregunta": pregunta.strip().lower(),
        "respuesta": [respuesta]
    }
    knowledge.append(nuevo_conocimiento)
    with open('knowledge.json', 'w', encoding='utf-8') as archivo:
        json.dump(knowledge, archivo, ensure_ascii=False, indent=2)
