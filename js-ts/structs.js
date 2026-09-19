/**
 * Sección 3 — Struct/Record en JavaScript.
 *
 * JavaScript no tiene un `struct` nativo. Lo más cercano es un objeto literal
 * simple ({ clave: valor }): es un contenedor de datos con campos con nombre,
 * sin clase ni métodos, igual que un struct de C/C#. En TypeScript se declara
 * su "forma" con una `interface` (o `type`), que solo existe en tiempo de
 * compilación y describe los campos; en ejecución sigue siendo un objeto
 * literal. Por eso es la representación más cercana a un struct: datos puros,
 * campos con nombre, sin comportamiento asociado.
 *
 * Equivalente en TypeScript (sintaxis, no se ejecuta aquí):
 *   interface Estudiante { nombre: string; edad: number; promedio: number }
 */

// 1. Declaración + 2. Inicialización: 3 instancias con datos ficticios ------
// (en JS la "declaración" es implícita: la forma la define el propio literal)
const e1 = { nombre: "Ana Pérez", edad: 20, promedio: 85.5 };
const e2 = { nombre: "Luis Gómez", edad: 22, promedio: 72.0 };
const e3 = { nombre: "María Ríos", edad: 19, promedio: 91.3 };

// 3. Recorrido: se guardan en un arreglo y se recorren -----------------------
const estudiantes = [e1, e2, e3];

console.log("== Listado inicial ==");
for (const est of estudiantes) {
  console.log(`${est.nombre} | edad: ${est.edad} | promedio: ${est.promedio}`);
}

// 4. Modificación: cambiar el promedio de un estudiante específico -----------
const objetivo = "Luis Gómez";
const encontrado = estudiantes.find((est) => est.nombre === objetivo);
if (encontrado) {
  encontrado.promedio = 78.4; // los objetos literales son mutables
}

console.log(`\n== Listado tras modificar el promedio de ${objetivo} ==`);
for (const est of estudiantes) {
  console.log(est); // console.log imprime el objeto con sus campos
}
