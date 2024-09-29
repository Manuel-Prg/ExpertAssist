import tkinter as tk
from tkinter import ttk
from procesamiento import buscar_respuesta, cargar_conocimiento
from agregar_respuesta import agregar_respuesta
from retroalimentacion import Feedback
import json


class AsistenteReparacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema Experto de Reparación de Equipos")
        self.geometry("500x600")
        self.configure(bg="#F0F0F5")

        # Cargar conocimiento desde archivo al iniciar la aplicación
        self.conocimiento = cargar_conocimiento()

        # Cargar el feedback
        self.feedback = Feedback()

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self, bg="#F0F0F5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título con emoji como icono
        title_frame = tk.Frame(main_frame, bg="#F0F0F5")
        title_frame.pack(fill=tk.X, pady=(20, 10))

        icon_label = tk.Label(title_frame, text="💻", font=("Segoe UI Emoji", 24), bg="#F0F0F5", fg="#5D5D5D")
        icon_label.pack(side=tk.LEFT, padx=(20, 10))

        title_label = tk.Label(title_frame, text="Asistente Experto", 
                               font=("Helvetica", 24, "bold"), bg="#F0F0F5", fg="#333333")
        title_label.pack(side=tk.LEFT)

        # Área de chat
        self.chat_frame = tk.Frame(main_frame, bg="#FFFFFF", bd=1, relief=tk.SOLID)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))

        self.canvas = tk.Canvas(self.chat_frame, bg="#FFFFFF")
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#FFFFFF")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Habilitar el scroll con el mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", lambda event: self._on_mousewheel(event, -1))    # Linux Scroll Up
        self.canvas.bind_all("<Button-5>", lambda event: self._on_mousewheel(event, 1))     # Linux Scroll Down

        # Frame para entrada y botón
        input_frame = tk.Frame(main_frame, bg="#F0F0F5")
        input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Entrada de texto
        self.entry = tk.Entry(input_frame, font=("Helvetica", 12), bg="#FFFFFF", fg="#333333", 
                              insertbackground="#333333", relief=tk.SOLID, bd=1)
        self.entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

        # Botón de enviar
        send_button = tk.Button(input_frame, text="Enviar", command=self.enviar_mensaje, 
                                bg="#4CAF50", fg="#FFFFFF", activebackground="#45a049", 
                                activeforeground="#FFFFFF", font=("Helvetica", 12),
                                relief=tk.FLAT, bd=0, padx=15, pady=5, cursor="hand2")
        send_button.pack(side=tk.RIGHT)

        # Bind para presionar "Enter"
        self.entry.bind("<Return>", lambda event: self.enviar_mensaje())
        
    def _on_mousewheel(self, event, direction=None):
        if direction is not None:  # Linux/Unix
            self.canvas.yview_scroll(direction, "units")
        else:  # Windows/macOS
            self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def enviar_mensaje(self):
        pregunta = self.entry.get().strip()
        if pregunta:
            self.mostrar_mensaje("Tú: " + pregunta, "usuario")
            respuesta = buscar_respuesta(pregunta, self.conocimiento)
            self.mostrar_mensaje("Bot: " + respuesta, "bot")
            
            # Llamará a la ventana de aprendizaje si no encuentra una respuesta
            if respuesta.startswith("Lo siento, no tengo una respuesta para eso"):
                self.ventana_aprendizaje(pregunta)
            else:
                # Si hay una respuesta válida, mostrar opciones de retroalimentación
                self.mostrar_retroalimentacion(pregunta, respuesta)
            
            self.entry.delete(0, tk.END)

    def mostrar_mensaje(self, mensaje, tipo):
        frame = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
        frame.pack(fill=tk.X, padx=10, pady=5)

        if tipo == "usuario":
            bubble = tk.Label(frame, text=mensaje, font=("Helvetica", 12), 
                              bg="#DFF8E6", fg="#000000", wraplength=400, 
                              justify="left", padx=10, pady=5)
            bubble.pack(side=tk.RIGHT)
        else:
            bubble = tk.Label(frame, text=mensaje, font=("Helvetica", 12), 
                              bg="#E9E9E9", fg="#000000", wraplength=400, 
                              justify="left", padx=10, pady=5)
            bubble.pack(side=tk.LEFT)

        bubble.configure(relief=tk.RAISED, bd=0)

        frame.update_idletasks()
        frame.configure(width=self.chat_frame.winfo_width() - 20)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)

    def ventana_aprendizaje(self, pregunta):
        ventana_agregar = tk.Toplevel(self)
        ventana_agregar.title("Agregar Nueva Respuesta")
        ventana_agregar.geometry("500x250")
        ventana_agregar.configure(bg="#F0F0F5")

        frame = tk.Frame(ventana_agregar, bg="#F0F0F5", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Agregar Nueva Respuesta", font=("Helvetica", 16, "bold"), bg="#F0F0F5", fg="#333333").pack(pady=(0, 20))
        tk.Label(frame, text=f"Pregunta: {pregunta}", font=("Helvetica", 12), bg="#F0F0F5", fg="#333333").pack(anchor="w", pady=(0, 10))

        entry_respuesta = tk.Entry(frame, width=50, font=("Helvetica", 12), bg="#FFFFFF", fg="#333333", insertbackground="#333333")
        entry_respuesta.pack(fill=tk.X, pady=(0, 20))

        def agregar_nueva_respuesta():
            respuesta = entry_respuesta.get()
            agregar_respuesta(pregunta, respuesta)
            self.mostrar_mensaje("Bot: ¡Gracias! He aprendido una nueva respuesta.", "bot")
            ventana_agregar.destroy()

        agregar_button = tk.Button(frame, text="Agregar Respuesta", command=agregar_nueva_respuesta, 
                                   bg="#4CAF50", fg="#FFFFFF", activebackground="#45a049", 
                                   activeforeground="#FFFFFF", font=("Helvetica", 12),
                                   relief=tk.FLAT, bd=0, padx=15, pady=5, cursor="hand2")
        agregar_button.pack()

    def mostrar_retroalimentacion(self, pregunta, respuesta):
        feedback_frame = tk.Frame(self.scrollable_frame, bg="#FFFFFF")
        feedback_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(feedback_frame, text="¿Te fue útil esta respuesta?", font=("Helvetica", 10)).pack(side=tk.LEFT)
        
        tk.Button(feedback_frame, text="Sí", command=lambda: self.procesar_feedback(pregunta, respuesta, True)).pack(side=tk.LEFT, padx=5)
        tk.Button(feedback_frame, text="No", command=lambda: self.procesar_feedback(pregunta, respuesta, False)).pack(side=tk.LEFT)

    def procesar_feedback(self, pregunta, respuesta, fue_util):
        valoracion = 1 if fue_util else 0  # "Sí" es 1 y "No" es 0
        self.feedback.agregar_feedback(pregunta, respuesta, valoracion)

        if fue_util:
            self.mostrar_mensaje("¡Gracias por tu retroalimentación!", "bot")
        else:
            self.mostrar_mensaje("Lo sentimos, intentaremos mejorar.", "bot")
    
    def cargar_feedback(self):
        try:
            with open('feedback.json', 'r', encoding='utf-8') as archivo:
                    # Leer el archivo y eliminar espacios en blanco
                contenido = archivo.read().strip()
                  # Si el archivo está vacío
                if not contenido:  
                    # Retornar una lista vacía
                    return []  
                return json.loads(contenido)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si no existe el archivo o hay un error en el formato JSON
            return []  

if __name__ == "__main__":
    app = AsistenteReparacion()
    app.mainloop()
