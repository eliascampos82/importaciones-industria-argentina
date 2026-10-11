# 11 · Para seguir aprendiendo

> **Nota (11-10-2026, al cierre):** este archivo describe el proyecto **antes** de las mejoras de cierre. Casi todo lo que marca como pendiente ya se hizo (uso económico, ventana común, corrección por comparaciones múltiples, conclusiones en el orden de la pregunta, pruebas, pipeline y versiones). El estado final está en [00_evaluacion_final.md](00_evaluacion_final.md).

Lecturas y técnicas elegidas para cerrar las brechas concretas de este proyecto. Ordenadas por prioridad.

---

## 1. El tema: comercio internacional y empleo

| Lectura | Qué te aporta |
|---|---|
| Autor, Dorn y Hanson (2013), «The China Syndrome: Local Labor Market Effects of Import Competition in the United States», *American Economic Review* | **La** referencia. Exposición por trabajador e instrumento con importaciones de otros países. Leer la introducción y la sección de estrategia empírica |
| Autor, Dorn y Hanson (2016), «The China Shock: Learning from Labor-Market Adjustment to Large Changes in Trade», *Annual Review of Economics* | Resumen accesible de toda la literatura |
| Acemoglu, Autor, Dorn, Hanson y Price (2016), «Import Competition and the Great US Employment Sag of the 2000s», *Journal of Labor Economics* | Análisis **por industria** (como el tuyo) y efectos de encadenamiento entre ramas |
| Pierce y Schott (2016), «The Surprisingly Swift Decline of US Manufacturing Employment», *American Economic Review* | Un cambio de política comercial usado como diferencias en diferencias: el modelo para la idea de la apertura de 2024 |

## 2. Inferencia causal (lo que más te falta)

| Recurso | Para qué |
|---|---|
| Nick Huntington-Klein, *The Effect* (libro gratuito online) | Variables instrumentales, diferencias en diferencias y efectos fijos, explicados con intuición. **Empezá por acá** |
| Scott Cunningham, *Causal Inference: The Mixtape* (gratuito online) | Lo mismo con más ejemplos y código |
| Angrist y Pischke, *Mostly Harmless Econometrics* | La referencia clásica, más técnica |

## 3. Inferencia estadística con muestras chicas

| Tema | Recurso |
|---|---|
| Comparaciones múltiples | Benjamini y Hochberg (1995), «Controlling the False Discovery Rate»; `statsmodels.stats.multitest` |
| Errores agrupados con pocos grupos | Cameron, Gelbach y Miller (2008), «Bootstrap-Based Improvements for Inference with Clustered Errors»; paquete `wildboottest` |
| Búsqueda de especificaciones | Simonsohn, Simmons y Nelson (2020), «Specification Curve Analysis», *Nature Human Behaviour* |
| Poder estadístico | Calcular antes qué efecto mínimo podés detectar con tu n (con 16 ramas, |ρ| ≈ 0,5) |

## 4. Datos y clasificaciones

| Recurso | Para qué |
|---|---|
| Naciones Unidas, clasificación BEC y tablas de correspondencia HS ↔ BEC ↔ ISIC | Separar consumo / intermedios / capital y mapear productos a actividades |
| WITS (Banco Mundial) y UN Comtrade | Comercio por producto de otros países (para el instrumento) |
| Matriz insumo-producto del INDEC | Valor de la producción por rama y encadenamientos |

## 5. Ingeniería del análisis

| Tema | Recurso |
|---|---|
| Git | «Pro Git» (libro gratuito, capítulos 1-3) |
| Pruebas | `pytest` (documentación oficial, «Get Started»); `streamlit.testing.v1.AppTest` para el dashboard |
| Pipelines reproducibles | Un `Makefile` o un script `pipeline.py`; más adelante, herramientas como DVC |
| Estimación en Python | `linearmodels` (paneles y variables instrumentales con buenas opciones de errores estándar) |

---

## Hábitos para el próximo proyecto

1. **Escribir la pregunta y si es descriptiva o causal antes de tocar los datos.**
2. **Decidir la especificación principal antes de ver resultados**; el resto es robustez.
3. **Calcular el poder estadístico** antes de prometer una respuesta.
4. **Buscar cómo lo midió la literatura** antes de inventar una medida propia.
5. **Proporcionalidad**: el tamaño de la letra de un resultado tiene que ser proporcional a su solidez.
6. **Git desde el primer día.**
7. **Repartir el tiempo**: datos 40%, método 35%, comunicación 25%. En este proyecto la comunicación se llevó más de lo que le tocaba.
