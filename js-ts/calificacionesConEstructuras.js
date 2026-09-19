/**
 * Actividad práctica — Analizador de Calificaciones con Struct/Record y Objetos.
 *
 * El analizador original trabajaba con un arreglo de N calificaciones sueltas
 * (enteros 0-100). Aquí el arreglo contiene `Estudiante` (nombre, edad,
 * promedio), y el analizador lee el campo `promedio` de cada uno. Hay dos
 * versiones:
 *
 *   1. struct/record: cada estudiante es un objeto literal { nombre, edad,
 *      promedio }, solo datos. La lógica (mostrar, decidir si aprobó) vive en
 *      funciones aparte.
 *   2. objeto: `Estudiante` es una clase con métodos `mostrarInfo()` y
 *      `aprobado()`. La lógica vive dentro del propio estudiante.
 *
 * El resto del análisis (promedio, mediana, moda, aprobados, histograma) es el
 * mismo para ambas: trabaja sobre la lista de notas extraída de los estudiantes.
 *
 * DECISIÓN — ¿cuál versión es más adecuada aquí?
 *   La versión de OBJETO. La regla "aprobó si promedio >= NOTA_APROBATORIA" y
 *   la forma de mostrar a un estudiante pertenecen al estudiante: con la clase
 *   van juntas con sus datos (`est.aprobado()`, `est.mostrarInfo()`) y si la
 *   regla cambia se modifica en un solo lugar. Además, el analizador no
 *   necesita saber cómo se decide o se muestra. Con el objeto literal esa
 *   lógica queda en funciones sueltas que hay que recordar pasar y mantener
 *   sincronizadas con los datos. El struct es suficiente (y más simple) si solo
 *   se quisieran guardar y leer datos, sin reglas asociadas; como aquí sí hay
 *   reglas (aprobado) y formato, el objeto encaja mejor.
 */
const readline = require("node:readline");

const NOTA_APROBATORIA = 60;
const ANCHO_INTERVALO = 10; // el histograma agrupa las notas en intervalos de 10

// =============================================================================
// Versión 1: Estudiante como struct/record (objeto literal, datos puros)
// =============================================================================
const crearStruct = (nombre, edad, promedio) => ({ nombre, edad, promedio });

const mostrarStruct = (est) =>
  console.log(`${est.nombre} (${est.edad} años) - promedio: ${est.promedio}`);

const aprobadoStruct = (est) => est.promedio >= NOTA_APROBATORIA;

// =============================================================================
// Versión 2: Estudiante como objeto (datos + métodos)
// =============================================================================
class EstudianteObjeto {
  constructor(nombre, edad, promedio) {
    this.nombre = nombre;
    this.edad = edad;
    this.promedio = promedio;
  }

  mostrarInfo() {
    console.log(`${this.nombre} (${this.edad} años) - promedio: ${this.promedio}`);
  }

  aprobado() {
    return this.promedio >= NOTA_APROBATORIA;
  }
}

// =============================================================================
// Adaptador: le dice al analizador cómo crear, mostrar y evaluar a un
// estudiante según la versión elegida, para no duplicar el análisis.
// =============================================================================
const VERSION_STRUCT = {
  nombre: "struct/record",
  crear: crearStruct,
  mostrar: mostrarStruct,
  aprobado: aprobadoStruct,
};
const VERSION_OBJETO = {
  nombre: "objeto",
  crear: (nombre, edad, promedio) => new EstudianteObjeto(nombre, edad, promedio),
  mostrar: (est) => est.mostrarInfo(),
  aprobado: (est) => est.aprobado(),
};

// Datos de ejemplo (ficticios): [nombre, edad, promedio]
const EJEMPLO = [
  ["Ana Pérez", 20, 85],
  ["Luis Gómez", 22, 72],
  ["María Ríos", 19, 91],
  ["Carlos Díaz", 21, 58],
  ["Sofía Torres", 23, 72],
  ["Juan Pardo", 20, 45],
  ["Laura Mejía", 22, 100],
  ["Pedro Salas", 24, 60],
  ["Camila Ruiz", 19, 72],
  ["Valentina Cruz", 21, 38],
];

// =============================================================================
// Estadísticas: trabajan sobre la lista de notas (el campo `promedio`)
// =============================================================================
const promedioGeneral = (notas) => notas.reduce((a, b) => a + b, 0) / notas.length;

function mediana(notas) {
  const ordenadas = [...notas].sort((a, b) => a - b);
  const mitad = Math.floor(ordenadas.length / 2);
  if (ordenadas.length % 2 === 1) return ordenadas[mitad];
  return (ordenadas[mitad - 1] + ordenadas[mitad]) / 2;
}

/** Devuelve las notas más repetidas ([] si todas aparecen una sola vez). */
function moda(notas) {
  const conteo = new Map();
  for (const nota of notas) conteo.set(nota, (conteo.get(nota) ?? 0) + 1);
  const maximo = Math.max(...conteo.values());
  if (maximo === 1) return [];
  return [...conteo.entries()]
    .filter(([, veces]) => veces === maximo)
    .map(([nota]) => nota)
    .sort((a, b) => a - b);
}

/** Cuenta cuántas notas caen en cada intervalo (0-9, 10-19, ..., 90-100). */
function frecuencias(notas) {
  const cantidad = 100 / ANCHO_INTERVALO;
  const conteo = new Array(cantidad).fill(0);
  for (const nota of notas) {
    conteo[Math.min(Math.floor(nota / ANCHO_INTERVALO), cantidad - 1)] += 1;
  }
  return conteo;
}

// =============================================================================
// Salida por pantalla
// =============================================================================
function listar(estudiantes, version) {
  console.log("\n== Listado de estudiantes ==");
  for (const est of estudiantes) version.mostrar(est);
}

function mostrarEstadisticas(estudiantes, version) {
  const notas = estudiantes.map((est) => est.promedio);
  const total = estudiantes.length;
  const aprobados = estudiantes.filter((est) => version.aprobado(est)).length;
  const reprobados = total - aprobados;

  console.log("\n== Estadísticas ==");
  console.log(`Estudiantes: ${total}`);
  console.log(`Promedio general: ${promedioGeneral(notas).toFixed(2)}`);
  console.log(`Mediana: ${mediana(notas)}`);

  const modas = moda(notas);
  if (modas.length > 0) {
    // se muestra quién obtuvo cada nota modal
    for (const nota of modas) {
      const nombres = estudiantes
        .filter((est) => est.promedio === nota)
        .map((est) => est.nombre)
        .join(", ");
      console.log(`Moda: ${nota} (${nombres})`);
    }
  } else {
    console.log("Moda: no hay (ninguna nota se repite)");
  }

  console.log(`Aprobados (>= ${NOTA_APROBATORIA}): ${aprobados} (${((aprobados / total) * 100).toFixed(1)}%)`);
  console.log(`Reprobados (< ${NOTA_APROBATORIA}): ${reprobados} (${((reprobados / total) * 100).toFixed(1)}%)`);
}

function mostrarHistograma(estudiantes) {
  const conteo = frecuencias(estudiantes.map((est) => est.promedio));
  console.log("\n== Histograma de frecuencias ==");
  conteo.forEach((veces, i) => {
    const inicio = i * ANCHO_INTERVALO;
    const fin = i === conteo.length - 1 ? 100 : inicio + ANCHO_INTERVALO - 1;
    const rango = `${String(inicio).padStart(3)}-${String(fin).padEnd(3)}`;
    console.log(`${rango} | ${"#".repeat(veces)} ${veces || ""}`.trimEnd());
  });
}

// =============================================================================
// Búsquedas (siempre muestran el nombre junto a la calificación)
// =============================================================================
function buscarPorNombre(estudiantes, texto, version) {
  const coincidencias = estudiantes.filter((est) =>
    est.nombre.toLowerCase().includes(texto.toLowerCase())
  );
  console.log(`\n== Búsqueda por nombre: '${texto}' ==`);
  if (coincidencias.length === 0) console.log("Sin resultados.");
  for (const est of coincidencias) version.mostrar(est);
}

function buscarPorNota(estudiantes, nota, version) {
  const coincidencias = estudiantes.filter((est) => est.promedio === nota);
  console.log(`\n== Búsqueda por calificación: ${nota} ==`);
  if (coincidencias.length === 0) console.log("Sin resultados.");
  for (const est of coincidencias) version.mostrar(est);
}

// =============================================================================
// Entrada de datos (lee una línea por vez; funciona con teclado y con tuberías)
// =============================================================================
const rl = readline.createInterface({ input: process.stdin });
const lineas = rl[Symbol.asyncIterator]();

async function preguntar(mensaje) {
  process.stdout.write(mensaje);
  const { value, done } = await lineas.next();
  if (done) throw new Error("EOF");
  return value.trim();
}

async function leerNumero(mensaje, entero, minimo, maximo) {
  while (true) {
    const texto = (await preguntar(mensaje)).replace(",", ".");
    const valor = Number(texto);
    if (texto === "" || Number.isNaN(valor) || (entero && !Number.isInteger(valor))) {
      console.log("  Valor no válido, intenta de nuevo.");
    } else if (valor < minimo || valor > maximo) {
      console.log(`  Debe estar entre ${minimo} y ${maximo}.`);
    } else {
      return valor;
    }
  }
}

async function elegirOpcion(mensaje, validas) {
  while (true) {
    const opcion = await preguntar(mensaje);
    if (validas.includes(opcion)) return opcion;
    console.log("  Opción no válida.");
  }
}

async function leerEstudiantes(version) {
  const n = await leerNumero("¿Cuántos estudiantes? ", true, 1, 1000);
  const estudiantes = [];
  for (let i = 1; i <= n; i++) {
    console.log(`Estudiante ${i}/${n}`);
    let nombre = "";
    while (!nombre) nombre = await preguntar("  Nombre: ");
    const edad = await leerNumero("  Edad: ", true, 1, 120);
    const promedio = await leerNumero("  Calificación (0-100): ", false, 0, 100);
    estudiantes.push(version.crear(nombre, edad, promedio));
  }
  return estudiantes;
}

const cargarEjemplo = (version) =>
  EJEMPLO.map(([nombre, edad, promedio]) => version.crear(nombre, edad, promedio));

// =============================================================================
// Programa principal
// =============================================================================
async function main() {
  console.log("=== Analizador de Calificaciones (Struct/Record y Objetos) ===");
  console.log("Versión del estudiante:\n  1. struct/record (objeto literal)\n  2. objeto (clase)");
  const version = (await elegirOpcion("Elige (1-2): ", ["1", "2"])) === "1" ? VERSION_STRUCT : VERSION_OBJETO;

  console.log("\nDatos:\n  1. Ingresar por teclado\n  2. Cargar lista de ejemplo");
  const estudiantes =
    (await elegirOpcion("Elige (1-2): ", ["1", "2"])) === "1"
      ? await leerEstudiantes(version)
      : cargarEjemplo(version);
  console.log(`\nVersión en uso: ${version.nombre} — ${estudiantes.length} estudiantes cargados.`);

  while (true) {
    console.log(
      "\nMenú:\n  1. Listado\n  2. Estadísticas\n  3. Histograma\n" +
        "  4. Buscar por nombre\n  5. Buscar por calificación\n  0. Salir"
    );
    const opcion = await elegirOpcion("Elige: ", ["0", "1", "2", "3", "4", "5"]);
    if (opcion === "0") {
      console.log("Hasta luego.");
      return;
    }
    if (opcion === "1") listar(estudiantes, version);
    else if (opcion === "2") mostrarEstadisticas(estudiantes, version);
    else if (opcion === "3") mostrarHistograma(estudiantes);
    else if (opcion === "4") buscarPorNombre(estudiantes, await preguntar("Nombre a buscar: "), version);
    else if (opcion === "5") buscarPorNota(estudiantes, await leerNumero("Calificación a buscar: ", false, 0, 100), version);
  }
}

main()
  .catch((error) => {
    if (error.message === "EOF") console.log("\nEntrada finalizada.");
    else throw error;
  })
  .finally(() => rl.close());
