# 04 · Revisión metodológica a fondo

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

Revisión técnica, paso por paso, de cómo se construyó la respuesta a la pregunta central. **Actualizado el 11-10-2026 para la pregunta nueva** (apartados 1, 4 y 5). Cada apartado tiene: **qué se hizo**, **evaluación** y **cómo lo haría un profesional**.

---

## 1. La pregunta

**Qué se hizo (versión original).** «¿Las ramas industriales donde más crecieron las importaciones (o más avanzó China) evolucionaron peor en empleo, salario real y producción?»

**Evaluación de la original.** Buena pregunta, con debate público real, pero mezclaba dos preguntas distintas:

| Tipo | Pregunta | Qué hace falta para responderla |
|---|---|---|
| Descriptiva / de coincidencia | ¿Coincide el avance importador con las ramas que peor evolucionaron? | Lo que ya tenés |
| Causal | ¿Las importaciones **hicieron** que esas ramas evolucionen peor? | Una fuente de variación exógena (instrumento, cambio de política, experimento natural) |

**Qué se hizo (11-10-2026).** Se reemplazó por:

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**

**Evaluación de la nueva.** ✅ Es la descriptiva, dicha sin ambigüedad: «justo en» pregunta por **coincidencia**, no por causa; fija un punto de partida (2018) y tres resultados.
Sacar China de la pregunta también es correcto: con la evidencia disponible, China es un **matiz de la respuesta**, no el eje.

Tres cosas que la pregunta nueva obliga a hacer y todavía no están hechas:

1. **Una ventana común.** «Desde 2018» contra «crecieron las importaciones» exige el mismo período en los dos lados: **2018 → 2025** (último año completo de todas las fuentes).
   El dashboard hoy compara exposición hasta 2025 con resultados hasta 2026.
2. **Una medida principal que salga de la pregunta.** La pregunta dice «donde más crecieron las importaciones»: la medida principal es el **crecimiento % de las importaciones en dólares** de cada rama.
   Toneladas e importaciones por puesto son pruebas de robustez; la participación de China y su aumento, un análisis complementario.
3. **Separar «perdió» por resultado.** Entre 2018 y 2025 la producción (−5,6%) y el salario real (−7,5%) caen, pero el empleo anual queda +0,7%: su caída empieza en 2024.

## 2. La clasificación de productos en ramas (NCM → rama)

**Qué se hizo.** Cada producto importado (NCM de 8 dígitos) se asigna a una de 16 ramas según su capítulo (2 dígitos), con excepciones a 4 dígitos. Se excluyen productos primarios.

**Evaluación.** Razonable para un primer paso y bien documentado. Dos problemas de fondo:

1. **Un producto importado no compite necesariamente con la rama que lo produce.** El hierro importado (cap. 72) va a «Metálicas básicas», pero lo compra «Productos de metal» como insumo.
   La exposición de una rama a la **competencia** depende de los bienes **finales parecidos a los suyos**, no de todo lo que se clasifica en su capítulo.
2. **Errores puntuales de asignación** (ver F13 en `03`): tractores en Automotores, remolques en Otro equipo de transporte, artículos de aluminio y cobre en Metálicas básicas, fertilizantes inflando Químicos.

**Cómo lo haría un profesional.**
- Usar una **tabla de correspondencia oficial** HS → ISIC (Naciones Unidas / WITS publican correspondencias HS 6 dígitos → ISIC Rev.3) en lugar de reglas por capítulo.
- Cruzar además con **BEC** (Broad Economic Categories) para separar consumo / intermedios / capital, y usar como exposición a la competencia solo los **bienes de consumo y los intermedios que la rama también produce**.

---

## 3. Las medidas de exposición

**Qué se hizo.** Cuatro medidas por rama: crecimiento % de importaciones en dólares, crecimiento % en toneladas, cambio en puntos de la participación de China y **nivel** de la participación de China.

**Evaluación.**

| Medida | Problema |
|---|---|
| Crecimiento % (USD o toneladas) | No normaliza por tamaño de la rama: +10% en una rama chica y en una grande pesan igual |
| Cambio de la participación de China | Puede subir porque China gana a otros proveedores, sin que aumente la competencia contra la producción local |
| **Nivel** de la participación de China | Mide **composición** (en qué productos vende China), no un shock. Está confundida con tendencias estructurales de esos sectores |

**Cómo lo haría un profesional.** La medida estándar de la literatura (Autor, Dorn y Hanson, 2013) es el **aumento de importaciones por trabajador**:

```
exposición_r = (M_r,fin − M_r,inicio) / L_r,inicio
```

donde `M` son las importaciones de la rama (idealmente solo desde China, o solo bienes que compiten) y `L` el empleo de la rama al inicio. Con tus datos se calcula en dos líneas
(está en `05_pruebas_de_robustez.md`). Si se consigue el valor de la producción, la **penetración importadora** `M / (P + M − X)` es la otra medida clásica.

---

## 4. Las correlaciones entre ramas

**Qué se hizo.** Spearman entre cada medida de exposición y cada resultado (empleo, salario, producción), para dos años base: 4 × 3 × 2 = 24 pruebas con 16 observaciones cada una.

**Evaluación.**

- ✅ Spearman es la elección correcta con 16 puntos dispares.
- ❌ **Sin corrección por comparaciones múltiples.** Con 24 pruebas al 5%, se esperan ~1,2 falsos positivos. Corrigiendo, sobrevive 1 (ver `05`).
- ❌ **Las dos ventanas no son independientes** (2018 → hoy contiene a 2023 → hoy), así que «se repite en las dos bases» vale menos de lo que parece.
- ❌ **Sin ponderar por tamaño.** Para una pregunta sobre puestos de trabajo, Tabaco y Alimentos no pueden pesar igual.
- ❌ **Poder estadístico.** Con n = 16, una correlación tiene que ser |ρ| ≳ 0,5 para dar significativa. Efectos moderados reales no se pueden detectar: «no significativo» acá no quiere decir «no hay efecto».

**Cómo lo haría un profesional.** Decidir **antes** una medida principal y una ventana principal (preregistro informal), reportar el resto como robustez, aplicar Benjamini-Hochberg, mostrar intervalos de confianza
por bootstrap para ρ, y una versión ponderada (regresión ponderada por empleo base).

**Ya está hecho para la pregunta nueva** en `pregunta_central.py` (resultados en `05`, parte A): 9 pruebas en la ventana 2018 → 2025, intervalos por bootstrap, Benjamini-Hochberg, versión ponderada,
control por tendencia previa y sacando cada rama de a una. Lo que falta es llevarlo al dashboard y al informe.

---

## 5. El modelo de panel

> **Con la pregunta nueva** el panel deja de ser central: pregunta «cuando las importaciones de una rama suben respecto de lo habitual, ¿su empleo sube o baja?», que es otra pregunta
> (de dinámica año a año, no de dónde se concentraron las pérdidas desde 2018). Conviene mostrarlo como análisis complementario, con la advertencia de abajo.

**Qué se hizo.** `log(resultado) ~ log(1 + importaciones) + efecto fijo de rama + efecto fijo de año`, errores agrupados por rama, 16 ramas × 10 años, con y sin refinación, con y sin rezago.

**Evaluación.**

| Aspecto | Evaluación |
|---|---|
| Efectos fijos de rama y año | ✅ Correcto: absorbe diferencias permanentes y shocks comunes |
| Interpretación | ✅ Bien explicada: relación «dentro de cada rama, respecto de las demás ese año» |
| **Endogeneidad / simultaneidad** | ❌ Grave. La demanda de cada rama mueve a la vez su producción y sus importaciones de insumos. Por eso todos los coeficientes son positivos. Es el sesgo esperado, no un hallazgo |
| Errores agrupados con 15-16 grupos | ❌ Subestiman la incertidumbre. Hace falta wild cluster bootstrap |
| 24 especificaciones | ❌ Búsqueda de especificaciones: destacar las significativas infla los falsos positivos |
| Dependencia de refinación | ⚠️ Bien detectada. Refinación tiene un salto de importaciones en 2022 (USD 7.000 millones, por la crisis energética: precio, no competencia). Sacarla está justificado, pero hay que decidirlo **antes** y por razones de contenido, no porque cambia el p-valor |
| `log(1 + M en millones)` | Inofensivo (no hay ceros), pero innecesario |
| Tendencias propias de cada rama | ❌ No se controlan. Con la persistencia que hay (ver `05`), conviene agregar tendencias lineales por rama |

**Cómo lo haría un profesional.**
1. Usar como regresor **solo importaciones de bienes que compiten** (BEC consumo + intermedios de la misma rama).
2. Agregar **tendencias por rama** (`C(rama):anio`).
3. **Instrumentar** las importaciones argentinas desde China con las importaciones desde China de **otros países parecidos** (Brasil, Chile, México, Colombia) en los mismos productos:
   capturan el empuje de la oferta china y no la demanda argentina. Es la estrategia de Autor-Dorn-Hanson adaptada.
4. Wild cluster bootstrap para los p-valores.
5. Una sola especificación principal; el resto, en una tabla de robustez completa.

---

## 6. Identificación: cómo pasar de descriptivo a causal

Tres caminos posibles con datos públicos, de más fácil a más difícil:

| Camino | Idea | Datos que faltan |
|---|---|---|
| **Cambio de política (diferencias en diferencias)** | Entre fines de 2023 y 2024 se levantaron restricciones a las importaciones (SIRA, cepo). Las ramas cuyos productos estaban más restringidos recibieron un «shock» mayor. Comparar antes/después entre ramas más y menos afectadas | Qué productos tenían licencias no automáticas o SIRA más demorado (normativa pública) |
| **Instrumento tipo Autor-Dorn-Hanson** | Usar las importaciones desde China de otros países latinoamericanos como instrumento de las argentinas | Comercio por producto de otros países (UN Comtrade, gratis) |
| **Shift-share regional** | Exposición de cada provincia/departamento según su mezcla de ramas | Empleo por departamento (OEDE lo publica) |

Cualquiera de los tres transforma el proyecto: pasa de «muestro qué se movió junto» a «estimo un efecto con supuestos explícitos».

---

## 7. Lo descriptivo (que está bien)

Para que quede claro: la parte descriptiva (cuánto cayó el empleo, la producción y el salario, en qué ramas, desde cuándo, cuánto avanzó China) está **bien hecha y es valiosa por sí misma**.
El problema no es lo que el análisis muestra, sino **el salto de lo descriptivo a lo explicativo**.
