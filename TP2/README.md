
## ✅ Ejercicio 1: CRUD básico

Crea una base de datos llamada `empresa`. Agrega una colección `empleados` con 3 documentos que incluyan nombre, edad y puesto. Actualiza la edad de uno de los empleados y elimina al empleado que tenga el puesto de "pasante".

```js
use("empresa");
db.createCollection("empleados");

db.empleados.insertMany([
    { nombre: "Marcos", edad: 22, puesto: "Ventas" },
    { nombre: "Pablo", edad: 46, puesto: "Desarrollo" },
    { nombre: "Juan", edad: 22, puesto: "Pasante" }
]);

db.empleados.updateOne(
    { nombre: "Pablo" },
    { $set: { edad: 25 } }
);

db.empleados.deleteOne(
    { puesto: "Pasante" }
);

db.empleados.find().pretty(); // Ver el resultado
```


## ✅ Ejercicio 2: Búsquedas con operadores

Consulta todos los empleados cuya edad esté entre 25 y 40 años. Usa operadores relacionales y lógicos.

```js
use("empresa");
db.empleados.find({
    $and: [
        { edad: { $gte: 25 } },
        { edad: { $lte: 40 } }
    ]
});
```


## ✅ Ejercicio 3: Uso de proyección

Recupera los nombres y puestos de todos los empleados, sin mostrar el `_id`.

```js
use("empresa");
db.empleados.find({}, { _id: 0, nombre: 1, puesto: 1 });
```


## ✅ Ejercicio 4: Documentos embebidos

Agrega un campo `direccion` que incluya calle, ciudad y código postal.

```js
use("empresa");
db.empleados.updateMany({}, {
    $set: {
        direccion: {
            calle: "Av. Alem",
            ciudad: "Bahia Blanca",
            codigo_postal: "8000"
        }
    }
})
```


## ✅ Ejercicio 5: Agregación

Dada una colección `ventas` con campos producto, cantidad y precio_unitario, calcula el total de ventas por producto usando `$group` y `$sum`.

```js
use("empresa");

db.createCollection("ventas");
db.ventas.insertMany([
    { producto: "Celular", cantidad: 4, precio_unitario: 120000 },
    { producto: "Celular", cantidad: 2, precio_unitario: 120000 },
    { producto: "Notebook", cantidad: 3, precio_unitario: 350000 },
    { producto: "Notebook", cantidad: 1, precio_unitario: 350000 },
    { producto: "Auriculares", cantidad: 10, precio_unitario: 15000 }
]);

db.ventas.aggregate([
    { 
        $project: {
            producto: 1,
            total_venta: { $multiply: ["$cantidad", "$precio_unitario"] }
        }
    },
    {
        $group: {
            _id: "$producto",
            total_venta: { $sum: "$total_venta" }
        }
    }
]);
```


## ✅ Ejercicio 6: Índices

Crea un índice compuesto sobre los campos `apellido` y `nombre` en una colección de `clientes`.

```js
use("empresa"); 

db.createCollection("clientes");

db.clientes.insertMany([
    { nombre: "Carlos", apellido: "López", edad: 45, puesto: "gerente", antiguedad: 15 },
    { nombre: "Lucía", apellido: "García", edad: 29, puesto: "analista", antiguedad: 4 },
    { nombre: "Martín", apellido: "Fernández", edad: 33, puesto: "vendedor", antiguedad: 7 },
    { nombre: "Verónica", apellido: "Martínez", edad: 41, puesto: "contadora", antiguedad: 10 },
    { nombre: "Andrés", apellido: "Ruiz", edad: 26, puesto: "asistente", antiguedad: 2 },
    { nombre: "Romina", apellido: "Sosa", edad: 38, puesto: "administrativa", antiguedad: 9 }
]);

// Crear índice compuesto sobre nombre y apellido
db.clientes.createIndex(
    { nombre: 1, apellido: 1 });


db.clientes.getIndexes();
```


## ✅ Ejercicio 7: Referencias

Crea una colección `cursos` y una colección `alumnos`. Luego inserta documentos donde los alumnos tengan una lista de `id_curso` referenciando a los cursos.

```js
use("escuela");

db.createCollection("cursos");
db.createCollection("alumnos");

db.cursos.insertMany([
    { _id: 101, nombre: "Física" },
    { _id: 102, nombre: "Literatura" },
    { _id: 103, nombre: "Bases de Datos" }
]);

db.alumnos.insertMany([
    {
        nombre: "Camila Torres",
        edad: 19,
        id_cursos: [101, 103]
    },
    {
        nombre: "Santiago López",
        edad: 23,
        id_cursos: [102]
    },
    {
        nombre: "Valentina Ruiz",
        edad: 21,
        id_cursos: [101, 102, 103]
    }
]);

db.cursos.find();
```


## ✅ Ejercicio 8: Uso de $lookup

Realiza una agregación donde se combinen los datos de `alumnos` y `cursos` usando `$lookup`.

```js
use("escuela");

db.alumnos.aggregate([
    {
        $lookup: {
            from: "cursos",               
            localField: "id_cursos",     
            foreignField: "_id",          
            as: "cursos_inscriptos"       
        }
    }
]);
```


## ✅ Ejercicio 9: Replicación y sharding (teórico)

Replica set es un conjunto de servidores en donde se mantienen copias sincronizadas de datos.
Tiene un nodo primario (donde se hacen las escrituras) y varios nodos secundarios (solo lectura y copia).
Ventajas de usar un Replica Set:
- Si el nodo primario falla, uno de los secundarios toma su lugar.
- Si un servidor cae los datos no se pierden.
Por esto mismo, al usar Replica Set obtenemos alta disponibilidad, seguridad de datos y tolerancia a fallos.

El Sharding consiste en dividir una base de datos muy grande en partes más pequeñas (shards),
distribuidas en diferentes servidores.
Los beneficios que aporta el sharding en una base de datos de alto volumen son:
- Distribución horizontal: permite agregar más servidores para manejar más datos y consultas.
- Mejor rendimiento: las operaciones se reparten entre shards, reduciendo la carga de cada uno.
- Manejo eficiente de grandes volúmenes: evita que una sola máquina se sobrecargue cuando los datos o el tráfico crecen mucho.


## ✅ Ejercicio 10: Seguridad y backups

Se crea un usuario con permisos de lectura y escritura, y se usan los comandos `mongodump` y `mongorestore` para hacer backup y restauración de la base de datos.

```js
use("empresa");

db.createUser({
    user: "admin",
    pwd: "5555",
    roles: [
        { role: "readWrite", db: "empresa" }  
    ]
});

/* 
Backup de la base de datos:
mongodump --db empresa --out ./backups
-------------------------------------------
Restauracion del backup:
mongorestore --db empresa ./backups/empresa
*/
```
