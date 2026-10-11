# 05 · Pruebas de robustez

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

Pruebas que corrí sobre los datos procesados del proyecto (`data/processed/`). **No modifican nada.** Dos partes:

- **Parte A — la respuesta a la pregunta central** (11-10-2026): `pregunta_central.py`
- **Parte B — robustez de los resultados originales** (24 correlaciones y panel): `pruebas_robustez.py`

Para repetirlas, desde la carpeta del proyecto:

```
.\.venv\Scripts\python.exe analisis_profesional/pregunta_central.py
.\.venv\Scripts\python.exe analisis_profesional/pruebas_robustez.py
```

---

# Parte A · Respuesta a la pregunta central

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**

**Ventana:** 2018 → 2025, promedios anuales (`panel_rama_anio.csv`). Es el último año completo en **todas** las fuentes, así que exposición y resultados miden el mismo período.
Las cifras pueden diferir de las del dashboard, que compara contra el último dato de cada fuente (1T 2026, jul-2026, etc.).

## A1. Qué perdió la industria

| Total industria | 2018 → 2025 |
|---|---|
| Producción (IPI) | **−5,6%** (13 de 16 ramas caen) |
| Salario real | **−7,5%** (las **16** ramas caen) |
| Empleo (promedio anual) | **+0,7%** (8 ramas pierden, 8 ganan); su caída empieza después del máximo de 2023 (1T 2026 contra 1T 2018: −3,6%) |

## A2. Rama por rama

Ordenadas por crecimiento de las importaciones en dólares (la medida principal).

| Rama | Importaciones USD | Importaciones toneladas | Aumento de importaciones por puesto (USD) | Empleo | Puestos | Producción | Salario real |
|---|---|---|---|---|---|---|---|
| Alimentos y bebidas | +80,4% | +88,5% | 2.333 | +8,2% | +31.405 | +6,9% | −10,0% |
| **Prendas de vestir, cuero y calzado** | **+35,6%** | **+60,8%** | 6.362 | **−18,8%** | **−13.922** | −13,8% | −12,8% |
| Maquinaria y equipo | +31,1% | +44,9% | 38.456 | +8,5% | +5.857 | +9,8% | −6,0% |
| Automotores y autopartes | +28,7% | +5,9% | 38.985 | +0,2% | +121 | −5,2% | −3,9% |
| Otro equipo de transporte | +28,6% | +35,1% | 34.649 | +0,3% | +28 | −9,6% | −10,2% |
| Caucho y plástico | +27,8% | +36,2% | 14.483 | −0,5% | −301 | −15,5% | −10,3% |
| Químicos (incl. farmacéuticos) | +27,4% | +12,3% | 25.206 | +3,4% | +3.543 | −0,5% | −0,5% |
| Muebles y otras manufacturas | +22,4% | +49,2% | 5.851 | +0,8% | +342 | −20,9% | −10,0% |
| Productos de metal | +22,1% | +18,2% | 3.908 | +1,1% | +1.070 | −29,9% | −2,5% |
| Metálicas básicas | +10,6% | +4,6% | 5.765 | −2,0% | −726 | −19,0% | −8,9% |
| Tabaco | +9,6% | −6,1% | 922 | −8,9% | −468 | −5,0% | −12,9% |
| Informática, electrónica, eléctricos | +8,0% | +8,9% | 18.712 | +1,5% | +684 | −14,9% | −12,3% |
| **Textiles (hilados y tejidos)** | +4,9% | **+45,1%** | 836 | −7,0% | −4.330 | −26,8% | −15,1% |
| Minerales no metálicos | +1,1% | −27,9% | 185 | −4,8% | −2.255 | −17,5% | −14,0% |
| Madera, papel, edición e impresión | −3,3% | −9,3% | −440 | −11,4% | −11.235 | −9,4% | −10,6% |
| Refinación de petróleo | −43,2% | −50,6% | −224.521 | −15,8% | −895 | +11,4% | −8,3% |

## A3. ¿Dónde se perdieron los puestos?

| Ramas, cortadas en la mediana de crecimiento de importaciones (USD) | Puestos | Empleo | Producción (mediana) | Salario real (mediana) |
|---|---|---|---|---|
| Crecieron **más** (8 ramas: alimentos, prendas, maquinaria, automotores, otro transporte, caucho, químicos, muebles) | **+27.072** | +3,3% | −7,4% | −10,0% |
| Crecieron **menos** (las otras 8) | **−18.153** | −4,6% | −16,2% | −11,5% |

De los 34.129 puestos que perdieron las 8 ramas en baja, **58%** estuvo en ramas donde las importaciones crecieron menos. El otro 42% es casi todo **Prendas** (−13.922).

## A4. Correlaciones (9 pruebas), con corrección e intervalos

| Exposición (2018 → 2025) | Resultado | ρ de Spearman | p | IC 95% (bootstrap) | p corregido (BH) |
|---|---|---|---|---|---|
| **Importaciones USD (principal)** | **Empleo** | **+0,49** | 0,053 | −0,12 a +0,92 | 0,24 |
| Importaciones USD | Producción | +0,22 | 0,42 | −0,36 a +0,74 | 0,63 |
| Importaciones USD | Salario real | +0,34 | 0,20 | −0,19 a +0,73 | 0,35 |
| Importaciones toneladas | Empleo | +0,40 | 0,12 | −0,22 a +0,88 | 0,27 |
| Importaciones toneladas | Producción | −0,17 | 0,54 | −0,66 a +0,42 | 0,70 |
| Importaciones toneladas | Salario real | 0,00 | 0,99 | −0,51 a +0,53 | 0,99 |
| Importaciones por puesto | Empleo | +0,59 | 0,017 | +0,07 a +0,89 | 0,16 |
| Importaciones por puesto | Producción | +0,12 | 0,67 | −0,46 a +0,66 | 0,76 |
| Importaciones por puesto | Salario real | +0,42 | 0,11 | −0,13 a +0,79 | 0,27 |

**Lectura.** Ninguna correlación es **negativa y significativa**, que es lo que haría falta para un «sí». Casi todas son positivas (más importaciones, mejor resultado), pero **ninguna sobrevive** a la corrección.
Los intervalos son anchísimos: con 16 ramas, los datos son compatibles con una relación nula o positiva, y apenas con una negativa moderada.

## A5. Ponderando por tamaño (regresión ponderada por empleo de 2018)

| Medida | Sin ponderar | Ponderada | Ponderada, sin Alimentos |
|---|---|---|---|
| Importaciones USD | +0,19 p.p. de empleo por cada 1% más de importaciones (p < 0,001) | +0,18 (p < 0,001) | +0,17 (**p = 0,47**) |
| Importaciones toneladas | +0,09 (p = 0,19) | +0,11 (p = 0,37) | — |

**Lectura.** El «muy significativo» ponderado **es Alimentos**: la rama más grande es también la de mayor crecimiento de importaciones (+80%) y la que más empleo ganó. Sin ella, nada.

## A6. Tendencia previa y sensibilidad

- **Controlando el empleo 2011-2017** (regresión sobre rangos): la tendencia previa pesa **+0,67 (p = 0,013)** y las importaciones **+0,29 (p = 0,27)**. Las ramas que perdían antes son las que pierden ahora;
  el crecimiento de las importaciones no agrega casi nada.
- **Sacando cada rama de a una**, la correlación principal (USD vs. empleo) va de +0,39 (sin Alimentos) a **+0,76 (sin Prendas)**. Prendas es el gran contraejemplo: la única rama grande donde crecieron
  mucho las importaciones y se perdió mucho empleo.
- **Con resultados hasta 2026** (lo que usa hoy el dashboard) la correlación es casi igual: +0,51 (p = 0,046). Cortar en 2025 no cambia la historia, pero la vuelve correcta.

## A7. La respuesta, en una oración

> **No: desde 2018 las pérdidas de empleo y producción no se concentraron en las ramas donde más crecieron las importaciones; en general fue al revés, porque gran parte de lo que se importa son insumos y máquinas
> de las ramas que crecen. La excepción son prendas y textiles, bienes de consumo donde entraron muchas más toneladas y se perdió empleo. Es una coincidencia medida, no un efecto, y la explica mejor la tendencia previa de cada rama.**

---

# Parte B · Robustez de los resultados originales

## 1. Corrección por comparaciones múltiples

**Pregunta.** De las 24 correlaciones entre exposición y resultados, ¿cuántas siguen siendo significativas si se tiene en cuenta que se probaron 24?

| Criterio | Significativas |
|---|---|
| p < 0,05 sin corregir | **3 de 24** |
| Bonferroni | **1** |
| Holm | **1** |
| Benjamini-Hochberg (tasa de falsos descubrimientos 5%) | **1** |

La única que sobrevive: **participación de China en 2025 (nivel) contra producción desde 2018, ρ = -0,74.**
Las otras dos (crecimiento de importaciones en USD ↔ empleo desde 2018, ρ = +0,51; aumento de China ↔ salario desde 2023, ρ = -0,54) **no sobreviven**.

**Lectura.** Con 24 pruebas al 5% se esperan ~1,2 resultados significativos por puro azar. Obtener 3 es apenas más que eso. El resultado sobre China es un **indicio**, no un patrón.

---

## 2. Panel de empleo dejando afuera cada rama de a una

**Pregunta.** ¿El resultado del modelo de panel (empleo ~ importaciones) depende de alguna rama en particular?

| Rama que se saca | Coeficiente | p-valor |
|---|---|---|
| Ninguna (las 16) | +0,023 | 0,64 |
| Cualquiera de las otras 15, de a una | entre +0,013 y +0,027 | entre 0,62 y 0,79 |
| **Refinación de petróleo (23)** | **+0,082** | **< 0,001** |

**Lectura.** El resultado es estable salvo por **una sola rama**. Refinación tiene un salto de importaciones de USD 7.000 millones en 2022 por la crisis energética (precio, no competencia).
Está bien sacarla, pero:
- hay que justificarlo **por contenido** (es energía, sus importaciones se mueven por precios internacionales) y decidirlo **antes** de mirar el p-valor;
- con 15 grupos, ese p < 0,001 de errores agrupados es demasiado optimista: hace falta **wild cluster bootstrap**.

---

## 3. Exposición estilo Autor-Dorn-Hanson (importaciones por trabajador)

**Pregunta.** Si en lugar del crecimiento porcentual se usa la medida estándar de la literatura (aumento de importaciones por puesto de trabajo de la rama en el año base), ¿cambia la historia?

| Base | Exposición | vs. empleo | vs. producción | vs. salario real |
|---|---|---|---|---|
| 2018 | ΔM/L total | **ρ = +0,57 (p = 0,022)** | -0,05 | +0,33 |
| 2018 | ΔM/L desde China | **ρ = +0,50 (p = 0,049)** | -0,21 | +0,27 |
| 2023 | ΔM/L total | +0,11 | -0,07 | +0,24 |
| 2023 | ΔM/L desde China | -0,24 | -0,32 | -0,15 |

**Lectura.**
- Con la medida estándar, las ramas donde más aumentaron las importaciones por trabajador desde 2018 (Automotores ≈ USD 39.000 por puesto, Maquinaria ≈ 38.500, Otro equipo de transporte ≈ 35.000,
  Químicos ≈ 25.000) tuvieron empleo **estable o en alza** (entre -0,9% y +7,1%), mientras que las de menor aumento (Textiles ≈ 840, Minerales no metálicos ≈ 190, Madera y papel ≈ -440) **perdieron** empleo
  (entre -6% y -12%). Es otra vez el **efecto demanda**: ramas que se sostienen importan más insumos, partes y máquinas. Sin separar por uso económico (BEC), ninguna medida de importaciones totales puede mostrar competencia.
- **Dato revelador sobre textiles:** desde 2018 las toneladas importadas crecieron 45% pero el valor en dólares apenas 5%. Se importa **mucho más volumen a precios más bajos**. Por eso las medidas en dólares
  subestiman la presión sobre textiles: para sectores de bienes de consumo baratos, la exposición debería medirse en **cantidades** o con precios unitarios.
- Con base 2023 las asociaciones de China son negativas pero chicas y no significativas: compatibles tanto con un efecto real moderado como con nada. **Con 16 ramas no hay poder para distinguirlo.**
- Esta tabla debería estar en el proyecto: es la primera pregunta que haría alguien que conoce el tema.

---

## 4. Placebo y persistencia (tendencias previas)

**Pregunta.** ¿Las ramas que hoy están más expuestas ya venían peor **antes** de 2018? Si fuera así, la exposición estaría captando una tendencia vieja.

| Empleo antes de 2018 vs… | 2008-2015 | 2011-2017 |
|---|---|---|
| Participación de China 2025 | +0,07 (p = 0,79) | +0,19 (p = 0,49) |
| Aumento de China (p.p.) | -0,13 (p = 0,64) | +0,21 (p = 0,44) |
| Crecimiento de importaciones | +0,21 (p = 0,43) | +0,30 (p = 0,26) |
| **Empleo 2018-2026 (persistencia)** | **+0,61 (p = 0,011)** | **+0,75 (p = 0,001)** |

**Lectura.**
- ✅ **Buena noticia para el proyecto:** la exposición a las importaciones **no** está correlacionada con la evolución previa del empleo. El placebo pasa (para empleo; para producción no hay IPI anterior a 2016).
- ⚠️ **Pero hay mucha persistencia:** las ramas que perdían empleo entre 2011 y 2017 son, en gran medida, las mismas que lo pierden desde 2018. Gran parte de la historia es **estructural**.
  Cualquier modelo de exposición debería **controlar por la tendencia previa** de cada rama (por ejemplo, incluyendo el cambio 2011-2017 como control, o tendencias por rama en el panel).

---

## 5. Resumen de lo que dicen las pruebas

| Afirmación del proyecto | ¿Resiste? |
|---|---|
| La industria retrocede desde 2023 (empleo, producción, empresas) | ✅ Sí (es descriptiva y está bien medida) |
| Hay reasignación de empleo entre ramas | ✅ Sí, y además es persistente desde antes de 2018 |
| No hay un patrón general «más importaciones → menos empleo» | ✅ Sí, se mantiene con todas las medidas probadas (con el matiz de que con 16 ramas tampoco se podría detectar un efecto moderado) |
| «La asociación con China es la más consistente» | ❌ No: sobrevive una sola prueba de 24, con una medida de composición |
| «Las importaciones acompañan la actividad» (signo positivo del panel) | ⚠️ Compatible, pero no demostrado: es el signo que produce el sesgo de demanda |
| Sin refinación, la asociación empleo-importaciones es positiva y significativa | ⚠️ Depende de una sola decisión y de errores agrupados con 15 grupos |
