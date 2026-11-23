"""
Módulo: entidades.py
Descripción: Clase abstracta Entidad y clase Cliente con encapsulación
Autor: Laura Julieth Pinzon
Fecha: 22/11/2026
"""

from abc import ABC, abstractmethod
from excepciones import ErrorValidacion
import re

class Entidad(ABC):
    """Clase abstracta que representa una entidad general del sistema"""
    
    def __init__(self, identificador: int, nombre: str):
        self._identificador = identificador
        self._nombre = nombre
    
    @property
    def identificador(self):
        return self._identificador
    
    @property
    def nombre(self):
        return self._nombre
    
    @abstractmethod
    def describir(self) -> str:
        """Método abstracto: cada entidad debe implementar su descripción"""
        pass
    
    @abstractmethod
    def validar(self) -> bool:
        """Método abstracto para validación de datos"""
        pass


class Cliente(Entidad):
    """Clase que representa a un cliente con validaciones estrictas"""
    
    def __init__(self, identificador: int, nombre: str, correo: str, telefono: str = ""):
        super().__init__(identificador, nombre)
        self._correo = correo
        self._telefono = telefono
        self._validado = False
    
    # Propiedades con acceso controlado (encapsulación)
    @property
    def correo(self):
        return self._correo
    
    @property
    def telefono(self):
        return self._telefono
    
    @property
    def esta_validado(self):
        return self._validado
    
    def validar(self) -> bool:
        """Valida que los datos del cliente sean correctos"""
        try:
            if not isinstance(self._identificador, int) or self._identificador <= 0:
                raise ErrorValidacion(f"ID inválido: {self._identificador}. Debe ser un número positivo.")
            
            if len(self._nombre.strip()) < 2:
                raise ErrorValidacion("El nombre debe tener al menos 2 caracteres.")
            
            patron_correo = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(patron_correo, self._correo):
                raise ErrorValidacion(f"Formato de correo inválido: {self._correo}")
            
            self._validado = True
            return True
        
        except ErrorValidacion:
            raise  # Re-lanzamos la excepción
        except Exception as e:
            raise ErrorValidacion(f"Error inesperado al validar cliente: {str(e)}") from e
    
    def describir(self) -> str:
        """Devuelve información completa del cliente"""
        return f"Cliente #{self._identificador}: {self._nombre} | Correo: {self._correo} | Teléfono: {self._telefono or 'No registrado'}"
    
    def __str__(self):
        return f"Cliente: {self._nombre} (ID: {self._identificador})"


# ─── PRUEBA DEL ARCHIVO ───
if __name__ == "__main__":
    print(" Probando archivo: entidades.py")
    
    try:
        # Cliente válido
        cliente1 = Cliente(1, "María López", "maria@ejemplo.com", "3101234567")
        if cliente1.validar():
            print(f" Cliente válido: {cliente1.describir()}")
        
        # Cliente con correo inválido (debe lanzar error)
        print("\n Intentando crear cliente con correo inválido...")
        cliente2 = Cliente(2, "Juan Pérez", "correo-invalido", "3209876543")
        cliente2.validar()
        
    except ErrorValidacion as e:
        print(f" Error detectado correctamente: {e}")
    
    print("\n Archivo ejecutado sin problemas")
