from models.ticket import Ticket, Comprador
from database.connection import DatabaseConnection
from bson import ObjectId
from datetime import datetime

class TicketService:
    def __init__(self):
        self.db = DatabaseConnection().get_db()
        self.tickets_collection = self.db['tickets']
        self.eventos_collection = self.db['eventos']
    
    def comprar_ticket(self, evento_id: str, tipo_ticket: str, comprador: Comprador) -> dict:
        # Verificar disponibilidad
        try:
            evento = self.eventos_collection.find_one({
            "_id": ObjectId(evento_id),
            "tiposTicket.nombre": tipo_ticket,
            "estado": "activo"
            })
            
            if not evento:
                return {"error": "Evento no encontrado o no activo"}
            
            tipo_ticket_info = next(
            (t for t in evento['tiposTicket'] if t['nombre'] == tipo_ticket), 
            None
            )
            
            if not tipo_ticket_info:
                return {"error": "Tipo de ticket no válido"}
            
            if tipo_ticket_info['vendidos'] >= tipo_ticket_info['cantidad']:
                return {"error": "No hay tickets disponibles para este tipo"}
            
            # Crear ticket
            nuevo_ticket = Ticket(
            eventoId=ObjectId(evento_id),
            comprador=comprador,
            tipoTicket=tipo_ticket,
            precio=tipo_ticket_info['precio']
            )

            # Insertar ticket y actualizar contador SIN transacción
            ticket_result = self.tickets_collection.insert_one(nuevo_ticket.to_dict())
            self.eventos_collection.update_one(
            {"_id": ObjectId(evento_id), "tiposTicket.nombre": tipo_ticket},
            {"$inc": {"tiposTicket.$.vendidos": 1}}
            )

            return {
            "ticket_id": str(ticket_result.inserted_id),
            "codigoQR": nuevo_ticket.codigoQR,
            "mensaje": "Compra exitosa"
            }
        except Exception as e:
            return {"error": f"Ocurrió un error al comprar el ticket: {str(e)}"}
        
    def validar_ticket(self, codigo_qr: str) -> dict:
        ticket = self.tickets_collection.find_one({"codigoQR": codigo_qr})
        if not ticket:
            return {"valido": False, "mensaje": "Ticket no encontrado"}
            
        if ticket['usado']:
            return {"valido": False, "mensaje": "Ticket ya utilizado"}
        
        # Marcar como usado
        self.tickets_collection.update_one(
            {"_id": ticket['_id']},
            {"$set": {"usado": True, "fechaUso": datetime.now()}}
        )
        
        evento = self.eventos_collection.find_one({"_id": ticket['eventoId']})
        
        return {
            "valido": True,
            "mensaje": "Ticket válido",
            "evento": evento['nombre'],
            "tipo": ticket['tipoTicket'],
            "comprador": ticket['comprador']['nombre']
        }
        
    def anular_ticket(self, ticket_id: str) -> bool:
        result = self.tickets_collection.delete_one({"_id": ObjectId(ticket_id)})
        return result.deleted_count > 0

    def obtener_todos_tickets(self) -> list:
        return list(self.tickets_collection.find())

    def obtener_ticket_por_id(self, ticket_id: str) -> dict:
        return self.tickets_collection.find_one({"_id": ObjectId(ticket_id)})

    def actualizar_ticket(self, ticket_id: str, datos_actualizados: dict) -> bool:
        result = self.tickets_collection.update_one(
            {"_id": ObjectId(ticket_id)},
            {"$set": datos_actualizados}
        )
        return result.modified_count > 0

    def eliminar_ticket(self, ticket_id: str) -> bool:
        result = self.tickets_collection.delete_one({"_id": ObjectId(ticket_id)})
        return result.deleted_count > 0