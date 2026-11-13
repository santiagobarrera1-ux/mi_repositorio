
class Boleta:

    def __init__(self, visitante, precio):

        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        self.__visitante = visitante
        self.__precio = precio

    @property
    def visitante(self):
        return self.__visitante

    @property
    def precio(self):
        return self.__precio

    def calcular_total(self):
        return self.__precio

    def mostrar_boleta(self):
        return (
            "\n---------- BOLETA ----------\n"
            f"{self.__visitante.mostrar_datos()}\n"
            f"Tipo: {self.__visitante.obtener_tipo()}\n"
            f"Precio: ${self.calcular_total():,.0f}\n"
            "----------------------------"
        )
