# ==========================================================
# Software FJ - Excepciones personalizadas
# Autor: Erick Mosquera Colorado
# ==========================================================
# Todas heredan de ErrorSistema, asi en el main se pueden
# capturar todas con un solo "except ErrorSistema".


class ErrorSistema(Exception):
    """Error general del sistema Software FJ."""
    pass


class DatoInvalidoError(ErrorSistema):
    """Un dato esta vacio, mal escrito o fuera de rango."""
    pass


class ServicioNoDisponibleError(ErrorSistema):
    """Se quiere reservar un servicio que no esta disponible."""
    pass


class OperacionNoPermitidaError(ErrorSistema):
    """La accion no se puede hacer en el estado actual de la reserva."""
    pass


class CalculoError(ErrorSistema):
    """El calculo del costo no tiene sentido."""
    pass


class ReservaError(ErrorSistema):
    """La reserva no se pudo crear o procesar."""
    pass
