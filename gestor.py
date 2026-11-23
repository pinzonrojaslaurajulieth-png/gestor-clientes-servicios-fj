"""
Módulo: gestor.py
Descripción: Gestor principal del sistema — administra clientes, servicios,
 reservas y escribe el registro de eventos en archivo de log
Autor: Laura Julieth Pinzon
Fecha: 22/11/2026
"""

from datetime import datetime
from entidades import Cliente
from servicios import Servicio
from reservas import Reserva

class GestorSistema:
    """Clase que centraliza toda la lógica de negocio y gestión de datos en memoria"""
    
    def __init__(self, archivo_log: str = "registro_eventos.log"):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self._prox_id_cliente = 1
        self._prox_id_reserva = 1
        self._archivo_log = archivo_log
    
    # ═══════════════════════════════════════════════════
    # MÓDULO: REGISTRO DE EVENTOS Y ERRORES (LOGS)
    # ═══════════════════════════════════════════════════
    def registrar_log(self, nivel: str, mensaje: str):
        """
        Registra eventos y errores en archivo de texto
        Usa bloque try/except/finally según requisito del Anexo 3
        """
        fecha = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        linea = f"[{fecha}] [{nivel.upper()}] {mensaje}\n"
        
        try:
            with open(self._archivo_log, "a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except Exception as error_archivo:
            print(f" No se pudo escribir en el archivo de registro: {error_archivo}")
        finally:
            # Este bloque siempre se ejecuta, haya error o no
            pass
    
    # ═══════════════════════════════════════════════════
    # MÓDULO: GESTIÓN DE CLIENTES
    # ═══════════════════════════════════════════════════
    def agregar_cliente(self, cliente: Cliente):
        """Agrega un nuevo cliente validado al sistema"""
        try:
            if not cliente.validar():
                self.registrar_log("warning", f"Datos inválidos para cliente: {cliente.nombre}")
                return False, "No se pudo registrar el cliente — datos inválidos"
            
            # Asignar ID automático
            cliente._identificador = self._prox_id_cliente
            self._clientes.append(cliente)
            self._prox_id_cliente += 1
            
            self.registrar_log("info", f"Cliente registrado: ID {cliente.identificador} — {cliente.nombre}")
            return True, f" Cliente registrado exitosamente con ID: {cliente.identificador}"
        
        except Exception as error:
            self.registrar_log("error", f"Error al registrar cliente: {str(error)}")
            return False, f" Error: {str(error)}"
    
    def buscar_cliente(self, identificador: int):
        """Busca un cliente por su ID"""
        return next((c for c in self._clientes if c.identificador == identificador), None)
    
    def listar_clientes(self):
        """Devuelve lista de todos los clientes registrados"""
        return self._clientes.copy()
    
    # ═══════════════════════════════════════════════════
    # MÓDULO: GESTIÓN DE SERVICIOS
    # ═══════════════════════════════════════════════════
    def agregar_servicio(self, servicio: Servicio):
        """Agrega un nuevo servicio al sistema evitando duplicados por código"""
        existe = self.buscar_servicio(servicio.codigo)
        
        if existe:
            self.registrar_log("error", f"Intento de duplicar servicio: {servicio.codigo}")
            return False, f" El servicio con código {servicio.codigo} ya existe"
        
        self._servicios.append(servicio)
        self.registrar_log("info", f"Servicio registrado: {servicio.codigo} — {servicio.nombre}")
        return True, f" Servicio {servicio.codigo} registrado correctamente"
    
    def buscar_servicio(self, codigo: str):
        """Busca un servicio por su código"""
        return next((s for s in self._servicios if s.codigo == codigo), None)
    
    def listar_servicios(self):
        """Devuelve lista de todos los servicios disponibles"""
        return self._servicios.copy()
    
    # ═══════════════════════════════════════════════════
    # MÓDULO: GESTIÓN DE RESERVAS
    # ═══════════════════════════════════════════════════
    def crear_reserva(self, cliente_id: int, servicio_codigo: str, duracion: int):
        """Crea una nueva reserva validando existencia de cliente y servicio"""
        try:
            cliente = self.buscar_cliente(cliente_id)
            servicio = self.buscar_servicio(servicio_codigo)
            
            if not cliente:
                raise ValueError(f"Cliente con ID {cliente_id} no encontrado en el sistema")
            if not servicio:
                raise ValueError(f"Servicio con código {servicio_codigo} no encontrado en el sistema")
            
            reserva = Reserva(self._prox_id_reserva, cliente, servicio, duracion)
            self._reservas.append(reserva)
            self._prox_id_reserva += 1
            
            self.registrar_log("info", f"Reserva creada: #{reserva.numero} — Cliente: {cliente.nombre} — Servicio: {servicio.nombre}")
            return True, reserva
        
        except Exception as error:
            self.registrar_log("error", f"Error creando reserva: {str(error)}")
            return False, f" No se pudo crear la reserva: {str(error)}"
    
    def listar_reservas(self):
        """Devuelve lista de todas las reservas del sistema"""
        return self._reservas.copy()
