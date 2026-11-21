# ==========================================================
# Software FJ - Programa principal
# Autor: Erick Mosquera Colorado
# Curso: Programacion - Fase 4
# ==========================================================
# Simula 13 operaciones (unas correctas y otras con errores).
# Ningun error detiene el programa: todos se capturan, se
# muestran en pantalla y se guardan en "eventos.log".
#
# Cada operacion usa try / except / else:
#   try    -> se intenta la operacion
#   except -> si hay error, se muestra y se guarda en el log
#   else   -> solo si NO hubo error, se muestra el resultado

from cliente import Cliente
from servicios import Sala, Equipo, Asesoria
from reserva import Reserva
from registro import escribir_log
from excepciones import ErrorSistema, DatoInvalidoError

# ----------------------------------------------------------
# LISTAS INTERNAS (aqui se guarda todo, no hay base de datos)
# ----------------------------------------------------------
clientes = []
servicios = []
reservas = []

exitosas = 0
fallidas = 0


# ----------------------------------------------------------
# Funciones de apoyo
# ----------------------------------------------------------
def registrar_cliente(datos):
    """Crea un cliente a partir de un diccionario y lo agrega a la lista."""
    try:
        nuevo = Cliente(**datos)
    except TypeError as e:
        # Si falta un dato, Python lanza TypeError. Lo cambiamos por un
        # error nuestro, guardando la causa original (encadenamiento).
        raise DatoInvalidoError("Faltan datos para registrar el cliente.") from e

    for c in clientes:
        if c.get_cedula() == nuevo.get_cedula():
            raise DatoInvalidoError(f"Ya existe un cliente con la cedula {nuevo.get_cedula()}.")

    clientes.append(nuevo)
    escribir_log("EVENTO", f"Cliente registrado: {nuevo.get_nombre()}")
    return nuevo


def registrar_servicio(servicio):
    servicios.append(servicio)
    escribir_log("EVENTO", f"Servicio creado: {servicio.get_nombre()}")
    return servicio


def crear_reserva(cliente, servicio, cantidad):
    nueva = Reserva(cliente, servicio, cantidad)
    reservas.append(nueva)
    escribir_log("EVENTO", f"Reserva #{nueva.get_id()} creada para {cliente.get_nombre()}")
    return nueva


def bien(mensaje):
    global exitosas
    exitosas += 1
    print(f"   OK -> {mensaje}")


def mal(error):
    global fallidas
    fallidas += 1
    texto = f"{type(error).__name__}: {error}"
    print(f"   ERROR -> {texto}")
    # Si el error viene encadenado, tambien se muestra la causa
    if error.__cause__:
        causa = f"{type(error.__cause__).__name__}: {error.__cause__}"
        print(f"            Causa: {causa}")
        texto += f" | Causa: {causa}"
    escribir_log("ERROR", texto)


# ==========================================================
# SIMULACION
# ==========================================================
print("=" * 60)
print("   SOFTWARE FJ - SIMULACION DE OPERACIONES")
print("=" * 60)
escribir_log("EVENTO", "===== Inicio de la simulacion =====")

# Variables que se usan entre operaciones
carlos = None
sala = None
equipo = None
asesoria = None
reserva1 = None
reserva2 = None
reserva3 = None

# ---------------- Operacion 1 ----------------
print("\n1. Registrar cliente correcto")
try:
    carlos = registrar_cliente({"nombre": "Carlos Perez", "cedula": "1007654321",
                                "correo": "carlos@gmail.com", "telefono": "3124567890"})
except ErrorSistema as e:
    mal(e)
except Exception as e:   # cualquier error inesperado tampoco detiene el programa
    mal(e)
else:
    bien(carlos.mostrar_datos())

# ---------------- Operacion 2 ----------------
print("\n2. Registrar cliente con nombre que tiene numeros")
try:
    registrar_cliente({"nombre": "Juan123", "cedula": "1002003004",
                       "correo": "juan@gmail.com", "telefono": "3001112233"})
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien("Cliente registrado")

# ---------------- Operacion 3 ----------------
print("\n3. Registrar cliente sin telefono (falta un dato)")
try:
    registrar_cliente({"nombre": "Maria Lopez", "cedula": "52123456",
                       "correo": "maria@hotmail.com"})
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien("Cliente registrado")

# ---------------- Operacion 4 ----------------
print("\n4. Crear servicios correctos (sala, equipo y asesoria)")
try:
    sala = registrar_servicio(Sala("Sala Cali", 40000, 15))
    equipo = registrar_servicio(Equipo("Portatil", 30000, "HP"))
    asesoria = registrar_servicio(Asesoria("Asesoria Python", 70000, "programacion"))
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien("3 servicios creados")
    for s in servicios:
        print("      -", s.describir())

# ---------------- Operacion 5 ----------------
print("\n5. Crear un servicio con precio negativo")
try:
    registrar_servicio(Sala("Sala Mala", -5000, 10))
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien("Servicio creado")

# ---------------- Operacion 6 ----------------
print("\n6. Reserva correcta: sala por 3 horas, confirmar y pagar con IVA")
try:
    reserva1 = crear_reserva(carlos, sala, 3)
    reserva1.confirmar()
    reserva1.procesar(con_iva=True)
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien(reserva1.mostrar_datos())

# ---------------- Operacion 7 ----------------
print("\n7. Reservar la sala por 20 horas (fuera del limite)")
try:
    crear_reserva(carlos, sala, 20)
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien("Reserva creada")

# ---------------- Operacion 8 ----------------
print("\n8. Reservar un equipo que no esta disponible")
try:
    equipo.set_disponible(False)
    crear_reserva(carlos, equipo, 2)
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien("Reserva creada")
finally:
    equipo.set_disponible(True)   # se deja disponible otra vez, pase lo que pase

# ---------------- Operacion 9 ----------------
print("\n9. Cancelar una reserva que ya fue pagada")
try:
    reserva1.cancelar()
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien("Reserva cancelada")

# ---------------- Operacion 10 ----------------
print("\n10. Pagar una asesoria con descuento de 80 % (no permitido)")
try:
    reserva2 = crear_reserva(carlos, asesoria, 2)
    reserva2.confirmar()
    reserva2.procesar(con_iva=False, descuento=80)
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien(reserva2.mostrar_datos())

# ---------------- Operacion 11 ----------------
print("\n11. Pagar la misma asesoria con descuento de 10 % (correcto)")
try:
    reserva2.procesar(con_iva=False, descuento=10)
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien(reserva2.mostrar_datos())

# ---------------- Operacion 12 ----------------
print("\n12. Alquilar equipo 4 dias y cancelar antes de pagar")
try:
    reserva3 = crear_reserva(carlos, equipo, 4)
    reserva3.cancelar()
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien(reserva3.mostrar_datos())

# ---------------- Operacion 13 ----------------
print("\n13. Confirmar una reserva que ya esta cancelada")
try:
    reserva3.confirmar()
except ErrorSistema as e:
    mal(e)
except Exception as e:
    mal(e)
else:
    bien("Reserva confirmada")


# ==========================================================
# RESUMEN FINAL
# ==========================================================
print("\n" + "=" * 60)
print("   RESUMEN")
print("=" * 60)
print(f"Operaciones exitosas: {exitosas}")
print(f"Operaciones con error: {fallidas}")
print(f"Clientes registrados: {len(clientes)}")
print(f"Servicios creados: {len(servicios)}")
print(f"Reservas creadas: {len(reservas)}")
for r in reservas:
    print("   -", r.mostrar_datos())
print("\nEl programa termino sin detenerse. Ver el archivo eventos.log")
escribir_log("EVENTO", "===== Fin de la simulacion =====")
