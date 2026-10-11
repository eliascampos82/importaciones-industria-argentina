# Revisión profesional del análisis «Importaciones e industria en Argentina, 2016-2026»

Revisión hecha como lo haría un analista de datos senior que recibe el proyecto para evaluarlo: se leyó el código (`src/`, `notebooks/`, `dashboard/`),
los datos procesados (`data/processed/`), los documentos (`README.md`, `explicacion.md`, `posibles_a_realizar.md`) y se corrieron **pruebas de robustez propias**
sobre los resultados. El objetivo no es poner una nota: es que el autor sepa **qué hizo muy bien, qué no se sostiene y qué hacer para que el próximo análisis sea mejor**.

Fecha de la revisión: octubre de 2026. Datos revisados: empleo al 1T 2026, producción a jul-2026, salarios a mar-2026, comercio exterior 2016-2025.
**Actualizada el 11 de octubre de 2026 para la pregunta nueva:**

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**

**Estado al cierre: el trabajo está terminado (versión 1). La evaluación final está en [00_evaluacion_final.md](00_evaluacion_final.md).** Los archivos 01 a 11 y `README_para_terminar.md` describen el proyecto antes de las mejoras de cierre y se conservan como registro.

---

## Cómo leer esta carpeta

| Archivo | Qué tiene | Para cuándo |
|---|---|---|
| [00_evaluacion_final.md](00_evaluacion_final.md) | **La evaluación final del trabajo terminado**: veredicto, nota, qué lo hace profesional y cómo presentarlo | **Para empezar** |
| [README_para_terminar.md](README_para_terminar.md) | **Qué falta, qué sacaría y qué dejaría para después** para cerrar la versión 1, con lista de control | **Para terminar** |
| [01_veredicto.md](01_veredicto.md) | La respuesta a la pregunta, lo alentador y lo desgarrador, y una nota por dimensión | Para empezar |
| [02_fortalezas.md](02_fortalezas.md) | Lo que está a nivel profesional y conviene repetir en cada trabajo | Para saber qué no perder |
| [03_falencias.md](03_falencias.md) | Los problemas, ordenados de más grave a menos grave | Para saber qué corregir primero |
| [04_revision_metodologica.md](04_revision_metodologica.md) | Revisión técnica a fondo: clasificación, medidas de exposición, correlaciones, modelo de panel | Para entender el porqué de cada falencia |
| [05_pruebas_de_robustez.md](05_pruebas_de_robustez.md) | **Parte A:** la respuesta a la pregunta central (2018 → 2025). **Parte B:** robustez de los resultados originales | Para ver la evidencia |
| [06_datos_y_fuentes.md](06_datos_y_fuentes.md) | Calidad, cobertura y límites de los datos | Antes de sumar datos nuevos |
| [07_comunicacion_y_dashboard.md](07_comunicacion_y_dashboard.md) | Cómo se cuenta el análisis: dashboard, documentos, tarjetas | Antes de presentarlo |
| [08_codigo_y_reproducibilidad.md](08_codigo_y_reproducibilidad.md) | Organización del código, pruebas, versiones, reproducibilidad | Antes de publicarlo |
| [09_plan_de_mejora.md](09_plan_de_mejora.md) | Hoja de ruta concreta: qué hacer en 1 día, 1 semana y 1 mes | Para trabajar |
| [10_preguntas_de_un_evaluador.md](10_preguntas_de_un_evaluador.md) | Las preguntas difíciles que te haría un entrevistador o un revisor, y cómo responderlas | Para entrevistas y presentaciones |
| [11_para_seguir_aprendiendo.md](11_para_seguir_aprendiendo.md) | Lecturas y técnicas para dar el siguiente salto | Para crecer |
| [pregunta_central.py](pregunta_central.py) | El script de la parte A de `05` (solo lee `data/processed/`) | `.\.venv\Scripts\python.exe analisis_profesional/pregunta_central.py` |
| [pruebas_robustez.py](pruebas_robustez.py) | El script con las pruebas de `05` (solo lee `data/processed/`, no modifica nada) | Para repetir las pruebas: `.\.venv\Scripts\python.exe analisis_profesional/pruebas_robustez.py` |

---

## El veredicto en cinco líneas

1. **Es un trabajo serio y por encima del promedio de un portfolio**: datos oficiales bien limpiados y validados contra totales, un dashboard cuidado y una honestidad poco común sobre los límites.
2. **La pregunta nueva es la correcta**: pregunta por coincidencia, no por causa, y el diseño puede responderla.
3. **La respuesta es «no»**: entre 2018 y 2025 las pérdidas no se concentraron donde más crecieron las importaciones; en general fue al revés (+27.000 puestos en las 8 ramas donde más crecieron, −18.000 en las otras 8).
   La excepción son **prendas y textiles**. Es una coincidencia, no un efecto, y no es firme: ninguna prueba sobrevive a la corrección y la tendencia previa explica más.
4. **El dashboard y el informe todavía cuentan la respuesta de la pregunta anterior** (China al frente). Es lo principal que hay que corregir.
5. **Para cerrar no hace falta más análisis**: hacen falta 3-4 días de reescribir, ordenar y publicar ([README_para_terminar.md](README_para_terminar.md)). La mejora de fondo para una versión 2 es la clasificación BEC.

**Nota global: 7 / 10, con camino claro a 8** — descriptivo y datos de nivel semi-senior; inferencia de nivel junior; comunicación que tiene que alinearse con la pregunta nueva. Detalle en [01_veredicto.md](01_veredicto.md).
