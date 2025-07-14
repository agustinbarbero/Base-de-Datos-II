from datetime import datetime
from typing import Dict
from bson import ObjectId

class Comprador:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "email": self.email
        }

class Ticket:
    def __init__(self, eventoId: ObjectId, comprador: Comprador, 
                            tipoTicket: str, precio: float, 
                            fechaCompra: datetime = datetime.now(),
                            codigoQR: str = None, usado: bool = False,
                            fechaUso: datetime = None):
        self.eventoId = eventoId
        self.comprador = comprador
        self.tipoTicket = tipoTicket
        self.precio = precio
        self.fechaCompra = fechaCompra
        self.codigoQR = codigoQR or self._generar_codigo_qr()
        self.usado = usado
        self.fechaUso = fechaUso

    def _generar_codigo_qr(self) -> str:
        # Implementación simple de generación de código QR
        import uuid
        return str(uuid.uuid4()).replace('-', '')[:12].upper()

    def to_dict(self):
        return {
            "eventoId": self.eventoId,
            "comprador": self.comprador.to_dict(),
            "tipoTicket": self.tipoTicket,
            "precio": self.precio,
            "fechaCompra": self.fechaCompra,
            "codigoQR": self.codigoQR,
            "usado": self.usado,
            "fechaUso": self.fechaUso
        }