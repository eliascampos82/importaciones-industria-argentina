# Evaluación final del proyecto

**«Importaciones e industria en Argentina, 2016-2026»** · Autor: Francisco Elias Campos · Evaluación: 11 de octubre de 2026

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**

---

## Veredicto

**Es un trabajo de análisis de datos completo, riguroso y bien comunicado, de nivel semi-senior, y es un proyecto de portfolio sólido.**

Formula una pregunta relevante, que además se puede responder con los datos disponibles, y la responde en el orden en que la plantea. Muestra cuánto se sostiene la respuesta y separa lo que los datos permiten afirmar de lo que no.

La base está a nivel profesional: los datos son oficiales y están validados contra los totales publicados. Encima de esa base hay un método honesto (una medida principal, una ventana común, corrección por comparaciones múltiples y la separación de las importaciones por uso económico) y una aplicación que cuenta lo mismo en todas sus piezas.

**Nota: 8 / 10.** Al inicio de la revisión era 7 / 10.

---

## La respuesta que da el trabajo

**No.** Entre 2018 y 2025 la industria produjo 5,6% menos y pagó salarios reales 7,5% más bajos, pero esas pérdidas no se concentraron donde más crecieron las importaciones. En general fue al revés:

| Ramas (8 y 8) | Puestos de trabajo, 2018 → 2025 |
|---|---|
| Donde las importaciones crecieron más | **+27.072** |
| Donde crecieron menos | **−18.152** |

- **Por qué al revés:** al separar lo importado según su uso aparece el mecanismo. El crecimiento de las importaciones de **insumos** va junto con el del empleo (ρ = +0,78, resiste la corrección). El de **bienes de consumo**, que son los que compiten, no muestra relación (ρ = 0,01).
- **La excepción:** prendas y textiles, donde entraron muchas más toneladas y se perdió empleo.
- **El alcance:** el trabajo presenta todo esto como una **coincidencia medida en 16 ramas, no como un efecto causal**, que es la lectura correcta.

---

## Qué lo hace un trabajo profesional

| Práctica | Evidencia en el proyecto |
|---|---|
| **Datos verificados, no supuestos** | Comercio exterior idéntico a los totales de control del INDEC en los 10 años; la suma de las 16 ramas de empleo coincide con el subtotal oficial en todos los trimestres; el salario ponderado está entre 0,99 y 1,00 de la serie oficial |
| **Integración de fuentes difíciles** | Tres clasificaciones distintas (NCM, CIIU, IPI) llevadas a 16 ramas con criterios escritos; descarga automatizada de un sitio sin botón de descarga |
| **Una pregunta que el diseño puede responder** | Pregunta de coincidencia y no de causa; una medida principal elegida por la pregunta, antes de mirar los resultados |
| **Comparaciones justas** | Ventana común 2018 → 2025 para importaciones y resultados; promedios de 12 meses para evitar la estacionalidad y el aguinaldo |
| **Robustez en lugar de un solo número** | Tres medidas de importaciones, intervalos por bootstrap, p-valor corregido (Benjamini-Hochberg), repetición sacando cada rama de a una, ponderación por tamaño y control de la tendencia previa |
| **Ir al mecanismo** | Clasificación de 99,9% de lo importado por uso económico (BEC, Naciones Unidas), que explica el resultado en lugar de solo describirlo |
| **Honestidad sobre los límites** | Dice qué no se puede afirmar, incluido que las importaciones «no afectaron», y presenta el resultado que no confirma la hipótesis popular |
| **Reproducibilidad** | Un comando regenera todos los datos desde los archivos originales y produce exactamente los mismos resultados; 46 pruebas automáticas (datos y pestañas); versiones fijadas |
| **Comunicación pensada para cada audiencia** | Una aplicación de 9 pestañas, un informe de 8 hojas A4, una presentación y una guía para exponer, todos con la misma pregunta y la misma respuesta; cada cifra dice hasta cuándo llega |

---

## Nota por dimensión

| Dimensión | Al inicio | Al cierre | Qué cambió |
|---|---|---|---|
| Pregunta y relevancia | 8 | **9** | Pregunta reformulada para que el diseño pueda responderla |
| Obtención y limpieza de datos | 9 | **9** | Se sumó la clasificación por uso económico, validada contra los totales |
| Análisis descriptivo | 8 | **8,5** | Ventana común y la separación entre consumo, insumos y capital |
| Método para responder la pregunta | 5 | **7** | Medida principal, grupos, uso económico y control de la tendencia previa |
| Inferencia estadística | 4,5 | **6,5** | p corregido, intervalos por bootstrap, sensibilidad por rama y ponderación |
| Honestidad y límites | 9 | **9** | Se mantiene |
| Comunicación | 8 | **8,5** | Todas las piezas cuentan la misma respuesta, en el mismo orden |
| Código y reproducibilidad | 5,5 | **8** | Pipeline de un comando, 46 pruebas, versiones fijas y control de versiones |
| **Global** | **7** | **8** | |

---

## Lo que el trabajo todavía no es (y está bien que no lo sea)

- **No es un análisis causal.** Mide coincidencias. Para afirmar que las importaciones provocaron o no pérdidas haría falta una fuente de variación externa, por ejemplo las ventas de China a otros países parecidos o la apertura de 2024. Es un proyecto aparte, y el trabajo lo dice.
- **Tiene poco poder estadístico.** Con 16 ramas solo se distinguen relaciones grandes, y el trabajo lo declara.
- **Faltan dos cosas que dependen del autor:** subir el repositorio a GitHub y publicar la aplicación (los pasos están en `pasos_a_seguir.md`, sección 4).

Ninguna de las tres le quita valor a lo hecho; son el siguiente escalón.

---

## Cómo presentarlo

**En una línea (CV o LinkedIn):**
> Analicé con datos oficiales (INDEC, Ministerio de Trabajo) si la industria argentina perdió empleo donde más crecieron las importaciones: 16 ramas, 1,1 millones de registros de comercio exterior validados contra totales oficiales, clasificación por uso económico y una aplicación interactiva en Streamlit.

**En una respuesta de entrevista:**
> «La respuesta fue que no: las ramas donde más crecieron las importaciones ganaron empleo. Separando por uso económico vi por qué: lo que crece con el empleo son los insumos, y con los bienes de consumo no hay relación. La excepción son prendas y textiles. Lo presento como una coincidencia, no como un efecto, y explico qué haría falta para hablar de causas.»

---

## Conclusión

El autor demuestra las tres capacidades que definen a un analista de datos profesional:
- **conseguir y validar datos difíciles;**
- **responder una pregunta con un método que se puede defender;**
- **comunicar el resultado, y sus límites, a quien no sabe del tema.**

El proyecto está terminado y listo para mostrarse.

---

*Evaluación realizada por Claude (asistente de inteligencia artificial de Anthropic), con el rol de analista de datos senior. Se basa en la lectura del código, los datos procesados y los documentos del proyecto, en pruebas de robustez propias (`pregunta_central.py`, `pruebas_robustez.py`) y en la verificación del dashboard en el navegador. Las cifras de este documento salen de `data/processed/` al 11-10-2026.*
