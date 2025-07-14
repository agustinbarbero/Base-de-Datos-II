from services.evento_service import EventoService
from services.ticket_service import TicketService
from models.evento import Evento, TipoTicket
from models.ticket import Comprador
from utils.helpers import mostrar_evento, formatear_fecha, validar_object_id
from datetime import datetime
import json

def main():
    evento_service = EventoService()
    ticket_service = TicketService()
    
    while True:
        print("\n--- Plataforma de Eventos y Tickets ---")
        print("1. Crear evento")
        print("2. Ver eventos próximos")
        print("3. Comprar ticket")
        print("4. Validar ticket")
        print("5. Reporte de ventas")
        print("6. Listar todos los eventos")
        print("7. Actualizar evento")
        print("8. Eliminar evento")
        print("9. Eliminar ticket")
        print("10. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            # Crear evento
            nombre = input("Nombre del evento: ")
            descripcion = input("Descripción: ")
            fecha_str = input("Fecha (DD/MM/YYYY HH:MM): ")
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
            ubicacion = input("Ubicación: ")
            capacidad = int(input("Capacidad máxima: "))
            
            tipos_ticket = []
            while True:
                nombre_ticket = input("Nombre del tipo de ticket (o 'fin' para terminar): ")
                if nombre_ticket.lower() == 'fin':
                    break
                precio = float(input("Precio: "))
                cantidad = int(input("Cantidad disponible: "))
                tipos_ticket.append(TipoTicket(nombre_ticket, precio, cantidad))
            
            nuevo_evento = Evento(nombre, descripcion, fecha, ubicacion, capacidad, tipos_ticket)
            evento_id = evento_service.crear_evento(nuevo_evento)
            print(f"Evento creado con ID: {evento_id}")
            
        elif opcion == "2":
            # Eventos próximos
            eventos = evento_service.eventos_proximos()
            print("\n--- Eventos Próximos ---")
            for evento in eventos:
                mostrar_evento(evento)
                
        elif opcion == "3":
            # Comprar ticket
            evento_id = input("ID del evento: ")
            if not validar_object_id(evento_id):
                print("ID de evento no válido")
                continue
                
            evento = evento_service.obtener_evento_por_id(evento_id)
            if not evento:
                print("Evento no encontrado")
                continue
                
            mostrar_evento(evento)
            tipo_ticket = input("Tipo de ticket a comprar: ")
            
            nombre = input("Nombre del comprador: ")
            email = input("Email del comprador: ")
            comprador = Comprador(nombre, email)
            
            resultado = ticket_service.comprar_ticket(evento_id, tipo_ticket, comprador)
            print("\nResultado de la compra:")
            print(json.dumps(resultado, indent=2))
            
        elif opcion == "4":
            # Validar ticket
            codigo_qr = input("Ingrese el código QR del ticket: ")
            resultado = ticket_service.validar_ticket(codigo_qr)
            print("\nResultado de validación:")
            print(json.dumps(resultado, indent=2))
            
        elif opcion == "5":
            # Reporte de ventas
            evento_id = input("ID del evento: ")
            if not validar_object_id(evento_id):
                print("ID de evento no válido")
                continue
                
            reporte = evento_service.reporte_ventas(evento_id)
            if not reporte:
                print("Evento no encontrado")
                continue
                
            print("\n--- Reporte de Ventas ---")
            print(f"Evento: {reporte['evento']}")
            print(f"Total vendido: ${reporte['total_vendido']:.2f}")
            print(f"Total tickets vendidos: {reporte['total_tickets']}")
            print("\nDetalle por tipo de ticket:")
            for ticket in reporte['detalle_tickets']:
                print(f" - {ticket['nombre']}: Vendidos {ticket['vendidos']} de {ticket['cantidad']}")
                
        elif opcion == "6":
            # Listar todos los eventos
            eventos = evento_service.obtener_todos_eventos()
            print("\n--- Todos los eventos ---")
            for evento in eventos:
                print(evento)

        elif opcion == "7":
            # Actualizar evento
            evento_id = input("ID del evento a actualizar: ")
            campo = input("Campo a actualizar (nombre, descripcion, ubicacion, etc): ")
            valor = input("Nuevo valor: ")
            if evento_service.actualizar_evento(evento_id, {campo: valor}):
                print("Evento actualizado correctamente.")
            else:
                print("No se pudo actualizar el evento.")

        elif opcion == "8":
            # Eliminar evento
            evento_id = input("ID del evento a eliminar: ")
            if evento_service.eliminar_evento(evento_id):
                print("Evento eliminado correctamente.")
            else:
                print("No se pudo eliminar el evento.")

        elif opcion == "9":
            # Eliminar ticket
            ticket_id = input("ID del ticket a eliminar: ")
            if ticket_service.eliminar_ticket(ticket_id):
                print("Ticket eliminado correctamente.")
            else:
                print("No se pudo eliminar el ticket.")

        elif opcion == "10":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida, intente nuevamente")

if __name__ == "__main__":
    main()