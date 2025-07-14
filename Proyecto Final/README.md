# Plataforma de Eventos y Tickets

Este proyecto es una plataforma para la gestión de eventos y la venta de tickets, desarrollada en Python.

## Requisitos previos
- Python 3.8 o superior
- Acceso a una instancia de MongoDB (local o remota)

## Instalación de dependencias

1. Abre una terminal en la carpeta del proyecto (`eventos_tickets`).
2. Ejecuta el siguiente comando para instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración de la base de datos

Asegúrate de tener una instancia de MongoDB en ejecución y configura la cadena de conexión en el archivo correspondiente.

## Inicialización y uso del proyecto

1. Abre una terminal en la carpeta `eventos_tickets`.
2. Ejecuta el archivo principal:

```bash
python main.py
```


Sigue las instrucciones del menú para crear eventos, comprar tickets, validar tickets, generar reportes, etc.

## Estructura del proyecto

- `main.py` : Archivo principal para ejecutar la aplicación.
- `requirements.txt`: Lista de dependencias del proyecto.
- `database/`: Conexión y utilidades para la base de datos MongoDB.
- `models/`: Definición de modelos de datos (Evento, Ticket, etc).
- `services/`: Lógica de negocio para eventos y tickets.
- `utils/`: Funciones auxiliares.

