# Posibles a realizar

Hoja de ruta del proyecto "Importaciones e industria en Argentina": qué se hizo, qué de lo planteado en `posibles.md` ya está
resuelto, qué se puede hacer con los datos que ya hay, qué necesita datos nuevos, y qué mejoras suman al portfolio.
**Última actualización: 20 de septiembre de 2026.**

**Resultado hasta ahora (para tener el contexto):** se cruzaron importaciones 2016-2025, empleo, salarios, producción y
empresas de 16 ramas industriales. Hay una reasignación fuerte de empleo entre ramas (textiles, prendas/calzado y madera/papel
perdieron; alimentos y maquinaria ganaron), el empleo industrial cayó 4,9% y la producción 9,4% desde 2023, pero **no se encontró una
relación simple "más importaciones → menos empleo"**: solo 2 de 24 correlaciones son significativas (la participación de China
se asocia con peor producción y peor salario real) y el modelo de panel no muestra pérdida de empleo por mayor importación. Además,
el resultado del panel **depende de una sola rama** (refinación de petróleo): sin ella, la asociación entre importaciones y empleo pasa a ser positiva y
significativa, lo que vuelve frágil cualquier conclusión.

---

## 0. Qué se hizo desde la versión anterior

| Área | Qué se hizo |
|---|---|
| **Error visible** | Los gráficos sin título mostraban la palabra "undefined". Se corrigió en un solo lugar (`core/tema.py`) |
| **Explicación de cada gráfico** | Cada gráfico tiene ahora su explicación en texto corrido: qué muestra y cómo leerlo, qué se observa (con cifras calculadas de los datos, no escritas a mano) y una aclaración final |
| **Presentación** | Cada gráfico va en un recuadro con borde que contiene título, gráfico y explicación; tamaños pensados para verse completos en una notebook (bloques de 310 a 530 px de alto en una pantalla de 1366 × 660) |
| **Organización de las páginas** | Título con subtítulo, introducción, indicadores, secciones numeradas con encabezado, "Síntesis de la página" al final, ancho de lectura acotado y aire suficiente bajo la barra de pestañas |
| **Advertencias** | Las cajas de color se reemplazaron por texto en cursiva y de color (`nota()`), en el mismo lugar |
| **Modularización** | El dashboard se separó en `dashboard/core/` (datos, formato, consultas, gráficos, tema, componentes) y `dashboard/paginas/` (una página por módulo); `Inicio.py` solo arma la navegación |
| **Página «Método y límites»** | Tabla de fuentes con "para qué se usa", decisiones de método, controles de calidad, límites y glosario |
| **Correcciones de contenido** | Se retiró la afirmación de que las importaciones eran «mucho más volátiles» que las exportaciones (los datos no la sostienen); "p = 0,000" pasó a "p < 0,001"; se incorporó el hallazgo de fragilidad del panel (con y sin refinación) |
| **Verificación** | Se probaron todas las páginas con todas las combinaciones de filtros (las 16 ramas, ambas unidades de importación, todos los años de balanza, 24 combinaciones de exposición y 4 del panel) sin errores, y se midió el tamaño de cada bloque en pantalla de notebook |
| **Documentación** | `explicacion.md`: informe completo para explicar el proyecto oralmente (conceptos desde cero, método, resultados por página, banco de preguntas y repreguntas, guion). `README.md` quedó reducido a cómo ejecutar y estructura de carpetas |

---

## 1. Estado de las 12 ideas de `posibles.md`

| # | Idea | Estado | Dónde está / qué falta |
|---|---|---|---|
| 1 | Importaciones vs. empleo industrial | **Hecho** | Página «Importaciones vs. resultados». Sin asociación negativa consistente |
| 2 | Importaciones vs. producción | **Hecho** | La participación de China se asocia con peor producción (base 2018, ρ = -0,74) |
| 3 | Importaciones vs. salarios reales | **Hecho** | El aumento de China se asocia con peor salario real (base 2023, ρ = -0,54) |
| 4 | Importaciones + empleo + producción | **Hecho** | «Comparador de ramas» (todo junto por rama) |
| 5 | Sectores que perdieron más empleo | **Hecho** | «Empleo y ramas» (mapa de calor, puestos absolutos) |
| 6 | Índice de exposición M / (P + M − X) | **Parcial** | Falta el **valor de la producción** por rama en dólares. Se usaron cuatro sustitutos: crecimiento de importaciones (USD y toneladas) y participación de China (nivel y aumento) |
| 7 | Puestos perdidos por cada +10% de importaciones | **Hecho como estimación** | Modelo de panel: con todas las ramas no es significativo (+2.682 puestos por +10%); sin refinación es positivo y significativo. Mejora posible con la idea A |
| 8 | China vs. empleo argentino | **Hecho por rama** | Falta bajar al detalle por producto (idea C) |
| 9 | Horas trabajadas | **Bloqueado** | No hay datos de horas en los archivos actuales (ver sección 3) |
| 10 | Sectores expuestos vs. no expuestos | **Hecho** | Ramas partidas por la mediana de exposición. Las más expuestas por crecimiento de importaciones evolucionaron **mejor**, no peor |
| 11 | Participación de la producción nacional en el mercado | **Bloqueado** | Requiere producción en valor por rama (ver sección 3) |
| 12 | Dimensión territorial | **Bloqueado** | Requiere empleo por departamento/provincia (ver sección 3) |

---

## 2. Se puede hacer ya, con los datos que hay

Ordenadas por valor para el proyecto. "Esfuerzo": bajo = una tarde, medio = un par de días.

| | Idea | Qué responde | Datos | Esfuerzo |
|---|---|---|---|---|
| C | **Detalle por producto (NCM a 4-6 dígitos)** | ¿Qué productos concretos explotaron en toneladas y en participación de China (calzado, tejidos, electrónica)? Ranking de los 20 productos con mayor crecimiento | Ya descargados (`importaciones/`) | Medio |
| D | **Socios comerciales por rama** | ¿Quién abastece cada rama (Brasil, China, EEUU, Alemania...) y cómo cambió? | Ya procesados (rama x país x año) | Bajo |
| P | **Corrección por comparaciones múltiples** | Con 24 correlaciones se esperan 1-2 «significativas» por azar. ¿Cuáles sobreviven a Bonferroni (p < 0,002) o a la tasa de falsos descubrimientos? Hoy solo sobreviviría la de ρ = -0,74 | Ya procesados | Bajo |
| Q | **Dejar afuera cada rama de a una** | El panel cambia mucho al sacar refinación. ¿Pasa con otras ramas? Muestra qué ramas «mueven» el resultado | Ya procesados | Bajo |
| R | **Ponderar por tamaño de rama** | Un % chico en una rama grande son muchos puestos. Repetir correlaciones y panel ponderando por puestos | Ya procesados | Bajo |
| E | **Pymes vs. grandes empresas** | ¿Perdieron más empleo las empresas chicas? | En el boletín de empleo anual (cuadros por tamaño y tramo de empleo de la empresa) | Medio |
| F | **Dispersión y mediana salarial** | ¿Cayó el salario promedio o el de quien está en el medio? ¿Aumentó la desigualdad dentro de cada rama? | En el boletín de remuneraciones (cuadros de mediana y de dispersión salarial) | Medio |
| G | **Quién pierde el empleo** | Perfil de los puestos que se pierden (edad, sexo, tipo de empresa) | Cuadro de características de los trabajadores del boletín de empleo anual | Medio |
| S | **Composición de las importaciones por intensidad tecnológica** | ¿Cambió el peso de productos primarios, de baja, media y alta tecnología en lo que se importa? Es una vista descriptiva (no por rama) y un primer paso hacia separar tipos de importación | Archivo ya descargado: `exportaciones_importaciones_intensidad_tecnologica.csv` (clasificaciones de Lall y UNCTAD), hoy sin usar | Bajo |
| H | **Agrupar ramas por trayectoria (clustering)** | Sin imponer grupos, ¿qué ramas se mueven parecido en empleo, producción e importaciones? | Ya procesados | Medio |
| I | **Pronóstico por rama** | ¿Hacia dónde va el empleo/producción de cada rama en los próximos trimestres? (modelos de series de tiempo con intervalo) | Ya procesados | Medio |
| J | **Sensibilidad de los resultados** | ¿Cambian las conclusiones si se usa otro año base, otra ventana o Pearson en vez de Spearman? | Ya procesados | Bajo |
| T | **Series mensuales sin suavizar** | Una opción para ver las series sin promedio móvil y detectar el momento exacto de los cambios (hoy se ven con demora) | Ya procesados | Bajo |

---

## 3. Necesita datos nuevos

| | Qué falta | Para qué sirve | Dónde buscarlo (a verificar disponibilidad y formato) |
|---|---|---|---|
| **A** | **Clasificación de productos por uso económico (BEC)**: bienes de consumo / insumos / bienes de capital | Es la mejora más importante: separar las importaciones que **compiten** con la producción local (bienes de consumo terminados) de las que la **complementan** (insumos, maquinaria). Es lo que hoy impide leer bien el signo positivo del modelo de panel (ideas 1 y 7) | Tabla de correspondencia SA/HS ↔ BEC de las Naciones Unidas |
| **B** | **Valor de la producción por rama** (valor bruto de producción o valor agregado) | Calcular la exposición importadora correcta M / (P + M − X) y el consumo aparente (ideas 6 y 11) | Cuentas nacionales / matriz insumo-producto de INDEC |
| **K** | **Empleo por departamento y provincia** | Idea 12: ¿dónde se concentra la pérdida de empleo? | OEDE publica empleo y remuneraciones por departamento (hay que descargarlo) |
| **L** | **Exportaciones por provincia de origen** | Complemento de la idea 12 (solo exportaciones) | Vienen dentro de los zips de exportaciones de comex (archivos `Datos_origen_*`), aún sin usar |
| **M** | **Horas trabajadas** | Idea 9: una empresa puede reducir horas sin despedir | Explorar microdatos de la EPH de INDEC (horas trabajadas por rama de actividad) y publicaciones de coyuntura industrial |
| **N** | **Tipo de cambio real y precios de importación** | Separar el efecto de la competitividad cambiaria del de las importaciones | BCRA (tipo de cambio real multilateral) |
| **O** | **Importaciones antes de 2016** | Alargar el panel (hoy 10 años) para dar más peso a los modelos | El mismo sistema comex tiene datos desde 2002 (hoy se descargan 2016-2025; se ajusta el script) |

---

## 4. Mejoras de la aplicación y del portfolio

### 4.1 Hecho

- **Informe escrito completo** para explicar el proyecto (`explicacion.md`), incluida una versión resumida de una página (sección 1) pensada para alguien no técnico.
- **Aplicación con presentación profesional**: explicaciones por gráfico, jerarquía de títulos, síntesis por página, página de método y glosario.
- **Código modular** (`core/` y `paginas/`).
- **Datos validados** contra los totales oficiales (comercio, empleo y salarios).

### 4.2 Pendiente

| Mejora | Qué implica | Esfuerzo |
|---|---|---|
| **Pruebas automáticas dentro del repositorio** | Hoy la verificación (recorrer todas las páginas y combinaciones de filtros) se hizo con un script temporal que no quedó guardado. Crear una carpeta `tests/` con ese recorrido y con los controles de totales (por ejemplo, que la suma de ramas coincida con el subtotal oficial) para que se puedan correr en cada cambio | Bajo |
| **Un solo comando para regenerar los datos** | Hoy los datos procesados se generan ejecutando tres cuadernos en orden (`notebooks/01`, `02`, `03`). Un script único (`src/`) permitiría regenerar todo y facilitaría actualizar el trabajo con datos nuevos | Medio |
| **Frases fijas a revisar cuando se actualicen los datos** | Los títulos de los hallazgos del Resumen («desde 2023 la industria retrocede», «el salario real se recuperó parcialmente»…) y algunas lecturas (por ejemplo, la del mapa de correlaciones y la de Estados Unidos en la página de Importaciones) están escritas a mano; las cifras se calculan pero esas afirmaciones no cambiarían solas si los datos cambian. Convertirlas en condicionales calculadas | Medio |
| **Etiquetas superpuestas en los gráficos de dispersión** | Con 16 ramas, algunos puntos cercanos se pisan las etiquetas. Mejorar la posición o mostrar el nombre solo al pasar el mouse | Bajo |
| **Probar tema oscuro y pantallas chicas** | El diseño se verificó en pantalla de notebook con tema claro; falta comprobar el tema oscuro y el celular | Bajo |
| **Publicar la aplicación** en Streamlit Community Cloud para tener un link para el CV/LinkedIn (los datos procesados ya son livianos y están listos para subirse). Antes, separar de `requirements.txt` las dependencias que solo sirven para los cuadernos (por ejemplo, `jupyter`) | Medio |
| **Subir el proyecto a GitHub** con los datos crudos de comex fuera del repositorio (se bajan con `src/download_comex.py`) | Bajo |
| **Informe exportable (PDF/HTML)** a partir de `explicacion.md`, para quien no vaya a abrir la aplicación | Bajo |
| **Un README por pestaña** (pedido el 26-09-2026) | Un archivo por pestaña (`docs/pestanas/presentacion.md`, `resumen.md`, `importaciones.md`, `empleo_ramas.md`, `exposicion.md`, `comparador.md`, `conclusiones.md`, `metodo.md`, `datos.md`), bien explicado: para qué sirve y qué pregunta responde; cada sección, gráfico y tarjeta en orden (qué muestra, cómo se lee, qué se observa); cifras clave con la fecha hasta la que llegan; de dónde salen los datos y cómo se calculan; límites; preguntas probables con respuestas. Hoy solo existe la sección 6 de `explicacion.md`, que cubre 6 de las 9 pestañas (faltan Presentación, Conclusiones y Datos) y tiene cifras de la versión anterior | Medio |
| **Mantener `explicacion.md` al día** | Si se actualizan los datos o se agregan análisis, las cifras y las respuestas del banco de preguntas deben revisarse | Continuo |

---

## Orden sugerido

1. **A** (clasificación BEC): es lo que más cambia la calidad de las conclusiones.
2. **P, Q y R** (comparaciones múltiples, dejar afuera cada rama, ponderar por tamaño): son rápidas, usan datos que ya están y fortalecen las conclusiones actuales.
3. **C** y **D**: profundizan sobre China con datos que ya están.
4. **B** para la exposición importadora "de manual".
5. **E**, **F** y **G**: tres ángulos sociales nuevos con datos que ya están descargados.
6. Pruebas automáticas en el repositorio y un comando único para regenerar los datos.
7. Publicar la aplicación y subir el proyecto a GitHub.
