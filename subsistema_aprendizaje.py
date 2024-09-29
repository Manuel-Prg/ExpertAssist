class SubsistemaAprendizaje:
    def __init__(self, subsistema_adquisicion, subsistema_coherencia):
        self.subsistema_adquisicion = subsistema_adquisicion
        self.subsistema_coherencia = subsistema_coherencia

    def aprender(self, pregunta, respuesta):
        if self.subsistema_coherencia.verificar_coherencia(pregunta):
            self.subsistema_adquisicion.agregar_nueva_respuesta(pregunta, respuesta)
            return "He aprendido una nueva respuesta."
        return "Ya conozco esta respuesta."
