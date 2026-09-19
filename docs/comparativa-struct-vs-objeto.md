# Comparativa: Struct/Record vs Objetos

Problema usado en todo el proyecto: `Estudiante` con `nombre`, `edad` y `promedio`.

## 1. Cómo representan Python y JS/TS un struct

Ninguno de los dos lenguajes tiene un `struct` nativo como C o C#.

| Aspecto | Python (`dataclass`) | JavaScript / TypeScript |
|---|---|---|
| Forma de representarlo | `@dataclass class Estudiante` | Objeto literal `{ nombre, edad, promedio }`; en TS se describe con una `interface` |
| Declaración | Explícita: la clase fija campos y tipos | Implícita en JS: la define el propio literal. En TS, la `interface` |
| Tipo con nombre | Sí (`Estudiante`) | No: es un objeto anónimo. La `interface` de TS desaparece al ejecutar |
| Métodos generados | `__init__`, `__repr__`, `__eq__` | Ninguno |
| Impresión | `Estudiante(nombre='Ana', ...)` | `{ nombre: 'Ana', ... }` |
| Mutabilidad | Mutable (`frozen=True` o `NamedTuple` lo vuelven inmutable) | Mutable (`Object.freeze` lo vuelve inmutable) |
| Tipado | Anotaciones sin verificación en ejecución | Ninguno en JS; en TS se verifica al compilar |

**Por qué el objeto literal es lo más cercano a un struct en JS/TS:** es un contenedor de campos con nombre, sin clase ni métodos, igual que un struct. La `interface` de TS solo añade la descripción de esa forma en tiempo de compilación.

## 2. Diferencia entre la clase y el struct/record

| Aspecto | Struct / record | Objeto (clase) |
|---|---|---|
| Contenido | Solo datos | Datos y métodos (`mostrarInfo`, `setPromedio`) |
| Modificar el promedio | Asignación directa (`est.promedio = x`) | Mediante `setPromedio(x)` |
| Validación | Ninguna | El método puede rechazar valores inválidos |
| Formato de salida | Automático | Lo decide `mostrarInfo()` |
| Idea central | Contenedor de datos | Encapsula estado y comportamiento |

Diferencias específicas por lenguaje en la versión de clase:

| Aspecto | Python | JavaScript |
|---|---|---|
| Constructor | `__init__(self, ...)` | `constructor(...)` |
| Referencia a la instancia | `self` explícito | `this` implícito |
| Nombres de métodos | `mostrar_info`, `set_promedio` | `mostrarInfo`, `setPromedio` |
| Instanciar | `Estudiante(...)` | `new Estudiante(...)` |
| Error de validación | `ValueError` | `RangeError` |
| Privacidad | Por convención (`_x`) | `#campo` privado real |
| Naturaleza | Modelo de objetos nativo | `class` es azúcar sobre prototipos |

## 3. Tabla comparativa general

| Criterio | Struct / record | Objeto |
|---|---|---|
| **Definición** | Agrupa campos de datos con nombre, sin comportamiento propio | Agrupa datos y métodos; representa una entidad con estado y comportamiento |
| **Mutabilidad** | Depende del lenguaje. En C/C# es una copia mutable. Los `record` de C#/Java y los `frozen` de Python son inmutables | Normalmente mutable; el estado se cambia a través de métodos que pueden controlar el cambio |
| **Tipado** | En lenguajes estáticos el compilador comprueba los campos. En dinámicos son solo anotaciones | Igual que el struct, pero además el tipo incluye los métodos disponibles |
| **Memoria** | En lenguajes con tipos por valor (C, C#, Go), el struct suele vivir en el stack y se copia al asignarlo | Vive en el heap y se maneja por referencia; asignarlo copia la referencia, no el dato |
| **Igualdad** | Por valor (mismos campos, mismo resultado) | Por identidad, salvo que se redefina la comparación |

> **Nota sobre stack/heap en Python y JS:** el criterio de memoria de la fila anterior aplica a lenguajes con tipos por valor. En Python y JavaScript no hay tipos por valor definidos por el usuario: el `dataclass` y el objeto literal viven en el heap y se manejan por referencia, igual que una clase. La diferencia práctica entre struct y objeto ahí es de diseño (datos puros vs comportamiento), no de memoria. Esto se ve en la ejecución de `python/comparativa.py`, punto 4.

## 4. Ejemplo en lenguaje estático (TypeScript)

Se usa TypeScript solo aquí, para ilustrar el tipado estático. El compilador detecta el error antes de ejecutar.

```ts
interface Estudiante {
  nombre: string;
  edad: number;
  promedio: number;
}

const e: Estudiante = { nombre: "Ana Pérez", edad: 20, promedio: 85.5 };
e.promedio = 90;        // correcto
// e.promedio = "alto"; // error de compilación: 'string' no es asignable a 'number'
// e.correo = "x@y.z";  // error de compilación: el campo 'correo' no existe en Estudiante
```

## 5. Ejemplo en lenguaje dinámico (Python)

En Python las anotaciones no se verifican al ejecutar: el código siguiente corre sin error aunque el tipo sea incorrecto.

```python
from dataclasses import dataclass

@dataclass
class Estudiante:
    nombre: str
    edad: int
    promedio: float

e = Estudiante("Ana Pérez", 20, 85.5)
e.promedio = "alto"   # Python no lo impide: la anotación es solo documentación
print(e)              # Estudiante(nombre='Ana Pérez', edad=20, promedio='alto')
```

## 6. Mismo problema como struct y como objeto (Python)

El código completo está en [`python/comparativa.py`](../python/comparativa.py). Resultado de su ejecución:

| Prueba | Struct (`dataclass`) | Objeto (clase) |
|---|---|---|
| Mostrar | `EstudianteStruct(nombre='Ana Pérez', ...)` (automático) | `Ana Pérez \| edad: 20 \| ...` (método `mostrar_info`) |
| Asignar promedio 500 | Lo acepta | Lo rechaza con `ValueError` |
| `==` con mismos datos | `True` (compara por valor) | `False` (compara por identidad) |
| Asignar a otra variable | Comparte el mismo dato | Comparte el mismo dato |

Conclusión: la diferencia real entre ambos en Python es el comportamiento. El struct describe datos y el objeto además los protege y opera sobre ellos. En memoria, ambos se comportan igual (referencia en el heap).
