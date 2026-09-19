"""Actividad práctica — Analizador de Calificaciones con Struct/Record y Objetos.

El analizador original trabajaba con un arreglo de N calificaciones sueltas
(enteros 0-100). Aquí el arreglo contiene `Estudiante` (nombre, edad, promedio),
y el analizador lee el campo `promedio` de cada uno. Hay dos versiones:

  1. struct/record: `Estudiante` es un dataclass, solo datos. La lógica
     (mostrar, decidir si aprobó) vive en funciones aparte.
  2. objeto: `Estudiante` es una clase con métodos `mostrar_info()` y
     `aprobado()`. La lógica vive dentro del propio estudiante.

El resto del análisis (promedio, mediana, moda, aprobados, histograma) es el
mismo para ambas: trabaja sobre la lista de notas extraída de los estudiantes.

DECISIÓN — ¿cuál versión es más adecuada aquí?
  La versión de OBJETO. La regla "aprobó si promedio >= NOTA_APROBATORIA" y la
  forma de mostrar a un estudiante pertenecen al estudiante: con la clase van
  juntas con sus datos (`est.aprobado()`, `est.mostrar_info()`) y si la regla
  cambia se modifica en un solo lugar. Además, el analizador no necesita saber
  cómo se decide o se muestra. Con el struct esa lógica queda en funciones
  sueltas que hay que recordar pasar y mantener sincronizadas con los datos.
  El struct es suficiente (y más simple) si solo se quisieran guardar y leer
  datos, sin reglas asociadas; como aquí sí hay reglas (aprobado) y formato,
  el objeto encaja mejor.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Callable

NOTA_APROBATORIA = 60
ANCHO_INTERVALO = 10  # el histograma agrupa las notas en intervalos de 10


# =============================================================================
# Versión 1: Estudiante como struct/record (datos puros, sin comportamiento)
# =============================================================================
@dataclass
class EstudianteStruct:
    nombre: str
    edad: int
    promedio: float


def mostrar_struct(est: EstudianteStruct) -> None:
    print(f"{est.nombre} ({est.edad} años) - promedio: {est.promedio:g}")


def aprobado_struct(est: EstudianteStruct) -> bool:
    return est.promedio >= NOTA_APROBATORIA


# =============================================================================
# Versión 2: Estudiante como objeto (datos + métodos)
# =============================================================================
class EstudianteObjeto:
    def __init__(self, nombre: str, edad: int, promedio: float) -> None:
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio

    def mostrar_info(self) -> None:
        print(f"{self.nombre} ({self.edad} años) - promedio: {self.promedio:g}")

    def aprobado(self) -> bool:
        return self.promedio >= NOTA_APROBATORIA


# =============================================================================
# Adaptador: le dice al analizador cómo crear, mostrar y evaluar a un estudiante
# según la versión elegida, para no duplicar el análisis.
# =============================================================================
@dataclass
class Version:
    nombre: str
    crear: Callable[[str, int, float], object]
    mostrar: Callable[[object], None]
    aprobado: Callable[[object], bool]


VERSION_STRUCT = Version("struct/record", EstudianteStruct, mostrar_struct, aprobado_struct)
VERSION_OBJETO = Version(
    "objeto",
    EstudianteObjeto,
    lambda est: est.mostrar_info(),
    lambda est: est.aprobado(),
)

# Datos de ejemplo (ficticios): (nombre, edad, promedio)
EJEMPLO = [
    ("Ana Pérez", 20, 85),
    ("Luis Gómez", 22, 72),
    ("María Ríos", 19, 91),
    ("Carlos Díaz", 21, 58),
    ("Sofía Torres", 23, 72),
    ("Juan Pardo", 20, 45),
    ("Laura Mejía", 22, 100),
    ("Pedro Salas", 24, 60),
    ("Camila Ruiz", 19, 72),
    ("Valentina Cruz", 21, 38),
]


# =============================================================================
# Estadísticas: trabajan sobre la lista de notas (el campo `promedio`)
# =============================================================================
def promedio_general(notas: list[float]) -> float:
    return sum(notas) / len(notas)


def mediana(notas: list[float]) -> float:
    ordenadas = sorted(notas)
    mitad = len(ordenadas) // 2
    if len(ordenadas) % 2 == 1:
        return ordenadas[mitad]
    return (ordenadas[mitad - 1] + ordenadas[mitad]) / 2


def moda(notas: list[float]) -> list[float]:
    """Devuelve las notas más repetidas ([] si todas aparecen una sola vez)."""
    conteo = Counter(notas)
    maximo = max(conteo.values())
    if maximo == 1:
        return []
    return sorted(nota for nota, veces in conteo.items() if veces == maximo)


def frecuencias(notas: list[float]) -> list[int]:
    """Cuenta cuántas notas caen en cada intervalo (0-9, 10-19, ..., 90-100)."""
    cantidad = 100 // ANCHO_INTERVALO
    conteo = [0] * cantidad
    for nota in notas:
        conteo[min(int(nota // ANCHO_INTERVALO), cantidad - 1)] += 1
    return conteo


# =============================================================================
# Salida por pantalla
# =============================================================================
def listar(estudiantes: list, version: Version) -> None:
    print("\n== Listado de estudiantes ==")
    for est in estudiantes:
        version.mostrar(est)


def mostrar_estadisticas(estudiantes: list, version: Version) -> None:
    notas = [est.promedio for est in estudiantes]
    total = len(estudiantes)
    aprobados = sum(1 for est in estudiantes if version.aprobado(est))
    reprobados = total - aprobados

    print("\n== Estadísticas ==")
    print(f"Estudiantes: {total}")
    print(f"Promedio general: {promedio_general(notas):.2f}")
    print(f"Mediana: {mediana(notas):g}")

    modas = moda(notas)
    if modas:
        # se muestra quién obtuvo cada nota modal
        for nota in modas:
            nombres = ", ".join(est.nombre for est in estudiantes if est.promedio == nota)
            print(f"Moda: {nota:g} ({nombres})")
    else:
        print("Moda: no hay (ninguna nota se repite)")

    print(f"Aprobados (>= {NOTA_APROBATORIA}): {aprobados} ({aprobados / total * 100:.1f}%)")
    print(f"Reprobados (< {NOTA_APROBATORIA}): {reprobados} ({reprobados / total * 100:.1f}%)")


def mostrar_histograma(estudiantes: list) -> None:
    notas = [est.promedio for est in estudiantes]
    conteo = frecuencias(notas)
    print("\n== Histograma de frecuencias ==")
    for i, veces in enumerate(conteo):
        inicio = i * ANCHO_INTERVALO
        fin = 100 if i == len(conteo) - 1 else inicio + ANCHO_INTERVALO - 1
        print(f"{inicio:>3}-{fin:<3} | {'#' * veces} {veces if veces else ''}".rstrip())


# =============================================================================
# Búsquedas (siempre muestran el nombre junto a la calificación)
# =============================================================================
def buscar_por_nombre(estudiantes: list, texto: str, version: Version) -> None:
    coincidencias = [est for est in estudiantes if texto.casefold() in est.nombre.casefold()]
    print(f"\n== Búsqueda por nombre: '{texto}' ==")
    if not coincidencias:
        print("Sin resultados.")
    for est in coincidencias:
        version.mostrar(est)


def buscar_por_nota(estudiantes: list, nota: float, version: Version) -> None:
    coincidencias = [est for est in estudiantes if est.promedio == nota]
    print(f"\n== Búsqueda por calificación: {nota:g} ==")
    if not coincidencias:
        print("Sin resultados.")
    for est in coincidencias:
        version.mostrar(est)


# =============================================================================
# Entrada de datos
# =============================================================================
def leer_numero(mensaje: str, tipo: type, minimo: float, maximo: float):
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            valor = tipo(texto)
        except ValueError:
            print("  Valor no válido, intenta de nuevo.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"  Debe estar entre {minimo:g} y {maximo:g}.")


def leer_estudiantes(version: Version) -> list:
    n = leer_numero("¿Cuántos estudiantes? ", int, 1, 1000)
    estudiantes = []
    for i in range(1, n + 1):
        print(f"Estudiante {i}/{n}")
        nombre = ""
        while not nombre:
            nombre = input("  Nombre: ").strip()
        edad = leer_numero("  Edad: ", int, 1, 120)
        promedio = leer_numero("  Calificación (0-100): ", float, 0, 100)
        estudiantes.append(version.crear(nombre, edad, promedio))
    return estudiantes


def cargar_ejemplo(version: Version) -> list:
    return [version.crear(nombre, edad, promedio) for nombre, edad, promedio in EJEMPLO]


def elegir_opcion(mensaje: str, validas: list[str]) -> str:
    while True:
        opcion = input(mensaje).strip()
        if opcion in validas:
            return opcion
        print("  Opción no válida.")


# =============================================================================
# Programa principal
# =============================================================================
def main() -> None:
    print("=== Analizador de Calificaciones (Struct/Record y Objetos) ===")
    print("Versión del estudiante:\n  1. struct/record (dataclass)\n  2. objeto (clase)")
    version = VERSION_STRUCT if elegir_opcion("Elige (1-2): ", ["1", "2"]) == "1" else VERSION_OBJETO

    print("\nDatos:\n  1. Ingresar por teclado\n  2. Cargar lista de ejemplo")
    if elegir_opcion("Elige (1-2): ", ["1", "2"]) == "1":
        estudiantes = leer_estudiantes(version)
    else:
        estudiantes = cargar_ejemplo(version)
    print(f"\nVersión en uso: {version.nombre} — {len(estudiantes)} estudiantes cargados.")

    while True:
        print(
            "\nMenú:\n  1. Listado\n  2. Estadísticas\n  3. Histograma\n"
            "  4. Buscar por nombre\n  5. Buscar por calificación\n  0. Salir"
        )
        opcion = elegir_opcion("Elige: ", ["0", "1", "2", "3", "4", "5"])
        if opcion == "0":
            print("Hasta luego.")
            return
        if opcion == "1":
            listar(estudiantes, version)
        elif opcion == "2":
            mostrar_estadisticas(estudiantes, version)
        elif opcion == "3":
            mostrar_histograma(estudiantes)
        elif opcion == "4":
            buscar_por_nombre(estudiantes, input("Nombre a buscar: ").strip(), version)
        elif opcion == "5":
            buscar_por_nota(estudiantes, leer_numero("Calificación a buscar: ", float, 0, 100), version)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada finalizada.")
