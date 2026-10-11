# 06 · Datos y fuentes

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

## Evaluación general

**Muy buena.** Es la parte más fuerte del proyecto: fuentes oficiales, bien documentadas, descargadas de manera reproducible y validadas contra totales publicados.

| Fuente | Uso | Calidad del trabajo | Observación |
|---|---|---|---|
| INDEC comex (importaciones y exportaciones por NCM y país, 2016-2025) | Exposición | ✅ Excelente: descarga automatizada, totales de control verificados | Solo años completos; 2026 mensual existe y no se usa (bien documentado como pendiente) |
| ARCA, códigos de país | Origen de las importaciones | ✅ | — |
| OEDE, empleo registrado por CIIU (trimestral) | Resultado | ✅ Suma = subtotal oficial | Solo asalariado privado registrado |
| OEDE, remuneraciones por CIIU (mensual) | Resultado | ✅ Ponderado por puestos, validado | Remuneración «por todo concepto» (incluye aguinaldo): bien tratado con promedios de 12 meses |
| OEDE, empresas activas | Resultado | ✅ | Llega solo a 2024 |
| INDEC, IPI manufacturero | Resultado | ✅ | Desde 2016: no permite mirar tendencias previas de producción |
| INDEC, capacidad instalada | Contexto | ✅ | Bloques más gruesos que las ramas (bien marcado como aproximado) |
| INDEC, IPC | Deflactor | ✅ | Desde dic-2016 |

## Puntos a mejorar

### 1. Coberturas temporales distintas
Cada fuente termina en una fecha distinta (comercio 2025, empleo 1T 2026, salarios mar-2026, producción jul-2026, empresas 2024). Para lo **descriptivo** está bien mostrar lo último de cada una
(y está señalado en cada cifra). Para el **análisis de exposición**, las ventanas tienen que coincidir: cortar todo en el último año completo común.
Con la pregunta nueva («desde 2018…») ese corte es **2018 → 2025**, y `panel_rama_anio.csv` ya tiene los promedios anuales de todas las fuentes para hacerlo (ver `05`, parte A).
**Sumar el comercio de enero-agosto de 2026 no hace falta para responder la pregunta**: solo actualizaría las páginas descriptivas.

### 2. Falta la variable que más importa: qué tipo de bien se importa
Sin la clasificación **BEC** (consumo / intermedios / capital) no se puede separar competencia de complementariedad. Es una tabla de correspondencia pública de Naciones Unidas (HS ↔ BEC).
Es el dato que más valor le agregaría al proyecto con el menor costo.

### 3. Falta el valor de la producción
Sin el valor bruto de producción por rama no se puede calcular la penetración importadora `M / (P + M − X)`. Alternativas: matriz insumo-producto del INDEC (año base) o la Encuesta Industrial.

### 4. Datos ya descargados que no se usan
La pestaña «Datos» muestra 8 conjuntos descargados sin usar: intensidad tecnológica (Lall/UNCTAD), encuesta de productos industriales, índice de salarios (registrados vs. no registrados), EMI 1994-2015.
- El **EMI** permitiría mirar tendencias de producción **antes de 2016** (placebo para producción).
- El **índice de salarios** permitiría comparar con el sector no registrado.
- La **encuesta de productos industriales** tiene producción en unidades físicas por producto: se podría comparar con importaciones del mismo producto. Es un cruce muy potente y está a mano.

### 5. Comex antes de 2016
El sistema tiene datos desde 2002. Más años = más poder en el panel y la posibilidad de estudiar el primer gran avance de China (2002-2011).

### 6. Datos de otros países (para identificación)
UN Comtrade (gratuito) tiene importaciones por producto de Brasil, Chile, México, etc. Son el insumo del instrumento estilo Autor-Dorn-Hanson (`04_revision_metodologica.md`, apartado 6).

## Buenas prácticas que ya tenés y conviene mantener

- Archivos originales **sin modificar** en `data/raw/`, procesados en `data/processed/`.
- Inventario con fuente, link, tamaño y uso de cada archivo.
- Notas sobre trampas de las fuentes (el archivo `_9` de remuneraciones con contenido de empleo; el anual 2026 de comex sin mes de corte). Ese tipo de notas salva horas a quien venga después.
