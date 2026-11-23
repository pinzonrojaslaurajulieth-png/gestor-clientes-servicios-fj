"""
Módulo: reservas.py
Descripción: Clase Reserva — asocia Cliente con Servicio
Gestiona estados, confirmación, cancelación y manejo de excepciones
Autor: Laura Julieth Pinzon
Fecha: 22/11/2026
"""

from datetime import datetime
from entidades import Cliente
from servicios import Servicio
from excepciones import ErrorReserva, ErrorValidacion, ErrorServicio

class Reserva:
    """Representa una reserva realizada por un cliente sobre un servicio"""
    
    ESTADOS = {'PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'COMPLETADA'}
    
    def __init__(self, numero_reserva: int, cliente: Cliente, servicio: Servicio, 
                 duracion: int, fecha_solicitud=None):
        self._numero = numero_reserva
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = 'PENDIENTE'
        self._fecha = fecha_solicitud or datetime.now()
        self._costo_final = 0.0
    
    # Propiedades de solo lectura
    @property
    def numero(self): return self._numero
    @property
    def estado(self): return self._estado
    @property
    def cliente(self): return self._cliente
    @property
    def servicio(self): return self._servicio
    @property
    def duracion(self): return self._duracion
    @property
    def costo_final(self): return self._costo_final
    @property
    def fecha(self): return self._fecha
    
    def confirmar(self, impuesto: float = 0.0, descuento: float = 0.0):
        """
        Confirma la reserva, valida condiciones y calcula el costo final
        Implementa manejo de excepciones con encadenamiento
        """
        try:
            # Validación de estado
            if self._estado != 'PENDIENTE':
                raise ErrorReserva(f"No se puede confirmar: la reserva está en estado {self._estado}")
            
            # Validación de cliente
            if not self._cliente.esta_validado:
                raise ErrorReserva("No se puede reservar: el cliente no ha sido validado")
            
            # Validación de disponibilidad del servicio
            if not self._servicio.disponible:
                raise ErrorServicio(f"El servicio {self._servicio.codigo} no está disponible actualmente")
            
            # Validación de duración
            if self._duracion <= 0:
                raise ErrorValidacion("La duración debe ser mayor a cero")
            
            # Cálculo del costo final
            self._costo_final = self._servicio.calcular_costo_total(self._duracion, impuesto, descuento)
            self._estado = 'CONFIRMADA'
            return True, f" Reserva #{self._numero} CONFIRMADA | Costo final: ${self._costo_final:,}"
        
        except ErrorReserva:
            self._estado = 'CANCELADA'
            raise  # Re-lanza la excepción preservando el contexto
        except Exception as e:
            self._estado = 'CANCELADA'
            raise ErrorReserva(f"Fallo inesperado en la reserva #{self._numero}") from e
    
    def cancelar(self):
        """Cancela la reserva si está en un estado permitido"""
        try:
            if self._estado == 'COMPLETADA':
                raise ErrorReserva("No se puede cancelar una reserva ya completada")
            
            if self._estado in ['PENDIENTE', 'CONFIRMADA']:
                self._estado = 'CANCELADA'
                return True, f" Reserva #{self._numero} CANCELADA exitosamente"
            
            return False, f" No se puede cancelar reserva #{self._numero}: estado actual es {self._estado}"
        
        except ErrorReserva:
            raise
        except Exception as e:
            raise ErrorReserva(f"Error al intentar cancelar: {str(e)}") from e
    
    def completar(self):
        """Marca la reserva como completada"""
        if self._estado == 'CONFIRMADA':
            self._estado = 'COMPLETADA'
            return f" Reserva #{self._numero} COMPLETADA"
        return f" No se puede completar reserva #{self._numero}: debe estar confirmada"
    
    def __str__(self):
        return (f" Reserva #{self._numero} | Servicio: {self._servicio.nombre} | "
                f"Cliente: {self._cliente.nombre} | Estado: {self._estado} | "
                f"Fecha: {self._fecha.strftime('%d/%m/%Y %H:%M')}")


# ─── PRUEBA DEL ARCHIVO ───
if __name__ == "__main__":
    print(" Probando archivo: reservas.py\n")
    
    from entidades import Cliente
    from servicios import ReservaSalas
    
    try:
        # 1. Crear y validar cliente
        cliente = Cliente(0, "Laura Pinzón", "laura@ejemplo.com", "3101234567")
        cliente.validar()
        print(f" Cliente validado: {cliente.nombre}")
        
        # 2. Crear servicio
        sala = ReservaSalas("SALA-02", "Sala de Reuniones", 40000, 15)
        print(f" Servicio creado: {sala.nombre}\n")
        
        # 3. Crear reserva
        reserva = Reserva(1, cliente, sala, 3)
        print(f" Reserva creada:\n{reserva}\n")
        
        # 4. Confirmar reserva con impuesto
        ok, mensaje = reserva.confirmar(impuesto=0.19)
        print(mensaje)
        print(f" Estado actual: {reserva.estado} | Costo: ${reserva.costo_final:,}\n")
        
        # 5. Intentar confirmar de nuevo (debe fallar)
        print(" Intentando confirmar la misma reserva por segunda vez...")
        reserva.confirmar()
        
    except ErrorReserva as e:
        print(f" Error controlado: {e}")
    
    print("\n Archivo ejecutado sin problemas")
