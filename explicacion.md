# Explicación completa del proyecto: importaciones e industria en Argentina (2016-2026)

Informe completo del proyecto: qué se preguntó, con qué datos, cómo se analizó, qué se encontró y qué no se puede afirmar.
Está escrito para alguien que **no sabe nada del tema** y para poder **explicarlo oralmente**, con las preguntas y repreguntas
más probables y los distintos puntos de vista sobre cada resultado.

Para ejecutar la aplicación, ver los pasos en `README.md`.

---

## Índice

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Conceptos explicados desde cero](#2-conceptos-explicados-desde-cero)
3. [La pregunta, las hipótesis y los distintos puntos de vista](#3-la-pregunta-las-hipótesis-y-los-distintos-puntos-de-vista)
4. [Los datos](#4-los-datos)
5. [El método, paso a paso](#5-el-método-paso-a-paso)
6. [Recorrido por la aplicación](#6-recorrido-por-la-aplicación)
7. [Conclusiones](#7-conclusiones)
8. [Limitaciones](#8-limitaciones)
9. [Banco de preguntas y repreguntas](#9-banco-de-preguntas-y-repreguntas)
10. [Guion para presentar oralmente](#10-guion-para-presentar-oralmente)
11. [Estructura del proyecto y cómo se reproduce](#11-estructura-del-proyecto-y-cómo-se-reproduce)
12. [Fuentes](#12-fuentes)

---

## 1. Resumen ejecutivo

### 1.1 En 30 segundos

La pregunta: **desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**
Se cruzaron datos oficiales del INDEC y del Ministerio de Trabajo, llevados a 16 ramas industriales, y se comparó cada rama entre 2018 y 2025.
**La respuesta es no.** La industria produce menos y paga salarios más bajos, pero esas pérdidas no se concentraron donde más crecieron las importaciones:
**en general fue al revés**, porque las ramas que crecen importan más insumos y máquinas. Con los **bienes de consumo**, que son los que compiten, no hay relación
con el empleo. La excepción son **prendas y textiles**. Es una coincidencia medida, no un efecto causal.

### 1.2 En 3 minutos: las cifras que hay que saber

| Tema | Cifra | Qué significa |
|---|---|---|
| Empleo industrial (1T 2026) | **1.200.862 puestos** | Asalariados privados registrados en la industria manufacturera |
| Empleo vs. 1T 2023 | **-64.907 (-5,1%)** | La caída es reciente: empieza después del máximo de 2023 |
| Empleo vs. 1T 2018 | -45.383 (-3,6%) | Con promedios anuales, 2025 estaba igual que 2018 (+0,7%): la pérdida es de 2024 en adelante |
| Producción (IPI), 12 meses a jul-2026 | **-9,4% vs. 2023**, -7,1% vs. 2018 | Cae en 13 de las 16 ramas |
| Salario real, 12 meses a mar-2026 | +2,4% vs. 2023, **-7,9% vs. 2018** | La caída principal fue entre 2017 y 2020; el mínimo, en agosto de 2024 |
| Empresas industriales activas | 54.970 (2023) → 54.070 (2024) | **900 empresas menos** (-1,6%) |
| Importaciones de bienes 2025 | **USD 75,8 mil millones** | +24,7% respecto de 2024 |
| China en las importaciones 2025 | **23,7%** del valor (13,1% de las toneladas) | El valor más alto de la serie 2016-2025 |
| **La respuesta (2018 → 2025)** | 8 ramas donde más crecieron las importaciones: **+27.072 puestos**; 8 donde menos: **-18.152** | No se perdió justo donde más se importó |
| El porqué | Insumos importados vs. empleo: **ρ = +0,78**; bienes de consumo: **ρ = 0,01** | Lo que crece con el empleo son los insumos; lo que compite no muestra relación |
| La excepción | **Prendas, cuero y calzado**: importaciones +61% en toneladas, **-13.922 puestos** (-18,8%) | Bienes de consumo baratos; China no es la que más avanzó ahí (44% → 39%) |
| Qué tan firme | De 9 pruebas de la respuesta, **ninguna** resiste la corrección por comparaciones múltiples | Es una descripción correcta, no una prueba |

### 1.3 La respuesta corta a la pregunta

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**
> **No.** Entre 2018 y 2025 la producción cayó 5,6% y el salario real 7,5% (en las 16 ramas), pero las 8 ramas donde más crecieron las importaciones sumaron empleo
> y las 8 donde menos crecieron lo perdieron. Ese «al revés» lo explican los insumos: una rama que crece importa más insumos y máquinas. Separando por uso económico,
> el crecimiento de las importaciones de **bienes de consumo** (lo que compite) no tiene relación con el empleo. La excepción visible son **prendas y textiles**.
> Es una coincidencia medida en 16 ramas: no prueba que las importaciones no afectaron a ninguna rama, ni que la afectaron.

---

## 2. Conceptos explicados desde cero

Esta sección sirve para explicar el informe a alguien que nunca vio estos temas. Cada concepto tiene una definición simple, un ejemplo y
una frase lista para decir en voz alta.

### 2.1 Conceptos de economía y comercio

**Industria manufacturera.** Todas las actividades que transforman materias primas en productos: fábricas de alimentos, textiles, autos,
máquinas, químicos, muebles, etc. No incluye el campo, la minería, la construcción ni los servicios.
*Frase:* «Cuando digo industria hablo de las fábricas, no del campo ni del comercio.»

**Rama industrial.** Un grupo de actividades parecidas. En este trabajo se usan **16 ramas** (alimentos y bebidas, tabaco, textiles, prendas
de vestir/cuero/calzado, madera-papel-impresión, refinación de petróleo, químicos, caucho y plástico, minerales no metálicos, metálicas
básicas, productos de metal, maquinaria y equipo, electrónica-eléctricos-instrumentos, automotores, otro equipo de transporte y muebles y
otras manufacturas). Es como dividir el «cajón de la industria» en 16 cajones.

**Importación / exportación.** Importar es comprar bienes al exterior; exportar es venderlos. La **balanza comercial** es exportaciones
menos importaciones: si es positiva hay superávit y si es negativa, déficit.

**CIF y FOB.** Dos formas de valuar un producto que cruza la frontera. **CIF** incluye el costo del producto más el flete y el seguro hasta llegar
al país (se usa para importaciones). **FOB** es el valor puesto a bordo en el país de origen, sin flete ni seguro (se usa para exportaciones).
*Ejemplo:* una máquina cuesta 100 en fábrica, 8 de flete y seguro: FOB = 100, CIF = 108. Por eso comparar importaciones CIF con exportaciones FOB
hace que el saldo parezca un poco peor de lo que es.

**Dólares corrientes vs. toneladas.** El valor en dólares mezcla dos cosas: **cantidad** y **precio**. Las toneladas miden solo la cantidad.
Si en dólares se importa lo mismo pero en toneladas se importa el doble, significa que lo importado es más barato por kilo. Por eso el dashboard
permite mirar las importaciones en las dos unidades.
*Frase:* «Los dólares dicen cuánto gastamos; las toneladas dicen cuánto entró. Si no coinciden, cambió el precio o el tipo de producto.»

**Insumos, bienes de capital y bienes de consumo.** Los **insumos** son materias primas y piezas que otras fábricas usan (por ejemplo, acero
o químicos); los **bienes de capital** son máquinas y equipos; los **bienes de consumo** son productos terminados para el hogar (ropa,
electrodomésticos). Esta distinción es clave: importar un bien de consumo **compite** con la producción local, mientras que importar un insumo o una
máquina puede **ayudarla**. El trabajo los separa con la clasificación **BEC** de Naciones Unidas (ver 5.7), y es lo que explica la respuesta.

**Exposición a las importaciones.** Qué tan fuerte es la presencia de productos importados en el mercado de una rama. La medida ideal
sería «importaciones / consumo aparente del país», pero requiere el valor de la producción en dólares por rama, que no está disponible. La medida principal es
**cuánto crecieron las importaciones de cada rama** entre 2018 y 2025 (ver 5.6).

### 2.2 Conceptos del mercado de trabajo

**Empleo registrado.** Trabajadores en relación de dependencia, en empresas privadas, **declarados al sistema previsional (SIPA)**. No incluye
trabajo informal, cuentapropistas ni empleo público. Se cuenta en **puestos de trabajo**: si una persona tiene dos empleos registrados, cuenta
como dos puestos.
*Frase:* «Cuando digo empleo me refiero al empleo formal privado; el informal no aparece en esta fuente.»

**Salario real.** El salario nominal (en pesos) dividido por los precios (IPC). Mide **cuánto se puede comprar** con el sueldo. Si el salario
nominal sube 10% pero los precios suben 20%, el salario real cayó.

**IPC (Índice de Precios al Consumidor).** Mide cuánto suben los precios de una canasta de consumo. Sirve para «descontar la inflación».

**Aguinaldo.** El sueldo anual complementario que se paga en junio y diciembre. Como la remuneración «por todo concepto» lo incluye, en esos
meses el salario medido sube de golpe. Por eso **no se comparan meses sueltos** (ver 5.3).

### 2.3 Conceptos de producción

**IPI manufacturero (Índice de Producción Industrial).** Mide el **volumen físico** que produce la industria (cantidades, no pesos). Lo publica INDEC
con base 2004 = 100. Es un índice: interesa cuánto cambia, no el número absoluto.

**Capacidad instalada utilizada.** Qué porcentaje de la capacidad de las plantas se usa. Si es 60%, las fábricas podrían producir 40% más con las máquinas que
ya tienen. Una capacidad baja y en caída indica **planta ociosa**.

### 2.4 Conceptos estadísticos (explicados para no técnicos)

**Índice base 100.** Se toma un valor de referencia (un año o un promedio) y se lo iguala a 100; el resto se expresa en relación con él. Un 90
significa 10% menos que la referencia. Permite **comparar la forma** de series que están en unidades distintas (puestos, pesos, toneladas).

**Promedio móvil de 12 meses.** Cada punto es el promedio de ese mes y los 11 anteriores. Elimina la estacionalidad (diciembre y enero producen menos;
junio y diciembre tienen aguinaldo) y muestra la tendencia. Tiene un costo: los cambios se ven **suavizados y con algunos meses de demora**.

**Punto porcentual (p.p.).** La diferencia entre dos porcentajes. Pasar de 18% a 23% es un aumento de **5 p.p.**, no de 5%.

**Correlación.** Una medida, de -1 a +1, de si dos cosas se mueven juntas. +1: cuando una sube, la otra también, siempre. -1: cuando una sube, la otra
baja. 0: no hay relación. **Correlación no es causalidad:** que los helados y los ahogamientos suban juntos en verano no significa que los helados
ahoguen a alguien (ambos dependen del calor).

**Correlación de Spearman (ρ).** Una correlación calculada sobre el **orden** (ranking) de los datos en vez de sobre sus valores. Es más robusta cuando hay
pocos datos (16 ramas) y algunos valores extremos: un solo dato muy raro no la domina.

**p-valor.** La probabilidad de ver una relación tan fuerte como la observada **si en realidad no hubiera ninguna**. Si es menor a 0,05 se dice que la relación
es «estadísticamente significativa». *Ojo:* no mide qué tan importante es la relación, sino qué tan poco probable es que sea casualidad.
*Analogía:* si tiro una moneda 10 veces y salen 9 caras, sospecho que está trucada; el p-valor cuantifica esa sospecha.

**Problema de las comparaciones múltiples.** Si se prueban 24 relaciones y el umbral es 5%, **se espera que 1 o 2 salgan «significativas» solo por azar**
(24 × 5% = 1,2). Por eso cada p-valor se muestra con su versión **corregida** (método de Benjamini-Hochberg): solo lo que resiste la corrección cuenta como resultado.

**Modelo de panel con efectos fijos.** Un panel sigue a las **mismas unidades (ramas) a lo largo del tiempo (años)**. Los **efectos fijos de rama** eliminan las
diferencias permanentes entre ramas (por ejemplo, que alimentos siempre sea más grande que tabaco); los **efectos fijos de año** eliminan lo que le pasa a toda la industria a
la vez (una devaluación, una recesión). Lo que queda es: *«cuando las importaciones de una rama suben respecto de lo habitual para esa rama, ¿su empleo sube o baja
respecto de lo habitual para esa rama?»*.

**Intervalo de confianza al 95%.** El rango de valores razonablemente compatible con la estimación. Si incluye el cero, no se puede distinguir de «sin efecto».

**Elasticidad.** Cuánto cambia (en %) una variable cuando otra cambia 1%. En el panel se usa `log(resultado) ~ log(importaciones)`, por lo que el
coeficiente es una elasticidad; se expresa como «efecto de un aumento de 10%» para que sea más fácil de leer.

---

## 3. La pregunta, las hipótesis y los distintos puntos de vista

### 3.1 Por qué importa

En los últimos años en Argentina se discutió mucho si las importaciones dañan a la industria nacional y al empleo, o si son necesarias para
producir y para que los precios bajen. Es una discusión con posturas fuertes, y por eso conviene resolverla con datos y no con impresiones.

### 3.2 La pregunta de investigación

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**

Es una pregunta de **coincidencia**, no de causa: se pregunta si las pérdidas se concentran en los sectores más expuestos, no si las importaciones las provocaron.

Se divide en tres preguntas más concretas:

1. **Descriptiva:** ¿qué le pasó a la industria (empleo, salario real, producción, empresas) y al comercio exterior?
2. **De reasignación:** ¿el resultado total esconde ramas que crecieron y ramas que se achicaron?
3. **De asociación (la central):** ¿los sectores que más perdieron son los mismos donde más crecieron las importaciones o más avanzó China?

### 3.3 Hipótesis

- **H1 (la del «tema»):** las ramas donde más crecieron las importaciones perdieron más empleo, producción y salario.
- **H0 (la contraria):** no hay relación, o la relación es la opuesta (más importaciones acompañan más actividad).
- **H2 (China):** el avance de China se asocia con peores resultados, incluso si las importaciones totales no lo hacen.

Un trabajo serio **no parte de la conclusión**: se plantea qué relación existe y se deja que los datos confirmen o refuten. Que la hipótesis H1 no se confirme es
un resultado válido y publicable.

### 3.4 Los distintos puntos de vista (para la discusión oral)

| Punto de vista | Qué sostiene | Qué evidencia de este trabajo lo apoya | Qué evidencia lo debilita |
|---|---|---|---|
| **Proteccionista / industrialista** | Las importaciones, en especial de China, destruyen empleo industrial y hay que protegerlas | Prendas y textiles: muchas más toneladas importadas y fuerte pérdida de empleo. El peso de China se asocia con peor producción (ρ = -0,74, la única de 24 que resiste la corrección) | Las 8 ramas donde más crecieron las importaciones sumaron 27.072 puestos; con bienes de consumo no hay relación con el empleo (ρ = 0,01) |
| **Aperturista / liberal** | Importar abarata insumos y acceso a tecnología; el problema de la industria son otros factores (costos, impuestos, tipo de cambio, recesión) | Las importaciones de insumos crecen con el empleo (ρ = +0,78); la producción cayó también en ramas con pocas importaciones | Prendas y textiles: pérdidas grandes donde entraron muchas más toneladas de bienes de consumo |
| **Intermedio / técnico** | Importaciones que compiten y que complementan tienen efectos opuestos y hay que separarlas | **Es lo que muestran los datos:** insumos ρ = +0,78 con el empleo; consumo ρ = 0,01 | Ninguna correlación de consumo es significativa: tampoco prueba que la competencia no afecte |
| **Macroeconómico** | La caída industrial se explica por la recesión, el tipo de cambio y la demanda interna, no por importaciones | La producción cae desde 2023 en 13 de 16 ramas, incluso en ramas cuyas importaciones bajaron (Madera y papel -14%, Metálicas básicas -20% en dólares desde 2023); la tendencia previa (2011-2017) explica el empleo mejor que las importaciones | No se midieron variables macro (tipo de cambio real, consumo); es una explicación plausible que este trabajo no puede probar |

*Frase para la exposición:* «Este trabajo no toma partido: muestra qué dicen los datos y qué no pueden decir.»

### 3.5 Lo que este trabajo NO pretende hacer

- No demuestra **causalidad** (que las importaciones «causen» una caída).
- No evalúa políticas (aranceles, cepo, tipo de cambio).
- No mide bienestar del consumidor (precios más bajos, variedad).
- No estudia empleo informal, público, ni servicios.

---

## 4. Los datos

Todos los datos son **públicos y oficiales**. Los archivos originales están en `data/raw/` (con su propio `README.md`) y los ya procesados, que lee
la aplicación, en `data/processed/`.

### 4.1 Resumen de fuentes

| Dato | Quién lo publica | Qué mide | Unidad | Cobertura | Para qué se usa |
|---|---|---|---|---|---|
| Importaciones por producto (NCM) y país | INDEC (sistema comex) | Cada operación de importación agregada por producto, país de origen y año | USD CIF, USD FOB (desde 2019), kg | 2016-2025, anual | Cuánto se importa, desde dónde y qué rama lo recibe |
| Exportaciones por producto y país | INDEC (comex) | Ídem para exportaciones | USD FOB, kg | 2016-2025, anual | Balanza comercial por rama |
| Códigos de país | ARCA | Tabla oficial de países | | vigente | Identificar el origen de cada operación |
| Empleo asalariado privado registrado, por CIIU | Ministerio de Trabajo, OEDE (SIPA) | Puestos de trabajo | puestos | 1996-1T 2026, trimestral | Empleo por rama |
| Remuneraciones por CIIU | Ministerio de Trabajo, OEDE (SIPA) | Remuneración media | pesos corrientes | 1995-mar 2026, mensual | Salarios (con el IPC, salario real) |
| Empresas activas por CIIU | Ministerio de Trabajo, OEDE | Empresas privadas con al menos un empleado registrado | empresas | 1996-2024, anual | Cierres netos de empresas |
| IPI manufacturero | INDEC | Volumen físico de producción, por rama y subrama | índice base 2004=100 | 2016-jul 2026, mensual | Producción |
| Utilización de la capacidad instalada | INDEC | % de la capacidad usada, por bloque | % | 2016-2026, mensual | Planta ociosa |
| IPC nacional | INDEC | Nivel de precios | índice | dic 2016-ago 2026, mensual | Deflactar salarios |
| Correspondencia HS → BEC | Banco Mundial (WITS) | Uso económico de cada producto | | HS 2012, 2017 y 2022 | Separar bienes de consumo, insumos y capital |

### 4.2 Cómo se obtuvieron los datos de comercio exterior

El sitio del INDEC (comex) funciona con JavaScript y no ofrece un botón de descarga simple. Se buscó dentro del propio código del sitio el patrón de
las direcciones de descarga (`/files/zips/{imports|exports}_{año}_Y.zip`) y se automatizó con el script `src/download_comex.py`, que baja cada año, extrae solo
las tablas principales y sus **totales de control** y es idempotente (no vuelve a descargar lo que ya está). Los archivos de comercio pesan cerca de 100 MB y por eso no
se guardan en el repositorio.

### 4.3 Las clasificaciones (por qué hubo que «traducir»)

Cada fuente usa un idioma distinto para agrupar:

| Fuente | Clasificación | Qué clasifica | Ejemplo |
|---|---|---|---|
| Comercio exterior | **NCM** (Nomenclatura Común del Mercosur), 8 dígitos | Productos | 6403 = calzado |
| Empleo, salarios, empresas | **CIIU** (actividades), 2 dígitos | Actividades de la empresa | 19 = curtido de cuero, calzado |
| Producción (IPI) | Divisiones del IPI | Actividades | «Prendas de vestir, cuero y calzado» |

Para poder cruzar todo, se llevó todo a las **16 ramas del IPI**, que es la agrupación más gruesa de las tres. El paso de producto (NCM) a rama se hace por
capítulo (los 2 primeros dígitos), con excepciones a 4 dígitos (computadoras, motos y bicicletas, iluminación). Además:

- Se excluye lo que **no es manufactura**: agro sin procesar, petróleo crudo, gas, carbón, electricidad, oro y piedras sin trabajar.
  Ese resto se llama internamente `NO_IND` (unos USD 7,2 mil millones de las importaciones de 2025).
- Del petróleo y sus derivados, solo cuentan los **derivados refinados** (rama «Refinación de petróleo»).

*Frase:* «Es como traducir tres idiomas a uno solo para poder compararlos; la traducción no es perfecta, pero es consistente en todo el trabajo.»

### 4.4 Controles de calidad (cómo se sabe que los datos están bien)

| Control | Resultado |
|---|---|
| Comercio exterior: cantidad de registros y valor total de importaciones y exportaciones contra los totales de control que publica INDEC | **Coinciden exactamente en los 10 años** |
| Empleo: la suma de las 16 ramas contra el subtotal oficial «Industria» de OEDE | **Igual en todos los trimestres** |
| Salarios: salario nominal ponderado por puestos contra la serie oficial «Industrias manufactureras» | **Entre 0,99 y 1,00** |

En la página «Método y límites» está la tabla año por año de los controles de comercio exterior.

### 4.5 Qué NO tienen los datos (importante para las preguntas)

- **Valor de la producción por rama** en dólares (no se puede calcular la participación de las importaciones en el consumo).
- **Horas trabajadas** (solo puestos).
- **Empleo informal, cuentapropista o público.**
- **Dimensión territorial** (provincias o departamentos).
- **Tipo de cambio real ni precios de importación.**
- **Exportaciones confidenciales:** desde 2018 INDEC oculta cerca de 5% de las exportaciones por secreto estadístico y no se pueden asignar a una rama.

### 4.6 Datos que están en la carpeta pero no se usaron

`exportaciones_importaciones_intensidad_tecnologica.csv` (comercio por intensidad tecnológica, clasificaciones de Lall y UNCTAD) e
`impo_soja_y_sub_productos_acum_2002_2025.xlsx`. Son material disponible para ampliar el trabajo (ver `pasos_a_seguir.md`).

---

## 5. El método, paso a paso

Cada paso incluye **qué se hizo**, **por qué** y **cómo explicarlo** sin tecnicismos.

### 5.1 Una clasificación común de 16 ramas

*Qué:* todo se lleva a las 16 ramas (sección 4.3). *Por qué:* sin un idioma común no se pueden cruzar comercio, empleo y producción.
*Alternativa:* usar más detalle (subramas), pero las fuentes de empleo y salarios no lo permiten de forma consistente.

### 5.2 «Total industria» es solo manufactura

Todo total de empleo, salario o producción se refiere a la manufactura (CIIU 15 a 37), **no a toda la economía**. Los totales de comercio exterior del
Resumen, en cambio, incluyen **todos los bienes** (combustibles, productos agropecuarios, etc.).

### 5.3 Promedios de 12 meses, nunca meses sueltos

*Qué:* las variaciones comparan el **promedio de un año base** con el **promedio de los últimos 12 meses** (4 trimestres en empleo).
*Por qué:* el IPI es bajo en diciembre y enero; la remuneración incluye aguinaldo en junio y diciembre. Comparar, por ejemplo, junio contra octubre daría
diferencias que no existen.
*Costo:* las curvas suavizadas muestran los cambios con algunos meses de demora.

### 5.4 Salario real

`salario real = remuneración nominal / IPC`, promediando los CIIU de cada rama **ponderados por sus puestos de trabajo** (un CIIU con más gente pesa más).
El IPC nacional continuo empieza en diciembre de 2016, por lo que **no hay salario real antes de 2017**. Es un salario **registrado** medio, no el
salario de una persona específica.

### 5.5 La ventana de la respuesta: 2018 → 2025

*Qué:* la respuesta compara cada rama entre el **promedio de 2018** y el **promedio de 2025**, el último año completo en todas las fuentes.
*Por qué:* así importaciones y resultados miden el mismo período (el comercio exterior llega a 2025; el empleo, a 2026).
Las páginas descriptivas, en cambio, muestran el **último dato** de cada fuente (empleo: 1T 2026) y usan dos años base, 2018 y 2023: por eso dicen que pierden empleo
14 de 16 ramas (1T 2018 → 1T 2026) y la respuesta dice 8 de 16 (2018 → 2025). La diferencia es la caída de 2024-2026.

### 5.6 La medida principal y las de robustez

La medida principal sale de la pregunta («donde más crecieron las importaciones») y se eligió antes de mirar resultados: **crecimiento % de las importaciones en dólares** de cada rama.
Las demás sirven para ver si la respuesta cambia al medir distinto:

| Medida | Qué captura | Papel |
|---|---|---|
| Importaciones en dólares (Δ%) | Cuánto más gasta el país en lo que produce esa rama | **Principal** |
| Importaciones en toneladas (Δ%) | Cantidad, sin efecto de precios | Robustez |
| Aumento de importaciones por puesto de trabajo (USD) | Tamaño del aumento respecto del tamaño de la rama (medida de Autor, Dorn y Hanson) | Robustez |
| Importaciones por uso económico (consumo, insumos, capital) | Qué compite y qué abastece | Robustez central (5.7) |
| Participación de China (nivel y aumento), base 2023 | El debate público sobre China; lo reciente | Complemento |

### 5.7 Importaciones por uso económico (BEC)

Cada producto importado (NCM; sus primeros 6 dígitos son el código internacional HS) se clasifica con las tablas oficiales HS → BEC del Banco Mundial en **bienes de consumo**
(alimentos para hogares, bienes durables y no durables, autos de pasajeros), **insumos** (materias primas, partes, combustibles) y **bienes de capital** (máquinas y equipo).
Se clasifica 99,9% del valor importado y la suma por rama coincide con el total.
*Frase:* «Separé lo que compite con la fábrica de lo que la fábrica compra para producir.»

### 5.8 Comparación entre ramas: grupos y correlaciones

- **Grupos:** las 16 ramas se parten por la mediana del crecimiento de las importaciones: 8 donde más crecieron y 8 donde menos. Se suman los puestos de cada grupo y se compara
  la mediana de producción y salario.
- **Correlación de Spearman** entre las 16 ramas, con un **intervalo de confianza** por bootstrap y el **p-valor corregido** (Benjamini-Hochberg).
- **Sensibilidad:** se repite sacando cada rama de a una, ponderando por el tamaño de cada rama y controlando la **tendencia previa** (empleo 2011-2017).

Se eligió Spearman porque con 16 datos y valores muy dispares (alimentos importa +80% y refinación -43%), la correlación común (Pearson) la domina un solo punto.

### 5.9 Complementos: China, base 2023 y modelo de panel

El análisis original (4 medidas × 3 resultados × 2 años base = 24 correlaciones, y un **modelo de panel** con efectos fijos de rama y de año, 2016-2025) se mantiene como complemento.
De las 24 correlaciones, 3 dan p < 0,05 y **1 resiste la corrección**: el peso de China en 2025 con la producción desde 2018 (ρ = -0,74). El panel da relaciones positivas
(+0,2% de empleo por +10% de importaciones con todas las ramas, no significativa; +0,8% sin refinación de petróleo): es el efecto de los insumos, no que importar cree empleo.

### 5.10 Lo que el método NO hace

No controla por tipo de cambio, demanda interna, aranceles ni tecnología; no distingue empresas grandes de chicas; y con 16 ramas solo detecta relaciones grandes (|ρ| de 0,5 o más).
Mide **coincidencias**: para hablar de causas haría falta otra fuente de variación (sección 7.3). Se detalla en la sección 8.

---

## 6. Recorrido por la aplicación

Cada gráfico de la aplicación trae su propia explicación (qué muestra, cómo leerlo y qué se observa, con cifras calculadas de los datos), así que esta sección solo dice
**qué aporta cada pestaña a la respuesta**. La versión anterior, con un guion por página, quedó en `archivo/explicacion_version_anterior.md`.

| Pestaña | Qué aporta a la respuesta | Qué mostrar si hay poco tiempo |
|---|---|---|
| Presentación | La pregunta, los datos y la respuesta en tres cifras | La diapositiva «Qué encontré» |
| Resumen | Qué se perdió (hallazgos 1 a 4) y la respuesta (hallazgo 5) | El hallazgo 5 y la nota de los dos períodos |
| Importaciones | De dónde vienen, qué ramas las reciben, China y qué tipo de bienes se importan | Secciones 3 (crecimiento por rama) y 7 (uso económico) |
| Empleo y ramas | En qué ramas se perdió empleo y desde cuándo | El mapa de calor y los puestos por rama |
| **Importaciones vs. resultados** | **La respuesta**, si cambia al medir distinto y los complementos | Sección A completa y la 6 (uso económico) |
| Comparador de ramas | Una rama frente a la pregunta (sus importaciones, su grupo, su empleo) | Prendas contra Alimentos |
| Conclusiones | El informe de 8 hojas A4 | Hoja 6 (la respuesta) y 7 (conclusiones) |
| Método y límites | Decisiones, controles y qué no se puede concluir | «Qué no se puede concluir» |
| Datos | Cada archivo original y dónde se descarga | Si preguntan de dónde salen los datos |

---

## 7. Conclusiones

### 7.1 Lo que sí se puede afirmar

1. **La industria produce menos y paga menos:** entre 2018 y 2025, producción -5,6% y salario real -7,5% (en las 16 ramas). Desde 2023, el empleo cae 5,1% (1T 2026) y hay 900 empresas menos.
2. **Las pérdidas no se concentraron donde más crecieron las importaciones; en general fue al revés:** +27.072 puestos en las 8 ramas donde más crecieron y -18.152 en las 8 donde menos.
3. **El «al revés» lo explican los insumos:** el crecimiento de las importaciones de insumos va junto con el del empleo (ρ = +0,78, resiste la corrección); el de bienes de consumo, no (ρ = 0,01).
4. **La excepción son prendas y textiles:** muchas más toneladas importadas de bienes de consumo y fuertes pérdidas de empleo.
5. **China avanzó** (18,4% del valor importado en 2018, 23,7% en 2025) y su peso se asocia con peor producción, pero mide sobre todo la composición de la industria.

### 7.2 Lo que NO se puede afirmar

- Que las importaciones **causaron** la pérdida de empleo o de producción en prendas, textiles u otras ramas.
- Que las importaciones **no** afectaron a la industria (ausencia de evidencia no es evidencia de ausencia; con 16 ramas, un efecto moderado no se detecta).
- Que importar **crea** empleo (la relación positiva es de los insumos que compran las ramas que crecen).
- Que el avance de China **explique** la caída de la producción.
- Nada sobre empleo informal, público o por provincias.

### 7.3 Qué haría falta para responder mejor

1. **Una fuente de variación externa** para pasar de «coincide» a «provoca»: lo que China le vende a otros países parecidos (Autor, Dorn y Hanson) o la apertura de importaciones de 2024.
2. **Datos a nivel de producto** (NCM de 4 a 6 dígitos), comparados con la producción física del mismo producto.
3. **Valor de la producción por rama** para el índice de exposición clásico.
4. **Tipo de cambio real** y otros controles macro.

Detalle en `pasos_a_seguir.md`.

---

## 8. Limitaciones

| # | Limitación | Por qué importa | Cómo se mitiga hoy | Qué haría falta |
|---|---|---|---|---|
| 1 | **Asociación no es causalidad** | En el período hubo devaluaciones, recesión, pandemia y cambios de política a la vez | Se dice explícitamente en todas las páginas; se usan efectos fijos de año | Diseño con variación exógena (por ejemplo, cambios de aranceles) |
| 2 | **El uso económico es aproximado** | Un insumo importado también puede competir con quien lo produce en el país | Se clasifica con la tabla oficial BEC; se muestran los tres usos | Datos por producto y por empresa |
| 3 | **Solo 16 ramas** | Poco poder estadístico; errores poco confiables | Se usa Spearman (robusta) y se informan intervalos | Más desagregación (producto) o más períodos |
| 4 | **Comparaciones múltiples** | Se esperan 1-2 «significativas» por azar | Cada p-valor se muestra con su versión corregida (Benjamini-Hochberg) | Una medida principal decidida antes (ya está) |
| 5 | **Exposición medida con sustitutos** | No es el índice de manual | Se usan 4 medidas distintas | Valor de la producción por rama |
| 6 | **Empleo solo registrado privado** | No incluye informalidad, cuentapropistas ni público | Se aclara siempre | Otras fuentes (EPH) |
| 7 | **Sin horas trabajadas** | Las empresas pueden reducir horas sin despedir | Se indica como límite | EPH u otras fuentes |
| 8 | **Valores nominales en dólares corrientes** | No descuentan inflación internacional | Se complementa con toneladas | Deflactar por precios internacionales |
| 9 | **Exportaciones confidenciales (~5%)** | No se pueden asignar a una rama | Se informa en el gráfico de balanza | No hay solución con datos públicos |
| 10 | **Traducción NCM → CIIU aproximada** | Un mismo producto puede servir a más de una actividad | Se aplica el mismo criterio a todo; se excluyen los productos primarios | Una tabla oficial de correspondencia detallada |
| 11 | **Promedios de 12 meses suavizan** | Los cambios se ven con demora | Se explica en cada gráfico | Mostrar también las series mensuales |
| 12 | **Fechas de corte distintas por fuente** | «Últimos 12 meses» termina en fechas distintas (empleo 1T 2026, producción jul 2026, salario mar 2026) | La respuesta usa la ventana común 2018 → 2025; el resto indica la fecha de cada indicador | — |
| 13 | **El resultado del panel depende de una rama (refinación)** | Fragilidad de la conclusión | Se muestran ambas muestras; la respuesta se repite sacando cada rama de a una (ninguna cambia el signo) | — |
| 14 | **Diferencias de tamaño entre ramas** | Un % chico en una rama grande son muchos puestos | Se muestran puestos absolutos y una versión ponderada (depende de Alimentos) | — |
| 15 | **Tendencias previas** | Las ramas que perdían empleo en 2011-2017 son, en gran parte, las que lo pierden ahora | Se controla en la prueba de sensibilidad | Modelos con tendencia por rama |

---

## 9. Banco de preguntas y repreguntas

Preguntas generales, ordenadas de más básicas a más difíciles. Cada una tiene una respuesta corta, posibles repreguntas y, cuando corresponde, otros puntos de vista.

### 9.1 Preguntas sobre el tema

**1. ¿De qué trata el trabajo en una frase?**
Mide si, desde 2018, la industria perdió empleo, producción y salario justo en las ramas donde más crecieron las importaciones, con datos oficiales; la respuesta es que no, salvo en prendas y textiles.

**2. ¿Por qué eligieron la industria y no otros sectores?**
Porque es el sector donde el debate sobre importaciones es más directo (productos que se pueden importar o producir localmente) y porque las fuentes oficiales permiten llevar comercio exterior, empleo y producción a una misma clasificación.
*Repregunta:* ¿Y los servicios? — No están comprometidos por importaciones de bienes; sería otro estudio.

**3. ¿Qué es una «rama»?**
Un grupo de actividades industriales parecidas (por ejemplo, textiles). Se usan 16.

**4. ¿Por qué 2016-2026?**
Es el período que cubren los datos de comercio exterior (2016-2025), la producción industrial (hasta julio de 2026) y el empleo (hasta el 1T 2026). La respuesta usa 2018 → 2025, el último año completo en todas las fuentes. Se podría ampliar hacia atrás: comex tiene datos desde 2002.

### 9.2 Preguntas sobre los datos

**5. ¿De dónde salen los datos? ¿Son confiables?**
De INDEC, del Ministerio de Trabajo (OEDE/SIPA) y de ARCA: fuentes oficiales y públicas. Se validaron: los totales de comercio coinciden exactamente con los que publica INDEC en los 10 años; la suma de las 16 ramas de empleo es igual al subtotal oficial en todos los trimestres.

**6. ¿Cómo bajaron los datos si el sitio del INDEC no tiene botón de descarga?**
Se buscó en el código del propio sitio el patrón de las direcciones de descarga y se automatizó con un script. Es reproducible: `python src/download_comex.py`.

**7. ¿Qué es el «empleo registrado»? ¿Y el informal?**
Empleo en relación de dependencia declarado al sistema previsional. El informal (sin registrar) no está en la fuente. Este trabajo **no** habla del empleo informal.
*Otro punto de vista:* si parte del ajuste se dio por la informalidad, el empleo registrado sobreestimaría la caída (o la subestimaría, si hubo formalización): no se sabe.

**8. ¿Por qué hay «NO_IND» y qué es?**
Lo importado que no es manufactura (agro sin procesar, petróleo crudo, gas, minerales, oro). Se excluye del análisis por rama, pero sí forma parte del total de importaciones del Resumen. En 2025 fueron unos USD 7,2 mil millones de 75,8.

**9. ¿Por qué el total del Resumen (USD 75,8 mil millones) no coincide con la suma de las ramas (68,6)?**
Porque el total incluye todo lo importado, y la suma de ramas solo las importaciones de origen manufacturero.

**10. ¿Por qué las series de empleo, producción y salario terminan en fechas distintas?**
Cada fuente publica con un rezago distinto. Se indica la fecha de cada indicador en la página.

### 9.3 Preguntas sobre el método

**11. ¿Por qué promedios de 12 meses?**
Para evitar comparar meses con estacionalidad distinta. Ejemplo: comparar el salario de junio con el de octubre daría una diferencia por aguinaldo, no por poder de compra.

**12. ¿Por qué Spearman y no Pearson?**
Porque con 16 datos y valores muy dispares, Pearson la domina un solo punto. Spearman usa el orden y es más robusta.
*Repregunta:* ¿Y si usaran Pearson? — Los resultados podrían cambiar, sobre todo por ramas extremas (alimentos, refinación). Es una prueba de sensibilidad posible.

**13. ¿Qué es un efecto fijo?**
Una variable que absorbe diferencias permanentes (de cada rama) o comunes (de cada año), para quedarse solo con lo que cambia dentro de cada rama respecto de las demás.

**14. ¿Por qué ese modelo (logaritmos)?**
Porque los coeficientes se interpretan como porcentajes («+10% de importaciones → +x% de empleo») y son comparables entre ramas de tamaños distintos.

**15. ¿Por qué la respuesta usa 2018 → 2025 y otras páginas 2018 y 2023?**
La respuesta necesita el mismo período para importaciones y resultados (2018 → 2025). Las páginas descriptivas muestran lo más reciente y comparan con 2018 (largo plazo) y 2023 (antes de la caída). Ver 5.5.

**16. ¿Por qué no usaron el índice de exposición clásico?**
Porque requiere el valor de la producción por rama en dólares (cuentas nacionales / matriz insumo-producto), que no está en los datos disponibles. Se usa el crecimiento de las importaciones y, como robustez, las importaciones por puesto de trabajo (la medida de la literatura).

**17. ¿Cómo se calcula el salario real de una rama?**
Se divide cada remuneración por el IPC y se promedian las actividades (CIIU) de la rama, ponderadas por sus puestos de trabajo.

**18. ¿Qué es «significativo»?**
Que el p-valor es menor a 0,05: hay menos de 5% de probabilidad de ver esa relación por casualidad si no existiera. No significa que sea importante ni que sea causal.

### 9.4 Preguntas sobre resultados

**19. ¿Cuál es el resultado principal?**
Que no: desde 2018 la industria perdió producción y salario, pero no justo en las ramas donde más crecieron las importaciones. Las 8 ramas donde más crecieron sumaron 27.072 puestos; las 8 donde menos crecieron perdieron 18.152.

**20. ¿Por qué «al revés»? ¿Importar crea empleo?**
No. Lo que crece con el empleo son las importaciones de **insumos** (ρ = +0,78): una rama que produce más compra más materias primas, partes y máquinas. Con los **bienes de consumo**, que son los que compiten, no hay relación (ρ = 0,01).
*Repregunta:* ¿Y si sacan Alimentos? — La relación ponderada por tamaño deja de ser significativa (p = 0,47): depende de esa rama.

**21. ¿Qué rama es la excepción?**
Prendas, cuero y calzado: sus importaciones crecieron 36% en dólares y 61% en toneladas, y perdió 13.922 puestos entre 2018 y 2025 (-18,8%; contra el 1T 2018, -22.641). Textiles importó 45% más en toneladas, aunque solo 5% más en dólares, y perdió 4.330.
*Repregunta:* ¿Es por China? — En Prendas, China perdió peso (de 44% a 39% de lo importado); en Textiles ganó (de 39% a 53%).

**22. ¿Cuánto empleo se perdió?**
Contra el 1T 2023, -64.907 puestos (-5,1%). Contra el 1T 2018, -45.383 (-3,6%). Con promedios anuales, 2025 estaba igual que 2018 (+0,7%): la pérdida es de 2024 en adelante.

**23. ¿Cuánto empleo se perdió «por culpa» de las importaciones?**
No se puede calcular: haría falta un efecto causal. El trabajo mide coincidencias.

**24. ¿Se puede decir que China destruye la industria argentina?**
No con estos datos. El peso de China se asocia con peor producción (es la única de 24 correlaciones que resiste la corrección), pero mide sobre todo en qué sectores vende China (textiles, muebles), que caen en muchos países.

**25. Si donde más se importó se ganó empleo, ¿está todo bien?**
No: la industria produce 5,6% menos que en 2018, los salarios reales son 7,5% más bajos y desde 2023 se perdieron 64.907 puestos. Que no coincida con las importaciones no significa que no haya problema.

**26. ¿Por qué la producción cae y el empleo menos?**
Por retención de personal, costos de despido o menor productividad. Los datos muestran el patrón pero no la causa.

**27. ¿Qué pasó con los salarios?**
Cayeron fuerte entre 2017 y 2020, tocaron un mínimo en agosto de 2024 y se recuperaron en parte: hoy están +2,4% sobre 2023 y -7,9% bajo 2018 (12 meses a marzo de 2026).

### 9.5 Preguntas difíciles o «trampa»

**28. «Entonces, ¿defienden abrir o cerrar las importaciones?»**
Ni una cosa ni la otra. El trabajo describe y mide; no evalúa políticas. Puede decirse que los datos no muestran que abrir destruya empleo en general, pero tampoco descartan que haya efectos en ramas específicas.

**29. «Con solo 16 datos, ¿cómo concluyen algo?»**
Con cautela: por eso no se afirman causas, se usan pruebas robustas (Spearman) y se muestran los límites. Es un análisis exploratorio, no confirmatorio.

**30. «Si probaron 24 combinaciones, ¿no está buscando hasta que salga algo?»**
Es una crítica válida. Por eso la respuesta usa **una medida principal** elegida por la pregunta, y cada p-valor se muestra corregido por comparaciones múltiples: de las 24 correlaciones originales resiste 1, y de las 9 de la respuesta, ninguna.

**31. «El modelo da positivo, ¿entonces importar crea empleo?»**
No. Es una **correlación** que probablemente refleja que las ramas que crecen importan más insumos. Para probar causalidad hace falta otra estrategia.

**32. «¿Por qué no miran el tipo de cambio?»**
Es un control importante que falta. Se incluyó en la lista de mejoras (datos del BCRA). Parte del efecto queda capturada por los efectos fijos de año, que absorben lo común a todas las ramas.

**33. «¿No será que la caída industrial es por la recesión y no por importaciones?»**
Es una explicación plausible y compatible con los datos: la producción cae en 13 de 16 ramas, incluso en ramas cuyas importaciones bajaron (Madera y papel, Metálicas básicas). Los efectos fijos de año en el modelo de panel intentan descontar lo común a toda la industria.

**34. «¿Cómo saben que sus cálculos están bien?»**
Por los controles: comercio coincide con los totales oficiales en los 10 años; empleo suma igual al subtotal oficial; el salario ponderado coincide con la serie oficial (0,99 a 1,00); y las páginas se probaron con todas las combinaciones de filtros sin errores.

**35. «¿Qué haría distinto si tuviera más tiempo?»**
(1) Buscar una fuente de variación externa para hablar de causas (lo que China le vende a otros países parecidos); (2) bajar al nivel de producto en prendas y textiles; (3) incluir tipo de cambio real; (4) extender el período a 2002.

**36. «¿Qué le diría a un político con este informe?»**
Que las pérdidas de la industria desde 2018 no coinciden con el crecimiento de las importaciones en general (gran parte de lo que se importa son insumos que la industria necesita), pero sí en prendas y textiles, que merecen un análisis por producto antes de cualquier decisión.

---

## 10. Guion para presentar oralmente

### 10.1 Antes de la presentación (checklist)

1. Abrir la terminal de VS Code y correr la aplicación (pasos en `README.md`). Comprobar que abre en `http://localhost:8501`.
2. Recorrer las 9 pestañas una vez para que carguen.
3. Tener este documento abierto en el segundo monitor o impreso: secciones 1.2 (cifras), 6 (recorrido) y 9 (preguntas).
4. Tener a mano tres cifras: **+27.072 / -18.152 puestos** (donde más y donde menos se importó), **ρ = +0,78 insumos / 0,01 consumo** y **-13.922 en Prendas**.
5. Elegir de antemano **dos ramas** para el comparador (por ejemplo, Prendas/calzado y Alimentos).

### 10.2 Estructura recomendada (20 minutos)

| Minuto | Qué mostrar | Qué decir | Sección de este documento |
|---|---|---|---|
| 0-2 | Presentación (portada, tema, preguntas) | La pregunta y por qué importa | 1.1, 3 |
| 2-4 | Presentación (datos) y Método y límites | Qué datos, cómo se llevaron a 16 ramas, los controles | 4, 5 |
| 4-7 | Resumen (hallazgos 1 a 4) | Qué se perdió y desde cuándo | 1.2 |
| 7-9 | Importaciones (secciones 3 y 7) | Cuánto creció cada rama; qué tipo de bienes se importan | 5.7 |
| 9-15 | **Importaciones vs. resultados (A y B)** | La respuesta, por qué «al revés» (insumos vs. consumo), la excepción y qué tan firme es | 1.3, 5.6-5.8 |
| 15-17 | Comparador (Prendas y Alimentos) | Las dos caras de la respuesta | 9.4 |
| 17-20 | Conclusiones (hoja 7) y Método (límites) | Lo que se puede y no se puede afirmar; qué haría después | 7, 8 |

### 10.3 Versión corta (5 minutos)

1. **Pregunta** (30 s): «Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?»
2. **Datos y método** (1 min): 16 ramas, INDEC y Ministerio de Trabajo, controles contra los totales oficiales; se compara 2018 con 2025.
3. **Qué se perdió** (1 min): producción -5,6% y salario real -7,5% desde 2018; empleo -5,1% desde 2023.
4. **La respuesta** (1,5 min): no; donde más se importó se ganaron 27.072 puestos y donde menos se perdieron 18.152; lo que crece con el empleo son los insumos; la excepción, prendas y textiles.
5. **Cierre** (1 min): es una coincidencia, no un efecto; para hablar de causas haría falta otra fuente de variación.

### 10.4 Versión de 10 minutos

Las secciones 1 a 5 de la tabla anterior, sin Comparador; con una rama de ejemplo.

### 10.5 Frases útiles

- Para abrir: «Antes de hablar de resultados, quiero aclarar qué se mide y qué no.»
- Para explicar el método: «Es como comparar el promedio de un año con el de otro, para no engañarnos con los meses de aguinaldo.»
- Para una correlación: «Ver que dos cosas suben juntas no prueba que una cause la otra.»
- Para un resultado inconcluso: «Con estos datos no se puede afirmar; para eso haría falta una fuente de variación que no dependa de la propia industria.»
- Para una pregunta que no se sabe: «Ese dato no está en este trabajo, pero es un buen punto: quedaría como una mejora.»
- Para cerrar: «El aporte es mostrar qué dicen los datos y qué no pueden decir.»

### 10.6 Cómo manejar preguntas difíciles

1. **Reconocer la pregunta:** «Es una crítica válida.»
2. **Responder lo que se sabe** con una cifra.
3. **Decir el límite** sin dramatizar: «Eso no lo podemos afirmar con estos datos.»
4. **Proponer el paso siguiente:** «Para responderlo haría falta…»
5. **Si no se sabe:** no inventar. «No lo tengo calculado; lo revisaría y lo agrego.»

### 10.7 Errores frecuentes a evitar

- Decir «las importaciones destruyeron empleo» o «no tienen ningún efecto»: ninguna de las dos se puede afirmar.
- Confundir **valor** con **toneladas** o **participación** con **monto**.
- Confundir p.p. con %.
- Presentar una correlación sin su p corregido, o decir «importar crea empleo».
- Olvidar que el empleo es **registrado**.

---

## 11. Estructura del proyecto y cómo se reproduce

```
dashboard/              Inicio.py (navegación), paginas/ (una por pestaña) y core/ (datos, gráficos, tarjetas, estilo)
src/                    carga de archivos, clasificación en ramas (ramas.py) y por uso económico (uso_economico.py), cálculos (analysis.py)
notebooks/              los tres cuadernos que generan los datos procesados
data/raw/               datos originales (con su README)
data/processed/         datos procesados que lee la aplicación
tests/                  pruebas automáticas: datos contra totales oficiales y cada pestaña sin errores
actualizar_datos.py     regenera todos los datos procesados con un comando
README.md               pasos para ejecutar la aplicación
explicacion.md          este documento
pasos_a_seguir.md       lo que falta y lo que se mejoró
analisis_profesional/   revisión del trabajo y evaluación final
archivo/                documentos de etapas anteriores
```

### 11.1 Cómo se generaron los datos procesados

Los tres cuadernos de `notebooks/` se ejecutan en orden y escriben los archivos de `data/processed/`. Todo se regenera con `.\.venv\Scripts\python.exe actualizar_datos.py`
(se comprobó que regenerar desde cero da exactamente los mismos archivos):

| Cuaderno | Qué hace | Archivos que produce |
|---|---|---|
| `01_limpieza_comercio_exterior` | Lee los CSV anuales de comex, **valida año por año contra los totales de control**, asigna cada producto a una rama | `importaciones_rama_pais_anio`, `exportaciones_rama_anio`, `resumen_comercio_anual`, `control_comex` |
| `02_limpieza_empleo_salarios_industria` | Extrae las series de los Excel de OEDE e INDEC con las funciones de `src/loaders.py` y las verifica contra los subtotales oficiales | `empleo_por_rama`, `empresas_por_rama`, `salario_real_por_rama`, `ipi_por_rama`, `ipi_subramas`, `capacidad_instalada` |
| `03_analisis_por_rama` | Series suavizadas, cambios por rama, comercio por rama, importaciones por uso económico, la respuesta (2018 → 2025), correlaciones, grupos y modelo de panel | `series_indexadas`, `cambios_por_rama`, `empleo_mismo_trimestre`, `comercio_por_rama_anio`, `importaciones_por_uso`, `respuesta_*`, `panel_rama_anio`, `exposicion_vs_resultados`, `correlaciones`, `grupos_exposicion`, `regresiones_panel`, `ipi_subramas_*` |

Las funciones de cálculo (medias móviles, ventanas de cambio, correlaciones, panel) están en `src/analysis.py`; la clasificación de ramas y el mapeo NCM/CIIU en `src/ramas.py`; la lectura de cada formato de archivo en `src/loaders.py`; y la descarga de comercio exterior en `src/download_comex.py`.

### 11.2 Organización del código del dashboard

- **`core/datos.py`**: carga de datos con caché y nombres cortos de las ramas.
- **`core/formato.py`**: formato de números y fechas en español.
- **`core/consultas.py`**: consultas frecuentes sobre las tablas (cambio de un indicador por rama, empleo por trimestre, estimación del panel).
- **`core/graficos.py`**: constructores de gráficos (líneas, barras, mapa de calor, dispersión, etc.).
- **`core/tema.py`**: colores, estilo de los gráficos y hoja de estilos de la aplicación.
- **`core/ui.py`**: bloques de presentación (recuadro con gráfico y explicación, notas, síntesis).
- **`core/tarjetas.py`**: las tarjetas tipo afiche del Resumen y de Importaciones vs. resultados.
- **`paginas/*.py`**: cada página tiene una función por sección y una función `mostrar()`; los textos de interpretación se calculan a partir de los datos, no se escriben a mano.

---

## 12. Fuentes

- **INDEC – Comercio exterior (comex):** bases anuales de importaciones y exportaciones por producto (NCM) y país. `comex.indec.gob.ar`
- **INDEC – Índice de producción industrial manufacturero (IPI)** y **utilización de la capacidad instalada.**
- **INDEC – Índice de precios al consumidor (IPC)**, nivel nacional.
- **Ministerio de Trabajo (OEDE) – Sistema Integrado Previsional Argentino (SIPA):** empleo asalariado privado registrado, remuneraciones y empresas, por actividad (CIIU).
- **ARCA – Tabla de códigos de país** (F2668).
- **Banco Mundial (WITS) – Tablas de correspondencia HS → BEC** (uso económico de los productos, clasificación de Naciones Unidas).
