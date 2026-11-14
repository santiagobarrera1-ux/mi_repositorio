import os
from openpyxl import Workbook, load_workbook


class BackendExcel:

    def __init__(self, ruta_archivo="datos/visitantes.xlsx"):

        self.__ruta_archivo = ruta_archivo

        carpeta = os.path.dirname(self.__ruta_archivo)

        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

        self.__crear_archivo()

    def __crear_archivo(self):

        if not os.path.exists(self.__ruta_archivo):

            libro = Workbook()
            hoja = libro.active
            hoja.title = "Visitantes"

            hoja.append([
                "Documento",
                "Nombre",
                "Edad",
                "Tipo",
                "Precio"
            ])

            libro.save(self.__ruta_archivo)
            libro.close()

    def obtener_todos(self):

        libro = load_workbook(self.__ruta_archivo)
        hoja = libro["Visitantes"]

        visitantes = []

        for fila in hoja.iter_rows(min_row=2, values_only=True):

            if fila[0] is not None:
                visitantes.append({
                    "documento": str(fila[0]),
                    "nombre": fila[1],
                    "edad": fila[2],
                    "tipo": fila[3],
                    "precio": fila[4]
                })

        libro.close()

        return visitantes

    def buscar_por_documento(self, documento):

        visitantes = self.obtener_todos()

        for visitante in visitantes:

            if visitante["documento"] == documento:
                return visitante

        return None


