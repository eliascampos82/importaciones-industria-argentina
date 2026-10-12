# Importaciones e industria en Argentina

**Ver el dashboard en línea:** https://importaciones-industria-argentina.streamlit.app/

> **Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?**

**Respuesta: no.** Entre 2018 y 2025 la industria produjo 5,6% menos y pagó salarios reales 7,5% más bajos. Pero las pérdidas no se concentraron donde más crecieron las importaciones, y en general fue al revés:
- **Donde más crecieron:** las 8 ramas sumaron 27.000 puestos.
- **Donde menos crecieron:** las otras 8 perdieron 18.000.

**Por qué al revés:** las ramas que crecen importan más insumos y máquinas. Con los bienes de consumo, que son los que compiten con lo que se produce acá, no hay relación con el empleo.

**La excepción** son prendas y textiles: entraron muchas más toneladas y se perdió empleo.

Es una coincidencia medida en 16 ramas, no un efecto causal.

El informe completo, de 8 páginas, está en [conclusiones.pdf](conclusiones.pdf).

## Cómo ejecutar

Lo más simple: hacer doble clic en `run.bat` (usa el entorno del proyecto e instala lo que falte).

O desde la terminal de VS Code (`Terminal` → `New Terminal`):

1. Instalar las dependencias (solo la primera vez, tarda 1-2 minutos):
   ```
   python -m pip install -r requirements.txt
   ```
2. Iniciar la aplicación:
   ```
   python -m streamlit run dashboard/Inicio.py
   ```
3. Abrir en el navegador (se abre solo; si no, pegar esta dirección):
   ```
   http://localhost:8501
   ```

Para cerrar la aplicación: `Ctrl+C` en la terminal.
Si aparece un error del tipo `unexpected keyword argument`, casi seguro se está usando otro Python con un Streamlit más viejo: abrir con `run.bat`.

## Qué muestra la aplicación

Cruza comercio exterior con empleo, salarios y producción de la industria argentina (16 ramas industriales, 2016-2026). Cada gráfico trae su explicación.

| Página | Qué responde |
|---|---|
| **Presentación** | La pregunta, los datos y la respuesta, en formato de diapositivas |
| **Resumen** | Los indicadores clave y los cinco hallazgos principales |
| **Importaciones** | De dónde vienen, qué ramas las reciben, cuánto avanzó China y qué tipo de bienes se importan (consumo, insumos y capital) |
| **Empleo y ramas** | Puestos ganados y perdidos por rama, salario real, producción y empresas; año por año |
| **Importaciones vs. resultados** | **La respuesta a la pregunta**, si cambia al medir distinto y los análisis complementarios |
| **Comparador de ramas** | Una rama de punta a punta contra el total de la industria |
| **Conclusiones** | El trabajo completo como informe de 8 hojas A4 (`Ctrl+P` → «Guardar como PDF») |
| **Método y límites** | Fuentes, decisiones de método, controles de calidad y qué no se puede concluir |
| **Datos** | Cada archivo original: de dónde sale, para qué se usó y dónde se descarga |

## Hasta dónde llega cada dato

| Dato | Último dato |
|---|---|
| Empleo registrado (OEDE) | 1T 2026 (el Ministerio corrige los últimos trimestres al actualizar) |
| Producción industrial (IPI) | jul-2026 |
| Capacidad instalada | jun-2026 |
| Salario real | mar-2026 |
| IPC | ago-2026 |
| Empresas activas | 2024 (serie anual) |
| Comercio exterior | dic-2025 (años completos) |

La respuesta a la pregunta usa **2018 → 2025**, el último año completo en todas las fuentes.

## Cómo regenerar los datos

Los datos procesados ya están incluidos (`data/processed/`), así que la aplicación funciona sin este paso. Para regenerarlos desde los archivos originales:

```
python -m pip install -r requirements.txt
python src/download_comex.py
```

El segundo comando descarga del INDEC las bases de comercio exterior 2016-2025 (unos 120 MB, no se incluyen en el repositorio). Después se ejecutan los tres
cuadernos de `notebooks/` en orden (01, 02 y 03). Las pruebas de todo el proyecto (datos y pestañas) se corren con `python -m pytest`.

## Fuentes

INDEC (comercio exterior, producción industrial, capacidad instalada, IPC), Ministerio de Trabajo - OEDE (empleo, remuneraciones y empresas registradas),
ARCA (códigos de país) y Banco Mundial - WITS (correspondencia de productos con uso económico, clasificación BEC de Naciones Unidas).

## Carpetas

```
dashboard/              la aplicación: Inicio.py (navegación), paginas/ (una por pestaña) y core/ (datos, gráficos, tarjetas, estilo)
src/                    carga de los archivos originales, clasificación en ramas y por uso económico, cálculos y descarga del comercio exterior
notebooks/              cuadernos que generan los datos procesados (01 comercio, 02 empleo/salarios/producción, 03 análisis)
data/raw/               datos originales de las fuentes (con su propio README)
data/processed/         datos procesados que lee la aplicación
tests/                  pruebas automáticas (datos y pestañas)
```

## Autor

Francisco Elias Campos  
Estudiante de la Tecnicatura: Técnico Superior en Ciencia de Datos e Inteligencia Artificial  
