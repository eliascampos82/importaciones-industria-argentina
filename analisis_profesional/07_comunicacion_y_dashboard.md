# 07 · Comunicación y dashboard

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

## Evaluación general

**Fuerte, con un riesgo.** El proyecto se comunica mejor que la mayoría de los portfolios de datos. El riesgo es que la **fuerza de la comunicación supere la fuerza de la evidencia**.

---

## Lo que está muy bien

- **Estructura narrativa**: presentación → resumen → detalle por tema → pregunta central → comparador → conclusiones → método → datos. Es el orden en que alguien entiende un trabajo.
- **Cada gráfico con su explicación** (qué muestra, cómo leerlo, qué se observa) y una **síntesis** por página.
- **Textos calculados**: las frases cambian solas si cambian los datos. Evita el error más común de los dashboards.
- **Cada cifra dice hasta cuándo llega.**
- **Pestaña de método y de datos**: cualquiera puede auditar el trabajo.
- **Informe imprimible y presentación**: el mismo análisis para tres audiencias (quien explora, quien lee, quien escucha).
- **Banco de preguntas y repreguntas** en `explicacion.md`: preparación de nivel profesional para defenderlo.

## Lo que hay que corregir

### 1. Proporcionalidad entre impacto visual y solidez de la evidencia
Las tarjetas tipo afiche son muy efectivas para cifras **descriptivas y sólidas** («-45.000 empleos industriales menos»). Usadas para **correlaciones** («ρ -0,74 / MENOS PRODUCCIÓN DONDE MÁS PESA CHINA»)
comunican certeza que no existe. Regla práctica:

| Tipo de resultado | Formato adecuado |
|---|---|
| Hecho medido (cuánto cayó, cuántos puestos) | Afiche, número grande |
| Asociación entre variables | Gráfico de dispersión con las 16 ramas visibles + intervalo de confianza |
| Resultado de un modelo | Coeficiente con intervalo, en lenguaje condicional («se asocia», «es compatible con») |

### 2. Coherencia entre documentos
`explicacion.md` y `posibles_a_realizar.md` tienen cifras de una versión anterior (2 de 24 correlaciones significativas, +1,3% de empleo desde 2018, 4T 2025). El dashboard dice otra cosa.
Para un evaluador, **dos cifras distintas para lo mismo = ninguna es confiable**. Solución: que los documentos tomen las cifras de los mismos datos (generarlos con un script) o marcarlos con fecha y versión.

### 3. Demasiadas piezas para mantener
Dashboard de 9 pestañas, informe A4 de 7 hojas, presentación, `explicacion.md` de 850 líneas, README, posibles, prompt de tarjetas… Cada pieza es valiosa, pero cada actualización de datos obliga a revisar todas.
Para un portfolio conviene: **un dashboard + un README corto + un informe de 2-3 páginas**, y el resto como anexo.

### 4. El mensaje principal tiene que caber en una oración y responder la pregunta de la portada
La portada pregunta: «Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?». El mensaje principal tiene que empezar con
la respuesta a eso, no con China. Propuesta, fiel a la evidencia (`05`, parte A):

> «No. Desde 2018 la industria produce menos y paga salarios más bajos, pero esas pérdidas no se concentraron donde más crecieron las importaciones; en general fue al revés.
> La excepción son prendas y textiles, donde entraron muchas más toneladas y se perdió empleo.»

Y una segunda oración para los límites: «Es una coincidencia medida en 16 ramas, no un efecto: la explica mejor la tendencia previa de cada rama, y las importaciones totales mezclan las que compiten con las que abastecen.»

### 4b. El orden de las conclusiones tiene que seguir el de la pregunta
Hoy el informe, la página Importaciones vs. resultados y el Resumen abren las conclusiones con China («la señal más consistente»). Orden que pide la pregunta nueva:
(1) qué se perdió desde 2018, (2) en qué ramas, (3) si coincide con el crecimiento de las importaciones (**no**), (4) matices: prendas y textiles, China, límites.

### 5. Dependencia del diseño visual en detalles internos de Streamlit
Mucho CSS apunta a estructuras internas de Streamlit (`stToolbar > div > div:nth-child(3)`, clases generadas). Con una actualización de Streamlit puede romperse sin aviso.
Fijar la versión en `requirements.txt` y agregar una prueba visual mínima (ver `08`).

### 6. Pensar en quién lo mira y cuánto tiempo tiene
Un reclutador mira un portfolio **entre 2 y 5 minutos**. La portada y el resumen tienen que contestar en ese tiempo: qué pregunta, qué datos, qué encontraste, qué no se puede afirmar, qué harías después.
Lo tenés casi todo; falta que la respuesta sea más corta y honesta en lo que **no** se pudo responder.
