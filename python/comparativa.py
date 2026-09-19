"""Sección 5 — Mismo problema (`Estudiante`) como struct/record y como objeto.

Ambas versiones en Python, una al lado de la otra, para señalar las
diferencias directamente en código.
"""
from __future__ import annotations

from dataclasses import dataclass


# --- Versión struct/record: datos puros --------------------------------------
@dataclass
class EstudianteStruct:
    nombre: str
    edad: int
    promedio: float


# --- Versión objeto: datos + comportamiento ----------------------------------
class EstudianteObjeto:
    def __init__(self, nombre: str, edad: int, promedio: float) -> None:
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio

    def mostrar_info(self) -> None:
        print(f"{self.nombre} | edad: {self.edad} | promedio: {self.promedio}")

    def set_promedio(self, nuevo: float) -> None:
        if not 0 <= nuevo <= 100:
            raise ValueError("El promedio debe estar entre 0 y 100")
        self.promedio = nuevo


def main() -> None:
    s = EstudianteStruct("Ana Pérez", 20, 85.5)
    o = EstudianteObjeto("Ana Pérez", 20, 85.5)

    # 1. Comportamiento: el objeto sabe mostrarse; el struct solo tiene datos.
    print("1) Mostrar")
    print("   struct:", s)  # __repr__ generado por dataclass
    print("   objeto: ", end="")
    o.mostrar_info()  # método propio

    # 2. Modificación y validación: el struct acepta cualquier valor.
    print("\n2) Asignar un promedio inválido (500)")
    s.promedio = 500
    print("   struct acepta:", s.promedio)
    try:
        o.set_promedio(500)
    except ValueError as error:
        print("   objeto rechaza:", error)

    # 3. Igualdad: el dataclass compara por valor; la clase, por identidad.
    print("\n3) Igualdad de dos estudiantes con los mismos datos")
    print("   struct  ==:", EstudianteStruct("Luis", 22, 72.0) == EstudianteStruct("Luis", 22, 72.0))
    print("   objeto  ==:", EstudianteObjeto("Luis", 22, 72.0) == EstudianteObjeto("Luis", 22, 72.0))

    # 4. Copia por asignación: en Python ambos son referencias (viven en el heap).
    print("\n4) Asignar a otra variable (no copia: comparten el mismo dato)")
    s2 = s
    s2.promedio = 10
    print("   struct: s.promedio =", s.promedio)  # cambió también en s
    o2 = o
    o2.set_promedio(10)
    print("   objeto: o.promedio =", o.promedio)  # cambió también en o


if __name__ == "__main__":
    main()
