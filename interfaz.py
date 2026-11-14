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

        barra = ttk.Scrollbar(
            marco_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(yscrollcommand=barra.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.tabla.bind(
            "<Double-1>",
            self.__mostrar_detalles
        )

        botones = ttk.Frame(self.pestana_visitantes)
        botones.pack(pady=5)

        ttk.Button(
            botones,
            text="Eliminar seleccionado",
            command=self.__eliminar_visitante
        ).pack(side="left", padx=5)

        ttk.Button(
            botones,
            text="Editar seleccionado",
            command=self.__ventana_edicion
        ).pack(side="left", padx=5)

    def __crear_pestana_reportes(self):

        marco = ttk.LabelFrame(
            self.pestana_reportes,
            text="Resumen del parque",
            padding=20
        )
        marco.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.etiqueta_cantidad = ttk.Label(
            marco,
            text="Cantidad de visitantes: 0",
            font=("Arial", 13)
        )
        self.etiqueta_cantidad.pack(pady=10)

        self.etiqueta_recaudacion = ttk.Label(
            marco,
            text="Recaudación total: $0",
            font=("Arial", 13)
        )
        self.etiqueta_recaudacion.pack(pady=10)

        ttk.Button(
            marco,
            text="Actualizar reportes",
            command=self.__actualizar_reportes
        ).pack(pady=10)

    def __registrar_visitante(self):

        documento = self.entrada_documento.get().strip()
        nombre = self.entrada_nombre.get().strip()
        edad_texto = self.entrada_edad.get().strip()

        try:

            if not documento or not nombre or not edad_texto:
                raise ValueError(
                    "Todos los campos son obligatorios."
                )

            edad = int(edad_texto)

            if edad <= 0:
                raise ValueError(
                    "La edad debe ser mayor que cero."
                )

            tipo_seleccionado = self.tipo_visitante.get()

            if tipo_seleccionado == "Mayor de edad" and edad < 18:
                raise ValueError(
                    "La edad no corresponde a un mayor de edad."
                )

            if tipo_seleccionado == "Menor de edad" and edad >= 18:
                raise ValueError(
                    "La edad no corresponde a un menor de edad."
                )

            # Revisar duplicados directamente en Excel.
            if self.backend.buscar_por_documento(documento):
                raise ValueError(
                    "Ya existe un visitante con ese documento."
                )

            # Crear la boleta usando las clases de la primera parte.
            boleta = self.parque.registrar_visitante(
                documento,
                nombre,
                edad
            )

            visitante = {
                "documento": documento,
                "nombre": nombre,
                "edad": edad,
                "tipo": boleta.visitante.obtener_tipo(),
                "precio": boleta.calcular_total()
            }

            # Guardar permanentemente en Excel.
            self.backend.guardar_visitante(visitante)

            messagebox.showinfo(
                "Registro exitoso",
                boleta.mostrar_boleta()
            )

            self.__limpiar_campos()
            self.__mostrar_visitantes()

        except ValueError as error:

            messagebox.showerror(
                "Error de registro",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudo registrar el visitante:\n{error}"
            )

    def __limpiar_campos(self):

        self.entrada_documento.delete(0, tk.END)
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_edad.delete(0, tk.END)

        self.tipo_visitante.set("Automático")

    def __mostrar_visitantes(self):

        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        visitantes = self.backend.obtener_todos()

        filtro = self.filtro_tipo.get()

        for visitante in visitantes:

            if filtro != "Todos" and visitante["tipo"] != filtro:
                continue

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    visitante["documento"],
                    visitante["nombre"],
                    visitante["edad"],
                    visitante["tipo"],
                    f"${visitante['precio']:,.0f}"
                )
            )

        self.__actualizar_reportes()

    def __actualizar_reportes(self):

        cantidad = self.backend.cantidad_visitantes()
        recaudacion = self.backend.calcular_recaudacion()

        self.etiqueta_cantidad.config(
            text=f"Cantidad de visitantes: {cantidad}"
        )

        self.etiqueta_recaudacion.config(
            text=f"Recaudación total: ${recaudacion:,.0f}"
        )

    def __obtener_documento_seleccionado(self):

        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selección",
                "Primero selecciona un visitante de la tabla."
            )
            return None

        valores = self.tabla.item(seleccion[0], "values")

        return str(valores[0])

    def __mostrar_detalles(self, evento):

        documento = self.__obtener_documento_seleccionado()

        if documento is None:
            return

        visitante = self.backend.buscar_por_documento(documento)

        if visitante:

            messagebox.showinfo(
                "Detalles del visitante",
                f"Documento: {visitante['documento']}\n"
                f"Nombre: {visitante['nombre']}\n"
                f"Edad: {visitante['edad']}\n"
                f"Tipo: {visitante['tipo']}\n"
                f"Precio: ${visitante['precio']:,.0f}"
            )

    def __ventana_busqueda(self):

        ventana = tk.Toplevel(self.ventana)
        ventana.title("Buscar visitante")
        ventana.geometry("350x180")
        ventana.transient(self.ventana)

        ttk.Label(
            ventana,
            text="Ingrese el documento:"
        ).pack(pady=10)

        entrada = ttk.Entry(ventana)
        entrada.pack(pady=5)

        def buscar():

            documento = entrada.get().strip()

            if not documento:
                messagebox.showwarning(
                    "Búsqueda",
                    "Escriba un documento."
                )
                return

            visitante = self.backend.buscar_por_documento(documento)

            if visitante:

                messagebox.showinfo(
                    "Visitante encontrado",
                    f"Nombre: {visitante['nombre']}\n"
                    f"Edad: {visitante['edad']}\n"
                    f"Tipo: {visitante['tipo']}\n"
                    f"Precio: ${visitante['precio']:,.0f}"
                )

            else:

                messagebox.showwarning(
                    "Sin resultados",
                    "No se encontró un visitante con ese documento."
                )

        ttk.Button(
            ventana,
            text="Buscar",
            command=buscar
        ).pack(pady=10)

    def __eliminar_visitante(self):

        documento = self.__obtener_documento_seleccionado()

        if documento is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Desea eliminar este visitante?"
        )

        if confirmar:

            try:

                self.backend.eliminar_visitante(documento)

                messagebox.showinfo(
                    "Eliminación",
                    "El visitante fue eliminado correctamente."
                )

                self.__mostrar_visitantes()

            except Exception as error:

                messagebox.showerror(
                    "Error",
                    str(error)
                )

    def __ventana_edicion(self):

        documento = self.__obtener_documento_seleccionado()

        if documento is None:
            return

        visitante = self.backend.buscar_por_documento(documento)

        if not visitante:
            messagebox.showerror(
                "Error",
                "No se encontró el visitante."
            )
            return

        ventana = tk.Toplevel(self.ventana)
        ventana.title("Editar visitante")
        ventana.geometry("350x300")
        ventana.transient(self.ventana)

        ttk.Label(ventana, text="Nombre:").pack(pady=5)

        entrada_nombre = ttk.Entry(ventana)
        entrada_nombre.pack()
        entrada_nombre.insert(0, visitante["nombre"])

        ttk.Label(ventana, text="Edad:").pack(pady=5)

        entrada_edad = ttk.Entry(ventana)
        entrada_edad.pack()
        entrada_edad.insert(0, str(visitante["edad"]))

        def guardar_cambios():

            try:

                nombre = entrada_nombre.get().strip()
                edad = int(entrada_edad.get().strip())


