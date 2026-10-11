
Sí. Para ese trabajo, lo más sólido es **no partir de la conclusión de que “el país está mal”**, sino formular problemas sociales/económicos que puedan ser **demostrados o refutados por los datos**.

Además, tenés una ventaja importante: INDEC permite consultar importaciones por producto y país desde 2002, mientras que existen estadísticas laborales por sector y datos de producción industrial. :chatgpt-content-reference{index="0"}

### 1. Importaciones vs. empleo industrial

**Problema:**

> ¿Los sectores industriales argentinos que experimentaron un mayor crecimiento de las importaciones registraron una mayor pérdida de empleo?

**Cruzar:**

- Importaciones por sector/producto.
- Cantidad de trabajadores registrados por sector.
- Variación porcentual del empleo.
- Producción industrial del sector.

**Hipótesis comprobable:**

> Los sectores con mayor crecimiento de las importaciones presentan una mayor reducción del empleo registrado.

Este probablemente sea **el eje central más interesante** de tu proyecto porque coincide directamente con el tema que te dieron.

---

### 2. Importaciones vs. producción industrial

**Problema:**

> ¿El aumento de las importaciones está asociado con una reducción de la producción de determinados sectores industriales argentinos?

**Cruzar:**

`Importaciones → Producción industrial`

Por ejemplo:

| Sector         | Importaciones | Producción | Empleo |
| -------------- | ------------: | ----------: | -----: |
| Textil         |            ↑ |          ↓ |     ↓ |
| Calzado        |            ↑ |          ↓ |     ↓ |
| Electrónica   |            ↑ |          ↓ |     ↓ |
| Muebles        |            ↑ |          ↓ |     ↓ |
| Metalmecánica |            ↑ |          ↓ |     ↓ |

La pregunta interesante sería:

> **¿En qué sectores el aumento de las importaciones coincide con una contracción de la producción nacional?**

---

### 3. Importaciones vs. salarios reales

Esta puede darle una dimensión **social** mucho más fuerte.

**Problema:**

> ¿Los sectores más expuestos a la competencia importadora presentan una evolución salarial menos favorable que los sectores menos expuestos?

**Cruzar:**

- Importaciones por sector.
- Salario promedio/mediano.
- Salario real.
- Empleo.

Hay datos oficiales de remuneraciones por sector de actividad, incluso con desagregación a 3 y 6 dígitos de CLAE. :chatgpt-content-reference{index="1"}

Podrías buscar algo como:

**Mayor exposición importadora → menor crecimiento salarial real**

---

### 4. Importaciones + empleo + producción

Esta sería una problemática más completa:

> **¿La mayor exposición a las importaciones se relaciona simultáneamente con una reducción del empleo y de la producción industrial?**

Acá tenés **tres dimensiones**:

**Comercio exterior**
→ importaciones

**Actividad económica**
→ producción industrial

**Mercado laboral**
→ empleo

Y podés construir un gráfico por sector:

```text
             IMPORTACIONES
                   ↓
          MAYOR EXPOSICIÓN
                   ↓
        ┌──────────┴──────────┐
        ↓                     ↓
     EMPLEO               PRODUCCIÓN
        ↓                     ↓
     ¿BAJA?                 ¿BAJA?
```

Esto tiene mucho más valor académico que simplemente mostrar que “aumentaron las importaciones”.

---

## 5. Sectores que perdieron más empleo

Otra problemática interesante:

> **¿Qué sectores industriales fueron los que más redujeron su empleo y qué relación tuvieron esos sectores con el crecimiento de las importaciones?**

Podés ordenar los sectores según:

**% variación del empleo 2018–2025**

y después observar:

**% crecimiento de importaciones**

Por ejemplo:

| Sector    | Δ Importaciones | Δ Empleo | Δ Producción |
| --------- | ---------------: | --------: | -------------: |
| Textil    |             +80% |      -15% |           -12% |
| Calzado   |             +65% |      -18% |           -20% |
| Muebles   |             +50% |      -10% |            -8% |
| Alimentos |             +15% |       +2% |            +4% |

No estoy afirmando que esos sean los resultados: **son solamente el formato del análisis**.

---

## 6. ¿La apertura importadora afecta más a algunos sectores que a otros?

Esta me gusta mucho para un proyecto de análisis de datos.

> **¿El impacto de la competencia importadora fue homogéneo en la industria argentina o algunos sectores estuvieron considerablemente más afectados?**

Podés crear un **índice de exposición importadora**.

Por ejemplo:

**Exposición importadora = Importaciones / (Producción nacional + Importaciones − Exportaciones)**

Después clasificás los sectores:

- baja exposición
- exposición media
- alta exposición

Y comparás:

**Alta exposición**

vs.

**Baja exposición**

en:

- empleo
- producción
- salarios
- horas trabajadas

Esto permite hacer análisis estadístico, correlaciones y regresiones.

---

# 7. Un problema social particularmente interesante

Podrías llevarlo al empleo industrial:

> **¿El aumento de la competencia importadora se relaciona con una pérdida de puestos de trabajo registrados en sectores industriales de mayor intensidad laboral?**

Acá agregás otra variable:

**Cantidad de trabajadores por sector.**

Porque no es lo mismo que cierre una actividad que emplea 5.000 personas que una que emplea 100.

Podés calcular:

**puestos de trabajo perdidos por cada aumento del 10% de las importaciones.**

Eso te daría un resultado mucho más interesante.

---

# 8. Importaciones desde China vs. empleo argentino

Este puede ser un proyecto muy visual.

> **¿Existe una relación entre el crecimiento de las importaciones provenientes de China y la evolución del empleo en los sectores industriales argentinos que producen bienes similares?**

INDEC permite consultar importaciones por producto y país de origen. :chatgpt-content-reference{index="2"}

Podrías estudiar:

**China → Argentina**

y seleccionar:

- textiles
- calzado
- electrónica
- maquinaria
- muebles
- productos metálicos
- juguetes

Después:

**Importaciones desde China ↑**

→ **Producción argentina ↓?**

→ **Empleo ↓?**

→ **Salarios ↓?**

Es una pregunta concreta y medible.

---

# 9. Importaciones vs. cierre/contracción del mercado laboral

Otra problemática social:

> **¿Los sectores industriales con mayor crecimiento de las importaciones presentan una mayor reducción del empleo registrado y de las horas trabajadas?**

Además del número de trabajadores, podés incorporar:

**Horas trabajadas.**

Eso es interesante porque una empresa puede **no despedir trabajadores pero reducir horas**.

Entonces:

```text
IMPORTACIONES ↑
       ↓
¿EMPLEO ↓?
       ↓
¿HORAS TRABAJADAS ↓?
       ↓
¿SALARIO REAL ↓?
       ↓
¿PRODUCCIÓN ↓?
```

Así no mirás solamente despidos.

---

# 10. Una comparación muy potente: sectores expuestos vs. no expuestos

Esta sería probablemente la estructura que elegiría para un trabajo académico:

### Pregunta principal

> **¿Los sectores industriales argentinos más expuestos a la competencia importadora tuvieron una evolución diferente en empleo, salarios y producción respecto de los sectores menos expuestos?**

Creás dos grupos:

### Grupo A

**Alta exposición a importaciones**

### Grupo B

**Baja exposición a importaciones**

Y comparás:

| Indicador        | Alta exposición | Baja exposición |
| ---------------- | ---------------: | ---------------: |
| Importaciones    |                % |                % |
| Empleo           |                % |                % |
| Producción      |                % |                % |
| Salario real     |                % |                % |
| Horas trabajadas |                % |                % |

Eso permite que **los datos hagan el argumento**.

---

# 11. Otra problemática: producción nacional desplazada

> **¿En qué sectores el crecimiento de las importaciones coincidió con una reducción de la participación de la producción nacional en el mercado interno?**

Esta es muy interesante porque no solamente preguntás:

**“¿aumentaron las importaciones?”**

sino:

> **¿Las importaciones ganaron participación mientras la producción nacional perdió participación?**

Podés calcular una aproximación de:

**Consumo aparente = Producción + Importaciones − Exportaciones**

y después:

**Participación importada = Importaciones / Consumo aparente**

Eso te permitiría detectar sectores donde el mercado interno fue abastecido crecientemente por productos extranjeros.

---

# 12. Una problemática territorial

Si conseguís datos laborales suficientemente desagregados:

> **¿Las regiones argentinas con mayor concentración de industrias expuestas a las importaciones experimentaron una evolución laboral diferente?**

Cruzarías:

**Provincia/departamento**

con:

- empleo industrial
- salarios
- establecimientos industriales
- importaciones de los sectores predominantes

Esto agrega una dimensión **territorial y social**.

---

# Las 5 que yo pondría como candidatas

Si tenés que presentar varias propuestas al profesor, llevaría estas:

### A — Empleo

> **¿Los sectores industriales con mayor crecimiento de las importaciones registraron una mayor reducción del empleo registrado?**

### B — Producción

> **¿El aumento de las importaciones se relaciona con una disminución de la producción industrial nacional en los sectores más expuestos?**

### C — Empleo + producción

> **¿Los sectores más expuestos a la competencia importadora tuvieron una evolución más desfavorable del empleo y la producción que los sectores menos expuestos?**

### D — Salarios

> **¿La mayor exposición a las importaciones se relaciona con una menor evolución del salario real en los sectores industriales?**

### E — Impacto integral

> **¿Qué relación existe entre la exposición a las importaciones y la evolución conjunta del empleo, los salarios, las horas trabajadas y la producción industrial?**

**La E es la más completa para un proyecto de análisis de datos**, porque no te limita a una sola variable.

Además, actualmente existen datos oficiales que permiten trabajar estas dimensiones: comercio exterior de INDEC, empleo registrado de SIPA, salarios por sector y producción industrial. :chatgpt-content-reference{index="3"}

Y hay algo importante: **no necesitás plantear desde el principio que las importaciones causaron la pérdida de empleo**. Metodológicamente es mucho mejor plantear *“qué relación existe”* y después dejar que correlaciones, gráficos y modelos estadísticos muestren si la hipótesis encuentra evidencia.
