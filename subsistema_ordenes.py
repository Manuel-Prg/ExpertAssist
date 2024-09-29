class SubsistemaOrdenes:
    def ejecutar_orden(self, comando):
        if comando.lower() == "apagar sistema":
            return "El sistema se está apagando."
        return "Comando no reconocido."
