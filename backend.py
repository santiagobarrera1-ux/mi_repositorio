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

    def guardar_visitante(self, visitante):

        if self.buscar_por_documento(
            visitante["documento"]
        ):
            raise ValueError(
                "Ya existe un visitante con ese documento."
            )

        libro = load_workbook(self.__ruta_archivo)
        hoja = libro["Visitantes"]

        hoja.append([
            visitante["documento"],
            visitante["nombre"],
            visitante["edad"],
            visitante["tipo"],
            visitante["precio"]
        ])

        libro.save(self.__ruta_archivo)
        libro.close()

    def actualizar_visitante(self, documento, nuevos_datos):

        libro = load_workbook(self.__ruta_archivo)
        hoja = libro["Visitantes"]

        encontrado = False

        for fila in range(2, hoja.max_row + 1):

            documento_actual = str(
                hoja.cell(fila, 1).value
            )

            if documento_actual == documento:

                hoja.cell(fila, 2).value = nuevos_datos["nombre"]
                hoja.cell(fila, 3).value = nuevos_datos["edad"]
                hoja.cell(fila, 4).value = nuevos_datos["tipo"]
                hoja.cell(fila, 5).value = nuevos_datos["precio"]

                encontrado = True
                break

        libro.save(self.__ruta_archivo)
        libro.close()

        if not encontrado:
            raise ValueError("No se encontró el visitante.")

    def eliminar_visitante(self, documento):

        libro = load_workbook(self.__ruta_archivo)
        hoja = libro["Visitantes"]

        encontrado = False

        for fila in range(2, hoja.max_row + 1):

            documento_actual = str(
                hoja.cell(fila, 1).value
            )

            if documento_actual == documento:

                hoja.delete_rows(fila, 1)
                encontrado = True
                break

        libro.save(self.__ruta_archivo)
        libro.close()

        if not encontrado:
            raise ValueError("No se encontró el visitante.")


