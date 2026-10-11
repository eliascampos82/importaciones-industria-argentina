# Para terminar el trabajo

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

Qué falta, qué sacaría y qué dejaría para después, mirado como analista de datos con un objetivo: **cerrar una versión 1 que se pueda mostrar**.
Fecha: 11 de octubre de 2026. Pregunta central:

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**

---

## Dónde está el trabajo

**Lo difícil ya está hecho.** Los datos están limpios y validados, el dashboard funciona y la pregunta coincide con lo que el diseño puede responder.
Lo que falta es, sobre todo, **contar la respuesta a esta pregunta** (hoy se cuenta la de la pregunta anterior) y **ordenar** la carpeta. No hace falta descargar datos nuevos ni hacer análisis nuevos para cerrar.

**La respuesta**, calculada con la ventana común 2018 → 2025 (detalle en [05_pruebas_de_robustez.md](05_pruebas_de_robustez.md), parte A):

> **No.** Desde 2018 la industria produce menos (−5,6%) y paga salarios reales más bajos (−7,5%, en las 16 ramas), pero esas pérdidas **no se concentraron** donde más crecieron las importaciones:
> las 8 ramas donde menos crecieron perdieron 18.000 puestos y las 8 donde más crecieron ganaron 27.000. **La excepción son prendas y textiles**, donde entraron muchas más toneladas y se perdió empleo.
> Es una coincidencia medida, no un efecto: la tendencia previa de cada rama la explica mejor.

---

## 1. Lo que falta (imprescindible para cerrar)

En orden. Las tareas 1 a 4 son las que cambian la nota.

| # | Tarea | Dónde | Esfuerzo |
|---|---|---|---|
| 1 | **Mostrar la respuesta directa.** Una sección nueva al principio de Importaciones vs. resultados: «La respuesta: 2018 → 2025», con la tabla de grupos (crecieron más / menos: puestos, empleo %, producción y salario) y la dispersión de crecimiento de importaciones contra empleo con las 16 ramas rotuladas. Destacar Prendas como excepción | [exposicion.py](../dashboard/paginas/exposicion.py), con los cálculos de [pregunta_central.py](pregunta_central.py) pasados a `src/analysis.py` | 1 día |
| 2 | **Reescribir las conclusiones del informe en el orden de la pregunta**: qué se perdió → dónde → ¿coincide con las importaciones? (no) → matices (prendas y textiles, China, límites). Hoy la sección 4 dice «La señal más consistente está en China» y la respuesta empieza por H2 | [informe.py:251](../dashboard/paginas/informe.py#L251) (conclusión principal), [informe.py:464-500](../dashboard/paginas/informe.py#L464-L500) | Medio día |
| 3 | **Cambiar el quinto hallazgo del Resumen.** Hoy son tarjetas de ρ («cruces significativos», «menos producción donde más pesa China»). Reemplazarlo por la respuesta: «+27.000 puestos donde más crecieron las importaciones / −18.000 donde menos / Prendas: −13.900». Título: «¿Coincide con las importaciones? No, salvo en prendas y textiles» | [resumen.py:176-194](../dashboard/paginas/resumen.py#L176-L194) | 2 horas |
| 4 | **Ajustar los textos que ponen a China al frente** en la página central: el «qué se observa» del mapa de calor y la síntesis | [exposicion.py:107](../dashboard/paginas/exposicion.py#L107), [exposicion.py:194](../dashboard/paginas/exposicion.py#L194) | 1 hora |
| 5 | **Mostrar el p corregido** (Benjamini-Hochberg) al lado de cada p-valor en el mapa de calor y en el informe | `src/analysis.py` (`statsmodels.stats.multitest.multipletests`) + las dos páginas | 2 horas |
| 6 | **Decir que el empleo cae desde 2023.** Con promedios anuales, el empleo de 2025 es +0,7% respecto de 2018; la caída es de 2024 en adelante. Una frase en la respuesta y en el informe evita la repregunta | Respuesta del informe y sección nueva de la tarea 1 | 15 minutos |
| 7 | **Actualizar `explicacion.md`**: la respuesta corta (1.3), las cifras (1.2: empleo 4T 2025, «2 de 24») y el banco de preguntas de la página Importaciones vs. resultados (6.4). Mejor aún, **reducirlo** (ver «Lo que sacaría») | [explicacion.md](../explicacion.md) | Medio día |
| 8 | **Actualizar el README del proyecto**: sacar el pendiente «un README por pestaña» (ver abajo), poner la respuesta en una línea debajo de la pregunta y una sección «Estado: versión 1» | [README.md](../README.md) | 30 minutos |
| 9 | **Git + GitHub**: `git init`, primer commit, repositorio público. El `.gitignore` ya existe | Carpeta del proyecto | 1 hora |
| 10 | **Fijar versiones** en `requirements.txt` (como mínimo `streamlit>=1.57`) y separar `jupyter` en `requirements-dev.txt` | [requirements.txt](../requirements.txt) | 30 minutos |
| 11 | **Publicar** en Streamlit Community Cloud y poner el link arriba del README | — | 1 hora |
| 12 | **Prueba de fuego**: copiar el proyecto a otra carpeta, seguir solo el README y comprobar que en 15 minutos el dashboard abre | — | 30 minutos |

**Total: 3-4 días de trabajo.** Después de esto, el proyecto está terminado como versión 1.

---

## 2. Lo que sacaría

Sacar también es trabajo de analista: cada pieza de más es algo que hay que mantener al día y que un evaluador puede encontrar desactualizado.

### Archivos de la carpeta del proyecto

| Archivo | Qué es | Qué haría | Por qué |
|---|---|---|---|
| `posibles.md` | Ideas iniciales de otra herramienta de IA, con marcas como `:chatgpt-content-reference` | **Borrar** (o mover a una carpeta personal fuera del proyecto) | Es un borrador de lluvia de ideas; en un portfolio se lee como material copiado |
| `ejecutar.md` | Cómo ejecutar el proyecto | **Borrar** | Repite lo que ya dice el README (y `run.bat`) |
| `prompt_card_impacto.md` | Especificación de diseño de las tarjetas «afiche» (526 líneas) | **Sacarlo del proyecto** y guardarlo aparte para otros trabajos | No es parte del análisis; es una herramienta tuya |
| `posibles_a_realizar.md` | Hoja de ruta del 20 de septiembre, con cifras viejas | **Borrar** | Lo reemplazan [09_plan_de_mejora.md](09_plan_de_mejora.md) y este archivo |
| `reports/figures/` | Carpeta vacía | **Borrar** | Una carpeta vacía sugiere algo sin terminar |
| `explicacion.md` | Guía para exponer, 858 líneas, cifras de la versión anterior | **Reducirla a ~250 líneas**: dejar el resumen (1), conceptos (2) y el banco de preguntas; sacar la sección 6 «página por página» | La sección 6 repite lo que cada gráfico ya explica en el dashboard, y es lo que más se desactualiza |

### Dentro del dashboard

| Qué | Qué haría | Por qué |
|---|---|---|
| **Tarjetas de ρ en el Resumen** (quinto hallazgo) | Reemplazarlas (tarea 3) | Una correlación entre 16 ramas no aguanta el formato afiche ([07](07_comunicacion_y_dashboard.md), punto 1) |
| **Las 4 medidas × 2 bases como resultado principal** | Dejar 1 medida principal (crecimiento de importaciones en USD, 2018 → 2025); las otras 3 medidas y la base 2023 pasan a una sección «Robustez» | Una pregunta, una respuesta; el resto, chequeos |
| **El panel «sin refinación» como resultado** | Mostrarlo solo como prueba de sensibilidad | Depende de una rama y de errores agrupados con 15 grupos |
| **H2 (China) como hipótesis al mismo nivel que H1** | Pasarla a «análisis complementario» | China ya no está en la pregunta |

### Pendientes que sacaría de la lista

| Pendiente (README del proyecto) | Qué haría | Por qué |
|---|---|---|
| **Un README por pestaña** (9 documentos) | **No hacerlo** | Cada gráfico ya trae «qué muestra / cómo leerlo / qué se observa» calculado de los datos. Nueve documentos escritos a mano se desactualizan con cada dato nuevo ([07](07_comunicacion_y_dashboard.md), punto 3) |
| **Comercio exterior enero-agosto 2026** | **Pasarlo a la versión 2** | No cambia la respuesta: la ventana de la pregunta cierra en 2025. Solo actualizaría páginas descriptivas |
| **Pronóstico por rama, clustering, ángulos sociales** (de `posibles_a_realizar.md`) | **Sacarlos** | Son otras preguntas; suman páginas sin mejorar la respuesta a esta |

---

## 3. Lo que dejaría para la versión 2

No hace falta para cerrar. Si después querés seguir, este es el orden:

1. **Clasificación BEC** (consumo / intermedios / capital): rehacer la parte A solo con importaciones de bienes de consumo. Es **lo único que puede cambiar la respuesta**: la excepción de prendas y textiles sugiere que
   las importaciones que compiten sí coinciden con pérdidas, y hoy quedan tapadas por los insumos y las máquinas.
2. Comercio exterior 2026 (enero-agosto).
3. Exposición por trabajador y tendencia previa en el dashboard.
4. Pruebas automáticas y un solo comando para regenerar los datos.
5. Una pregunta causal, como proyecto aparte ([04](04_revision_metodologica.md), apartado 6).

---

## 4. Lista de control de entrega

- [ ] La portada, el Resumen, la página central y el informe dicen **la misma pregunta** y **la misma respuesta**, en el mismo orden
- [ ] La respuesta usa la ventana 2018 → 2025 y lo dice
- [ ] Ninguna tarjeta tipo afiche muestra una correlación
- [ ] Cada p-valor tiene al lado su versión corregida
- [ ] Ninguna cifra de `explicacion.md` contradice al dashboard
- [ ] La carpeta no tiene borradores (`posibles.md`, `ejecutar.md`, `prompt_card_impacto.md`, `posibles_a_realizar.md`, `reports/` vacía)
- [ ] `requirements.txt` con versiones
- [ ] Repositorio en GitHub con el link del dashboard publicado en el README
- [ ] Prueba de fuego en otra carpeta: funciona siguiendo solo el README
