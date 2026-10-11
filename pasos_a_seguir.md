# Pasos a seguir

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**

Hoja de ruta para terminar el proyecto: **qué falta, qué mejoraría y cómo hacerlo**. Reemplaza a `plan_de_trabajo.md` (su contenido está acá).
Empezada el 11 de octubre de 2026. Estado: ⬜ pendiente · 🔄 en curso · ✅ hecho.
**Estado al 11-10-2026: la versión 1 está terminada.** Lo único pendiente es lo que tenés que hacer vos (sección 4) y lo que queda para una versión 2 (sección 3).

---

## ¿Está bien el trabajo?

**Sí. Para un portfolio de analista de datos es un trabajo bueno, por encima del promedio.** Lo más fuerte:

- **Los datos:** oficiales, limpios y **validados contra los totales publicados**.
- **El cuidado del método descriptivo:** estacionalidad, aguinaldo y ponderaciones.
- **La honestidad sobre los límites.**

**Lo que le cambiaría** es poco y concreto:

1. **Que todo el proyecto cuente la misma respuesta**, en el orden de la pregunta. Hoy dos pestañas la cuentan bien (Importaciones vs. resultados y Resumen); el informe, la presentación y los documentos todavía cuentan la de la pregunta anterior.
2. **Separar las importaciones por uso económico** (consumo, insumos y capital). Es la mejora de método que más valor agrega.
   - Ya está probada: la relación positiva entre importaciones y empleo **es de los insumos** (ρ = +0,78);
   - con los bienes de consumo, los que compiten, **desaparece** (ρ = 0,01).
3. **Que se pueda reproducir y mostrar:**
   - un solo comando que regenere los datos;
   - pruebas automáticas;
   - versiones fijas;
   - control de versiones (git);
   - una carpeta sin borradores.

---

## Cómo se contesta la pregunta (reglas para todo el proyecto)

**Respuesta:** **No.** Desde 2018 la industria produce menos y paga salarios más bajos, pero esas pérdidas no se concentraron donde más crecieron las importaciones; en general fue al revés.
- **El «al revés» se explica por los insumos:** las ramas que crecen importan más insumos y máquinas.
- **Con los bienes de consumo**, que son los que compiten, no hay relación con el empleo.
- **La excepción** son prendas y textiles.
- **Es una coincidencia medida, no un efecto.**

**Reglas:**

1. **El orden de la respuesta sigue al de la pregunta:**
   1. qué se perdió;
   2. en qué ramas;
   3. si coincide con las importaciones;
   4. por qué (insumos contra consumo);
   5. los matices: prendas y textiles, China y los límites.
2. **Una medida principal:** crecimiento de las importaciones en dólares, 2018 → 2025.
   - El uso económico es la prueba central de robustez.
   - Toneladas, importaciones por puesto, base 2023, China y el panel son complementos: **se muestran después y no se borran**.
3. **La respuesta usa una ventana común:** 2018 → 2025, promedios anuales. Las páginas descriptivas muestran el último dato y dicen hasta cuándo llega.
4. **El empleo cae desde 2023:** con promedios anuales, 2025 está igual que 2018 (+0,7%).
5. **Cada p-valor va con su versión corregida** (Benjamini-Hochberg).
6. **Las tarjetas se quedan; lo que cambia es su contenido.** Las tarjetas son para hechos medidos, no para correlaciones.
7. **Lenguaje de coincidencia:** «coincide», «va junto con»; nunca «provoca» ni «destruye».

---

## 1. Lo que falta (para cerrar la versión 1)

### 1.1 Base de cálculo ✅
- [x] `src/analysis.py`: `respuesta_por_rama`, `respuesta_grupos`, `respuesta_correlaciones` y `respuesta_sensibilidad` (ventana 2018 → 2025); p corregido en `correlaciones.csv`
- [x] Cuaderno 03 re-ejecutado; las cifras coinciden con `analisis_profesional/pregunta_central.py`

### 1.2 Pestañas del dashboard

| Pestaña | Qué falta | Cómo | Estado |
|---|---|---|---|
| Importaciones vs. resultados | Respuesta, robustez y exploración | Ya hecha (revisada por Francisco) | ✅ |
| Resumen | Quinto hallazgo con la respuesta y nota de los dos períodos | Ya hecho | ✅ |
| Conclusiones (informe A4) | **Responde la pregunta vieja**: conclusión principal «la señal está en China», H2 primero | Reescribir el resumen, la sección 3.5 (tabla y figura de la respuesta), la sección 4 y «Respuesta a la pregunta» en el orden de la respuesta; volver a medir las hojas para que sigan saliendo en A4 | ✅ Reescrito en el orden de la respuesta; hoja 6 con tabla y figura nuevas; las 8 hojas miden A4 |
| Presentación | La diapositiva «Qué encontré» muestra «3 de 24 asociaciones» y China; la de «Los datos» cuenta «24 correlaciones / 24 modelos» | Las tres cifras pasan a ser qué se perdió, dónde y la excepción; en «Los datos», qué se comparó | ✅ «La respuesta, en tres cifras»: −5,6% producción, +27.000 donde más se importó, −13.900 en Prendas |
| Método y límites | Sin la ventana común, sin la medida principal, sin la corrección ni el uso económico | Agregar esas decisiones y sus límites | ✅ |
| Importaciones | No muestra el uso económico ni dice qué medida usa la respuesta | Gráfico nuevo de importaciones por uso (consumo, insumos y capital) por año; frase que conecta la sección 3 con la respuesta | ✅ Sección 7 nueva, con selector de rama |
| Empleo y ramas | No dice que la caída del empleo es de 2024 en adelante | Una frase calculada en la síntesis | ✅ |
| Comparador de ramas | No dice, para la rama elegida, cuánto crecieron sus importaciones ni en qué grupo cae | Tarjetas o métricas con importaciones 2018 → 2025 (total y consumo) y el grupo | ✅ Fila «Frente a la pregunta central» |
| Datos | No lista las tablas de uso económico nuevas | Agregarlas al catálogo | ✅ |

### 1.3 Documentos

| Documento | Qué falta | Cómo | Estado |
|---|---|---|---|
| `README.md` | No dice la respuesta; el pendiente «un README por pestaña» ya no hace falta | La respuesta en una línea; cómo actualizar los datos; estado «versión 1» | ✅ |
| `explicacion.md` | 858 líneas con cifras y respuesta viejas | Actualizar la respuesta corta, las cifras y el banco de preguntas; sacar la sección 6 «página por página», que repite al dashboard | ✅ 668 líneas; la versión anterior completa quedó en `archivo/` |
| `analisis_profesional/` | La revisión es anterior a estos cambios | Actualizar el veredicto y agregar la evaluación final | ✅ Ver `analisis_profesional/00_evaluacion_final.md` |

### 1.4 Orden de la carpeta

| Qué | Cómo | Estado |
|---|---|---|
| Borradores en la raíz: `posibles.md`, `ejecutar.md`, `prompt_card_impacto.md`, `posibles_a_realizar.md` | **Movidos** a `archivo/` (con un `LEEME.md`), sin borrarlos | ✅ |
| `reports/figures/` vacía | Movida a `archivo/` | ✅ |

---

## 2. Lo que mejoraría (y cómo)

| # | Mejora | Por qué | Cómo | Estado |
|---|---|---|---|---|
| M1 | **Importaciones por uso económico (BEC)** | Separa lo que compite (consumo) de lo que abastece (insumos y capital). Es la mejora que más cambia lo que el análisis puede decir | Tablas oficiales HS → BEC del Banco Mundial (WITS) en `data/raw/comercio_exterior/clasificaciones/`; módulo `src/uso_economico.py`; respuesta recalculada con cada uso | ✅ Con bienes de consumo, ρ = 0,01 con el empleo; con insumos, ρ = +0,78 |
| M2 | **Un solo comando para regenerar los datos** | Hoy son tres cuadernos que hay que acordarse de correr en orden | `actualizar_datos.py`: ejecuta los cuadernos 01, 02 y 03 en orden y avisa si algo falla | ✅ Probado: regenera todo en unos 2 minutos y da exactamente los mismos archivos |
| M3 | **Pruebas automáticas** | Que un cambio no rompa un cálculo o una página sin que nadie se entere | Carpeta `tests/` con `pytest`: suma de ramas = total oficial; comercio exterior = totales de control; respuesta coherente; cada página carga sin error | ✅ 46 pruebas, todas pasan (`.\.venv\Scripts\python.exe -m pytest`) |
| M4 | **Versiones fijas** | Que funcione igual en otra computadora | `requirements.txt` con versiones mínimas; `requirements-dev.txt` con jupyter y pytest | ✅ |
| M5 | **Control de versiones (git)** | Historial, respaldo y evidencia de cómo trabajás | `git init` y primer commit (local). **Subirlo a GitHub lo hacés vos** (pasos en la sección 4) | ✅ Repositorio local con el primer commit |

---

## 3. Lo que dejaría para una versión 2 (no hace falta para cerrar)

- **Comercio exterior 2026 (enero-agosto).** Actualiza lo descriptivo; no cambia la respuesta, porque la ventana cierra en 2025.
  Cómo: el INDEC publica `https://comex.indec.gob.ar/files/zips/imports_2026_M.zip` y `exports_2026_M.zip` (también `_2025_M`, con columna de mes, para comparar enero-agosto contra enero-agosto;
  se verificó que el total de 2026 da importaciones USD 48.999 M y exportaciones USD 67.248 M). Guardarlos en una carpeta aparte, porque sus nombres se parecen a los anuales; el archivo anual de 2026
  no sirve solo porque no dice hasta qué mes llega.
- **Salarios más recientes.** El Ministerio publicó `remuneraciones_mensual_9` (sept-2026), pero el sitio sirve por error el archivo de empleo; reintentar más adelante y, cuando funcione, correr `actualizar_datos.py 02 03`.
- **Una pregunta causal**, como proyecto aparte. Por ejemplo, un instrumento tipo Autor-Dorn-Hanson (las importaciones desde China de otros países) o diferencias en diferencias con la apertura de 2024. Ver `analisis_profesional/04_revision_metodologica.md`, apartado 6.
- **Empleo por provincia y detalle por producto.**

---

## 4. Lo que tenés que hacer vos (no lo puedo hacer yo)

1. **Revisar cada pestaña** en el navegador: doble clic en `run.bat`.
2. **Crear el repositorio en GitHub:**
   1. Entrá a github.com → «New repository» → nombre `importaciones-industria-argentina` → sin README → «Create».
   2. En la terminal de VS Code, pegá las dos líneas que GitHub muestra en «…or push an existing repository» (`git remote add origin …` y `git push -u origin main`).
3. **Publicar el dashboard:**
   1. Entrá a share.streamlit.io con tu cuenta de GitHub → «Create app».
   2. Elegí el repositorio, la rama `main` y el archivo `dashboard/Inicio.py` → «Deploy».
   3. Copiá el link y pegalo arriba en el `README.md`.

---

## Registro

| Fecha | Qué se hizo |
|---|---|
| 11-10-2026 | Pregunta nueva en todo el proyecto. Revisión profesional actualizada |
| 11-10-2026 | Base de cálculo de la respuesta. Pestaña Importaciones vs. resultados (revisada: ok) |
| 11-10-2026 | Pestaña Resumen: quinto hallazgo con la respuesta y nota de los dos períodos |
| 11-10-2026 | Mejora M1 probada: con bienes de consumo la relación con el empleo desaparece (ρ = 0,01); con insumos es ρ = +0,78 |
| 11-10-2026 | Todas las pestañas acomodadas a la pregunta; M1 a M5 hechas; README y `explicacion.md` actualizados; borradores a `archivo/`; evaluación final |
