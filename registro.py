class RegistroVisitas:

    def __init__(self):
        self.__boletas = []
        self.__visitantes = {}

    def registrar_boleta(self, boleta):

        documento = boleta.visitante.documento

        if documento in self.__visitantes:
            raise ValueError(
                "Ya existe un visitante con ese documento."
            )

        self.__boletas.append(boleta)
        self.__visitantes[documento] = boleta.visitante

    def buscar_visitante(self, documento):
        return self.__visitantes.get(documento)

    def obtener_visitantes(self):
        return list(self.__visitantes.values())

    def obtener_boletas(self):
        return list(self.__boletas)

    def calcular_recaudacion(self):
        return sum(
            boleta.calcular_total()
            for boleta in self.__boletas
        )

    def cantidad_visitantes(self):
        return len(self.__visitantes)

