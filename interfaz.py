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

    def __crear_icono(self):

        # Crear una imagen pequeña con forma de hoja.
        self.icono = tk.PhotoImage(width=32, height=32)

        self.icono.put("#ffffff", to=(0, 0, 32, 32))

        # Tallo de la hoja.
        for y in range(8, 26):
            x = 16 - (y - 8) // 5
            self.icono.put("#286b35", (x, y))

        # Forma de la hoja.
        for y in range(5, 27):
            ancho = int(10 * (1 - abs(y - 16) / 12))

            for x in range(16 - ancho, 16 + ancho + 1):
                if 0 <= x < 32:
                    self.icono.put("#65a947", (x, y))

        # Nervadura central.
        for y in range(8, 25):
            x = 16 - (y - 8) // 5
            self.icono.put("#e0f0c9", (x, y))

        self.ventana.iconphoto(True, self.icono)

    def __crear_menu(self):

        menu_principal = tk.Menu(self.ventana)

        menu_archivo = tk.Menu(menu_principal, tearoff=0)
        menu_archivo.add_command(
            label="Exportar archivo Excel",
            command=self.__exportar_excel
        )
        menu_archivo.add_separator()
        menu_archivo.add_command(
            label="Salir",
            command=self.ventana.destroy
        )

        menu_principal.add_cascade(
            label="Archivo",
            menu=menu_archivo
        )

        menu_ayuda = tk.Menu(menu_principal, tearoff=0)
        menu_ayuda.add_command(
            label="Acerca del programa",
            command=lambda: messagebox.showinfo(
                "Acerca de",
                "Sistema de gestión de entradas del Parque Botánico."
            )
        )

        menu_principal.add_cascade(
            label="Ayuda",
            menu=menu_ayuda
        )

        self.ventana.config(menu=menu_principal)

