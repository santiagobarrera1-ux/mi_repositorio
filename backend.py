import os
from openpyxl import Workbook, load_workbook


class BackendExcel:

    def __init__(self, ruta_archivo="datos/visitantes.xlsx"):

        self.__ruta_archivo = ruta_archivo

        carpeta = os.path.dirname(self.__ruta_archivo)

        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

        self.__crear_archivo()


