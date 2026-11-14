from persona import Persona


class MayorEdad(Persona):

    def __init__(self, documento, nombre, edad):

        if edad < 18:
            raise ValueError(
                "El visitante debe tener 18 años o más."
            )

        super().__init__(documento, nombre, edad)

    def obtener_tipo(self):
        return "Mayor de edad"


class MenorEdad(Persona):

    def __init__(self, documento, nombre, edad):

        if edad >= 18:
            raise ValueError(
                "El visitante debe ser menor de 18 años."
            )

        super().__init__(documento, nombre, edad)

    def obtener_tipo(self):
        return "Menor de edad"
