// Configuración inicial del bulto actual en la mesa de empaque
let bultoActivo = {
  numeroSecuencial: 1,
  pesoAcumuladoKG: 0.0,
  articulos: [],
};

// Constante de restricción física (Regla de negocio)
const LIMITE_PESO_MAXIMO = 25.0;

/**
 * Registra el impacto en el bulto cuando la pistola realiza una lectura correcta
 * @param {number} gramajeProducto - Peso unitario en gramos configurado en el catálogo
 * @param {number} multiplicadorEmpaque - Equivalencia según el código escaneado (Individual=1, Inner=N, Master=M)
 */
function procesarLecturaPistola(gramajeProducto, multiplicadorEmpaque) {
  // 1. Transformamos los gramos ingresados a Kilogramos
  let pesoIngresadoKG = (gramajeProducto * multiplicadorEmpaque) / 1000;

  // 2. Acumulamos el peso en la estructura local del navegador (IndexedDB / PWA Cache)
  bultoActivo.pesoAcumuladoKG += pesoIngresadoKG;

  // 3. Capturamos el componente UI de Bootstrap para actualizarlo dinámicamente
  const indicadorPesoUI = document.getElementById("indicador-peso-bulto");

  if (indicadorPesoUI) {
    indicadorPesoUI.innerText = `${bultoActivo.pesoAcumuladoKG.toFixed(2)} kg / ${LIMITE_PESO_MAXIMO} kg`;

    // 4. LÓGICA DE ALERTA NO BLOQUEANTE: Cambia el color visual según el peso acumulado
    if (bultoActivo.pesoAcumuladoKG >= LIMITE_PESO_MAXIMO) {
      // El operario superó los 25 kg. Se marca en rojo de alerta, pero sigue operativo.
      indicadorPesoUI.className =
        "badge bg-danger p-3 fs-4 w-100 d-block text-white";
      console.warn(
        "Regla de negocio: El bulto ha sobrepasado los 25 Kg sugeridos. Queda a criterio del operario cerrar la caja.",
      );
    } else if (bultoActivo.pesoAcumuladoKG >= 22.0) {
      // Advertencia preventiva (Color amarillo) cuando está cerca de llenarse
      indicadorPesoUI.className =
        "badge bg-warning p-3 fs-4 w-100 d-block text-dark";
    } else {
      // Rango seguro (Color verde)
      indicadorPesoUI.className =
        "badge bg-success p-3 fs-4 w-100 d-block text-white";
    }
  }
}
