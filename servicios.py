"""
Módulo: servicios.py
Descripción: Clase abstracta Servicio y tres servicios especializados
 Implementa herencia, polimorfismo y métodos sobrecargados
Autor: Laura Julieth Pinzon
Fecha: 22/11/2026
"""

from abc import ABC, abstractmethod
from excepciones import ErrorValidacion

# ═══════════════════════════════════════════════════
# Clase Abstracta Servicio
# ═══════════════════════════════════════════════════
class Servicio(ABC):
    """Clase abstracta base para todos los servicios ofrecidos por la empresa"""
    
    def __init__(self, codigo: str, nombre: str, precio_base: float, disponible: bool = True):
        self._codigo = codigo
        self._nombre = nombre
        self._precio_base = precio_base
        self._disponible = disponible
    
    # Métodos de acceso (solo lectura para algunos)
    @property
    def codigo(self):
        return self._codigo
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def precio_base(self):
        return self._precio_base
    
    @property
    def disponible(self):
        return self._disponible
    
    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = valor
    
    # ── Métodos abstractos (Polimorfismo) ──
    @abstractmethod
    def calcular_costo(self, duracion: int) -> float:
        """Calcula el costo según la duración — implementado en cada tipo de servicio"""
        pass
    
    @abstractmethod
    def describir(self) -> str:
        """Devuelve información completa del servicio"""
        pass
    
    # ── Método sobrecargado ──
    def calcular_costo_total(self, duracion: int, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Calcula el costo total con impuesto y descuento
        Sobrecarga: puede llamarse con 1, 2 o 3 parámetros
        """
        try:
            costo = self.calcular_costo(duracion)
            
            if impuesto < 0:
                raise ErrorValidacion("El impuesto no puede ser negativo")
            if descuento < 0 or descuento > 1:
                raise ErrorValidacion("El descuento debe estar entre 0 y 1")
            
            total = costo * (1 + impuesto) * (1 - descuento)
            return round(total, 2)
        
        except TypeError:
            raise ErrorValidacion("La duración debe ser un número entero")
    
    def __str__(self):
        return f"Servicio {self._codigo}: {self._nombre}"


# ═══════════════════════════════════════════════════
# Servicio 1: Reserva de Salas
# ═══════════════════════════════════════════════════
class ReservaSalas(Servicio):
    """Servicio de reserva de salas de reunión"""
    
    def __init__(self, codigo: str, nombre: str, precio_base: float, capacidad: int, disponible: bool = True):
        super().__init__(codigo, nombre, precio_base, disponible)
        self._capacidad = capacidad
    
    def calcular_costo(self, horas: int) -> float:
        """Costo calculado por horas de uso de la sala"""
        if horas <= 0:
            raise ErrorValidacion("Las horas de reserva deben ser un número positivo")
        return self._precio_base * horas
    
    def describir(self) -> str:
        estado = " Disponible" if self._disponible else " No disponible"
        return f" Reserva de Sala: {self._nombre} | Código: {self._codigo} | Capacidad: {self._capacidad} personas | Precio por hora: ${self._precio_base:,} | {estado}"


# ═══════════════════════════════════════════════════
# Servicio 2: Alquiler de Equipos
# ═══════════════════════════════════════════════════
class AlquilerEquipos(Servicio):
    """Servicio de alquiler de equipos tecnológicos"""
    
    def __init__(self, codigo: str, nombre: str, precio_base: float, tipo_equipo: str, disponible: bool = True):
        super().__init__(codigo, nombre, precio_base, disponible)
        self._tipo_equipo = tipo_equipo
    
    def calcular_costo(self, dias: int) -> float:
        """Costo calculado por días de alquiler"""
        if dias <= 0:
            raise ErrorValidacion("Los días de alquiler deben ser un número positivo")
        return self._precio_base * dias
    
    def describir(self) -> str:
        estado = " Disponible" if self._disponible else " No disponible"
        return f" Alquiler de Equipo: {self._nombre} | Código: {self._codigo} | Tipo: {self._tipo_equipo} | Precio por día: ${self._precio_base:,} | {estado}"


# ═══════════════════════════════════════════════════
# Servicio 3: Asesorías Especializadas
# ═══════════════════════════════════════════════════
class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría profesional especializada"""
    
    def __init__(self, codigo: str, nombre: str, precio_base: float, especialista: str, disponible: bool = True):
        super().__init__(codigo, nombre, precio_base, disponible)
        self._especialista = especialista
    
    def calcular_costo(self, horas: int) -> float:
        """Costo por hora — se cobra mínimo 1 hora aunque sea menos tiempo"""
        if horas <= 0:
            raise ErrorValidacion("Las horas de asesoría deben ser un número positivo")
        horas_cobro = max(horas, 1)
        return self._precio_base * horas_cobro
    
    def describir(self) -> str:
        estado = " Disponible" if self._disponible else " No disponible"
        return f" Asesoría Especializada: {self._nombre} | Código: {self._codigo} | Especialista: {self._especialista} | Precio por hora: ${self._precio_base:,} | {estado}"


# ─── PRUEBA DEL ARCHIVO ───
if __name__ == "__main__":
    print(" Probando archivo: servicios.py\n")
    
    try:
        # Crear instancias de cada servicio
        sala = ReservaSalas("SALA-01", "Sala de Conferencias Principal", 50000, 30)
        equipo = AlquilerEquipos("EQP-007", "Laptop de Diseño", 25000, "Portátil")
        asesoria = AsesoriaEspecializada("ASES-001", "Consultoría en Programación", 80000, "Ing. Carlos Pérez")
        
        # Mostrar descripciones (polimorfismo)
        print(sala.describir())
        print(equipo.describir())
        print(asesoria.describir())
        
        # Calcular costos
        print("\n Prueba de cálculo de costos:")
        print(f"Sala — 3 horas: ${sala.calcular_costo(3):,}")
        print(f"Equipo — 5 días: ${equipo.calcular_costo(5):,}")
        print(f"Asesoría — 2 horas: ${asesoria.calcular_costo(2):,}")
        
        # Método sobrecargado — con impuesto y descuento
        print(f"\n Sala — 4 horas + 19% impuesto + 10% descuento: "
              f"${sala.calcular_costo_total(4, impuesto=0.19, descuento=0.10):,}")
        
        # Prueba de error
        print("\n Intentando calcular costo con horas negativas...")
        sala.calcular_costo(-2)
        
    except ErrorValidacion as e:
        print(f" Error detectado correctamente: {e}")
    
    print("\n Archivo ejecutado sin problemas")
