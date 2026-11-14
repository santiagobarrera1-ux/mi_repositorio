import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import shutil


class InterfazGrafica:

    def __init__(self, parque, backend):

        self.parque = parque
        self.backend = backend

        self.ventana = tk.Tk()
        self.ventana.title("Gestión del Parque Botánico")
        self.ventana.geometry("950x650")
        self.ventana.minsize(800, 550)

        self.__crear_icono()
        self.__crear_menu()
        self.__crear_interfaz()

        self.__mostrar_visitantes()

        self.ventana.bind("<F5>", lambda evento: self.__mostrar_visitantes())



