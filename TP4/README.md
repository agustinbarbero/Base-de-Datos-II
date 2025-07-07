# TP4 - Neo4j y Cypher

Trabajo práctico orientado a modelado y consultas en **Neo4j** utilizando **Cypher**.

**Grupo**:  
- Agustin Barbero  
- Felipe Fernandez  
- Luciano Nicolas Lopez Gonzalez  
- Juan Ignacio Tarsia  

---

## 🗂️ Ejercicio 1: Sistema de Gestión de Proyectos

## Modelado

```cypher
CREATE
  // Proyectos
  (p1:Proyecto {nombre: "proyecto1"}),
  (p2:Proyecto {nombre: "proyecto2"}),

  // Departamentos
  (d1:Departamento {area: "Informatica"}),
  (d2:Departamento {area: "Economia"}),
  (d3:Departamento {area: "Logistica"}),
  (d4:Departamento {area: "Marketing"}),

  // Empleados
  (f:Empleado {nombre: "Felipe"}),
  (l:Empleado {nombre: "Lucho"}),
  (a:Empleado {nombre: "Agustin"}),
  (r:Empleado {nombre: "Rapha"}),

  // Relaciones Empleado -> Departamento
  (f)-[:PERTENECE_A]->(d1),
  (l)-[:PERTENECE_A]->(d2),
  (a)-[:PERTENECE_A]->(d3),
  (r)-[:PERTENECE_A]->(d4),

  (f)- [:Lidera_el]->(p1),
  (r)- [:Lidera_el]->(p2),

  (f)- [:Trabaja_en {horas_semanales:'30'}]->(p1),
  (l)- [:Trabaja_en {horas_semanales:'25'}]->(p1),
  (r)- [:Trabaja_en {horas_semanales:'40'}]->(p2),
  (a)- [:Trabaja_en {horas_semanales:'20'}]->(p2);
```
## Consultas
### Obtener el nombre del proyecto, su líder y los empleados asignados
```cypher
MATCH (líder:Empleado)-[:Lidera_el]->(p:Proyecto)
OPTIONAL MATCH (emp:Empleado)-[t:Trabaja_en]->(p)
RETURN p.nombre AS proyecto,
       líder.nombre AS lider,
       collect(emp.nombre) AS empleados_asignados;
```
### Calcular el total de horas semanales por proyecto
```cypher
MATCH (:Empleado)-[t:Trabaja_en]->(p:Proyecto)
RETURN p.nombre AS proyecto,
       sum(toInteger(t.horas_semanales)) AS total;
```

### Listar los empleados que trabajan en más de un proyecto
```cypher
MATCH (e:Empleado)-[:Trabaja_en]->(p:Proyecto)
WITH e, count(p) AS cantidad_proyectos
WHERE cantidad_proyectos > 1
RETURN e.nombre, cantidad_proyectos;
// (devuelve vacío, nadie trabaja en 2 proyectos a la vez)
```

---

## 📚 Ejercicio 2: Biblioteca Universitaria Extendida
## Modelado

```cypher
CREATE
  (e1:Estudiante {nombre: "Felipe"}),
  (e2:Estudiante {nombre: "Agus"}),
  (e3:Estudiante {nombre: "Lucho"}),

  (c1:Categoria {nombre: "Ficción"}),
  (c2:Categoria {nombre: "Acción"}),
  (c3:Categoria {nombre: "Suspenso"}),
  (c4:Categoria {nombre: "Matemática"}),

  (r1:Carrera {nombre: "Informática"}),
  (r2:Carrera {nombre: "Ingeniería"}),
  (r3:Carrera {nombre: "Arte"}),

  (e1)-[:Estudia]->(r1),
  (e2)-[:Estudia]->(r2),
  (e3)-[:Estudia]->(r3),

  (l1:Libro {titulo: "El Hobbit"}),
  (l2:Libro {titulo: "Misión Imposible"}),
  (l3:Libro {titulo: "La Sombra"}),
  (l4:Libro {titulo: "Álgebra Lineal"}),

  (l1)-[:PERTENECE_A]->(c1),
  (l2)-[:PERTENECE_A]->(c2),
  (l3)-[:PERTENECE_A]->(c3),
  (l4)-[:PERTENECE_A]->(c4),

  (e1)-[:PIDIO {fecha: "2024-06-01", estado: "Activo"}]->(l1),
  (e2)-[:PIDIO {fecha: "2024-05-15", estado: "Devuelto"}]->(l2),
  (e1)-[:PIDIO {fecha: "2024-06-10", estado: "Activo"}]->(l3),
  (e3)-[:PIDIO {fecha: "2024-06-03", estado: "Devuelto"}]->(l4),
  (e3)-[:PIDIO {fecha: "2024-06-20", estado: "Activo"}]->(l1);
```

## Consultas

### Obtener todos los libros actualmente prestados (estado "Activo")

```cypher
MATCH (est:Estudiante)-[p:PIDIO {estado:"Activo"}]->(lib:Libro)
RETURN est.nombre AS estudiante, lib.titulo AS libro, p.fecha AS fecha_prestamo;
```

### Listar cuántos libros ha pedido prestado cada estudiante

```cypher
MATCH (est:Estudiante)-[:PIDIO]->(:Libro)
RETURN est.nombre AS estudiante, COUNT(*) AS cantidad_prestamos;
```

### Mostrar las categorías con más préstamos activos

```cypher
MATCH (:Estudiante)-[p:PIDIO {estado: "Activo"}]->(l:Libro)-[:PERTENECE_A]->(c:Categoria)
RETURN c.nombre AS categoria, COUNT(*) AS prestamos_activos
ORDER BY prestamos_activos DESC;
```

### Encontrar los estudiantes que no tienen préstamos activos

```cypher
MATCH (e:Estudiante)
WHERE NOT (e)-[:PIDIO {estado: "Activo"}]->(:Libro)
RETURN e.nombre AS estudianteSinPrestamosActivos;
```
---

## 👥 Ejercicio 3: Red Social Profesional

## Modelado

```cypher
CREATE
  (u1:Usuario {nombre: "Felipe"}),
  (u2:Usuario {nombre: "Agus"}),
  (u3:Usuario {nombre: "Lucho"}),
  (u4:Usuario {nombre: "Juani"}),

  (p1:Post {nombre: "Selfie", fechaPublicacion:date('2025-04-10')}),
  (p2:Post {nombre: "Comida", fechaPublicacion:date('2025-02-09')}),
  (p3:Post {nombre: "Paisaje", fechaPublicacion:date('2025-03-11')}),

  (h1:Habilidad {nombre: "Correr"}),
  (h2:Habilidad {nombre: "Nadar"}),
  (h3:Habilidad {nombre: "Saltar"}),
  (h4:Habilidad {nombre: "Girar"}),
  (h5:Habilidad {nombre: "Dormir"}),
  (h6:Habilidad {nombre: "Pelear"}),
  (h7:Habilidad {nombre: "Relacionarse"}),
  (h8:Habilidad {nombre: "Comer"}),

  (u1)-[:Conoce]->(u2),
  (u2)-[:Conoce]->(u3),
  (u3)-[:Conoce]->(u4),
  (u4)-[:Conoce]->(u1),
  (u4)-[:Conoce]->(u3),
  (u2)-[:Conoce]->(u4),
  (u1)-[:Conoce]->(u3),

  (u1)-[:Publica]->(p1),
  (u2)-[:Publica]->(p2),
  (u3)-[:Publica]->(p3),

  (u1)-[:Tiene]->(h1),
  (u2)-[:Tiene]->(h2),
  (u3)-[:Tiene]->(h3),
  (u4)-[:Tiene]->(h4),
  (u1)-[:Tiene]->(h5),
  (u2)-[:Tiene]->(h6),
  (u3)-[:Tiene]->(h7),
  (u4)-[:Tiene]->(h8),

  (u1)-[:Endosa]->(h4),
  (u2)-[:Endosa]->(h3),
  (u3)-[:Endosa]->(h2),
  (u4)-[:Endosa]->(h1);
```

## Consultas

### Listar los usuarios con más conexiones

```cypher
MATCH (u:Usuario)-[:Conoce]->(otro)
RETURN u.nombre AS Usuario, COUNT(otro) AS total_conexiones
ORDER BY total_conexiones DESC;
```

### Obtener los 2 usuarios con más publicaciones

```cypher
MATCH (u:Usuario)-[:Publica]->(p:Post)
RETURN u.nombre AS Usuario, COUNT(p) AS total_publicaciones
ORDER BY total_publicaciones DESC
LIMIT 2;
```

### Mostrar las habilidades más endosadas en total

```cypher
MATCH (:Usuario)-[:Endosa]->(h:Habilidad)
RETURN h.nombre AS Habilidades, COUNT(*) AS habilidades_endosadas
ORDER BY habilidades_endosadas DESC;
```

### Listar las habilidades que un usuario aún no ha endosado

```cypher
MATCH (h:Habilidad)
WHERE NOT EXISTS {
    MATCH (u:Usuario {nombre: "Agus"})-[:Endosa]->(h)
}
RETURN h.nombre AS habilidades_no_endosadas;
```

---

## 🎓 Ejercicio 4: Sistema de Cursos y Calificaciones

## Modelado
```cypher
CREATE
  (e1:Estudiante {nombre: "Felipe"}),
  (e2:Estudiante {nombre: "Agus"}),
  (e3:Estudiante {nombre: "Lucho"}),

  (c1:Curso {nombre: "Oratoria"}),
  (c2:Curso {nombre: "Excel"}),
  (c3:Curso {nombre: "Inteligencia Artificial"}),
  (c4:Curso {nombre: "Marketing"}),

  (m1:Materia {nombre: "Matemática"}),
  (m2:Materia {nombre: "Filosofia"}),
  (m3:Materia {nombre: "Algebra"}),

  (e1)-[:INSCRIPTO_EN {nota: 4}]->(c1),
  (e2)-[:INSCRIPTO_EN {nota: 9}]->(c2),
  (e3)-[:INSCRIPTO_EN {nota: 6}]->(c3),
  (e1)-[:INSCRIPTO_EN {nota: 7}]->(c3),
  (e2)-[:INSCRIPTO_EN {nota: 7}]->(c1),
  (e3)-[:INSCRIPTO_EN {nota: 8}]->(c2),

  (c1)-[:CORRESPONDE_A]->(m1),
  (c2)-[:CORRESPONDE_A]->(m2),
  (c3)-[:CORRESPONDE_A]->(m3),
  (c4)-[:CORRESPONDE_A]->(m1),

  (m3)-[:PRERREQUISITO]->(m1);
```

## Consultas

### Transcripción académica de un estudiante

```cypher
MATCH (e:Estudiante {nombre: 'Agus'})-[i:INSCRIPTO_EN]->(c:Curso)-[:CORRESPONDE_A]->(m:Materia)
RETURN m.nombre AS Materia, c.nombre AS Curso, i.nota AS Nota
ORDER BY m.nombre;
```

### Verificar si un estudiante puede inscribirse en una materia (prerrequisitos)

```cypher
MATCH (m:Materia {nombre: 'Algebra'})-[:PRERREQUISITO]->(prerrequisito)<-[:CORRESPONDE_A]-(c:Curso)<-[i:INSCRIPTO_EN]-(e:Estudiante {nombre: 'Agus'})
WHERE i.nota >= 6
RETURN e.nombre AS Estudiante, prerrequisito.nombre AS Prerrequisito, i.nota AS Nota, 'Puede inscribirse' AS Estado;
```

### Calcular el promedio de calificaciones por estudiante

```cypher
MATCH (e:Estudiante)-[i:INSCRIPTO_EN]->(c:Curso)
RETURN e.nombre AS Estudiante, avg(i.nota) AS Promedio_notas;
```

### Detectar materias con promedio inferior a 7

```cypher
MATCH (e:Estudiante)-[i:INSCRIPTO_EN]->(c:Curso)-[:CORRESPONDE_A]->(m:Materia)
WITH m.nombre AS Materia, avg(i.nota) AS Promedio
WHERE Promedio < 7
RETURN Materia, ROUND(Promedio) AS Promedio
ORDER BY Promedio ASC;
```


---



