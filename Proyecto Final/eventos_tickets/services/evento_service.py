from models.evento import Evento, TipoTicket
from database.connection import DatabaseConnection
from bson import ObjectId
from datetime import datetime

class EventoService:
    def __init__(self):
        self.db = DatabaseConnection().get_db()
        self.eventos_collection = self.db['eventos']
        self.tickets_collection = self.db['tickets']
    
    def crear_evento(self, evento: Evento) -> ObjectId:
        result = self.eventos_collection.insert_one(evento.to_dict())
        return result.inserted_id
    
    def obtener_evento_por_id(self, evento_id: str) -> dict:
        return self.eventos_collection.find_one({"_id": ObjectId(evento_id)})
    
    def eventos_proximos(self) -> list:
        ahora = datetime.now()
        return list(self.eventos_collection.find({
            "fecha": {"$gte": ahora},
            "estado": "activo"
        }).sort("fecha", 1))
    
    def reporte_ventas(self, evento_id: str) -> dict:
        evento = self.obtener_evento_por_id(evento_id)
        if not evento:
            return None
            
        total_vendido = sum(t['precio'] * t['vendidos'] for t in evento['tiposTicket'])
        total_tickets = sum(t['vendidos'] for t in evento['tiposTicket'])
        
        return {
            "evento": evento['nombre'],
            "total_vendido": total_vendido,
            "total_tickets": total_tickets,
            "detalle_tickets": evento['tiposTicket']
        }
    
    def actualizar_tickets_vendidos(self, evento_id: str, tipo_ticket: str) -> bool:
        return self.eventos_collection.update_one(
            {"_id": ObjectId(evento_id), "tiposTicket.nombre": tipo_ticket},
            {"$inc": {"tiposTicket.$.vendidos": 1}}
        ).modified_count > 0
        
    def cancelar_evento(self, evento_id: str) -> bool:
        result = self.eventos_collection.update_one(
            {"_id": ObjectId(evento_id)},
            {"$set": {"estado": "cancelado"}}
        )
        return result.modified_count > 0
    def asistentes_por_tipo(self, evento_id: str) -> dict:
        pipeline = [
            {"$match": {"eventoId": ObjectId(evento_id)}},
            {"$group": {
                "_id": "$tipoTicket",
                "total": {"$sum": 1},
                "usados": {
                    "$sum": {"$cond": [{"$eq": ["$usado", True]}, 1, 0]}
                }
            }}
        ]
        return list(self.tickets_collection.aggregate(pipeline))

    def obtener_todos_eventos(self) -> list:
        return list(self.eventos_collection.find())

    def actualizar_evento(self, evento_id: str, datos_actualizados: dict) -> bool:
        result = self.eventos_collection.update_one(
            {"_id": ObjectId(evento_id)},
            {"$set": datos_actualizados}
        )
        return result.modified_count > 0

    def eliminar_evento(self, evento_id: str) -> bool:
        result = self.eventos_collection.delete_one({"_id": ObjectId(evento_id)})
        return result.deleted_count > 0

