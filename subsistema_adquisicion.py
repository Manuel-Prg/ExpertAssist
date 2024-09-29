class SubsistemaAdquisicion:
    def __init__(self, base_conocimiento):
        self.base_conocimiento = base_conocimiento

    def agregar_nueva_respuesta(self, pregunta, respuesta):
        conocimiento = self.base_conocimiento.cargar_conocimiento()
        nuevo_conocimiento = {
            "pregunta": pregunta.strip().lower(),
            "respuesta": [respuesta]
        }
        conocimiento.append(nuevo_conocimiento)
        self.base_conocimiento.guardar_conocimiento(conocimiento)
