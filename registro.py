# ==========================================================
# Software FJ - Archivo de registro (log)
# Autor: Erick Mosquera Colorado
# ==========================================================
# Guarda los eventos y errores en el archivo "eventos.log".
# Se usa open() en modo "a" (agregar), asi no se borra lo anterior.

from datetime import datetime

ARCHIVO_LOG = "eventos.log"


def escribir_log(tipo, mensaje):
    """Escribe una linea en el archivo de log.
    tipo puede ser: "EVENTO" o "ERROR"."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{fecha}] {tipo}: {mensaje}\n")
    except OSError:
        # Si no se puede escribir el archivo, el programa sigue igual
        print("  (No se pudo escribir en el archivo de log)")
