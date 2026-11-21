# ==========================================================
# Software FJ - Clase Cliente
# Autor: Erick Mosquera Colorado
# ==========================================================
# Los datos son privados (doble guion bajo) y solo se cambian
# con los metodos set_..., que validan antes de guardar.

from entidad import Entidad
from excepciones import DatoInvalidoError


class Cliente(Entidad):

    def __init__(self, nombre, cedula, correo, telefono):
        self.set_nombre(nombre)
        self.set_cedula(cedula)
        self.set_correo(correo)
        self.set_telefono(telefono)
        super().__init__()   # se le da id solo si todos los datos estan bien

    # ---------------- nombre ----------------
    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        if nombre is None or str(nombre).strip() == "":
            raise DatoInvalidoError("El nombre del cliente es obligatorio.")
        nombre = str(nombre).strip()
        if not nombre.replace(" ", "").isalpha():
            raise DatoInvalidoError(f"El nombre '{nombre}' solo debe tener letras.")
        self.__nombre = nombre

    # ---------------- cedula ----------------
    def get_cedula(self):
        return self.__cedula

    def set_cedula(self, cedula):
        cedula = str(cedula).strip()
        if not cedula.isdigit():
            raise DatoInvalidoError(f"La cedula '{cedula}' solo debe tener numeros.")
        if len(cedula) < 6 or len(cedula) > 10:
            raise DatoInvalidoError("La cedula debe tener entre 6 y 10 digitos.")
        self.__cedula = cedula

    # ---------------- correo ----------------
    def get_correo(self):
        return self.__correo

    def set_correo(self, correo):
        correo = str(correo).strip()
        if "@" not in correo or "." not in correo.split("@")[-1]:
            raise DatoInvalidoError(f"El correo '{correo}' no es valido.")
        self.__correo = correo

    # ---------------- telefono ----------------
    def get_telefono(self):
        return self.__telefono

    def set_telefono(self, telefono):
        telefono = str(telefono).strip()
        if not telefono.isdigit() or len(telefono) != 10:
            raise DatoInvalidoError(f"El telefono '{telefono}' debe tener 10 numeros.")
        self.__telefono = telefono

    # ---------------- metodo de Entidad ----------------
    def mostrar_datos(self):
        return (f"Cliente #{self.get_id()}: {self.__nombre} - C.C. {self.__cedula} - "
                f"{self.__correo} - Tel. {self.__telefono}")
