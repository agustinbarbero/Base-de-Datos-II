
## Ejercicio 3
***
En READ COMMITTED, si no se utiliza FOR UPDATE, pueden ocurrir condiciones de carrera que lleven a resultados incorrectos, ya que dos transacciones pueden leer el mismo saldo y luego modificarlo sin saber del cambio del otro. En cambio, con SERIALIZABLE, el sistema impone un control más estricto que evita este tipo de conflictos, ejecutando las transacciones como si fueran secuenciales, asegurando la consistencia de los datos.

### Read comitted con for update
![Read comitted con for update](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/punto3primera.jpeg)

**Resultado observado:**
- Usuario B leyó el saldo 1000.00 y actualizó a 900.00.
- Usuario A leyó el saldo actualizado (900.00) después del commit de B.

Resultado final correcto: 800.00

**¿Qué ocurrió?**
- Al usar FOR UPDATE, la fila quedó bloqueada hasta que la transacción terminó.
- Usuario A esperó que Usuario B finalizara antes de continuar.
- Se evitó la condición de carrera.

**Conclusión:**
Con `FOR UPDATE`, READ COMMITTED logra una consistencia correcta. Es seguro si se usan bloqueos explícitos para evitar interferencias entre transacciones.

### Read comitted sin for update

![alt text](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/punto3segunda.jpeg)

**Resultado observado:**
- Ambos usuarios leyeron el mismo saldo: 1000.00
- Ambos restaron 100, creyendo que el saldo era suficiente
- El saldo final quedó en 900.00 en vez de 800.00

**¿Qué ocurrió?**
- Al no usar FOR UPDATE, no se bloqueó la fila al leer.
- Ambos hilos accedieron al saldo al mismo tiempo, generando una condición de carrera.
- Uno de los updates sobrescribió el del otro.

**Conclusión:**
READ COMMITTED por sí solo no evita errores de concurrencia si no se bloquea explícitamente la fila. Es inseguro en operaciones críticas como transacciones bancarias.

### Serializable sin for update

![Serializable](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/punto3tercera.jpeg)

**Resultado observado:**
- Ambos usuarios intentaron leer y modificar el mismo saldo.
- Uno completó su transacción exitosamente.
- El otro recibió un error de **deadlock (1213)** y su transacción fue cancelada.

**¿Qué ocurrió?**
- SERIALIZABLE fuerza que las transacciones se ejecuten como si fueran secuenciales.
- MySQL detectó un conflicto y abortó una de las transacciones para evitar inconsistencia.

**Conclusión:**
SERIALIZABLE es el nivel más seguro, pero puede generar **deadlocks**. En sistemas reales, se recomienda manejar esto con reintentos automáticos.

---
## Ejercicio 4
Creamos un SQL con tres tablas: `categorias`, `marcas`, y `productos`. Se insertaron **100.000 registros** en la tabla `productos`.
Luego ejecutamos la consulta **sin índice**:
```sql
EXPLAIN SELECT * FROM marcas WHERE nombre = 'Oscorp';
```

![Consulta sin índice](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/usandoWHERE.png)

Posteriormente, creamos el índice y volvimos a ejecutar la consulta:

```sql
CREATE INDEX idx_nombre_marca ON marcas(nombre);
EXPLAIN SELECT * FROM marcas WHERE nombre = 'Oscorp';
```

![Consulta con índice](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/usandoINDEX.png)

**Resultados:**
- Sin índice: tiempo de respuesta entre **300 y 800 ms**.
- Con índice: tiempo de respuesta entre **20 y 100 ms**, mucho más eficiente ya que no recorre toda la tabla.

---
## Ejercicio 5
### Explain sin indices

![Consulta sin índices](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/punto5.jpg)

- `type: ALL` → Búsqueda completa (*Full Table Scan*).
- `key: NULL` → No se utiliza ningún índice.
- `rows: 20` → MySQL estima analizar 20 filas.

**Conclusión:** Consulta poco eficiente.


### Consulta usando índice
![Consulta con índice](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/image-3.png)
- `type: ref` → Búsqueda por índice, más eficiente.
- `key: idx_departamento` → Se utiliza el índice en `departamento`.
- `rows: 6` → Solo se examinan 6 filas.

**Conclusión:** El índice mejora significativamente el rendimiento.


### Consulta con múltiples índices posibles
![Consulta con multiples índices](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/image-4.png)
- `possible_keys`: `idx_departamento`, `idx_salario`.
- Solo se utiliza `idx_departamento`.
- `filtered: 55.00` → El filtro mejora el resultado.

**Conclusión:** Se sigue usando solo un índice, pero ya con un segundo filtro. Aún así, muy eficiente.

### Consulta con índice combinado disponible
![alt text](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/image-5.png)
- `possible_keys`: `idx_departamento`, `idx_salario`, `idx_departamento_salario` (índice combinado).
- Se sigue utilizando `idx_departamento`, aunque el índice combinado también era una opción.
- `filtered: 61.11` → El filtro es más eficaz.

**Conclusión:** Aunque hay más índices disponibles, MySQL decide usar solo uno (en este caso idx_departamento).

***
## Ejercicio 6

Creación de una tabla ventas y una vista resumen_mensual.
```sql
CREATE TABLE ventas (
    id INT PRIMARY KEY,
    nombre_producto VARCHAR(100), 
    mes INT, 
    cantidad INT
);

CREATE VIEW resumen_mensual AS (
    SELECT nombre_producto, mes, SUM(cantidad) AS total 
    FROM ventas 
    GROUP BY nombre_producto, mes
);
```

```sql
INSERT INTO ventas (id, nombre_producto, mes, cantidad) VALUES
(1, 'Zapatilla Runner X', 1, 30),
(2, 'Zapatilla Runner X', 2, 45),
(3, 'Remera DryFit', 1, 50),
(4, 'Remera DryFit', 2, 60),
(5, 'Short Deportivo', 1, 20),
(6, 'Short Deportivo', 2, 25),
(7, 'Campera Impermeable', 1, 10),
(8, 'Campera Impermeable', 2, 5),
(9, 'Medias Técnicas', 1, 70),
(10, 'Medias Técnicas', 2, 80),
(11, 'Gorra UV', 1, 15),
(12, 'Gorra UV', 2, 20);
```

Consulta que devuelve los 5 productos más vendidos.
```sql
SELECT nombre_producto, SUM(total) AS total 
FROM resumen_mensual 
GROUP BY nombre_producto 
ORDER BY total DESC 
LIMIT 5;
```

![Resultado](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/punto6.jpg)

***
## Ejercicio 8
Se creó una tabla clientes y una tabla auditoria_clientes.
```sql
-- Tabla principal
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100)
);

-- Tabla de auditoría
CREATE TABLE auditoria_clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    accion VARCHAR(10),
    cliente_id INT,
    datos_viejos JSON,
    datos_nuevos JSON,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);
```


También se creó un trigger que registra los cambios en la tabla clientes.
```sql
-- Creación del Trigger
DELIMITER $$

CREATE TRIGGER t_auditoria_clientes
AFTER UPDATE ON clientes
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_clientes (
        accion,
        cliente_id,
        datos_viejos,
        datos_nuevos
    ) VALUES (
        'UPDATE',
        OLD.id,
        JSON_OBJECT('nombre', OLD.nombre, 'email', OLD.email),
        JSON_OBJECT('nombre', NEW.nombre, 'email', NEW.email)
    );
END$$

DELIMITER ;
```


Para probar el trigger insertamos un cliente y después le modificamos el nombre.
```sql
-- Prueba del Trigger
-- Insertar un cliente
INSERT INTO clientes (nombre, email) 
VALUES ('Juan Pérez', 'juan@example.com');

-- Actualizar el cliente para disparar el trigger
UPDATE clientes
SET nombre = 'Juan P. Gómez'
WHERE id = 1;

-- Consultar la tabla de auditoría
SELECT * FROM auditoria_clientes;
```


Luego hacemos una consulta a la tabla de auditoría, que muestra los datos viejos y los datos nuevos del cliente.
![consola](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/consola.PNG)

***
## Ejercicio 9 

Este documento describe paso a paso cómo realizar un **backup completo** de una base de datos MySQL, cómo **restaurarlo**, y cómo **simular una pérdida de datos** para comprobar la efectividad del proceso.


### 1. Creación de una Base de Datos de Prueba

```sql
CREATE DATABASE tienda;
USE tienda;

CREATE TABLE productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50),
    precio DECIMAL(10,2)
);

INSERT INTO productos (nombre, precio) VALUES
('Manzana', 1.50),
('Banana', 0.80),
('Naranja', 1.00);
```

### 2. Realizar un Backup Completo

Usar `mysqldump`:

```bash
mysqldump -u root -p tienda > punto_9.sql
```


### 3. Simular una Pérdida de Datos

```sql
DROP DATABASE tienda;
```


### 4. Restaurar la Base de Datos

Primero crear la base vacía (si el script no la incluye):

```sql
CREATE DATABASE tienda;
```

Restaurar desde el archivo:

```bash
mysql -u root -p tienda < punto_9.sql
```


### 5. Verificar la Restauración

Entrar a MySQL y consultar:

```sql
USE tienda;
SELECT * FROM productos;
```


### Resumen de Comandos

| Acción                   | Comando                                             |
|--------------------------|-----------------------------------------------------|
| Backup                   | `mysqldump -u root -p tienda > punto_9.sql`         |
| Pérdida de datos         | `DROP DATABASE tienda;`                             |
| Crear base vacía         | `CREATE DATABASE tienda;`                           |
| Restaurar                | `mysql -u root -p tienda < punto_9.sql`             |

---
