# 03 · Falencias

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

Ordenadas de más grave a menos grave. **Actualizado el 11-10-2026 para la pregunta nueva** (F1 y F1b reescritas; notas nuevas en F2, F6 y F8). Cada una dice **qué pasa, por qué importa y qué hacer**. El detalle técnico está en `04_revision_metodologica.md` y la evidencia en `05_pruebas_de_robustez.md`.

---

## 🔴 Graves (afectan la conclusión)

### F1. La pregunta se corrigió, pero las conclusiones responden la anterior *(parcialmente resuelta el 11-10-2026)*

- **Qué pasó.** La pregunta original («¿las ramas más expuestas evolucionaron peor?») sonaba causal y el diseño es descriptivo. Se reemplazó por
  **«Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?»**, que es de coincidencia y el diseño sí puede responder. ✅
- **Qué falta.** La conclusión principal del informe («la señal más consistente está en China»), la respuesta por hipótesis (H2 primero), el texto de la sección 2 de Importaciones vs. resultados
  («la participación de China es la medida que más se asocia…») y el quinto hallazgo del Resumen (tarjetas de ρ) siguen contestando la pregunta vieja.
  Para la nueva, la respuesta principal es: **no, las pérdidas no se concentraron donde más crecieron las importaciones; en general fue al revés, con la excepción de prendas y textiles** (ver `05`, parte A).
- **Qué hacer.** Reescribir esas cuatro piezas en este orden: (1) qué se perdió, (2) dónde, (3) si coincide con el crecimiento de las importaciones, (4) China y prendas/textiles como matices. Detalle en `README_para_terminar.md`.

### F1b. La respuesta directa a la pregunta no está en el dashboard

- **Qué pasa.** La comparación que responde la pregunta (ramas donde las importaciones crecieron más vs. menos, **2018 → 2025 con promedios anuales**, en puestos, producción y salario) no se muestra:
  la página usa resultados hasta 2026 contra exposición hasta 2025, y mezcla 4 medidas y 2 años base en 24 combinaciones.
- **Por qué importa.** Quien lee la pregunta en la portada busca **una** respuesta. Hoy tiene que deducirla de un mapa de calor.
- **Qué hacer.** Una medida principal elegida por la pregunta (crecimiento de las importaciones en dólares, 2018 → 2025) contra los tres resultados, con la tabla de grupos y el gráfico de dispersión;
  toneladas, importaciones por puesto, base 2023 y China pasan a «robustez». El cálculo está hecho en `pregunta_central.py`.

### F2. El resultado sobre China no resiste la corrección por comparaciones múltiples

- **Qué pasa.** Se probaron 24 correlaciones; 3 dan p < 0,05. Con 24 pruebas se esperan ~1,2 falsos positivos por azar. Corrigiendo (Bonferroni, Holm y Benjamini-Hochberg dan lo mismo)
  **sobrevive 1**: participación de China en 2025 contra producción desde 2018 (ρ = -0,74).
- **Por qué importa.** Los documentos y el dashboard presentan «la asociación con China es la más consistente». Con una sola prueba que sobrevive, de una sola ventana, con una sola medida,
  **no es consistente**: es un indicio.
- **Qué hacer.** Aplicar la corrección y reportarla al lado de cada p-valor. Cambiar el lenguaje a «un indicio que no se repite en las otras medidas».
- **Con la pregunta nueva** pesa menos (China ya no está en la pregunta), pero sigue encabezando las conclusiones: ver F1. Para la pregunta nueva se probaron 9 correlaciones
  (3 medidas de crecimiento × 3 resultados, 2018 → 2025) y **ninguna** sobrevive a Benjamini-Hochberg (la mínima, p corregido = 0,16).

### F3. La medida «participación de China (nivel)» mide composición, no exposición

- **Qué pasa.** Que China provea el 53% de lo que importa la rama textil en 2025 dice **en qué productos compite China** (bienes intensivos en mano de obra), no cuánto
  **aumentó** la competencia. Esos mismos sectores vienen en declive estructural en muchos países por razones que no son las importaciones argentinas.
- **Por qué importa.** Es justo la medida que da el único resultado robusto. Si la medida está confundida con la composición sectorial, el resultado también.
- **Qué hacer.** Usar **cambios** de exposición normalizados por tamaño (aumento de importaciones por trabajador, ver `04`) y controlar por la tendencia previa de cada rama.

### F4. El modelo de panel tiene un sesgo de signo conocido

- **Qué pasa.** Todos los coeficientes del panel son positivos (más importaciones ↔ más empleo, producción y salario). Cuando una rama crece, compra más insumos y máquinas del exterior:
  importaciones y producción se mueven juntas por la **demanda**. Es el sesgo de simultaneidad clásico.
- **Por qué importa.** El signo positivo se interpreta como «las importaciones acompañan la actividad». Es una explicación posible, pero el modelo no puede distinguirla de la otra (que haya un efecto
  negativo de la competencia tapado por el efecto demanda).
- **Qué hacer.** Separar las importaciones por uso (BEC: consumo / intermedios / capital) y usar solo las de **bienes de consumo** como exposición; idealmente, instrumentar.

### F5. Inferencia con pocos grupos y búsqueda de especificaciones

- **Qué pasa.** El panel tiene 15-16 ramas. Los errores agrupados («cluster») con tan pocos grupos **subestiman** la incertidumbre: el p < 0,001 del panel «sin refinación» no es creíble.
  Además se corrieron 24 especificaciones (3 resultados × 2 importaciones × 2 muestras × 2 rezagos) y se destacan las que dan significativas.
- **Por qué importa.** Un revisor técnico lo va a ver enseguida. Es la clase de detalle que define si te toman como analista junior o semi-senior.
- **Qué hacer.** Wild cluster bootstrap (paquete `wildboottest` o `boottest`), reportar **todas** las especificaciones juntas (tabla o gráfico de «curva de especificaciones») y decidir antes
  cuál es la principal.

---

## 🟠 Importantes (afectan la calidad)

### F6. Ventanas de tiempo que no coinciden (y cambian la premisa)

La exposición se mide hasta **2025** (comercio anual) y los resultados hasta **1T 2026 / mar-2026 / jul-2026** según la fuente. Se compara un cambio de importaciones con resultados de otro período.
Lo marcaste como limitación 12, pero la solución es simple: **cortar todo en el último período común** (por ejemplo, 2025 completo) para el análisis de exposición.

Con la pregunta nueva importa más, porque dice «desde 2018»: el empleo industrial de 2025 (promedio anual) es **+0,7%** respecto de 2018, y el del 1T 2026 es **−3,6%** respecto del 1T 2018.
La caída del empleo es de 2024 en adelante. La respuesta tiene que separarlo: producción (−5,6%) y salario real (−7,5%) caen desde 2018; el empleo, desde el máximo de 2023.

### F7. Exposición sin normalizar por tamaño

El crecimiento porcentual de las importaciones no dice cuánto pesa ese aumento para la rama. Entre 2018 y 2025, Tabaco pasó de USD 51 a 55 millones (+10%) y Químicos de USD 9.700 a 12.400 millones (+27%):
por trabajador, eso es **≈ USD 1.000 más por puesto en Tabaco y ≈ USD 25.000 más por puesto en Químicos**. La literatura usa justamente el **aumento de importaciones por trabajador** de la rama en el año base.
Con tus datos se puede calcular hoy (ver `05`).

### F8. Ramas sin ponderar

Spearman entre 16 ramas da el mismo peso a Tabaco (≈4.700 puestos en el 1T 2026) que a Alimentos y bebidas (≈418.000). Para una pregunta sobre **empleo**, el resultado debería ponderarse por el tamaño de cada rama, o al menos mostrarse
las dos versiones.

Ya está probado (`05`, parte A): ponderando por empleo de 2018 la pendiente es positiva y «muy significativa» (p < 0,001), **pero solo por Alimentos**: sin esa rama el p-valor pasa a 0,47.
Ponderar no cambia la respuesta («no»), pero muestra que el signo positivo descansa en una sola rama grande.

### F9. El año base 2023 no es un año «normal» para importaciones

2023 tuvo restricciones fuertes a las importaciones (cepo, SIRA). Que las importaciones crezcan desde 2023 mide en buena parte la **salida de esas restricciones**, un cambio de política. Eso no está discutido
— y es una oportunidad: un cambio de política es exactamente el tipo de variación que sirve para un diseño causal (ver `09_plan_de_mejora.md`).

### F10. Tendencias estructurales no controladas

Las ramas que perdían empleo entre 2011 y 2017 siguen perdiéndolo entre 2018 y 2026 (ρ = 0,75, p = 0,001; ver `05`). Gran parte de lo que se observa es **tendencia estructural**. Cualquier análisis de
exposición debería controlar por la tendencia previa de cada rama.

### F11. Documentos desactualizados y contradictorios entre sí

`explicacion.md` dice «solo 2 de 24 correlaciones significativas» y «el empleo casi no cambió desde 2018 (+1,3%)»; los datos actuales dicen 3 de 24 y -3,6%. El dashboard calcula sus textos, los documentos no.
**Un evaluador que encuentra una cifra distinta en dos lugares deja de confiar en las dos.**

### F12. El formato «de impacto» puede sobrevender resultados débiles

Tarjetas como «ρ -0,74 / MENOS PRODUCCIÓN DONDE MÁS PESA CHINA» (quinto hallazgo del Resumen) comunican con la fuerza de un titular un resultado que es una correlación entre 16 puntos. El impacto visual tiene que ser proporcional a la
solidez de la evidencia: las cifras descriptivas (puestos perdidos) aguantan un afiche; las correlaciones, no.

---

## 🟡 Menores (pulido)

- **F13. Clasificación NCM → rama a nivel capítulo**: los tractores (8701) caen en Automotores (en CIIU van a Maquinaria agrícola), los remolques (8716) en Otro equipo de transporte (van con Automotores),
  los artículos de aluminio y cobre (74-76) en Metálicas básicas (muchos son productos de metal), los fertilizantes (31) inflan Químicos. Ninguno cambia la historia, pero conviene documentarlos o corregirlos.
- **F14. `log(1 + importaciones en millones)`**: con montos de cientos de millones el `+1` no cambia nada; es inofensivo pero raro. Usar `log` directo y explicar por qué no hay ceros.
- **F15. Valores en dólares corrientes**: para correlaciones de rangos no importa (un deflactor común no cambia el orden), pero para los niveles y el gráfico del Resumen sí.
- **F16. El esfuerzo se fue al diseño**: muchas iteraciones visuales mientras los pendientes metodológicos marcados como «los más importantes» siguen abiertos. En un portfolio de datos conviene invertir la proporción.
