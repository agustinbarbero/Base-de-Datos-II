from datetime import datetime
from typing import List, Dict, Optional
from pymongo.collection import Collection

class TipoTicket:
    def __init__(self, nombre: str, precio: float, cantidad: int, vendidos: int = 0):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.vendidos = vendidos

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "vendidos": self.vendidos
        }

class Evento:
    def __init__(self, nombre: str, descripcion: str, fecha: datetime, 
                ubicacion: str, capacidadMaxima: int, 
                tiposTicket: List[TipoTicket], estado: str = "activo"):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha = fecha
        self.ubicacion = ubicacion
        self.capacidadMaxima = capacidadMaxima
        self.tiposTicket = tiposTicket
        self.estado = estado

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha": self.fecha,
            "ubicacion": self.ubicacion,
            "capacidadMaxima": self.capacidadMaxima,
            "tiposTicket": [ticket.to_dict() for ticket in self.tiposTicket],
            "estado": self.estado
        }