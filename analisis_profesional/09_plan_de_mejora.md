# 09 · Plan de mejora

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

Hoja de ruta ordenada por **impacto sobre la calidad del análisis por hora de trabajo**. **Actualizado el 11-10-2026 para la pregunta nueva:**

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**

Con esta pregunta, el proyecto **ya no necesita un diseño causal para estar terminado**. El plan se divide en dos:
**versión 1 (cerrar el trabajo)**, que es casi todo reescribir y ordenar, y **versión 2 (después)**, que es análisis nuevo.
La lista de cierre, con el detalle de cada tarea y lo que conviene sacar, está en [README_para_terminar.md](README_para_terminar.md).

---

## Versión 1 · Para terminar el trabajo

### Nivel 1 · Que la respuesta coincida con la pregunta (1-2 días)

| # | Tarea | Por qué | Cómo |
|---|---|---|---|
| 1 | **Llevar la parte A de `05` al dashboard y al informe** | Es la respuesta directa a la pregunta y hoy no está en ningún lado | Ventana 2018 → 2025, medida principal: crecimiento de importaciones en USD; tabla de grupos (más/menos) y dispersión. Cálculo hecho en `pregunta_central.py` |
| 2 | **Reescribir las conclusiones en el orden de la pregunta** | Hoy abren con China | Informe sección 4 y «Respuesta a la pregunta», texto de la sección 2 de Importaciones vs. resultados, quinto hallazgo del Resumen |
| 3 | **Corrección por comparaciones múltiples visible** | Sin ella, cualquier p < 0,05 parece un hallazgo | Columna de p corregido (Benjamini-Hochberg) al lado de cada p-valor |
| 4 | **China, toneladas, base 2023 y panel → «robustez y complementos»** | Una medida principal, el resto como chequeo | Reordenar la página Importaciones vs. resultados (secciones) sin borrar nada |
| 5 | **Decir que el empleo cae desde 2023, no desde 2018** | La pregunta dice «desde 2018» y el empleo anual 2025 es +0,7% contra 2018 | Una frase en la respuesta y en el informe |

### Nivel 2 · Que se pueda mostrar (1 día)

| # | Tarea | Por qué | Cómo |
|---|---|---|---|
| 6 | **Actualizar `explicacion.md`** o reducirlo a guía de exposición | Tiene cifras viejas y la respuesta vieja | Ver `README_para_terminar.md` |
| 7 | **Ordenar la carpeta** (borrar o archivar documentos de trabajo) | Un evaluador abre la carpeta y ve borradores | Ver `README_para_terminar.md`, «Lo que sacaría» |
| 8 | **Git + GitHub** | Historial, respaldo y evidencia de trabajo | `git init`, primer commit, repositorio público |
| 9 | **Fijar versiones** en `requirements.txt` | Que funcione igual en otra computadora | Al menos `streamlit>=1.57`; mejor versiones exactas |
| 10 | **Publicar el dashboard** | Un link vale más que una carpeta | Streamlit Community Cloud |

## Versión 2 · Después (análisis nuevo)

| # | Tarea | Por qué | Cómo |
|---|---|---|---|
| 11 | **Clasificación BEC** (consumo / intermedios / capital) | **La única mejora que puede cambiar la respuesta**: la excepción de prendas y textiles sugiere que las importaciones de consumo sí coinciden con pérdidas | Tabla HS 6 → BEC (Naciones Unidas); rehacer la parte A solo con bienes de consumo |
| 12 | **Exposición por trabajador (ADH)** en el dashboard | Medida estándar de la literatura | Ya calculada en `pregunta_central.py` y `pruebas_robustez.py` |
| 13 | **Control por tendencia previa** en el dashboard | La tendencia 2011-2017 explica más que las importaciones | Mostrar el empleo 2011-2017 al lado de cada rama |
| 14 | **Comercio enero-agosto 2026** | Actualiza lo descriptivo | Ver README del proyecto, «Lo que falta» |
| 15 | **Correspondencia HS → ISIC oficial** | Reemplaza las reglas por capítulo | Tablas de WITS / Naciones Unidas |
| 16 | **Pruebas automáticas y pipeline único** | Reproducibilidad | `tests/` con `pytest`; `src/pipeline.py` |
| 17 | **Una pregunta causal** (proyecto aparte) | Pasar de «coincide» a «provoca» | Instrumento tipo Autor-Dorn-Hanson (importaciones desde China de otros países, UN Comtrade) o diferencias en diferencias con la apertura de 2024. Ver `04`, apartado 6 |

---

## Si solo hacés tres cosas

1. **Tareas 1 y 2**: que la respuesta a la pregunta de la portada esté en el dashboard y en el informe, en ese orden. Es lo que más sube la nota.
2. **Tarea 7 + 8**: carpeta ordenada y en GitHub.
3. **Tarea 11 (BEC)** si te queda una semana: es lo único que podría convertir el «no, con una excepción» en una respuesta más fina.
