# 08 · Código y reproducibilidad

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

## Evaluación general

**Código ordenado y bien documentado; flujo de trabajo frágil.** Alguien que reciba el proyecto puede entender el código, pero le costaría reproducir los datos desde cero y no tendría forma de saber si un cambio rompió algo.

---

## Lo que está bien

- **Separación de responsabilidades**: `loaders.py` (lectura de cada formato), `ramas.py` (clasificación), `analysis.py` (cálculos), `dashboard/core` (datos, formato, gráficos, estilo) y `dashboard/paginas` (una página por archivo).
- **Docstrings que explican decisiones** («la remuneración incluye el aguinaldo, por eso promedios de 12 meses»).
- **Constantes en un solo lugar** (`RAMA_LABELS`, `BASES`, `EXPOSICIONES`).
- **Script de descarga reproducible e idempotente** con verificación de que la respuesta sea un zip.
- **Datos procesados livianos** y separados de los crudos.

## Lo que falta

| Problema | Riesgo | Solución | Esfuerzo |
|---|---|---|---|
| **No hay control de versiones (git)** | No se puede volver atrás, ver qué cambió ni mostrar el historial (que en un portfolio también es evidencia de cómo trabajás) | `git init`, `.gitignore` (ya existe), commits chicos con mensajes claros, subir a GitHub | 1 hora |
| **Sin pruebas automáticas** | Un cambio puede romper un cálculo o una página sin que nadie se entere | Carpeta `tests/` con `pytest`: (1) suma de ramas = total oficial; (2) totales comex = control; (3) cada página carga sin error (`streamlit.testing.v1.AppTest`) | 1 día |
| **Flujo de datos en 3 notebooks manuales** | Hay que acordarse del orden; un notebook con estado oculto puede dar resultados distintos | Un script `src/pipeline.py` (o `make`) que regenere `data/processed/` de punta a punta; los notebooks quedan para explorar | 1 día |
| **`requirements.txt` sin versiones** | En otra computadora puede instalarse un Streamlit que rompa el CSS o la API | Fijar versiones (`streamlit==1.63.0`, etc.) o al menos mínimos; separar `requirements-dev.txt` con `jupyter` | 30 minutos |
| **Notebook de análisis de 2.400 líneas** | Difícil de revisar; mezcla exploración con resultados | Mover la lógica a `src/` (ya está a medias) y dejar el notebook como narración corta | Medio |
| **Textos de documentos escritos a mano** | Quedan desactualizados (ver `07`) | Generar las cifras de los documentos desde los datos (plantilla + script) | Medio |
| **Semillas y entorno no registrados** | Menor acá (no hay aleatoriedad), pero será importante cuando sumes bootstrap | Fijar semillas y registrar versión de Python | Bajo |

## Nota sobre esta carpeta

`pregunta_central.py` y `pruebas_robustez.py` son scripts sueltos que solo leen `data/processed/`. Si los resultados de la parte A pasan al dashboard,
conviene mover el cálculo a `src/analysis.py` (como el resto) y que el script de esta carpeta lo importe, para que haya una sola fuente de cada cifra.

## Prueba de fuego de reproducibilidad

Antes de publicar, hacé esto: **cloná el proyecto en una carpeta nueva, en otra computadora o una máquina virtual, y seguí solo el README**.
Si en 15 minutos no tenés el dashboard funcionando y los datos regenerados, falta documentación o automatización. Es la misma prueba que va a hacer, sin decírtelo, quien evalúe tu trabajo.
