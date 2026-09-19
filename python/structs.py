"""Sección 3 — Struct/Record en Python.

Python no tiene un `struct` nativo como C o C#. Lo más cercano son los
`dataclass` (mutables) y los `NamedTuple` (inmutables): ambos son contenedores
de datos puros, sin comportamiento propio. Aquí se usa `dataclass`, porque el
ejercicio pide modificar el promedio de un estudiante.
"""
from __future__ import annotations

from dataclasses import dataclass


# 1. Declaración -------------------------------------------------------------
@dataclass
class Estudiante:
    """Struct/record: solo datos, sin métodos de negocio."""

    nombre: str
    edad: int
    promedio: float


def main() -> None:
    # 2. Inicialización: 3 instancias con datos ficticios --------------------
    e1 = Estudiante(nombre="Ana Pérez", edad=20, promedio=85.5)
    e2 = Estudiante(nombre="Luis Gómez", edad=22, promedio=72.0)
    e3 = Estudiante(nombre="María Ríos", edad=19, promedio=91.3)

    # 3. Recorrido: se guardan en una lista y se recorren --------------------
    estudiantes: list[Estudiante] = [e1, e2, e3]

    print("== Listado inicial ==")
    for est in estudiantes:
        print(f"{est.nombre} | edad: {est.edad} | promedio: {est.promedio}")

    # 4. Modificación: cambiar el promedio de un estudiante específico -------
    objetivo = "Luis Gómez"
    for est in estudiantes:
        if est.nombre == objetivo:
            est.promedio = 78.4
            break

    print("\n== Listado tras modificar el promedio de", objetivo, "==")
    for est in estudiantes:
        print(est)  # el dataclass genera un __repr__ legible automáticamente


if __name__ == "__main__":
    main()
