"""Página «Método y límites»: fuentes, decisiones de método, controles de calidad, límites del análisis y glosario."""
import pandas as pd
import streamlit as st

from core.datos import leer
from core.ui import nota


def _introduccion():
    st.markdown(
        """
Esta página documenta **cómo se construyó el análisis**: de dónde salen los datos, qué decisiones se tomaron para que sean comparables, qué controles se hicieron
para verificar que están bien y, sobre todo, qué **no** se puede concluir con ellos. Está pensada para que cualquier resultado de las otras páginas pueda auditarse.
"""
    )


def _fuentes():
    st.subheader("1. Fuentes de datos")
    st.table(
        pd.DataFrame([
            ("Importaciones y exportaciones por producto (NCM) y país", "INDEC, sistema de consulta de comercio exterior", "2016-2025, anual",
             "Qué ramas importan, de dónde y cuánto (valor y toneladas)"),
            ("Códigos de país", "ARCA (tabla oficial de países)", "vigente", "Identificar el origen de cada operación"),
            ("Empleo asalariado privado registrado, por CIIU", "Ministerio de Trabajo, OEDE (SIPA)", "1996-1T 2026, trimestral", "Puestos de trabajo por rama"),
            ("Remuneraciones por CIIU", "Ministerio de Trabajo, OEDE (SIPA)", "1995-mar 2026, mensual", "Salario de cada rama (con el IPC, salario real)"),
            ("Empresas privadas activas, por CIIU", "Ministerio de Trabajo, OEDE", "1996-2024, anual", "Cierres netos de empresas"),
            ("Producción industrial (IPI manufacturero)", "INDEC", "2016-jul 2026, mensual", "Producción física por rama y por subsector"),
            ("Utilización de la capacidad instalada", "INDEC", "2016-2026, mensual", "Planta ociosa por bloque de la industria"),
            ("Índice de precios al consumidor (IPC nacional)", "INDEC", "dic 2016-ago 2026, mensual", "Deflactar salarios"),
            ("Correspondencia de productos (HS) con uso económico (BEC rev. 4)", "Banco Mundial, WITS (tablas HS 2012, 2017 y 2022)", "vigente",
             "Separar lo importado en bienes de consumo, insumos y bienes de capital"),
        ], columns=["Dato", "Fuente", "Cobertura", "Para qué se usa"]).set_index("Dato")
    )
    st.caption("Todos los datos son públicos y oficiales. Los archivos originales están en la carpeta de datos del proyecto y los ya procesados, en la de datos procesados.")


def _decisiones():
    st.subheader("2. Decisiones de método")
    st.markdown(
        """
**La pregunta y cómo se responde.** «Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?» es una pregunta
de **coincidencia**, no de causa. Se responde comparando las 16 ramas entre **2018 y 2025**, el último año completo en todas las fuentes, con promedios anuales: así importaciones y resultados
miden el mismo período. La **medida principal** se eligió por la pregunta, antes de mirar los resultados: crecimiento de las importaciones en dólares de cada rama. Las demás (toneladas, dólares por
puesto, uso económico, China, base 2023, modelo de panel) se muestran como pruebas de robustez o complementos.

**Importaciones por uso económico.** Cada producto importado se clasifica con la clasificación BEC de Naciones Unidas (tablas de correspondencia del Banco Mundial, según la versión del HS
de cada año) en **bienes de consumo** (alimentos para hogares, bienes durables y no durables, autos de pasajeros), **insumos** (materias primas, partes, combustibles) y **bienes de capital**
(máquinas y equipo). Los bienes de consumo son los que compiten por el mismo comprador final; los insumos y el capital crecen cuando la industria crece. Se clasifica 99,9% del valor importado y la suma por rama
coincide con el total.

**Corrección por comparaciones múltiples.** Cuando se prueban muchas correlaciones, algunas dan «significativas» por azar. Cada p-valor se muestra con su versión corregida por el método de
Benjamini-Hochberg: solo lo que resiste la corrección se considera un resultado.

**Una clasificación común de 16 ramas.** Comercio exterior usa productos (NCM), empleo y salarios usan actividades (CIIU) y la producción usa las divisiones del IPI. Todo se lleva a
las 16 agrupaciones del IPI. No existe una tabla oficial uno a uno entre NCM y CIIU: el paso de producto a rama se hace a nivel de capítulo (2 dígitos), con algunas excepciones a 4 dígitos
(computadoras, motos, iluminación). El petróleo crudo, el gas, el oro y las piedras sin trabajar se excluyen porque son productos primarios, no manufactura. Es una aproximación: un mismo
producto puede servir a más de una actividad.

**«Total industria» es solo manufactura** (CIIU 15 a 37), no toda la economía. Los totales del Resumen sobre comercio exterior, en cambio, incluyen todos los bienes.

**Promedios de 12 meses, nunca meses sueltos.** El IPI tiene estacionalidad fuerte (diciembre y enero son bajos) y la remuneración «por todo concepto» incluye el aguinaldo (junio y
diciembre): comparar dos meses distintos produce diferencias que no existen. Por eso se compara el promedio de un año base contra el promedio de los últimos 12 meses (4 trimestres en empleo).

**Salario real por rama** = remuneración nominal dividida por el IPC, promediando los CIIU de la rama **ponderados por sus puestos de trabajo**. El IPC nacional continuo empieza en dic-2016,
así que no hay salario real antes de 2017.

**Importaciones en valor CIF y en toneladas.** 2016-2018 solo publican CIF; las toneladas no dependen de los precios y permiten distinguir «se importa más» de «se importa lo mismo más barato».
Los valores son nominales, en dólares corrientes.

**Correlación de Spearman** (sobre rangos) entre ramas: con 16 observaciones y valores muy dispares, la de Pearson la domina un solo punto. Se reporta junto con su p-valor, su p corregido y,
en la respuesta, un intervalo de confianza por bootstrap (remuestreando ramas).

**Modelo de panel (complemento)**: `log(resultado) ~ log(1 + importaciones) + efecto fijo de rama + efecto fijo de año`, con errores agrupados por rama. Los efectos fijos de rama absorben las diferencias
permanentes entre ramas y los de año, lo que le pasa a toda la industria a la vez (devaluaciones, recesión). Lo que queda es la relación entre el movimiento de las importaciones de una rama
y el de su empleo, producción o salario respecto de las demás ramas ese año.
"""
    )


def _controles():
    control = leer("control_comex.csv")
    st.subheader("3. Controles de calidad")
    st.markdown(
        """
- **Comercio exterior:** en los 10 años, la cantidad de registros y el valor total de importaciones y exportaciones **coinciden exactamente** con los totales de control que publica INDEC.
- **Empleo:** la suma de las 16 ramas es **igual** al subtotal oficial «Industria» de OEDE en todos los trimestres.
- **Salarios:** el salario nominal ponderado por puestos queda entre 0,99 y 1,00 de la serie oficial de «Industrias manufactureras».
"""
    )
    with st.expander("Ver la tabla de controles de comercio exterior"):
        t = control.assign(cif_total_mm=(control.cif_total / 1e6).round(0), fob_total_mm=(control.fob_total / 1e6).round(0))
        t = t[["anio", "registros_imp", "cif_total_mm", "coincide_imp", "registros_exp", "fob_total_mm", "coincide_exp"]]
        t.columns = ["Año", "Registros import.", "CIF total (USD M)", "Coincide", "Registros export.", "FOB total (USD M)", "Coincide "]
        st.dataframe(t, width="stretch", hide_index=True)


def _limites():
    st.subheader("4. Qué no se puede concluir")
    limites = [
        ("Causalidad.", "Todo lo que se muestra son coincidencias. En 2018-2025 hubo devaluaciones, recesión, pandemia, cambios de política comercial y cambios en precios internacionales al mismo tiempo. "
                        "Que las pérdidas no coincidan con las importaciones no prueba que las importaciones no afectaron a ninguna rama."),
        ("El uso económico es aproximado.", "Cada producto se clasifica por su uso más habitual y se asigna a la rama que lo fabrica según su capítulo del nomenclador. Un insumo importado también puede competir con quien lo "
                                            "produce en el país (el acero importado compite con las acerías locales), y algunos bienes sirven a la vez para consumo y para producir."),
        ("Pocas ramas.", "Son 16 observaciones: solo correlaciones grandes (|ρ| de 0,5 o más) se distinguen del azar. Por eso se corrigen los p-valores y «no significativo» no quiere decir «no hay relación». "
                         "En el panel, con 16 grupos, los errores estándar agrupados son poco confiables."),
        ("Tendencias previas.", "Las ramas que perdían empleo entre 2011 y 2017 son, en gran parte, las que lo pierden desde 2018: buena parte de lo que se ve es estructural y anterior al período."),
        ("Empleo registrado.", "Solo cuenta trabajo asalariado privado registrado: no incluye informalidad, cuentapropistas ni sector público."),
        ("Exportaciones confidenciales.", "Desde 2018 INDEC oculta cerca de 5% de las exportaciones por secreto estadístico; no se pueden asignar a una rama."),
        ("Falta el valor de la producción por rama.", "Sin él no se puede calcular la exposición importadora clásica (importaciones sobre consumo aparente); por eso se usan sustitutos: crecimiento de las importaciones y participación de China."),
    ]
    for titulo, texto in limites:
        nota(texto, titulo=titulo)


def _glosario():
    st.subheader("5. Glosario")
    st.table(
        pd.DataFrame([
            ("CIF", "Valor de una importación que incluye el costo, el flete y el seguro hasta llegar al país."),
            ("FOB", "Valor de una mercadería puesta a bordo en origen, sin flete ni seguro. Se usa para las exportaciones."),
            ("NCM", "Nomenclatura Común del Mercosur: clasificación de productos del comercio exterior."),
            ("CIIU", "Clasificación de actividades económicas que usan el empleo, las remuneraciones y las empresas."),
            ("IPI manufacturero", "Índice de volumen físico de la producción industrial que publica INDEC. Base 2004 = 100."),
            ("OEDE / SIPA", "Observatorio de Empleo del Ministerio de Trabajo, que trabaja con el Sistema Integrado Previsional Argentino (trabajo registrado)."),
            ("Salario real", "Salario nominal deflactado por el IPC: mide poder de compra, no pesos corrientes."),
            ("Índice base 100", "Una serie dividida por su valor de referencia (un año o un promedio) y multiplicada por 100. Permite comparar trayectorias de series en distintas unidades."),
            ("Promedio móvil de 12 meses", "Cada punto es el promedio de ese mes y los 11 anteriores; elimina estacionalidad y aguinaldo."),
            ("p.p. (punto porcentual)", "Diferencia entre dos porcentajes: pasar de 18% a 23% es un aumento de 5 p.p., no de 5%."),
            ("Correlación de Spearman (ρ)", "Medida de asociación entre dos variables de -1 a +1, calculada sobre los rangos."),
            ("p-valor", "Probabilidad de observar una asociación al menos así de fuerte si en realidad no hubiera ninguna. Debajo de 0,05 se la considera significativa."),
            ("Efectos fijos", "Variables que absorben diferencias permanentes entre ramas o lo que le pasa a toda la industria en un año, para aislar lo que cambia dentro de cada rama."),
            ("Intervalo de confianza al 95%", "Rango de valores compatibles con la estimación; si incluye el cero, no se distingue de «sin efecto»."),
            ("p corregido", "p-valor ajustado porque se probaron varias asociaciones a la vez (método de Benjamini-Hochberg). Debajo de 0,05, el resultado resiste la corrección."),
            ("BEC (uso económico)", "Clasificación de Naciones Unidas que agrupa los productos según su uso: bienes de consumo, insumos y bienes de capital."),
            ("Ventana común", "Mismo período para todas las variables que se comparan (acá, 2018 a 2025), para no comparar importaciones de un período con resultados de otro."),
        ], columns=["Término", "Significado"]).set_index("Término")
    )


def mostrar():
    _introduccion()
    _fuentes()
    _decisiones()
    _controles()
    _limites()
    _glosario()
