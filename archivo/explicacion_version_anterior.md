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
6. [Resultados, página por página](#6-resultados-página-por-página)
7. [Conclusiones](#7-conclusiones)
8. [Limitaciones](#8-limitaciones)
9. [Banco de preguntas y repreguntas](#9-banco-de-preguntas-y-repreguntas)
10. [Guion para presentar oralmente](#10-guion-para-presentar-oralmente)
11. [Estructura del proyecto y cómo se reproduce](#11-estructura-del-proyecto-y-cómo-se-reproduce)
12. [Fuentes](#12-fuentes)

---

## 1. Resumen ejecutivo

### 1.1 En 30 segundos

Se estudió qué pasó con la **industria argentina** entre 2016 y 2026 (empleo, salarios y producción) y si se perdió empleo, producción y
salario justo en los sectores donde más crecieron las **importaciones** o más avanzó **China**. Se cruzaron datos oficiales del INDEC y del
Ministerio de Trabajo, agrupados en 16 ramas industriales. Resultado: la industria **retrocede desde 2023** y hubo una **reasignación de
empleo entre ramas** (perdieron textiles, prendas y calzado, y madera y papel; ganaron alimentos y maquinaria), pero **no aparece una relación
simple y consistente de «más importaciones, menos empleo»**. Los datos disponibles no alcanzan para afirmar causas.

### 1.2 En 3 minutos: las cifras que hay que saber

| Tema | Cifra | Qué significa |
|---|---|---|
| Empleo industrial (4T 2025) | **1.206.593 puestos** | Trabajadores asalariados privados registrados en la industria manufacturera |
| Empleo vs. 4T 2018 | +15.318 (+1,3%) | Casi igual que hace siete años |
| Empleo vs. 4T 2023 | **-62.506 (-4,9%)** | Retroceso desde el último año de recuperación |
| Producción (IPI) vs. 2023 | **-9,4%** | Promedio de los últimos 12 meses contra el promedio de 2023 |
| Producción (IPI) vs. 2018 | -7,1% | |
| Salario real vs. 2023 | +2,3% | Recuperación parcial |
| Salario real vs. 2018 | **-8,0%** | Sigue por debajo de 2018: la caída principal fue entre 2017 y 2020 |
| Empresas industriales activas | 54.970 (2023) → 54.070 (2024) | **900 empresas menos** (-1,6%) |
| Importaciones totales 2025 | **USD 75,8 mil millones** | +24,7% respecto de 2024 |
| China en las importaciones 2025 | **23,7%** del valor total (13,1% de las toneladas) | El valor más alto de la serie 2016-2025 |
| Correlaciones probadas | 24, de las cuales **solo 2 son significativas** | No hay un patrón general «más importaciones, peor resultado» |

### 1.3 La respuesta corta a la pregunta

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**
> Depende de cómo se mida la exposición. Cuando se mide con el **avance de China**, hay señales de peor producción y peor salario en las ramas
> más expuestas. Cuando se mide con el **crecimiento de las importaciones en general**, no hay evidencia de peores resultados: incluso las ramas con
> más importaciones tuvieron mejor empleo (porque muchas importaciones son insumos y maquinaria que acompañan a la actividad). Para separar
> «importaciones que compiten» de «importaciones que complementan» hacen falta datos que este trabajo no tiene, y por eso **no se afirman causas**.

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
máquina puede **ayudarla**. Los datos usados no permiten separar estos tipos, y esa es la principal limitación del trabajo (ver sección 8).

**Exposición a las importaciones.** Qué tan fuerte es la presencia de productos importados en el mercado de una rama. La medida ideal
sería «importaciones / consumo aparente del país», pero requiere el valor de la producción en dólares por rama, que no está disponible. Por eso se usan
**cuatro medidas sustitutas** (ver 5.6).

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
(24 × 5% = 1,2). Por eso una sola relación significativa aislada no alcanza para concluir.

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
| **Proteccionista / industrialista** | Las importaciones, en especial de China, destruyen empleo industrial y hay que protegerlas | Textiles, prendas/calzado y muebles: fuerte avance de China, caída de producción y de empleo. El avance de China se asocia con peor producción (ρ = -0,74) y salario | Alimentos importa mucho más y su empleo creció (+8,1% contra 2018); Automotores importa más y su empleo se mantiene (+0,1% contra 2018); solo 2 de 24 correlaciones son significativas |
| **Aperturista / liberal** | Importar abarata insumos y acceso a tecnología; el problema de la industria son otros factores (costos, impuestos, tipo de cambio, recesión) | Las importaciones acompañan la actividad: el panel da relación positiva empleo-importaciones; la producción cayó también en ramas con pocas importaciones | El caso de textiles, con caída fuerte de producción y avance de China del 39% al 53% |
| **Intermedio / técnico** | Importaciones que compiten y que complementan tienen efectos opuestos y hay que separarlas | Es exactamente el límite del trabajo: el signo positivo del panel sugiere insumos | Para probarlo faltan datos por uso económico (bienes de consumo, insumos, capital) |
| **Macroeconómico** | La caída industrial se explica por la recesión, el tipo de cambio y la demanda interna, no por importaciones | La producción cae desde 2023 en 13 de 16 ramas, incluso en ramas cuyas importaciones bajaron (Madera y papel -14%, Metálicas básicas -20% en dólares desde 2023); importaciones y producción caen juntas en 2019-2020 | No se midieron variables macro (tipo de cambio real, consumo); es una explicación plausible que este trabajo no puede probar |

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
| Empleo asalariado privado registrado, por CIIU | Ministerio de Trabajo, OEDE (SIPA) | Puestos de trabajo | puestos | 1996-2025, trimestral | Empleo por rama |
| Remuneraciones por CIIU | Ministerio de Trabajo, OEDE (SIPA) | Remuneración media | pesos corrientes | 1995-mar 2026, mensual | Salarios (con el IPC, salario real) |
| Empresas activas por CIIU | Ministerio de Trabajo, OEDE | Empresas privadas con al menos un empleado registrado | empresas | 1996-2024, anual | Cierres netos de empresas |
| IPI manufacturero | INDEC | Volumen físico de producción, por rama y subrama | índice base 2004=100 | 2016-jul 2026, mensual | Producción |
| Utilización de la capacidad instalada | INDEC | % de la capacidad usada, por bloque | % | 2016-2026, mensual | Planta ociosa |
| IPC nacional | INDEC | Nivel de precios | índice | dic 2016-ago 2026, mensual | Deflactar salarios |

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

- **Uso económico de lo importado** (consumo / insumo / capital).
- **Valor de la producción por rama** en dólares (no se puede calcular la participación de las importaciones en el consumo).
- **Horas trabajadas** (solo puestos).
- **Empleo informal, cuentapropista o público.**
- **Dimensión territorial** (provincias o departamentos).
- **Tipo de cambio real ni precios de importación.**
- **Exportaciones confidenciales:** desde 2018 INDEC oculta cerca de 5% de las exportaciones por secreto estadístico y no se pueden asignar a una rama.

### 4.6 Datos que están en la carpeta pero no se usaron

`exportaciones_importaciones_intensidad_tecnologica.csv` (comercio por intensidad tecnológica, clasificaciones de Lall y UNCTAD) e
`impo_soja_y_sub_productos_acum_2002_2025.xlsx`. Son material disponible para ampliar el trabajo (ver `posibles_a_realizar.md`).

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

### 5.5 Los dos años base: 2018 y 2023

Se usan dos puntos de comparación:

- **2018:** un año previo a la pandemia y al ciclo reciente; permite ver el cambio «de largo plazo» (siete años).
- **2023:** el último año de recuperación, antes del retroceso reciente; permite ver «lo que pasó últimamente».

Se muestran los dos porque **las conclusiones dependen del punto de partida** y elegir uno solo podría parecer forzado. Los cambios son
**promedio del año base vs. promedio de los últimos 12 meses disponibles** (los datos de empleo llegan al 4T 2025, la producción a julio de 2026 y los
salarios a marzo de 2026, por lo que «últimos 12 meses» termina en fechas distintas para cada indicador; se indica en cada gráfico).

### 5.6 Cuatro maneras de medir la exposición a las importaciones

La medida ideal (importaciones / consumo aparente) necesita el valor de la producción por rama, que no está. Se usan cuatro sustitutos, todos calculados entre el
año base y 2025:

| Medida | Cómo se calcula | Qué captura | Debilidad |
|---|---|---|---|
| Crecimiento de las importaciones (USD) | Variación % del valor CIF importado por la rama | Cuánto más gasta el país en esa rama | Mezcla cantidad y precio |
| Crecimiento de las importaciones (toneladas) | Variación % del peso importado | Cantidad importada, sin efecto de precios | Toneladas no distinguen productos caros y baratos |
| Aumento de la participación de China (p.p.) | Puntos porcentuales que China ganó en lo importado por la rama | Si China gana lugar frente a otros orígenes | No dice cuánto se importa en total |
| Participación de China (nivel) | % del valor importado por la rama que viene de China en 2025 | Dependencia de China | Es una foto de 2025, no un cambio |

### 5.7 Correlación de Spearman entre ramas

Para cada combinación (4 medidas de exposición × 3 resultados × 2 años base = **24 combinaciones**) se calcula la correlación de Spearman entre las
16 ramas. Se eligió Spearman porque con 16 datos y valores muy dispares (por ejemplo, alimentos importa +80% y refinación -43%), la correlación común
(Pearson) la domina un solo punto.

### 5.8 Ramas de mayor vs. menor exposición

Las 16 ramas se parten por la **mediana** de cada medida de exposición: 8 de mayor y 8 de menor exposición. Se compara la **mediana** del cambio de empleo, salario y producción en
cada mitad. Es un análisis descriptivo, sin prueba estadística; sirve para ver «con los ojos» si los grupos difieren.

### 5.9 Modelo de panel con efectos fijos

`log(resultado) ~ log(1 + importaciones) + efecto fijo de rama + efecto fijo de año`, con errores agrupados por rama. Cubre 2016-2025 (160 observaciones: 16 ramas × 10 años).
Se estiman **24 variantes** combinando: 3 resultados (empleo, producción, salario real) × 2 medidas de importaciones (totales y desde China) × 2 muestras (todas las ramas o
sin refinación de petróleo) × 2 momentos (mismo año o año anterior). Se reporta el efecto de **+10% de importaciones**.

**Por qué «sin refinación de petróleo»:** es una rama atípica (sus importaciones cayeron 43% mientras su producción subió), y una rama muy distinta puede mover los
resultados. Que el resultado cambie tanto al excluirla es en sí un hallazgo: **la conclusión es frágil**.

### 5.10 Lo que el método NO hace

No controla por tipo de cambio, demanda interna, aranceles ni tecnología; no separa importaciones que compiten de las que complementan; no distingue empresas grandes de chicas; y con 16 ramas
tiene poco poder estadístico. Esto se detalla en la sección 8.

---

## 6. Resultados, página por página

Recorrido por el dashboard tal como se puede mostrar en vivo. Cada sección tiene: qué hay en pantalla, las cifras clave, **qué decir**, las **preguntas probables**
con sus respuestas, **repreguntas** y **otros puntos de vista**.

### 6.1 Página «Resumen»

**En pantalla:** la pregunta, los datos y el enfoque; cinco indicadores clave; cinco hallazgos; tres gráficos de contexto (industria, comercio exterior, China).

**Los cinco hallazgos, con sus cifras:**

1. **El empleo casi no cambió desde 2018, pero por dentro hubo una reasignación grande.** Total: +15.318 puestos (+1,3%) entre el 4T 2018 y el 4T 2025. Pero contra el promedio
   de 2018 perdieron **Prendas, cuero y calzado (-13.935 puestos, -18,8%)**, **Madera, papel e impresión (-11.239, -11,4%)** y **Textiles (-4.340, -7,0%)**, y ganaron **Alimentos y bebidas
   (+31.251, +8,1%)**, **Maquinaria y equipo (+5.830, +8,5%)** y **Químicos (+3.542, +3,4%)**.
2. **Desde 2023 la industria retrocede.** Empleo -62.506 puestos (-4,9%) entre el 4T 2023 y el 4T 2025; producción -9,4%; 900 empresas activas menos. La producción cae
   más que el empleo (-9,4% contra -3,2% en promedios de 12 meses): las empresas ajustaron menos personal que producción.
3. **El salario real se recuperó parcialmente:** +2,3% sobre 2023 pero -8,0% respecto de 2018. La caída principal fue entre 2017 (índice 118,2) y 2020; el mínimo fue 96,0 en agosto de 2024.
4. **Textiles y prendas/calzado están entre las ramas más golpeadas:** producción -34,5% y -18,4% respecto de 2023; empleo -9,3% y -12,1%.
5. **La relación con las importaciones es matizada.** De 24 asociaciones, solo 2 son significativas. En el panel, +10% de importaciones se asocia con +0,2% de empleo (no significativo); sin refinación de petróleo,
   +0,8% (significativo y positivo).

**Sobre los tres gráficos de contexto:**

- *La industria en un gráfico:* la producción tocó su piso de 83,7 en agosto de 2020 y el empleo el suyo de 89,9 en julio de 2020; el empleo llegó a su máximo (100,0) en enero de 2024 y la producción a 102,6 en mayo de 2023;
  desde entonces la producción cae hasta 90,6 (jul-2026) y el empleo hasta 96,8. El salario real parte de 118,2 (nov-2017), toca 96,0 (ago-2024) y remonta a 102,3 (mar-2026).
- *Comercio exterior:* importaciones mínimas de USD 42,4 mil millones en 2020 y máximas de 81,7 en 2022; la mayor caída anual fue en 2019 (-25,0%) mientras las exportaciones subían, y solo hubo déficit en 2017, 2018 y 2023.
  En 2025 las importaciones subieron 24,7% hasta USD 75,8 mil millones, con saldo positivo de USD 11,3 mil millones.
- *China:* entre 2016 y 2024 la participación se movió entre 18,4% y 21,4%; en 2025 saltó a 23,7% (+4,5 p.p. respecto de 2024).

**Qué decir (guion de 1 minuto):** «La industria argentina tiene hoy prácticamente los mismos puestos que en 2018, pero por dentro cambió mucho: se achicaron textiles, prendas y madera y papel; crecieron alimentos y
maquinaria. Desde 2023 el empleo cae casi 5% y la producción cerca de 9%. Además las importaciones crecieron 25% en 2025 y China llegó a casi una cuarta parte. La pregunta es si estas dos cosas están relacionadas.»

**Preguntas probables y respuestas**

- **P: ¿Por qué el empleo industrial «casi no cambió» si hubo una crisis?**
  R: Porque se compara 2018 con 2025 y en el medio hubo caída (pandemia) y recuperación. El total esconde pérdidas en unas ramas y ganancias en otras: alimentos ganó 31.251 puestos, mientras
  prendas y madera y papel perdieron más de 25.000 entre las dos.
  *Repregunta:* ¿Los que perdieron un puesto en prendas pasaron a alimentos? — *No se puede saber:* estos datos cuentan puestos, no personas; no hay seguimiento individual.
- **P: ¿Por qué la producción cae más que el empleo?**
  R: Hay varias explicaciones posibles: las empresas retienen personal esperando una recuperación, el costo de despedir es alto, o bajó la productividad (se produce menos por persona). Los datos muestran el patrón,
  no la causa.
  *Otro punto de vista:* parte del ajuste puede estar en **horas** o en trabajo **informal**, que estos datos no miden.
- **P: ¿El salario real +2,3% es una buena noticia?**
  R: Es parcial. Está 2,3% por encima de 2023 pero 8% por debajo de 2018. Además es el salario **registrado promedio**: no dice nada de los que pierden el empleo ni de quienes trabajan informalmente.
- **P: ¿Por qué dice «Total industria» y no toda la economía?**
  R: Porque todos los totales de empleo, salario y producción son de manufactura (CIIU 15 a 37). El comercio exterior del Resumen, en cambio, incluye todos los bienes.

### 6.2 Página «Importaciones»

**En pantalla (6 secciones):**

1. **Cuánto se importa y de dónde** (barras apiladas por origen).
2. **Cuánto pesa cada origen** (participación de Brasil, China, Estados Unidos y Alemania).
3. **Cuánto crecieron las importaciones de cada rama respecto de 2018** (mapa de calor).
4. **Dónde más avanzó China** (gráfico de dos puntos, 2018 vs. 2025).
5. **Valor, volumen y precio de una rama** (selector de rama).
6. **Balanza comercial por rama** (selector de año).

Hay un selector arriba para medir en **valor (USD)** o en **toneladas**, que afecta a las secciones 1, 2 y 3.

**Cifras clave:**

- Total importado (todos los bienes): USD 65,5 mil millones en 2018 → 75,8 en 2025 (+15,7%). Solo las 16 ramas industriales: 57,2 → 68,6 (+19,9%) en valor, pero en toneladas 20,7 → 20,4 millones (**-1,7%**).
  Es decir: se paga más pero entra casi lo mismo, lo que indica que **subió el precio por kilo o cambió el tipo de producto importado**.
- Lo importado desde China subió de USD 10,5 a 17,9 mil millones entre 2016 y 2025 (+71,3%), mucho más que el total (+35,7%).
- Orden de origen en 2025 (valor): Brasil 24,2%, China 23,7%, Estados Unidos 8,7%, Alemania 4,1%.
- China pesa **23,7% del valor pero 13,1% de las toneladas** en 2025: compra a China son manufacturas caras por kilo; lo que llega de otros orígenes (por ejemplo, graneles) pesa mucho más en toneladas.
- Mapa de calor (valor): en 2020, **15 de 16 ramas** importaban menos que en 2018 (recesión y pandemia); en 2025, **14 de 16** superan el nivel de 2018 en valor (12 de 16 en toneladas). Mayores aumentos: Alimentos y bebidas +80,4%,
  Prendas, cuero y calzado +35,6%, Maquinaria y equipo +31,1%; cae Refinación de petróleo -43,2%.
- China por rama (2018 → 2025): Caucho y plástico 12% → 27%, Textiles 39% → 53%, Productos de metal 24% → 34%. China provee la mitad o más de lo importado en **Muebles (59%)**, **Otro equipo de transporte (54%)** y **Textiles (53%)**;
  ganó terreno en 12 de 16 ramas y perdió en Prendas, cuero y calzado (44% → 39%).
- Las ramas que más importan en dólares en 2025: Automotores (USD 13,2 mil millones, 10% de China), Químicos (12,4; 19%), Electrónica (11,6; **46%**), Maquinaria (11,2; 28%).
- Ejemplo valor-volumen-precio (Textiles, 2018 → 2025): valor +4,9%, toneladas +45,1%, precio por kilo -27,7%: se importa mucho más volumen a menor precio.
- Balanza comercial 2025 (solo ramas industriales, FOB): déficit total de **USD 24,3 mil millones**. Los mayores déficits: Electrónica (-10,8), Maquinaria (-9,5), Químicos (-7,1), Automotores (-5,4). Solo Alimentos (**+20,2**) y Tabaco tienen superávit.

**Qué decir (guion de 2 minutos):** «Primero miramos de dónde vienen las importaciones: Brasil y China son los dos grandes orígenes y hoy están casi empatados. China ganó peso en 12 de las 16 ramas y en tres de ellas provee
más de la mitad de lo que se importa. Después vemos que no importa igual todo el mundo: en dólares se importa 20% más que en 2018, pero en toneladas casi lo mismo. Y la balanza muestra que el déficit industrial se
concentra en electrónica, maquinaria, químicos y automotores, mientras que alimentos es el único gran superávit.»

**Preguntas probables y respuestas**

- **P: ¿Qué diferencia hay entre valor y toneladas? ¿Cuál es «la verdadera»?**
  R: Ninguna es la verdadera: miden cosas distintas. El valor mezcla cantidad y precio; las toneladas miden cantidad pero no distinguen un kilo de plástico de un kilo de un microchip. Por eso se muestran las dos.
  *Repregunta:* ¿Entonces por qué elegir una para el análisis? — En las correlaciones se usan ambas como medidas separadas de exposición (4 medidas en total).
- **P: ¿China pasó a Brasil como principal origen?**
  R: No todavía en 2025: Brasil 24,2% y China 23,7% del valor. Pero China venía de 19,2% en 2024 y llegó a 23,7% en un año. En 2020-2022 China superó a Brasil en algunos años (por ejemplo, 2021: China 21,4%, Brasil 19,6%).
- **P: ¿Por qué el porcentaje de China es distinto en valor y en toneladas?**
  R: Porque las toneladas están dominadas por productos pesados y baratos (graneles, combustibles, minerales) que casi no vienen de China; el valor está dominado por manufacturas, donde China pesa mucho.
- **P: ¿La suba de las importaciones en 2025 es por más cantidad o más precio?**
  R: Según los datos industriales, las toneladas casi no cambiaron respecto de 2018 mientras el valor subió 20%. Eso sugiere precio o composición, aunque en el último año a nivel total también hubo mayor volumen: no conviene sobreinterpretar sin ver el desglose.
  *Otro punto de vista:* algunos economistas dirían que la suba nominal es en parte **inflación de precios en dólares**, porque los valores son corrientes y no están ajustados.
- **P: ¿Alimentos importa 80% más y sin embargo es la rama con mayor superávit?**
  R: Sí. Alimentos importa mucho (insumos, ingredientes), pero exporta más de USD 22 mil millones. Es un ejemplo clave de que **importar más no significa perder mercado**.
- **P: ¿Un déficit grande en electrónica es un problema?**
  R: Depende. Una rama con déficit grande depende de bienes importados, pero eso no es «bueno» ni «malo» por sí solo: Argentina casi no produce ciertos bienes electrónicos y los importa; el debate es de política industrial.

### 6.3 Página «Empleo y ramas»

**En pantalla:** selector de año base (2018 o 2023), cinco indicadores de toda la industria y tres gráficos: mapa de calor de cuatro indicadores por rama, barras de puestos ganados/perdidos, y
dispersión producción vs. empleo. Además, una tabla descargable.

**Cifras clave con base 2023:**

- **15 de las 16 ramas perdieron empleo** (solo Alimentos ganó: +7.263 puestos, +1,8%).
- 13 redujeron su producción, 4 tienen un salario real menor y 13 tienen menos empresas.
- **Caen en los cuatro indicadores a la vez:** Textiles, Minerales no metálicos y Metálicas básicas.
- La producción es el indicador con mayor dispersión: de **-34,5% en Textiles** a +10,8% en Otro equipo de transporte.
- Puestos perdidos: Prendas, cuero y calzado -8.306 (-12,1%), Madera, papel e impresión -5.967, Textiles -5.854 (-9,3%), Productos de metal -4.863, Minerales no metálicos -4.438. Las tres primeras concentran **42% de todos los puestos perdidos**;
  las ramas que perdieron suman -48.150 y las que ganaron +7.263: neto -40.887.
- Producción vs. empleo: por cada 10 puntos que cae la producción de una rama, su empleo varía en promedio 2 puntos. Ramas que redujeron su producción más de 15% pero perdieron menos de 5% de su empleo (**retuvieron personal**): Productos de metal, Maquinaria y equipo, Automotores.

**Qué decir (guion de 2 minutos):** «Este mapa de calor es la fotografía más clara: casi todas las ramas están en naranja en empleo. Textiles, minerales no metálicos y metálicas básicas empeoraron en los cuatro indicadores. Lo que muestra el gráfico de barras es dónde
están los puestos: tres ramas concentran el 42% de las pérdidas. Y el último gráfico muestra algo interesante: la producción se mueve unas cinco veces más que el empleo, o sea, las empresas retuvieron gente aunque produjeran mucho menos.»

**Preguntas probables y respuestas**

- **P: ¿Por qué usan dos años base?**
  R: Porque la conclusión depende del punto de partida. 2018 muestra el cambio de largo plazo (empleo total casi igual, +1,3%); 2023 muestra lo reciente (empleo -4,9%). Mostrar solo uno podría parecer una elección para llegar a un resultado.
- **P: ¿Qué quiere decir «retuvieron personal»?**
  R: Que la producción cayó mucho más que el empleo: las empresas mantuvieron gente aunque produzcan menos. Puede ser por costos de despido, expectativa de recuperación o suspensión temporal. Los datos no permiten saber el motivo.
- **P: ¿Por qué los porcentajes de ramas chicas «no cuentan igual»?**
  R: Porque un cambio de 10% en una rama de 4.000 puestos (Tabaco) son 400 personas, y en Alimentos (411.703 puestos) son 41.000. Por eso el gráfico de barras en puestos complementa al mapa de calor.
- **P: El salario real subió en muchas ramas pero el empleo cae. ¿Cómo se explica?**
  R: Puede ser un **efecto de composición**: si los puestos que se pierden son los de menor salario, el salario promedio sube sin que nadie gane más. Es una hipótesis, no un resultado.
  *Otro punto de vista:* también puede ser que las empresas que sobreviven paguen más. Los datos no permiten separar.
- **P: ¿Por qué Alimentos gana empleo?**
  R: Es la rama más grande (411.703 puestos), exportadora (más de USD 22 mil millones), y su producción creció. Es un ejemplo de rama que sube por otros motivos (demanda externa, agroindustria).
  *Repregunta:* ¿Y no será que la rama absorbe empleo de otras? — Los datos no permiten afirmarlo.

### 6.4 Página «Importaciones vs. resultados»

Es la página **central**: intenta responder la pregunta de investigación.

**En pantalla:** tres filtros (base 2018/2023, medida de exposición, resultado) y cuatro secciones: (1) dispersión con correlación de Spearman, (2) mapa de las 12 combinaciones para la base elegida, (3) mayor vs. menor exposición, (4) modelo de panel.

**Cifras clave:**

- **Correlaciones:** de 24 probadas, solo 2 son significativas al 5%:
  - *Participación de China en las importaciones (nivel) con Δ% producción, base 2018:* ρ = **-0,74**, p = 0,001. Las ramas donde China pesa más en las importaciones tuvieron peor producción.
  - *Aumento de la participación de China (p.p.) con Δ% salario real, base 2023:* ρ = **-0,54**, p = 0,031.
- Una relación **casi significativa** pero de signo **contrario** a la hipótesis: crecimiento de las importaciones en USD con Δ% empleo, base 2018: ρ = **+0,49**, p = 0,053 (más importaciones, *mejor* empleo).
- **Ramas de mayor vs. menor exposición** (base 2018, crecimiento de importaciones en USD): la mediana del empleo fue **+0,5%** en las 8 ramas de mayor exposición y **-5,9%** en las 8 de menor; en producción -11,5% contra -19,9%; en salario real -10,4% contra -11,6%. **Las más expuestas evolucionaron mejor.**
  Con base 2023 y la participación de China (nivel), en cambio, el empleo fue -5,6% en las más expuestas contra -3,2% en las menos; y la producción -21,0% contra -4,4%.
- **Panel (todas las ramas):** +10% de importaciones totales → empleo **+0,2%** (intervalo de -0,7% a +1,1%; p = 0,64). Solo 1 de 12 estimaciones es significativa.
- **Panel sin refinación de petróleo:** +10% → empleo **+0,78%** (intervalo de +0,35% a +1,21%; p < 0,001). **11 de 12** estimaciones significativas y todas positivas.

**Qué decir (guion de 3 minutos):** «Acá está el corazón del trabajo. Probamos 24 relaciones entre cuánto se expuso cada rama a las importaciones y cómo le fue. Solo dos dieron significativas, y las dos tienen que ver con China, no con las importaciones en general.
Las ramas donde China pesa más tuvieron peor producción y peor salario. Pero cuando miramos las importaciones en general, no solo no hay peores resultados sino que las ramas que más importaron tuvieron incluso mejor empleo. La explicación más probable es que
importar acompaña a producir: una rama que crece necesita más insumos y maquinaria. Para separar lo que compite de lo que complementa faltarían datos que no tenemos.»

**Preguntas probables y respuestas**

- **P: ¿Entonces las importaciones NO destruyen empleo?**
  R: Este trabajo no puede afirmarlo ni negarlo. Lo que dice es que **entre estas 16 ramas y en este período no hay una relación negativa consistente** entre importaciones y empleo. Eso es distinto de «no tienen efecto». Un efecto real podría estar oculto porque las importaciones
  que compiten (bienes de consumo terminados) y las que complementan (insumos y maquinaria) tienen efectos opuestos y aquí están mezcladas.
- **P: Dos correlaciones significativas, ¿no es evidencia de que China afecta?**
  R: Es una señal, no una prueba. Con 24 pruebas se espera 1 o 2 «significativas» solo por azar (24 × 5% = 1,2). Además las dos aparecen con **bases y resultados distintos** (una con producción y base 2018, otra con salario y base 2023): un patrón que se repite entre medidas y bases sería más convincente.
  *Repregunta:* ¿Y por qué no corregir por comparaciones múltiples? — Es una mejora posible (por ejemplo, Bonferroni: exigiría p < 0,002 y solo sobreviviría la de ρ = -0,74, p = 0,001). Con 16 ramas el poder estadístico es limitado.
- **P: ¿Qué pasa si sacan refinación de petróleo? ¿No es hacer trampa?**
  R: No es hacer trampa, es un **control de robustez**: se muestra el resultado con y sin esa rama y se informan las dos. Refinación es atípica (importaciones -43%, producción +10%). Que al sacarla el efecto pase de no significativo a significativo indica que
  **la conclusión depende de una sola rama y es frágil**. Lo honesto es reportar ambos resultados.
- **P: ¿Qué significa «+0,78% de empleo por +10% de importaciones»? ¿Es mucho?**
  R: Es poco: si las importaciones de una rama suben 10%, su empleo sube menos de 1%. Además es una asociación: probablemente refleja que una rama que crece importa más, no que importar genere empleo.
- **P: ¿Por qué el modelo de panel «descuenta lo que le pasa a toda la industria»?**
  R: Porque en un año de crisis (por ejemplo 2020) todas las ramas caen juntas y esa caída no tiene que ver con importaciones específicas. Los efectos fijos de año quitan esa parte común y dejan solo lo que diferencia a unas ramas de otras.
- **P: Con 16 ramas, ¿es confiable?**
  R: Es limitado. 16 puntos por año y 160 observaciones en el panel (16 × 10) dan errores estándar poco confiables, y se probaron muchas combinaciones. Por eso las conclusiones son cautelosas.
- **P: ¿Cómo interpreto que las ramas más expuestas (por crecimiento de importaciones) evolucionaron mejor en empleo?**
  R: Tres explicaciones posibles, no excluyentes: (a) **efecto complementario**: mucho de lo importado son insumos y maquinaria para producir; (b) **causalidad inversa**: una rama que crece atrae importaciones; (c) **composición**: ramas grandes como alimentos, que crecen por exportación, empujan el resultado.
  *Otro punto de vista:* un proteccionista podría decir que igualmente hay ramas específicas (textiles, prendas, muebles) donde la relación sí es negativa; lo que muestra que el promedio esconde heterogeneidad.

### 6.5 Página «Comparador de ramas»

**En pantalla:** un selector de rama y siete bloques: (1) importaciones, producción, empleo y salario de la rama con 2018 = 100; (2) empleo, (3) producción y (4) salario real de la rama contra el total de la industria (2023 = 100);
(5) capacidad instalada utilizada; (6) empresas activas; (7) detalle de producción por producto. Cierra con una síntesis de la rama elegida.

**Cómo usarlo en vivo:** conviene mostrar 3 o 4 ramas para ver contrastes.

| Rama (2025 vs 2018 = 100) | Importaciones (ton.) | Empleo | Producción | Salario real | China (% de lo importado) | Lectura |
|---|---:|---:|---:|---:|---:|---|
| **Prendas, cuero y calzado** | 161 | 81 | 86 | 87 | 39% | Importaciones suben y producción, empleo y salario caen: patrón típico de pérdida de mercado |
| **Textiles** | 145 | 93 | 73 | 85 | 53% | Igual patrón, con China ya en más de la mitad |
| **Alimentos y bebidas** | 189 | 108 | 107 | 90 | 3% | Importaciones **suben más que en cualquier otra** y aun así producción y empleo crecen: importar y producir van juntos |
| **Automotores** | 106 | 100 | 95 | 96 | 10% | Importaciones y producción estables: la actividad no se explica por importaciones |
| **Refinación de petróleo** | 49 | 84 | 111 | 92 | 1% | Importaciones caen a la mitad, la producción sube pero el empleo baja: es la rama atípica |
| **Maquinaria y equipo** | 145 | 109 | 110 | 94 | 28% | Importaciones suben y también empleo y producción: importación de bienes de capital que acompaña a la actividad |

**Ejemplo desarrollado: Prendas, cuero y calzado.** Puestos: 57.386 (-11.604 contra el 4T 2023, -16,8%). Producción -18,4% contra 2023 y -21,0% contra 2018. Salario real +2,9% contra 2023 pero -13,4% contra 2018. Capacidad instalada del bloque textil:
46,6% contra 59,1% del total (jun-2026), con un mínimo de 4,2% en abril de 2020. Empresas: 4.113, índice 86,8 (2018 = 100) contra 97,3 del total. El último gráfico de la página separa los subsectores (prendas de vestir, curtido y artículos de cuero, calzado): sus trayectorias no son parejas, lo que muestra que la evolución de una rama puede concentrarse en algunos productos.

**Qué decir (guion de 3 minutos):** «Esta página permite verificar el análisis rama por rama. Miremos prendas y calzado: las importaciones en toneladas están 61% arriba de 2018, mientras la producción cayó 14%, el empleo 19% y el salario real 13%. Es el patrón de una rama que pierde mercado interno.
Ahora miremos alimentos: sus importaciones subieron casi 90% y sin embargo su producción y su empleo crecieron. Este contraste es exactamente por qué no hay una relación simple entre importaciones y resultados.»

**Preguntas probables y respuestas**

- **P: ¿Por qué comparar contra «Total industria»?**
  R: Para saber si lo que le pasó a la rama es propio o es parte de un movimiento general. Si la rama cae igual que el total, la causa probable es común (macro); si cae más, hay algo específico.
- **P: ¿Qué significa que la línea empiece en 100 en 2023?**
  R: Es un índice: todo se expresa relativo al promedio de 2023. Sirve para comparar formas, no niveles. La rama y el total no tienen los mismos niveles, pero sí se pueden comparar su recorrido.
- **P: ¿La capacidad instalada de Prendas es del bloque «textil»?**
  R: Sí, INDEC publica un bloque que agrupa varias ramas; por eso en algunas ramas la comparación es **aproximada**. Está indicado en cada gráfico.
- **P: ¿Cómo sé que los cambios de una rama no dependen de la elección de 2018?**
  R: Se muestran los dos años base en las otras páginas; en el comparador se usa 2018 para importaciones y empresas, y 2023 para empleo, producción y salario. Es una decisión de diseño (ver sección 5.5).

### 6.6 Página «Método y límites»

**En pantalla:** fuentes, decisiones de método, controles de calidad, qué no se puede concluir y un glosario. Sirve como **anexo metodológico** y como respuesta preparada a las preguntas difíciles.

**Cuándo mostrarla:** al final, o cuando alguien pregunte «¿cómo sabés que los datos están bien?» o «¿esto prueba que…?».

---

## 7. Conclusiones

### 7.1 Lo que sí se puede afirmar

1. **La industria retrocede desde 2023:** -4,9% de empleo, -9,4% de producción y 900 empresas menos.
2. **Hay una reasignación de empleo entre ramas:** ganaron Alimentos y Maquinaria; perdieron Prendas/calzado, Madera/papel y Textiles. Un total casi igual a 2018 esconde esa reasignación.
3. **China avanzó:** de 18,4% del valor importado en 2018 a 23,7% en 2025 (total de bienes) y provee más de la mitad de lo importado en Muebles, Otro equipo de transporte y Textiles.
4. **No hay evidencia general de «más importaciones, peor resultado»:** solo 2 de 24 correlaciones son significativas y no hay un patrón que se repita en todas las medidas y bases.
5. **Las importaciones parecen acompañar la actividad más que reemplazarla** en muchas ramas (alimentos, maquinaria), lo que explica el signo positivo del modelo de panel.
6. **La asociación con China es la más consistente** con la hipótesis de sustitución (peor producción y salario en ramas donde China pesa más), aunque no es concluyente.

### 7.2 Lo que NO se puede afirmar

- Que las importaciones **causaron** la pérdida de empleo o de producción en textiles, prendas u otras ramas.
- Que las importaciones **no** afectaron a la industria (ausencia de evidencia no es evidencia de ausencia).
- Que el avance de China **explique** la caída de la producción.
- Nada sobre empleo informal, público o por provincias.

### 7.3 Qué haría falta para responder mejor

1. **Clasificar las importaciones por uso económico** (consumo / insumo / capital): permite aislar las que compiten.
2. **Valor de la producción por rama** para el índice de exposición clásico.
3. **Tipo de cambio real** y otros controles macro.
4. **Datos a nivel de producto** (NCM de 4 a 6 dígitos): las ramas agrupan productos muy distintos.
5. **Más años de historia** (el sistema comex tiene datos desde 2002).

Estas mejoras están detalladas en `posibles_a_realizar.md`.

---

## 8. Limitaciones

| # | Limitación | Por qué importa | Cómo se mitiga hoy | Qué haría falta |
|---|---|---|---|---|
| 1 | **Asociación no es causalidad** | En el período hubo devaluaciones, recesión, pandemia y cambios de política a la vez | Se dice explícitamente en todas las páginas; se usan efectos fijos de año | Diseño con variación exógena (por ejemplo, cambios de aranceles) |
| 2 | **No se separan importaciones que compiten de las que complementan** | Efectos opuestos que se cancelan entre sí | Se muestra y se explica el signo positivo del panel | Clasificación por uso económico (BEC) |
| 3 | **Solo 16 ramas** | Poco poder estadístico; errores poco confiables | Se usa Spearman (robusta) y se informan intervalos | Más desagregación (producto) o más períodos |
| 4 | **Comparaciones múltiples (24 pruebas)** | Se esperan 1-2 «significativas» por azar | Se advierte explícitamente en la aplicación | Corrección formal (Bonferroni, FDR) |
| 5 | **Exposición medida con sustitutos** | No es el índice de manual | Se usan 4 medidas distintas | Valor de la producción por rama |
| 6 | **Empleo solo registrado privado** | No incluye informalidad, cuentapropistas ni público | Se aclara siempre | Otras fuentes (EPH) |
| 7 | **Sin horas trabajadas** | Las empresas pueden reducir horas sin despedir | Se indica como límite | EPH u otras fuentes |
| 8 | **Valores nominales en dólares corrientes** | No descuentan inflación internacional | Se complementa con toneladas | Deflactar por precios internacionales |
| 9 | **Exportaciones confidenciales (~5%)** | No se pueden asignar a una rama | Se informa en el gráfico de balanza | No hay solución con datos públicos |
| 10 | **Traducción NCM → CIIU aproximada** | Un mismo producto puede servir a más de una actividad | Se aplica el mismo criterio a todo; se excluyen los productos primarios | Una tabla oficial de correspondencia detallada |
| 11 | **Promedios de 12 meses suavizan** | Los cambios se ven con demora | Se explica en cada gráfico | Mostrar también las series mensuales |
| 12 | **Fechas de corte distintas por fuente** | «Últimos 12 meses» termina en fechas distintas (empleo 4T 2025, producción jul 2026, salario mar 2026) | Se indica la fecha de cada indicador | Alinear al último período común |
| 13 | **El resultado del panel depende de una rama (refinación)** | Fragilidad de la conclusión | Se muestran ambas muestras | Análisis dejando afuera cada rama de a una |
| 14 | **Diferencias de tamaño entre ramas** | Un % chico en una rama grande son muchos puestos | Se muestran puestos absolutos | Ponderar por tamaño |

---

## 9. Banco de preguntas y repreguntas

Preguntas generales, ordenadas de más básicas a más difíciles. Cada una tiene una respuesta corta, posibles repreguntas y, cuando corresponde, otros puntos de vista.

### 9.1 Preguntas sobre el tema

**1. ¿De qué trata el trabajo en una frase?**
Analiza si las ramas industriales donde más crecieron las importaciones (o más avanzó China) tuvieron peor empleo, salario y producción que las demás, con datos oficiales de 2016 a 2026.

**2. ¿Por qué eligieron la industria y no otros sectores?**
Porque es el sector donde el debate sobre importaciones es más directo (productos que se pueden importar o producir localmente) y porque las fuentes oficiales permiten llevar comercio exterior, empleo y producción a una misma clasificación.
*Repregunta:* ¿Y los servicios? — No están comprometidos por importaciones de bienes; sería otro estudio.

**3. ¿Qué es una «rama»?**
Un grupo de actividades industriales parecidas (por ejemplo, textiles). Se usan 16.

**4. ¿Por qué 2016-2026?**
Es el período que cubren los datos de comercio exterior descargados (2016-2025), la producción industrial (hasta julio de 2026) y el empleo (hasta el 4T 2025). Se podría ampliar hacia atrás: comex tiene datos desde 2002.

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

**15. ¿Por qué se usan dos años base?**
Porque la conclusión depende del punto de partida (sección 5.5).

**16. ¿Por qué no usaron el índice de exposición clásico?**
Porque requiere el valor de la producción por rama en dólares (cuentas nacionales / matriz insumo-producto), que no está en los datos disponibles. Se usaron 4 medidas sustitutas.

**17. ¿Cómo se calcula el salario real de una rama?**
Se divide cada remuneración por el IPC y se promedian las actividades (CIIU) de la rama, ponderadas por sus puestos de trabajo.

**18. ¿Qué es «significativo»?**
Que el p-valor es menor a 0,05: hay menos de 5% de probabilidad de ver esa relación por casualidad si no existiera. No significa que sea importante ni que sea causal.

### 9.4 Preguntas sobre resultados

**19. ¿Cuál es el resultado principal?**
La industria retrocede desde 2023, hubo reasignación de empleo entre ramas y no hay una relación general y consistente entre más importaciones y peores resultados; sí hay señales de que el avance de China se asocia con peor producción y salario.

**20. ¿Qué rama es la más golpeada?**
Textiles: producción -34,5% (contra 2023), empleo -9,3%, China pasó de 39% a 53% de lo importado, y cae en los cuatro indicadores. Prendas, cuero y calzado pierde más puestos (-8.306).
*Repregunta:* ¿Y qué rama se salva? — Alimentos: única con más empleo que en 2023 (+1,8%).

**21. ¿Cuánto empleo se perdió?**
Contra el 4T 2023, -62.506 puestos (-4,9%). Contra 2018, la industria tiene 15.318 más (+1,3%).

**22. ¿Cuánto empleo se perdió «por culpa» de las importaciones?**
No se puede calcular. Sería necesario un efecto causal. La estimación del panel, que da +2.682 puestos por cada +10% de importaciones (no significativa), indica que la relación **no es negativa**, pero no debe leerse como ganancia de empleo.

**23. ¿Se puede decir que China destruye la industria argentina?**
No con estos datos. Hay señales (peor producción y salario donde China pesa más; textiles, prendas y muebles con fuerte avance de China), pero son 2 de 24 asociaciones, con posible efecto del azar, y no controlan otras causas.

**24. Si las importaciones crecieron y el empleo no bajó, ¿está todo bien?**
No: el empleo total no cayó desde 2018, pero perdieron textiles, prendas y madera/papel; y desde 2023 la industria retrocede. «No hay relación con importaciones» no significa «no hay problema».

**25. ¿Por qué la producción cae y el empleo menos?**
Por retención de personal, costos de despido o menor productividad. Los datos muestran el patrón pero no la causa.

**26. ¿Qué pasó con los salarios?**
Cayeron fuerte entre 2017 y 2020, se estabilizaron, tocaron un mínimo en agosto de 2024 y se recuperaron. Hoy están +2,3% sobre 2023 y -8,0% bajo 2018.

**27. ¿Por qué el resultado cambia cuando se saca refinación?**
Porque esa rama es atípica: sus importaciones cayeron 43% mientras la producción subió. Que una sola rama cambie el resultado indica fragilidad.

### 9.5 Preguntas difíciles o «trampa»

**28. «Entonces, ¿defienden abrir o cerrar las importaciones?»**
Ni una cosa ni la otra. El trabajo describe y mide; no evalúa políticas. Puede decirse que los datos no muestran que abrir destruya empleo en general, pero tampoco descartan que haya efectos en ramas específicas.

**29. «Con solo 16 datos, ¿cómo concluyen algo?»**
Con cautela: por eso no se afirman causas, se usan pruebas robustas (Spearman) y se muestran los límites. Es un análisis exploratorio, no confirmatorio.

**30. «Si probaron 24 combinaciones, ¿no está buscando hasta que salga algo?»**
Es una crítica válida y está reconocida: con 24 pruebas se esperan 1-2 significativas por azar. Por eso se reportan todas (no solo las significativas) y se advierte que una sola celda no alcanza. Una corrección formal por comparaciones múltiples sería la mejora natural.

**31. «El modelo da positivo, ¿entonces importar crea empleo?»**
No. Es una **correlación** que probablemente refleja que las ramas que crecen importan más insumos. Para probar causalidad hace falta otra estrategia.

**32. «¿Por qué no miran el tipo de cambio?»**
Es un control importante que falta. Se incluyó en la lista de mejoras (datos del BCRA). Parte del efecto queda capturada por los efectos fijos de año, que absorben lo común a todas las ramas.

**33. «¿No será que la caída industrial es por la recesión y no por importaciones?»**
Es una explicación plausible y compatible con los datos: la producción cae en 13 de 16 ramas, incluso en ramas cuyas importaciones bajaron (Madera y papel, Metálicas básicas). Los efectos fijos de año en el modelo de panel intentan descontar lo común a toda la industria.

**34. «¿Cómo saben que sus cálculos están bien?»**
Por los controles: comercio coincide con los totales oficiales en los 10 años; empleo suma igual al subtotal oficial; el salario ponderado coincide con la serie oficial (0,99 a 1,00); y las páginas se probaron con todas las combinaciones de filtros sin errores.

**35. «¿Qué haría distinto si tuviera más tiempo?»**
(1) Clasificar importaciones por uso económico; (2) incluir tipo de cambio real; (3) bajar al nivel de producto; (4) ponderar por tamaño de rama y corregir por comparaciones múltiples; (5) extender el período a 2002.

**36. «¿Qué le diría a un político con este informe?»**
Que la evidencia no respalda una relación simple entre importaciones y pérdida de empleo industrial, pero sí señala ramas específicas (textiles, prendas/calzado, muebles) y un rol de China que merecen análisis por producto. Y que cualquier decisión de política debería usar datos por uso económico de las importaciones.

---

## 10. Guion para presentar oralmente

### 10.1 Antes de la presentación (checklist)

1. Abrir la terminal de VS Code y correr la aplicación (pasos en `README.md`). Comprobar que abre en `http://localhost:8501`.
2. Recorrer las 6 pestañas una vez para que carguen.
3. Tener este documento abierto en el segundo monitor o impreso: secciones 1.2 (cifras), 6 (guiones) y 9 (preguntas).
4. Tener a mano tres cifras: **-62.506 puestos**, **-9,4% de producción**, **2 de 24 correlaciones**.
5. Elegir de antemano **dos ramas** para el comparador (por ejemplo, Prendas/calzado y Alimentos).

### 10.2 Estructura recomendada (20 minutos)

| Minuto | Qué mostrar | Qué decir | Sección de este documento |
|---|---|---|---|
| 0-2 | Resumen (arriba) | La pregunta y por qué importa; qué se hizo | 1.1, 3 |
| 2-4 | Resumen (indicadores y hallazgos) | Las cifras clave; cinco hallazgos | 1.2, 6.1 |
| 4-6 | Método y límites (fuentes y decisiones) | Qué datos, cómo se compararon (16 ramas, promedios de 12 meses) | 4, 5 |
| 6-9 | Importaciones | De dónde vienen, China por rama, balanza | 6.2 |
| 9-12 | Empleo y ramas | Reasignación de empleo, mapa de calor, puestos | 6.3 |
| 12-16 | Importaciones vs. resultados | Correlaciones, mayor vs. menor exposición, panel | 6.4 |
| 16-18 | Comparador (2 ramas) | Contraste Prendas vs. Alimentos | 6.5 |
| 18-20 | Volver al Resumen / Método (límites) | Conclusión y qué falta | 7, 8 |

### 10.3 Versión corta (5 minutos)

1. **Pregunta** (30 s): «Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?»
2. **Datos y método** (1 min): 16 ramas, INDEC y Ministerio de Trabajo, controles.
3. **Qué pasó** (1 min): empleo -62.506 desde 2023, producción -9,4%, reasignación.
4. **La relación con importaciones** (1,5 min): 2 de 24 significativas, las dos con China; panel positivo.
5. **Cierre** (1 min): no hay relación simple; falta separar importaciones que compiten de las que complementan.

### 10.4 Versión de 10 minutos

Las secciones 1 a 5 de la tabla anterior, sin Comparador; con una rama de ejemplo.

### 10.5 Frases útiles

- Para abrir: «Antes de hablar de resultados, quiero aclarar qué se mide y qué no.»
- Para explicar el método: «Es como comparar el promedio de un año con el de otro, para no engañarnos con los meses de aguinaldo.»
- Para una correlación: «Ver que dos cosas suben juntas no prueba que una cause la otra.»
- Para un resultado inconcluso: «Con estos datos no se puede afirmar; con datos por uso económico sí se podría.»
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
- Presentar solo la correlación significativa sin decir que fueron 24 pruebas.
- Olvidar que el empleo es **registrado**.

---

## 11. Estructura del proyecto y cómo se reproduce

```
dashboard/
  Inicio.py       punto de entrada: define las páginas y la navegación
  paginas/        una página por módulo (resumen, importaciones, empleo_ramas, exposicion, comparador, metodologia)
  core/           código compartido: datos, formato, gráficos, tema y componentes de presentación
data/processed/   datos ya procesados que lee la aplicación (22 archivos CSV)
data/raw/         datos originales descargados de las fuentes (con su README)
notebooks/        los tres cuadernos que generan los datos procesados
src/              código de carga y análisis de los datos
README.md         pasos para ejecutar la aplicación
explicacion.md    este documento: informe completo para explicar el proyecto
posibles.md       ideas de partida del proyecto (12 preguntas posibles)
posibles_a_realizar.md   estado de esas ideas y lo que queda por hacer
```

### 11.1 Cómo se generaron los datos procesados

Los tres cuadernos de `notebooks/` se ejecutan en orden y escriben los archivos de `data/processed/`:

| Cuaderno | Qué hace | Archivos que produce |
|---|---|---|
| `01_limpieza_comercio_exterior` | Lee los CSV anuales de comex, **valida año por año contra los totales de control**, asigna cada producto a una rama | `importaciones_rama_pais_anio`, `exportaciones_rama_anio`, `resumen_comercio_anual`, `control_comex` |
| `02_limpieza_empleo_salarios_industria` | Extrae las series de los Excel de OEDE e INDEC con las funciones de `src/loaders.py` y las verifica contra los subtotales oficiales | `empleo_por_rama`, `empresas_por_rama`, `salario_real_por_rama`, `ipi_por_rama`, `ipi_subramas`, `capacidad_instalada` |
| `03_analisis_por_rama` | Series suavizadas, cambios por rama, comercio por rama, correlaciones, grupos y modelo de panel | `series_indexadas`, `cambios_por_rama`, `empleo_mismo_trimestre`, `comercio_por_rama_anio`, `panel_rama_anio`, `exposicion_vs_resultados`, `correlaciones`, `grupos_exposicion`, `regresiones_panel`, `ipi_subramas_*` |

Las funciones de cálculo (medias móviles, ventanas de cambio, correlaciones, panel) están en `src/analysis.py`; la clasificación de ramas y el mapeo NCM/CIIU en `src/ramas.py`; la lectura de cada formato de archivo en `src/loaders.py`; y la descarga de comercio exterior en `src/download_comex.py`.

### 11.2 Organización del código del dashboard

- **`core/datos.py`**: carga de datos con caché y nombres cortos de las ramas.
- **`core/formato.py`**: formato de números y fechas en español.
- **`core/consultas.py`**: consultas frecuentes sobre las tablas (cambio de un indicador por rama, empleo por trimestre, estimación del panel).
- **`core/graficos.py`**: constructores de gráficos (líneas, barras, mapa de calor, dispersión, etc.).
- **`core/tema.py`**: colores, estilo de los gráficos y hoja de estilos de la aplicación.
- **`core/ui.py`**: bloques de presentación (recuadro con gráfico y explicación, notas, síntesis).
- **`paginas/*.py`**: cada página tiene una función por sección y una función `mostrar()`; los textos de interpretación se calculan a partir de los datos, no se escriben a mano.

---

## 12. Fuentes

- **INDEC – Comercio exterior (comex):** bases anuales de importaciones y exportaciones por producto (NCM) y país. `comex.indec.gob.ar`
- **INDEC – Índice de producción industrial manufacturero (IPI)** y **utilización de la capacidad instalada.**
- **INDEC – Índice de precios al consumidor (IPC)**, nivel nacional.
- **Ministerio de Trabajo (OEDE) – Sistema Integrado Previsional Argentino (SIPA):** empleo asalariado privado registrado, remuneraciones y empresas, por actividad (CIIU).
- **ARCA – Tabla de códigos de país** (F2668).
