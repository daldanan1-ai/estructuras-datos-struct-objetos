# Struct/Record y Objetos — Analizador de Calificaciones

## Datos de identificación
- **Estudiante:** Domingo Aldana Noel
- **Código:** 7502523002
- **Asignatura:** Estructuras de datos
- **Programa:** Ingeniería del Software
- **IES:** Universidad de Cartagena
- **Tutor:** John Carlos Arrieta Arrieta
- **Actividad:** Unidad 1 — Protocolo Actividad de Aprendizaje Individual (Struct/Record y Objetos)

## Qué contiene el proyecto

Se representa un `Estudiante` (nombre, edad, promedio) de dos formas, como struct/record y como objeto, en **Python** y **JavaScript**. Al final se aplica a un Analizador de Calificaciones.

```
python/
  structs.py                            Sección 3: struct/record (dataclass)
  objetos.py                            Sección 4: clase con métodos
  comparativa.py                        Sección 5: mismo problema como struct y como objeto
  calificaciones_con_estructuras.py     Práctica final: analizador de calificaciones
js-ts/
  structs.js                            Sección 3: struct/record (objeto literal)
  objetos.js                            Sección 4: clase con métodos
  calificacionesConEstructuras.js       Práctica final: analizador de calificaciones
docs/
  comparativa-struct-vs-objeto.md       Sección 5: tabla comparativa y ejemplos
```

| Parte | Qué hace |
|---|---|
| **Struct/record** (`structs.*`) | Declara `Estudiante` como datos puros, crea 3 instancias ficticias, las recorre y modifica el promedio de una. En Python usa `dataclass`; en JS, un objeto literal (lo más cercano a un struct, porque JS no lo tiene nativo). |
| **Objetos** (`objetos.*`) | Clase `Estudiante` con `mostrarInfo()` y `setPromedio()` (este valida que el promedio esté entre 0 y 100). Crea 3 instancias en un arreglo, las recorre y modifica una. |
| **Comparativa** (`comparativa.py`, `docs/`) | Mismo problema como struct y como objeto en Python, con las diferencias en código (mostrar, validación, igualdad, asignación), más la tabla de definición, mutabilidad, tipado y memoria. |
| **Práctica final** (`calificaciones*`) | Analizador de calificaciones donde el arreglo contiene `Estudiante` en vez de notas sueltas. Ver la sección siguiente. |

## Práctica final: Analizador de Calificaciones

Lee un arreglo de `Estudiante` (nombre, edad, calificación 0-100) y calcula, sobre el campo `promedio`: promedio general, mediana, moda (indicando quién obtuvo la nota modal), porcentaje de aprobados y reprobados (`NOTA_APROBATORIA = 60`) e histograma de frecuencias en texto. El listado y las búsquedas (por nombre y por calificación) muestran el nombre junto a la nota.

Al iniciar se elige:

1. **La versión del estudiante:** struct/record (datos puros, con `mostrar` y `aprobado` como funciones aparte) u objeto (clase con `mostrarInfo()` y `aprobado()`).
2. **El origen de los datos:** ingresarlos por teclado o cargar una lista de ejemplo de 10 estudiantes ficticios.

**Versión más adecuada para este caso: objeto.** La regla de aprobación y el formato de salida pertenecen al estudiante, por lo que la clase los mantiene junto a sus datos y un cambio de regla se hace en un solo lugar. El struct bastaría solo para guardar y leer datos. El razonamiento completo está comentado al inicio de cada archivo.

## Cómo ejecutar

Requisitos: Python 3.9 o superior y Node.js 18 o superior. No hay dependencias que instalar.

```bash
# Python
python3 python/structs.py
python3 python/objetos.py
python3 python/comparativa.py
python3 python/calificaciones_con_estructuras.py

# JavaScript
node js-ts/structs.js
node js-ts/objetos.js
node js-ts/calificacionesConEstructuras.js
```

## Ejemplo de entrada/salida (práctica final)

Se elige la versión struct/record (`1`), la lista de ejemplo (`2`) y luego, del menú, listado (`1`), estadísticas (`2`), histograma (`3`) y búsqueda por calificación 72 (`5`). Las dos versiones y los dos lenguajes producen la misma salida.

```
=== Analizador de Calificaciones (Struct/Record y Objetos) ===
Versión del estudiante:
  1. struct/record (dataclass)
  2. objeto (clase)
Elige (1-2): 1

Datos:
  1. Ingresar por teclado
  2. Cargar lista de ejemplo
Elige (1-2): 2

Versión en uso: struct/record — 10 estudiantes cargados.

== Listado de estudiantes ==
Ana Pérez (20 años) - promedio: 85
Luis Gómez (22 años) - promedio: 72
María Ríos (19 años) - promedio: 91
Carlos Díaz (21 años) - promedio: 58
Sofía Torres (23 años) - promedio: 72
Juan Pardo (20 años) - promedio: 45
Laura Mejía (22 años) - promedio: 100
Pedro Salas (24 años) - promedio: 60
Camila Ruiz (19 años) - promedio: 72
Valentina Cruz (21 años) - promedio: 38

== Estadísticas ==
Estudiantes: 10
Promedio general: 69.30
Mediana: 72
Moda: 72 (Luis Gómez, Sofía Torres, Camila Ruiz)
Aprobados (>= 60): 7 (70.0%)
Reprobados (< 60): 3 (30.0%)

== Histograma de frecuencias ==
  0-9   |
 10-19  |
 20-29  |
 30-39  | # 1
 40-49  | # 1
 50-59  | # 1
 60-69  | # 1
 70-79  | ### 3
 80-89  | # 1
 90-100 | ## 2

== Búsqueda por calificación: 72 ==
Luis Gómez (22 años) - promedio: 72
Sofía Torres (23 años) - promedio: 72
Camila Ruiz (19 años) - promedio: 72
```

Con la opción de teclado, el programa pide la cantidad de estudiantes y luego nombre, edad y calificación de cada uno. Valida que la edad y la calificación sean números en rango y acepta coma o punto decimal.
