from datetime import datetime
from bson import ObjectId

def formatear_fecha(fecha: datetime) -> str:
    return fecha.strftime("%d/%m/%Y %H:%M")

def validar_object_id(id_str: str) -> bool:
    try:
        ObjectId(id_str)
        return True
    except:
        return False

def mostrar_evento(evento: dict) -> None:
    print(f"\n--- {evento['nombre']} ---")
    print(f"Fecha: {formatear_fecha(evento['fecha'])}")
    print(f"Ubicación: {evento['ubicacion']}")
    print(f"Descripción: {evento['descripcion']}")
    print("\nTipos de tickets disponibles:")
    for ticket in evento['tiposTicket']:
        disponibles = ticket['cantidad'] - ticket['vendidos']
        print(f" - {ticket['nombre']}: ${ticket['precio']} ({disponibles} disponibles)")
        

