
# 3
***
En READ COMMITTED, si no se utiliza FOR UPDATE, pueden ocurrir condiciones de carrera que lleven a resultados incorrectos, ya que dos transacciones pueden leer el mismo saldo y luego modificarlo sin saber del cambio del otro. En cambio, con SERIALIZABLE, el sistema impone un control más estricto que evita este tipo de conflictos, ejecutando las transacciones como si fueran secuenciales, asegurando la consistencia de los datos.

![alt text](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/punto3primera.jpeg)
### Read comitted con for update
Resultado observado:

Usuario B leyó el saldo 1000.00 y actualizó a 900.00.
Usuario A leyó el saldo actualizado (900.00) después del commit de B.

Resultado final correcto: 800.00

¿Qué ocurrió?
Al usar FOR UPDATE, la fila quedó bloqueada hasta que la transacción terminó.
Usuario A esperó que Usuario B finalizara antes de continuar.
Se evitó la condición de carrera.

Conclusión:
Con FOR UPDATE, READ COMMITTED logra consistencia correcta. Es seguro si se usan bloqueos explícitos para evitar interferencias entre transacciones.

![alt text](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/punto3segunda.jpeg)
## Read comitted sin for update
Ambos usuarios leyeron el mismo saldo: 1000.00

Ambos restaron 100, creyendo que el saldo era suficiente

El saldo final quedó en 900.00 en vez de 800.00

¿Qué ocurrió?

Al no usar FOR UPDATE, no se bloqueó la fila al leer.

Ambos hilos accedieron al saldo al mismo tiempo, generando una condición de carrera.

Uno de los updates sobrescribió el del otro.

Conclusión:

El nivel READ COMMITTED por sí solo no evita errores de concurrencia si no se bloquea explícitamente la fila. Es inseguro en operaciones críticas como transacciones bancarias.

![alt text](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/punto3tercera.jpeg)
### Serializable sin for update
Resultado observado:

Ambos usuarios intentaron leer y modificar el mismo saldo.

Uno completó correctamente su transacción.

El otro recibió un error de deadlock (1213) y la transacción fue cancelada.

¿Qué ocurrió?
SERIALIZABLE fuerza que las transacciones se ejecuten como si fueran una detrás de otra.
MySQL detectó un posible conflicto y aborta una de las transacciones automáticamente para evitar inconsistencia.
Esto es un mecanismo de protección del sistema.

Conclusión:

SERIALIZABLE es el nivel más seguro, pero puede producir deadlocks. Idealmente se deben manejar con reintentos automáticos en sistemas reales.

***
## 4
Creamos un SQL con tres tablas: categorias, marcas, productos. Insertamos 100 mil registros a la tabla productos.
Luego ejecutamos la consulta sin indice:
EXPLAIN SELECT * FROM marcas WHERE nombre = 'Oscorp';

![sin indice](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/usandoWHERE.png)

Después creamos el indice y se ejecutó la consulta usando el indice:
CREATE INDEX idx_nombre_marca ON marcas(nombre);
EXPLAIN SELECT * FROM marcas WHERE nombre = 'Oscorp';

![con indice](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/usandoINDEX.png)

Para examinar 100.000 filas, una consulta sin indice lo hace en 300-800 ms aproximadamente.
Una consulta con indice lo hace en 20-100 ms, un tiempo mucho mas bajo ya que no necesita recorrer cada fila de la tabla.

## 5
explain sin indices


![alt text](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/punto5.jpg)

type: ALL → Búsqueda completa (Full Table Scan).

No se utiliza ningún índice (key: NULL).

rows: 20 → MySQL estima que analizará las 20 filas.

Esto ocurre cuando no hay índice sobre el campo que estás filtrando o no se está aplicando en la consulta.

Conclusión: Consulta poco eficiente.

![alt text](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/image-3.png)
type: ref → Búsqueda por índice, más eficiente.

key: idx_departamento → Se está usando el índice sobre el campo departamento.

rows: 6 → Solo se examinan 6 filas, lo que es mucho mejor.

Conclusión: Ya se está aprovechando el índice y se mejora el rendimiento.

![alt text](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/image-4.png)
possible_keys: idx_departamento, idx_salario

Pero solo se utiliza idx_departamento.

Aunque haya índice en salario, MySQL decide usar el de departamento por ser más selectivo o útil.

filtered: 55.00 → El filtro logra reducir aún más el resultado.

Conclusión: Se sigue usando solo un índice, pero ya con un segundo filtro. Aún así, muy eficiente.

![alt text](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/image-5.png)
possible_keys: idx_departamento, idx_salario, idx_departamento_salario (índice combinado).

Se sigue usando idx_departamento, aunque el índice combinado también era una opción.

filtered: 61.11 → El filtro es más eficaz.

Conclusión: Aunque hay más índices disponibles, MySQL decide usar solo uno (en este caso idx_departamento).

## 6




## 8
Se creó una tabla clientes y una tabla auditoria_clientes.

![tablas](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/tablas.PNG)


También se creó un trigger que registra los cambios en la tabla clientes.
![trigger](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/trigger.PNG)


Para probar el trigger insertamos un cliente y después le modificamos el nombre.
![prueba trigger](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/pruebaTrigger.PNG)

Luego hacemos una consulta a la tabla de auditoría, que muestra los datos viejos y los datos nuevos del cliente.
![consola](https://github.com/agustinbarbero/Base-de-Datos-II/blob/main/TP1/img/consola.PNG)
