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

    def __crear_interfaz(self):

        titulo = ttk.Label(
            self.ventana,
            text="GESTIÓN DEL PARQUE BOTÁNICO",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=15)

        # Componente adicional: Notebook.
        # Permite organizar la aplicación en pestañas.
        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.pestana_visitantes = ttk.Frame(self.pestanas)
        self.pestana_reportes = ttk.Frame(self.pestanas)

        self.pestanas.add(
            self.pestana_visitantes,
            text="Visitantes"
        )

        self.pestanas.add(
            self.pestana_reportes,
            text="Reportes"
        )

        self.__crear_pestana_visitantes()
        self.__crear_pestana_reportes()

    def __crear_pestana_visitantes(self):

        formulario = ttk.LabelFrame(
            self.pestana_visitantes,
            text="Registrar visitante",
            padding=12
        )
        formulario.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(formulario, text="Documento:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )

        self.entrada_documento = ttk.Entry(formulario)
        self.entrada_documento.grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(formulario, text="Nombre:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )

        self.entrada_nombre = ttk.Entry(formulario)
        self.entrada_nombre.grid(
            row=1, column=1, padx=5, pady=5
        )

        ttk.Label(formulario, text="Edad:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )

        self.entrada_edad = ttk.Entry(formulario)
        self.entrada_edad.grid(
            row=2, column=1, padx=5, pady=5
        )

        ttk.Label(formulario, text="Tipo de visitante:").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )

        self.tipo_visitante = tk.StringVar(value="Automático")

        self.radio_automatico = ttk.Radiobutton(
            formulario,
            text="Automático según edad",
            variable=self.tipo_visitante,
            value="Automático"
        )
        self.radio_automatico.grid(
            row=3, column=1, sticky="w"
        )

        self.radio_mayor = ttk.Radiobutton(
            formulario,
            text="Mayor de edad",
            variable=self.tipo_visitante,
            value="Mayor de edad"
        )
        self.radio_mayor.grid(
            row=4, column=1, sticky="w"
        )

        self.radio_menor = ttk.Radiobutton(
            formulario,
            text="Menor de edad",
            variable=self.tipo_visitante,
            value="Menor de edad"
        )
        self.radio_menor.grid(
            row=5, column=1, sticky="w"
        )

        ttk.Button(
            formulario,
            text="Registrar visitante",
            command=self.__registrar_visitante
        ).grid(
            row=6, column=0, columnspan=2, pady=10
        )

        # Zona de búsqueda y filtro.
        filtros = ttk.Frame(self.pestana_visitantes)
        filtros.pack(fill="x", padx=10, pady=5)

        ttk.Label(
            filtros,
            text="Filtrar por tipo:"
        ).pack(side="left", padx=5)

        self.filtro_tipo = ttk.Combobox(
            filtros,
            values=[
                "Todos",
                "Mayor de edad",
                "Menor de edad"
            ],
            state="readonly",
            width=20
        )
        self.filtro_tipo.set("Todos")
        self.filtro_tipo.pack(side="left", padx=5)

        self.filtro_tipo.bind(
            "<<ComboboxSelected>>",
            lambda evento: self.__mostrar_visitantes()
        )

        ttk.Button(
            filtros,
            text="Actualizar tabla",
            command=self.__mostrar_visitantes
        ).pack(side="left", padx=5)

        ttk.Button(
            filtros,
            text="Buscar por documento",
            command=self.__ventana_busqueda
        ).pack(side="left", padx=5)

        # Tabla de visitantes.
        marco_tabla = ttk.Frame(self.pestana_visitantes)
        marco_tabla.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columnas = (
            "documento",
            "nombre",
            "edad",
            "tipo",
            "precio"
        )

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings"
        )

        self.tabla.heading("documento", text="Documento")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("edad", text="Edad")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("precio", text="Precio")

        self.tabla.column("documento", width=120)
        self.tabla.column("nombre", width=180)
        self.tabla.column("edad", width=60)
        self.tabla.column("tipo", width=130)
        self.tabla.column("precio", width=100)


