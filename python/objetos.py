"""Sección 4 — Objetos en Python.

A diferencia del struct/record de `structs.py` (datos puros), aquí `Estudiante`
es una clase: agrupa datos y comportamiento (métodos) y controla cómo se
modifica su estado.
"""
from __future__ import annotations


# 1. Declaración -------------------------------------------------------------
class Estudiante:
    """Objeto: datos + métodos que operan sobre esos datos."""

    def __init__(self, nombre: str, edad: int, promedio: float) -> None:
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio

    def mostrar_info(self) -> None:
        # equivalente a mostrarInfo() del enunciado (snake_case en Python)
        print(f"{self.nombre} | edad: {self.edad} | promedio: {self.promedio}")

    def set_promedio(self, nuevo_promedio: float) -> None:
        # el método puede validar antes de cambiar el estado; un struct no
        if not 0 <= nuevo_promedio <= 100:
            raise ValueError("El promedio debe estar entre 0 y 100")
        self.promedio = nuevo_promedio


def main() -> None:
    # 2. Inicialización: 3 instancias almacenadas en una lista ---------------
    estudiantes: list[Estudiante] = [
        Estudiante("Ana Pérez", 20, 85.5),
        Estudiante("Luis Gómez", 22, 72.0),
        Estudiante("María Ríos", 19, 91.3),
    ]

    # 3. Recorrido: se llama a mostrar_info() en cada objeto -----------------
    print("== Listado inicial ==")
    for est in estudiantes:
        est.mostrar_info()

    # 4. Modificación: set_promedio() sobre un estudiante específico ---------
    objetivo = "Luis Gómez"
    for est in estudiantes:
        if est.nombre == objetivo:
            est.set_promedio(78.4)
            break

    print("\n== Listado tras modificar el promedio de", objetivo, "==")
    for est in estudiantes:
        est.mostrar_info()

    # 5. Comparativa con el struct/record del bloque anterior ----------------
    # - struct (dataclass): solo datos; se modifica el campo directamente
    #   (est.promedio = x) y no hay validación ni comportamiento propio.
    # - objeto (clase): además de los datos tiene métodos (mostrar_info,
    #   set_promedio) que encapsulan la lógica y pueden validar el cambio.
    # - Salida: el dataclass imprime su __repr__ automático; aquí el formato
    #   lo decide el método mostrar_info().


if __name__ == "__main__":
    main()
