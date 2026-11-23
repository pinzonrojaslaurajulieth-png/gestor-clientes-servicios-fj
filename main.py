"""
Archivo principal: Sistema Integral de Gestión — Software FJ
Curso: Programación — Código 213023 | UNAD — Fase 4
Autor: Laura Julieth Pinzon
Fecha: 22/11/2026
Ejecuta al menos 10 operaciones completas según requisitos del Anexo 3
"""

from gestor import GestorSistema
from entidades import Cliente
from servicios import ReservaSalas, AlquilerEquipos, AsesoriaEspecializada
from excepciones import ErrorValidacion, ErrorReserva, ErrorServicio

def encabezado(texto):
    print(f"\n{'═'*60}")
    print(f"  {texto}")
    print(f"{'═'*60}")

def main():
    print("\n" + "█"*60)
    print("█   SISTEMA INTEGRAL DE GESTIÓN — SOFTWARE FJ")
    print("█   Fase 4 — Programación 213023 — UNAD")
    print("█   Estudiante: Laura Julieth Pinzón")
    print("█"*60)
    
    gestor = GestorSistema()
    gestor.registrar_log("inicio", "=== Inicio de ejecución del sistema ===")
    
    # ══════════════════════════════════════════════════════════
    # OPERACIÓN 1: Registrar cliente VÁLIDO
    # ══════════════════════════════════════════════════════════
    encabezado("OPERACIÓN 1 — Registrar cliente válido")
    try:
        cliente1 = Cliente(0, "Laura Julieth Pinzón", "laura.pinzon@unad.edu.co", "3101234567")
        ok, msg = gestor.agregar_cliente(cliente1)
        print(msg)
    except Exception as e:
        print(f" {e}")
    
    # ══════════════════════════════════════════════════════════
    # OPERACIÓN 2: Registrar cliente INVÁLIDO (correo incorrecto)
    # ══════════════════════════════════════════════════════════
    encabezado("OPERACIÓN 2 — Registrar cliente con correo inválido")
    try:
        cliente2 = Cliente(0, "Juan Pérez", "correo.sin-arroba", "3209876543")
        ok, msg = gestor.agregar_cliente(cliente2)
        print(msg)
    except ErrorValidacion as e:
        print(f" Error controlado: {e}")
    
    # ══════════════════════════════════════════════════════════
    # OPERACIÓN 3: Crear servicio — Reserva de Sala
    # ══════════════════════════════════════════════════════════
    encabezado("OPERACIÓN 3 — Crear servicio: Reserva de Sala")
    sala = ReservaSalas("SALA-01", "Sala de Conferencias Principal", 50000, 30)
    ok, msg = gestor.agregar_servicio(sala)
    print(msg)
    print(sala.describir())
    
    # ══════════════════════════════════════════════════════════
    # OPERACIÓN 4: Crear servicio — Alquiler de Equipo
    # ══════════════════════════════════════════════════════════
    encabezado("OPERACIÓN 4 — Crear servicio: Alquiler de Equipos")
    equipo = AlquilerEquipos("EQP-001", "Laptop Diseño Gráfico", 35000, "Portátil Alta Gama")
    ok, msg = gestor.agregar_servicio(equipo)
    print(msg)
    print(equipo.describir())
    
    # ══════════════════════════════════════════════════════════
    # OPERACIÓN 5: Crear servicio — Asesoría Especializada
    # ══════════════════════════════════════════════════════════
    encabezado("OPERACIÓN 5 — Crear servicio: Asesoría Especializada")
    asesoria = AsesoriaEspecializada("ASES-001", "Consultoría en Desarrollo de Software", 95000, "Ing. María Gómez")
    ok, msg = gestor.agregar_servicio(asesoria)
    print(msg)
    print(asesoria.describir())
    
    # ══════════════════════════════════════════════════════════
    # OPERACIÓN 6: Intentar crear servicio DUPLICADO
    # ══════════════════════════════════════════════════════════
    encabezado("OPERACIÓN 6 — Intentar duplicar código de servicio")
    sala_duplicada = ReservaSalas("SALA-01", "Sala Pequeña", 25000, 10)
    ok, msg = gestor.agregar_servicio(sala_duplicada)
    print(msg)
    
    # ══════════════════════════════════════════════════════════
    # OPERACIÓN 7: Crear y confirmar reserva VÁLIDA
    # ══════════════════════════════════════════════════════════
    encabezado("OPERACIÓN 7 — Crear y confirmar reserva válida")
    ok, resultado = gestor.crear_reserva(1, "SALA-01", 3)
    if ok:
        reserva = resultado
        print(f" Reserva creada:\n{reserva}")
        ok_conf, msg_conf = reserva.confirmar(impuesto=0.19, descuento=0.05)
        print(msg_conf)
    else:
        print(resultado)
    
    # ══════════════════════════════════════════════════════════
    # OPERACIÓN 8: Reserva con cliente NO EXISTENTE
    # ══════════════════════════════════════════════════════════
    encabezado("OPERACIÓN 8 — Crear reserva con cliente inexistente")
    ok, resultado = gestor.crear_reserva(999, "SALA-01", 2)
    print(resultado)
    
    # ══════════════════════════════════════════════════════════
    # OPERACIÓN 9: Reserva con servicio NO DISPONIBLE
    # ══════════════════════════════════════════════════════════
    encabezado("OPERACIÓN 9 — Reserva sobre servicio no disponible")
    # Marcar servicio como no disponible
    sala.disponible = False
    ok, resultado = gestor.crear_reserva(1, "SALA-01", 4)
    if ok:
        try:
            resultado.confirmar()
        except ErrorServicio as e:
            print(f" Error controlado: {e}")
    else:
        print(resultado)
    # Restaurar disponibilidad
    sala.disponible = True
    
    # ══════════════════════════════════════════════════════════
    # OPERACIÓN 10: Cancelar reserva existente
    # ══════════════════════════════════════════════════════════
    encabezado("OPERACIÓN 10 — Cancelar reserva")
    ok, resultado = gestor.crear_reserva(1, "EQP-001", 5)
    if ok:
        reserva_nueva = resultado
        print(f" {reserva_nueva}")
        ok_cancel, msg_cancel = reserva_nueva.cancelar()
        print(msg_cancel)
        print(f" Estado final: {reserva_nueva.estado}")
    
    # ══════════════════════════════════════════════════════════
    # OPERACIÓN 11: Cálculo de costo con descuento e impuesto
    # ══════════════════════════════════════════════════════════
    encabezado("OPERACIÓN 11 — Cálculo de costo con impuesto y descuento")
    print(f"Asesoría — 4 horas | Base: $95.000/hora")
    print(f"Sin impuesto/descuento: ${asesoria.calcular_costo_total(4):,.2f}")
    print(f"+ 19% impuesto:          ${asesoria.calcular_costo_total(4, impuesto=0.19):,.2f}")
    print(f"+ 19% impuesto - 10% desc: ${asesoria.calcular_costo_total(4, 0.19, 0.10):,.2f}")
    
    # ══════════════════════════════════════════════════════════
    # RESUMEN FINAL
    # ══════════════════════════════════════════════════════════
    encabezado("RESUMEN DEL SISTEMA")
    print(f" Clientes registrados: {len(gestor.listar_clientes())}")
    print(f" Servicios disponibles: {len(gestor.listar_servicios())}")
    print(f" Reservas creadas:      {len(gestor.listar_reservas())}")
    print(f" Archivo de log:       registro_eventos.log")
    
    gestor.registrar_log("finalizacion", "=== Ejecución finalizada exitosamente ===")
    print("\n Sistema finalizado correctamente. Revisa el archivo 'registro_eventos.log'")
    print("█"*60)

if __name__ == "__main__":
    main()
