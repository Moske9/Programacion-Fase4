# ==========================================================
# Software FJ - Clase abstracta Entidad
# Autor: Erick Mosquera Colorado
# ==========================================================
# Es la clase "padre" de Cliente, Servicio y Reserva.
# Le da a cada objeto un numero de id automatico.
# Cada tipo de clase lleva su propia cuenta:
# Cliente #1, Cliente #2... Reserva #1, Reserva #2...

from abc import ABC, abstractmethod


class Entidad(ABC):

    contadores = {}   # un contador por cada tipo de clase

    def __init__(self):
        # Las clases hijas llaman a este constructor DESPUES de validar,
        # asi un objeto con datos malos no gasta un numero.
        tipo = type(self).__name__
        Entidad.contadores[tipo] = Entidad.contadores.get(tipo, 0) + 1
        self._id = Entidad.contadores[tipo]

    def get_id(self):
        return self._id

    @abstractmethod
    def mostrar_datos(self):
        """Cada clase hija debe mostrar su informacion."""
        pass
