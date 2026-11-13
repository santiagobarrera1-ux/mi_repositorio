
class Persona:

    def __init__(self, documento, nombre, edad):

        if not documento.strip():
            raise ValueError("El documento no puede estar vacío.")

        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if edad <= 0:
            raise ValueError("La edad debe ser mayor que cero.")

        self.__documento = documento
        self.__nombre = nombre
        self.__edad = edad

    @property
    def documento(self):
        return self.__documento

    @property
    def nombre(self):
        return self.__nombre

    @property
    def edad(self):
        return self.__edad

    def mostrar_datos(self):
        return (
            f"Documento: {self.documento}\n"
            f"Nombre: {self.nombre}\n"
            f"Edad: {self.edad}"
        )

    def obtener_tipo(self):
        raise NotImplementedError(
            "Este método debe ser implementado por las clases hijas."
        )
