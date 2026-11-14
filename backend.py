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

