# ==========================================================
# Software FJ - Clase Reserva
# Autor: Erick Mosquera Colorado
# ==========================================================
# Une un cliente, un servicio, la cantidad (horas o dias) y un estado.
# Estados posibles: "Pendiente", "Confirmada", "Cancelada", "Pagada"
#
#   Pendiente --confirmar()--> Confirmada --procesar()--> Pagada
#       |                          |
#       +-------cancelar()---------+--> Cancelada

from entidad import Entidad
from cliente import Cliente
from servicios import Servicio
from registro import escribir_log
from excepciones import (ReservaError, ServicioNoDisponibleError,
                         OperacionNoPermitidaError, CalculoError, DatoInvalidoError)


class Reserva(Entidad):

    def __init__(self, cliente, servicio, cantidad):
        if not isinstance(cliente, Cliente):
            raise ReservaError("La reserva necesita un cliente.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("La reserva necesita un servicio.")
        if not servicio.esta_disponible():
            raise ServicioNoDisponibleError(f"El servicio '{servicio.get_nombre()}' no esta disponible.")

        # Cada servicio revisa la cantidad a su manera (polimorfismo)
        servicio.validar_parametros(cantidad)

        self.__cliente = cliente
        self.__servicio = servicio
        self.__cantidad = cantidad
        self.__estado = "Pendiente"
        self.__total = 0
        super().__init__()   # se le da id solo si la reserva es valida

    def get_estado(self):
        return self.__estado

    def get_total(self):
        return self.__total

    # ------------------------------------------------------
    # CONFIRMAR
    # ------------------------------------------------------
    def confirmar(self):
        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(
                f"La reserva #{self.get_id()} no se puede confirmar, esta {self.__estado}.")
        if not self.__servicio.esta_disponible():
            raise ServicioNoDisponibleError(
                f"El servicio '{self.__servicio.get_nombre()}' ya no esta disponible.")
        self.__estado = "Confirmada"
        escribir_log("EVENTO", f"Reserva #{self.get_id()} confirmada.")

    # ------------------------------------------------------
    # CANCELAR
    # ------------------------------------------------------
    def cancelar(self):
        if self.__estado == "Pagada" or self.__estado == "Cancelada":
            raise OperacionNoPermitidaError(
                f"La reserva #{self.get_id()} no se puede cancelar, esta {self.__estado}.")
        self.__estado = "Cancelada"
        escribir_log("EVENTO", f"Reserva #{self.get_id()} cancelada.")

    # ------------------------------------------------------
    # PROCESAR (cobrar) -> usa try / except / finally
    #                      y ENCADENAMIENTO (raise ... from e)
    # ------------------------------------------------------
    def procesar(self, con_iva=True, descuento=0):
        if self.__estado != "Confirmada":
            raise OperacionNoPermitidaError(
                f"La reserva #{self.get_id()} debe estar confirmada para procesarla.")

        try:
            self.__total = self.__servicio.calcular_total(self.__cantidad, con_iva, descuento)
            self.__estado = "Pagada"
            escribir_log("EVENTO", f"Reserva #{self.get_id()} pagada por ${self.__total:,.2f}")
        except (CalculoError, DatoInvalidoError) as e:
            # Encadenamiento: se lanza un error nuevo, pero se guarda la causa (e)
            raise ReservaError(f"No se pudo procesar la reserva #{self.get_id()}.") from e
        finally:
            # Esto se ejecuta SIEMPRE, haya error o no
            escribir_log("EVENTO", f"Fin del proceso de la reserva #{self.get_id()}. "
                                   f"Estado: {self.__estado}")

    def mostrar_datos(self):
        return (f"Reserva #{self.get_id()}: {self.__cliente.get_nombre()} - "
                f"{self.__servicio.get_nombre()} x {self.__cantidad} - "
                f"{self.__estado} - Total: ${self.__total:,.2f}")
