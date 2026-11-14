from parque import ParqueBotanico
from backend import BackendExcel
from interfaz import InterfazGrafica


parque = ParqueBotanico(
    "Jardín Botánico",
    precio_mayor=50000,
    precio_menor=20000
)

backend = BackendExcel("datos/visitantes.xlsx")

aplicacion = InterfazGrafica(parque, backend)

aplicacion.iniciar()

print("hola")
