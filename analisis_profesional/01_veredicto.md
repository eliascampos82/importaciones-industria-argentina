# 01 · Veredicto

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

**Pregunta central (desde el 11 de octubre de 2026):**

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**

## La respuesta que dan tus datos

**No.** Entre 2018 y 2025 (último año completo en todas las fuentes) la industria produjo 5,6% menos y pagó salarios reales 7,5% más bajos, y las 16 ramas perdieron salario real.
Pero las pérdidas **no se concentraron** donde más crecieron las importaciones. En general fue al revés:

| Ramas (8 y 8, cortadas en la mediana) | Empleo 2018 → 2025 | Producción (mediana) | Salario real (mediana) |
|---|---|---|---|
| Donde las importaciones **crecieron más** | **+27.000 puestos (+3,3%)** | −7,4% | −10,0% |
| Donde las importaciones **crecieron menos** | **−18.000 puestos (−4,6%)** | −16,2% | −11,5% |

Con **una excepción visible: Prendas, cuero y calzado** (importaciones +36% en dólares y +61% en toneladas, −13.900 puestos, −19%). **Textiles** se le parece cuando se mira en toneladas (+45%), aunque en dólares apenas creció (+5%).
Son las dos ramas de **bienes de consumo** donde se cumple la historia del debate público.

**Qué tan firme es esa respuesta:** es una descripción correcta, no un efecto.
- Ninguna de las 9 correlaciones de la pregunta sobrevive a la corrección por comparaciones múltiples.
- El signo positivo depende de Alimentos.
- La **tendencia previa** de cada rama (2011-2017) explica el empleo mejor que las importaciones.

El detalle está en [05_pruebas_de_robustez.md](05_pruebas_de_robustez.md), parte A.

## Lo alentador

Si este proyecto llegara a mi escritorio como parte de una búsqueda de analista de datos, **pasaría la primera ronda sin dudas**:

- **Validaste tus datos contra los totales oficiales**: comercio exterior idéntico a los totales de control del INDEC en los 10 años, suma de ramas igual al subtotal oficial de empleo,
  salario ponderado entre 0,99 y 1,00 de la serie oficial.
- **Resolviste un problema de datos real y feo**: tres clasificaciones (NCM, CIIU, IPI) llevadas a 16 ramas, con criterios escritos, y descarga automatizada de un sitio sin botón de descarga.
- **Pensaste en la estacionalidad y el aguinaldo** (promedios de 12 meses, mismo trimestre contra mismo trimestre).
- **Fuiste honesto con los resultados** y escribiste qué no se puede afirmar.
- **Corregiste la pregunta para que coincida con lo que el diseño puede responder.** Es la decisión metodológica más importante que tomaste en todo el proyecto:
  pasar de una pregunta que sonaba causal («¿evolucionaron peor?») a una de **coincidencia** («¿perdió justo donde…?») hace que el análisis, por primera vez, **responda** su pregunta.

## Lo desgarrador

- **La pregunta cambió, pero las conclusiones todavía responden la anterior.** El informe (sección 4), la página Importaciones vs. resultados y el quinto hallazgo del Resumen siguen
  encabezados por «la señal más consistente está en China». Para la pregunta nueva, China es un resultado secundario; la respuesta principal es la tabla de arriba, y **hoy no aparece en ningún lado del dashboard
  con la ventana común 2018-2025**.
- **El resultado de China sigue siendo una sola correlación.** De las 24 originales sobrevive 1 a la corrección (participación de China en 2025 contra producción desde 2018), y mide la *composición* de la industria
  más que un *shock* de importaciones.
- **«Desde 2018» y el empleo.** Con promedios anuales el empleo de 2025 es **+0,7%** respecto de 2018; con el 1T 2026 contra el 1T 2018 es **−3,6%**. La pérdida de empleo es de **2024 en adelante** (desde el máximo de 2023).
  La pregunta se sostiene, pero la respuesta tiene que decirlo: la producción y el salario caen desde 2018; el empleo, desde 2023.
- **El modelo de panel mide la demanda, no la competencia.** Todos los coeficientes son positivos porque cuando una rama crece importa más insumos y máquinas. No responde la pregunta y conviene
  bajarlo a «análisis complementario».
- **Las importaciones totales mezclan lo que compite con lo que abastece.** Por eso la excepción (prendas y textiles, bienes de consumo) queda tapada por el promedio. Separar por uso económico (BEC) es lo que
  haría la respuesta realmente informativa.

## Nota por dimensión

| Dimensión | Nota | Antes | Comentario |
|---|---|---|---|
| Pregunta y relevancia | **9** | 8 | Clara, relevante y, ahora, **respondible con los datos** |
| Obtención y limpieza de datos | **9** | 9 | Lo mejor del proyecto |
| Análisis descriptivo | **8** | 8 | Correcto y cuidadoso. Falta la comparación con la ventana común 2018-2025, que es la que responde la pregunta |
| Método para responder la pregunta | **6** | 5 | La pregunta ya no exige causalidad; falta elegir una medida principal y mostrarla primero |
| Inferencia estadística | **4,5** | 4,5 | Sin corrección por comparaciones múltiples en el dashboard; panel con 16 grupos |
| Honestidad y límites | **9** | 9 | Excepcional |
| Comunicación (dashboard y documentos) | **7,5** | 8 | Baja medio punto: la pregunta nueva y las conclusiones viejas conviven, y eso un evaluador lo nota |
| Código y reproducibilidad | **5,5** | 5,5 | Sin git, sin pruebas, sin versiones fijadas |
| **Global** | **7** | 7 | **Sube a 8 cerrando la lista de [README_para_terminar.md](README_para_terminar.md)**: casi todo es reescribir conclusiones y ordenar, no análisis nuevo |

## La frase para llevarse

> Ya hiciste la parte difícil: datos limpios, validados y una pregunta que tus datos pueden responder. Lo que falta es **contar la respuesta a esa pregunta** (y no a la anterior) en el mismo orden en que la pregunta la pide:
> primero qué se perdió, después dónde, después si coincide con las importaciones, y recién al final China.
