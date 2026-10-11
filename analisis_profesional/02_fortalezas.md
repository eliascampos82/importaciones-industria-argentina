# 02 · Fortalezas

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

Lo que está bien hecho y conviene convertir en hábito en todos los trabajos.

---

## 1. Validación de los datos contra totales oficiales

**Qué hiciste.** Comparaste la cantidad de registros y los valores totales de importaciones y exportaciones de cada año con los «totales de control» que publica INDEC
(coinciden exactamente en los 10 años); verificaste que la suma de las 16 ramas de empleo es igual al subtotal oficial «Industria» en todos los trimestres; y que el salario
ponderado queda entre 0,99 y 1,00 de la serie oficial de «Industrias manufactureras».

**Por qué importa.** Es la diferencia entre «creo que los datos están bien» y «sé que están bien». En un equipo profesional, un análisis sin esta verificación no sale.

**Hábito para repetir.** Antes de analizar, buscar siempre un número oficial contra el cual chequear (un total, un subtotal, un dato publicado en un informe) y dejar la
comparación guardada (como hiciste en `control_comex.csv`).

## 2. Obtención de datos difíciles

- Descubriste el patrón de URL de las bases de comercio exterior **leyendo el código del sitio** del INDEC, que no tiene botón de descarga, y lo automatizaste en un script
  (`src/download_comex.py`) que además **verifica que la respuesta sea un zip** (el sitio devuelve HTML con código 200 cuando el archivo no existe). Eso es pensar como ingeniero de datos.
- El script es **idempotente** (no vuelve a descargar lo que ya está). Detalle profesional.

## 3. Integración de tres clasificaciones distintas

Comercio exterior (productos, NCM), empleo y salarios (actividades, CIIU) y producción (divisiones del IPI) no hablan el mismo idioma. Elegiste el nivel común más grueso (16 ramas),
escribiste las reglas en un solo lugar (`src/ramas.py`) y tomaste decisiones razonables y **documentadas**: excluir crudo, gas, oro y piedras sin trabajar porque no son manufactura;
mover computadoras, motos e iluminación a su rama correcta a 4 dígitos.

## 4. Cuidado con la estacionalidad y la comparabilidad

- Promedios de 12 meses para el IPI (diciembre y enero son bajos) y para el salario (el aguinaldo infla junio y diciembre).
- Empleo comparado **mismo trimestre contra mismo trimestre**.
- Salario de cada rama **ponderado por puestos** de cada CIIU, no un promedio simple.
- Importaciones en **valor y en toneladas**, para separar «se importa más» de «se importa lo mismo más caro».

Son errores típicos que evitaste sin que nadie te los marque.

## 5. Dos años base y varias medidas de exposición

Comparar contra 2018 y contra 2023, y medir la exposición de cuatro maneras, es una forma básica pero correcta de **no depender de una sola elección arbitraria**.
(La falencia es cómo se interpretan los resultados después; ver `03_falencias.md`).

## 6. Honestidad intelectual

- Cuando los datos no confirmaron la hipótesis, lo dijiste: «no aparece una relación simple y consistente de "más importaciones, menos empleo"».
- Separaste «lo que sí se puede afirmar» de «lo que NO se puede afirmar», incluido «que las importaciones **no** afectaron» (ausencia de evidencia no es evidencia de ausencia).
- Tabla de 14 limitaciones con por qué importan, cómo se mitigan y qué haría falta.
- Marcaste vos mismo que el panel depende de una sola rama (refinación).

Esta es la fortaleza más valiosa del proyecto y la más difícil de enseñar.

## 7. Elección de herramientas estadísticas razonables

- **Spearman** en lugar de Pearson con 16 observaciones muy dispares: correcto.
- **Efectos fijos de rama y de año** en el panel: la especificación base que usaría cualquiera.
- **Errores agrupados por rama**: la intuición es correcta (aunque con 16 grupos no alcanza; ver falencias).
- **Rezagos de un año** como prueba adicional.

## 8. Comunicación pensada para la audiencia

- Un dashboard con 9 pestañas, explicaciones al lado de cada gráfico, una síntesis por página, glosario, página de método y una de datos con links de descarga.
- Textos **calculados a partir de los datos** (si una cifra cambia de signo, cambia la frase): eso evita el error más común de los dashboards, que el texto quede desactualizado.
- Cada cifra dice **hasta qué mes o trimestre llega**.
- Un documento para exponer oralmente con banco de preguntas, repreguntas y puntos de vista opuestos. Muy pocos portfolios tienen esto.

## 9. Código legible y documentado

- Funciones chicas con docstrings que explican **por qué** (no solo qué): «la remuneración incluye el aguinaldo, así que un mes suelto no es comparable».
- Separación clara: carga (`loaders.py`), clasificación (`ramas.py`), cálculos (`analysis.py`), presentación (`dashboard/core` y `dashboard/paginas`).

## 10. Saber cambiar la pregunta

El 11-10-2026 reemplazaste una pregunta que sonaba causal por una de coincidencia («¿perdió justo donde más crecieron las importaciones?») y sacaste a China de la pregunta,
porque la evidencia no da para ponerla en el centro. Ajustar la pregunta a lo que el diseño puede responder, en lugar de forzar el diseño, es lo que hace un analista con criterio.
**Hábito para repetir:** escribir la pregunta, revisar si los datos pueden responderla tal como está escrita y corregir la redacción antes de presentar.

## 11. Inventario de datos

La pestaña «Datos» con cada archivo, su fuente, para qué se usó, su tamaño y su link es una práctica de **gobierno de datos** que en empresas se valora mucho
y casi nadie hace en proyectos personales.
