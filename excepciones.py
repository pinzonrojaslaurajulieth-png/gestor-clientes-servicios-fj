"""
Módulo: excepciones.py
Descripción: Define excepciones personalizadas para el sistema de gestión
Autor: Laura Julieth Pinzon
Fecha: 22/11/2026
"""

class ErrorSistema(Exception):
    """Clase base para excepciones del sistema"""
    pass

class ErrorValidacion(ErrorSistema):
    """Se lanza cuando los datos de entrada no cumplen los requisitos"""
    pass

class ErrorCliente(ErrorSistema):
    """Se lanza ante operaciones inválidas con clientes"""
    pass

class ErrorServicio(ErrorSistema):
    """Se lanza ante problemas con disponibilidad o parámetros de servicios"""
    pass

class ErrorReserva(ErrorSistema):
    """Se lanza ante intentos de reserva incorrectos o cancelaciones inválidas"""
    pass
