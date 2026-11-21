# ==========================================================
# Software FJ - Servicios
# Autor: Erick Mosquera Colorado
# ==========================================================
# Servicio es una clase abstracta. De ella heredan:
#   - Sala      (se cobra por hora)
#   - Equipo    (se cobra por dia)
#   - Asesoria  (se cobra por hora)
#
# Cada hija escribe su propia version de:
#   calcular_costo(), describir() y validar_parametros()
# Eso es POLIMORFISMO: se llaman igual pero hacen cosas distintas.

from abc import abstractmethod
from entidad import Entidad
from excepciones import DatoInvalidoError, CalculoError


class Servicio(Entidad):

    def __init__(self, nombre, precio, disponible=True):
        if nombre is None or str(nombre).strip() == "":
            raise DatoInvalidoError("El servicio necesita un nombre.")
        if not isinstance(precio, (int, float)) or precio <= 0:
            raise DatoInvalidoError(f"El precio de '{nombre}' debe ser un numero mayor a 0.")
        self._nombre = nombre
        self._precio = precio
        self._disponible = disponible
        super().__init__()   # se le da id solo si los datos estan bien

    def get_nombre(self):
        return self._nombre

    def esta_disponible(self):
        return self._disponible

    def set_disponible(self, valor):
        self._disponible = valor

    # ------- metodos que cada servicio debe escribir -------
    @abstractmethod
    def calcular_costo(self, cantidad):
        pass

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self, cantidad):
        pass

    def mostrar_datos(self):
        return self.describir()

    # ---------------------------------------------------------
    # METODO "SOBRECARGADO"
    # Python no permite dos metodos con el mismo nombre, por eso
    # se usan parametros con valor por defecto. Asi el mismo metodo
    # se puede llamar de varias formas:
    #   calcular_total(3)                     -> solo el costo
    #   calcular_total(3, True)               -> con IVA del 19 %
    #   calcular_total(3, False, 10)          -> con 10 % de descuento
    #   calcular_total(3, True, 10)           -> con IVA y descuento
    # ---------------------------------------------------------
    def calcular_total(self, cantidad, con_iva=False, descuento=0):
        if descuento < 0 or descuento > 50:
            raise CalculoError(f"El descuento debe estar entre 0 y 50 %. Se pidio {descuento} %.")

        total = self.calcular_costo(cantidad)
        total = total - (total * descuento / 100)
        if con_iva:
            total = total * 1.19

        if total <= 0:
            raise CalculoError("El total calculado no puede ser 0 o negativo.")
        return round(total, 2)


# ==========================================================
# SERVICIO 1: SALA
# ==========================================================
class Sala(Servicio):

    def __init__(self, nombre, precio_hora, capacidad, disponible=True):
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser un numero mayor a 0.")
        self._capacidad = capacidad
        super().__init__(nombre, precio_hora, disponible)

    def validar_parametros(self, cantidad):
        # cantidad = horas. Se permite de 1 a 12 horas
        if not isinstance(cantidad, int) or cantidad < 1 or cantidad > 12:
            raise DatoInvalidoError("La sala se reserva por horas enteras, de 1 a 12.")

    def calcular_costo(self, cantidad):
        self.validar_parametros(cantidad)
        return self._precio * cantidad

    def describir(self):
        return (f"Sala '{self._nombre}' - {self._capacidad} personas - "
                f"${self._precio:,} la hora")


# ==========================================================
# SERVICIO 2: EQUIPO
# ==========================================================
class Equipo(Servicio):

    COSTO_ENTREGA = 15000   # valor fijo por llevar el equipo

    def __init__(self, nombre, precio_dia, marca, disponible=True):
        self._marca = marca
        super().__init__(nombre, precio_dia, disponible)

    def validar_parametros(self, cantidad):
        # cantidad = dias. Se permite de 1 a 15 dias
        if not isinstance(cantidad, int) or cantidad < 1 or cantidad > 15:
            raise DatoInvalidoError("El equipo se alquila de 1 a 15 dias.")

    def calcular_costo(self, cantidad):
        self.validar_parametros(cantidad)
        return self._precio * cantidad + Equipo.COSTO_ENTREGA

    def describir(self):
        return (f"Equipo '{self._nombre}' ({self._marca}) - "
                f"${self._precio:,} el dia + ${Equipo.COSTO_ENTREGA:,} de entrega")


# ==========================================================
# SERVICIO 3: ASESORIA
# ==========================================================
class Asesoria(Servicio):

    def __init__(self, nombre, precio_hora, tema, disponible=True):
        self._tema = tema
        super().__init__(nombre, precio_hora, disponible)

    def validar_parametros(self, cantidad):
        # cantidad = horas. Se permite de 1 a 5 horas
        if not isinstance(cantidad, int) or cantidad < 1 or cantidad > 5:
            raise DatoInvalidoError("La asesoria dura de 1 a 5 horas.")

    def calcular_costo(self, cantidad):
        self.validar_parametros(cantidad)
        costo = self._precio * cantidad
        # Desde 3 horas se hace un 5 % de rebaja
        if cantidad >= 3:
            costo = costo * 0.95
        return costo

    def describir(self):
        return (f"Asesoria '{self._nombre}' sobre {self._tema} - "
                f"${self._precio:,} la hora")
