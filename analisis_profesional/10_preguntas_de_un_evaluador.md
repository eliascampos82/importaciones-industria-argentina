# 10 · Preguntas de un evaluador

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

Las preguntas que te haría un entrevistador técnico o un revisor al ver este proyecto, de la más probable a la más difícil.
Para cada una: **la respuesta que hoy podrías dar** y **la que podrías dar después del plan de mejora** (`09`).

---

### 1. «¿Cuál es la conclusión principal en una oración?»
- **Hoy (con la pregunta nueva):** «No: desde 2018 la industria produce menos y paga salarios más bajos, pero esas pérdidas no se concentraron donde más crecieron las importaciones; en general fue al revés.
  La excepción son prendas y textiles, donde entraron muchas más toneladas y se perdió empleo.»
- **Cuidado:** no digas «las importaciones no afectaron» (ausencia de evidencia ≠ evidencia de ausencia), ni «importar crea empleo», ni «China causó la caída».

### 1b. «¿Por qué cambiaste la pregunta? ¿No es acomodarla al resultado?»
- **Respuesta:** «La cambié para que coincida con lo que el diseño puede responder, no con el resultado: la original sonaba causal ("¿evolucionaron peor?") y con 16 ramas y sin una fuente de variación
  externa solo puedo medir coincidencias. La respuesta a la pregunta nueva es "no", que es la menos llamativa: no la elegí para que diera algo.»

### 1c. «Si donde más se importó se ganó empleo, ¿importar crea empleo?»
- **Respuesta:** «No se puede decir. Gran parte de lo que se importa son insumos y máquinas: cuando una rama crece, importa más. El signo positivo es lo que se espera de ese efecto demanda.
  Además depende de Alimentos: sin esa rama, la relación ponderada desaparece (p = 0,47).»

### 1d. «Tu pregunta dice "desde 2018". ¿La industria perdió empleo desde 2018?»
- **Respuesta:** «Producción (−5,6%) y salario real (−7,5%) sí, entre 2018 y 2025. El empleo anual de 2025 estaba igual que en 2018 (+0,7%); cae desde el máximo de 2023, y en el 1T 2026 está 3,6% abajo del 1T 2018.»

### 2. «¿Cómo sabés que tus datos están bien?»
- **Hoy (excelente respuesta):** totales de comex iguales a los de control de INDEC en los 10 años; suma de ramas = subtotal oficial de empleo; salario ponderado 0,99-1,00 de la serie oficial.

### 3. «¿Por qué el coeficiente del panel es positivo? ¿Importar crea empleo?»
- **Hoy:** «No. Cuando una rama crece compra más insumos y máquinas importadas: importaciones y producción se mueven juntas por la demanda. El modelo no separa ese efecto del de la competencia.»
- **Después:** «Separé las importaciones por uso (BEC). Las de bienes de consumo que compiten tienen coeficiente [X]; las de insumos y capital, positivo.»

### 4. «Probaste 24 correlaciones. ¿Cuántas esperabas que salieran significativas por azar?»
- **Hoy:** «Alrededor de una. Salieron tres y, corrigiendo por comparaciones múltiples, sobrevive una.» (Si no lo sabés responder rápido, es la pregunta que más daño hace).

### 5. «¿Por qué medís la exposición con el crecimiento porcentual y no por trabajador?»
- **Hoy:** reconocer que la medida estándar es ΔM/L y mostrar que con ella el resultado es parecido (ver `05`).

### 6. «Con 16 ramas, ¿qué tan grande tiene que ser una correlación para ser significativa?»
- **Respuesta:** |ρ| de alrededor de 0,5. Por eso «no significativo» no quiere decir «no hay efecto»: efectos moderados no se pueden detectar con esta muestra.

### 7. «¿Por qué sacaste refinación de petróleo? ¿No es elegir la muestra que te conviene?»
- **Respuesta honesta:** «Sus importaciones son energía y se mueven por precios internacionales (saltaron a USD 7.000 millones en 2022 por la crisis energética), no por competencia. Muestro ambas muestras.
  Reconozco que con 15 grupos los errores agrupados subestiman la incertidumbre; con wild bootstrap el resultado [es/no es] significativo.»

### 8. «¿Cómo separarías importaciones que compiten de las que complementan?»
- **Respuesta:** clasificación BEC de Naciones Unidas (consumo / intermedios / capital) + correspondencia HS → ISIC.

### 9. «¿Cómo harías para estimar un efecto causal?»
- **Respuesta:** instrumento estilo Autor-Dorn-Hanson (importaciones desde China de otros países latinoamericanos) o diferencias en diferencias con el levantamiento de restricciones en 2024.
  Explicar el supuesto de cada uno: que el instrumento solo afecta a la industria argentina a través de las importaciones argentinas; que sin la apertura las ramas habrían seguido tendencias paralelas.

### 10. «¿Las ramas que caen no venían cayendo de antes?»
- **Con la pregunta nueva:** «Sí, y pesa más que las importaciones: controlando el empleo 2011-2017, la tendencia previa es significativa (p = 0,013) y el crecimiento de las importaciones no (p = 0,27).»
- **Respuesta (con `05`):** «En parte sí: la caída de empleo es muy persistente (ρ = 0,75 con 2011-2017). Pero la exposición a las importaciones no está correlacionada con esa tendencia previa, así que no es
  solo eso. Igual habría que controlarla en el modelo.»

### 11. «¿Por qué el valor en dólares y no en cantidades?»
- **Respuesta:** «Uso las dos. En textiles se ve por qué importa: desde 2018 las toneladas importadas subieron 45% y el valor solo 5%; se importa más volumen más barato.»

### 12. «¿Qué no hiciste que te hubiera gustado hacer?»
- **Buena respuesta:** nombrar 2 o 3 cosas concretas del plan de mejora con el porqué de cada una. Mostrar que sabés **dónde** está el límite de tu propio trabajo es lo que más valora un evaluador.

### 13. «¿Cuánto tiempo te llevó y qué fue lo más difícil?»
- **Respuesta sugerida:** la integración de las tres clasificaciones y la validación contra totales. Es lo que distingue el proyecto y lo que muestra criterio.

### 14. «Si un ministro te pregunta "¿hay que cerrar la importación textil?", ¿qué le decís?»
- **Respuesta profesional:** «Mis datos muestran que textiles cayó mucho y que las importaciones textiles crecieron en volumen, pero no permiten afirmar cuánto de la caída se debe a las importaciones y cuánto
  a la demanda interna o a tendencias previas. Antes de recomendar una política haría [instrumento / diferencias en diferencias]. Además una política tiene costos para quienes usan esos insumos y para los consumidores.»
  (Saber decir «mis datos no alcanzan para eso» es una señal de madurez profesional).
