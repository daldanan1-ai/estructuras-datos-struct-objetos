/**
 * Sección 4 — Objetos en JavaScript.
 *
 * A diferencia del objeto literal de `structs.js` (datos puros), aquí
 * `Estudiante` es una clase: agrupa datos y comportamiento (métodos) y
 * controla cómo se modifica su estado.
 */

// 1. Declaración -------------------------------------------------------------
class Estudiante {
  constructor(nombre, edad, promedio) {
    this.nombre = nombre;
    this.edad = edad;
    this.promedio = promedio;
  }

  mostrarInfo() {
    console.log(`${this.nombre} | edad: ${this.edad} | promedio: ${this.promedio}`);
  }

  setPromedio(nuevoPromedio) {
    // el método puede validar antes de cambiar el estado; un objeto literal no
    if (nuevoPromedio < 0 || nuevoPromedio > 100) {
      throw new RangeError("El promedio debe estar entre 0 y 100");
    }
    this.promedio = nuevoPromedio;
  }
}

// 2. Inicialización: 3 instancias almacenadas en un arreglo ------------------
const estudiantes = [
  new Estudiante("Ana Pérez", 20, 85.5),
  new Estudiante("Luis Gómez", 22, 72.0),
  new Estudiante("María Ríos", 19, 91.3),
];

// 3. Recorrido: se llama a mostrarInfo() en cada objeto ----------------------
console.log("== Listado inicial ==");
for (const est of estudiantes) {
  est.mostrarInfo();
}

// 4. Modificación: setPromedio() sobre un estudiante específico --------------
const objetivo = "Luis Gómez";
const encontrado = estudiantes.find((est) => est.nombre === objetivo);
if (encontrado) {
  encontrado.setPromedio(78.4);
}

console.log(`\n== Listado tras modificar el promedio de ${objetivo} ==`);
for (const est of estudiantes) {
  est.mostrarInfo();
}

// 5. Comparativa con el struct/record del bloque anterior --------------------
// - struct (objeto literal): solo datos; se modifica el campo directamente
//   (est.promedio = x) y no hay validación ni comportamiento propio.
// - objeto (clase): además de los datos tiene métodos (mostrarInfo,
//   setPromedio) que encapsulan la lógica y pueden validar el cambio.
// - Tipo: con `class`, `est instanceof Estudiante` es true y el objeto tiene
//   un tipo con nombre; el literal es un objeto anónimo sin tipo propio.
// - Los métodos viven en el prototipo compartido, no se copian en cada
//   instancia.
