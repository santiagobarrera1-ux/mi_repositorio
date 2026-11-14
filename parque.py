from visitante import MayorEdad, MenorEdad
from boleta import Boleta
from registro import RegistroVisitas


class ParqueBotanico:

    def __init__(self, nombre, precio_mayor, precio_menor):

        if precio_mayor < 0 or precio_menor < 0:
            raise ValueError(
                "Los precios no pueden ser negativos."
            )

        self.__nombre = nombre
        self.__precio_mayor = precio_mayor
        self.__precio_menor = precio_menor
        self.__registro = RegistroVisitas()

    @property
    def nombre(self):
        return self.__nombre

    def registrar_visitante(self, documento, nombre, edad):

        if edad >= 18:
            visitante = MayorEdad(documento, nombre, edad)
            precio = self.__precio_mayor
        else:
            visitante = MenorEdad(documento, nombre, edad)
            precio = self.__precio_menor

        boleta = Boleta(visitante, precio)

        self.__registro.registrar_boleta(boleta)

        return boleta

    def buscar_visitante(self, documento):
        return self.__registro.buscar_visitante(documento)

    def obtener_visitantes(self):
        return self.__registro.obtener_visitantes()

    def consultar_recaudacion(self):
        return self.__registro.calcular_recaudacion()

    def consultar_cantidad_visitantes(self):
        return self.__registro.cantidad_visitantes()
