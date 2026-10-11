"""Página «Importaciones vs. resultados»: ¿se perdió empleo, producción y salario justo donde más crecieron las importaciones?

Orden de la página (el mismo que el de la respuesta):
  A. La respuesta, 2018 -> 2025 (ventana común; medida principal: crecimiento de las importaciones en USD).
  B. ¿Cambia la respuesta si se mide distinto? (otras medidas, p corregido, ponderación, cada rama, tendencia previa).
  C. Exploración y complementos (las 4 medidas y las 2 bases de siempre, China y el modelo de panel).
"""
import pandas as pd
import streamlit as st

from core.consultas import empleo_trimestre
from core.datos import TOTAL, leer, nombre
from core.formato import fmt_miles, fmt_num, fmt_p, fmt_pct
from core.graficos import barras_agrupadas, barras_h, barras_signo, coeficientes, dispersion, heatmap
from core.tarjetas import afiche, fila_hallazgo, redondo
from core.tema import AZUL, ESCALA_RESULTADO, NARANJA
from core.ui import bloque, figura, nota, sintesis

UNIDAD = {"d_imp_cif": "%", "d_imp_kg": "%", "d_china_pp": "p.p.", "pct_china": "%"}
MAS, MENOS = "Importaciones crecieron más", "Importaciones crecieron menos"
COLOR_GRUPO = {MAS: NARANJA, MENOS: AZUL}
PRENDAS, TEXTILES, ALIMENTOS = "18-19", "17", "15"
OEDE_INDEC = "OEDE · INDEC"


# ------------------------------------------------------------------------------------------ datos
def _respuesta():
    """Tablas de la respuesta (2018 -> 2025) ya calculadas en el cuaderno 03."""
    r = leer("respuesta_por_rama.csv").assign(etiqueta=lambda x: x.rama.map(nombre))
    g = leer("respuesta_grupos.csv").set_index("grupo")
    c = leer("respuesta_correlaciones.csv")
    s = leer("respuesta_sensibilidad.csv")
    return r, g, c, s


def _opciones():
    corr = leer("correlaciones.csv")
    expo = corr[["exposicion_col", "exposicion"]].drop_duplicates().set_index("exposicion_col").exposicion.to_dict()
    res = corr[["resultado_col", "resultado"]].drop_duplicates().set_index("resultado_col").resultado.to_dict()
    return expo, res


def _fuerza(rho: float) -> str:
    a = abs(rho)
    return "muy débil" if a < 0.2 else "débil" if a < 0.4 else "moderada" if a < 0.6 else "fuerte"


def _significativas(n: int, total: int) -> str:
    return f"{n} de {total} estimaciones {'es significativa' if n == 1 else 'son significativas'}"


def _minuscula(s: str) -> str:
    """Primera letra en minúscula, sin tocar siglas ni nombres propios (USD, China, IPI)."""
    return s[:1].lower() + s[1:]


def _resisten(n: int) -> str:
    return "ninguna resiste" if n == 0 else f"{'resiste' if n == 1 else 'resisten'} {n}"


# ------------------------------------------------------------------------------------ introducción
def _introduccion():
    st.markdown(
        """
**La pregunta:** desde 2018, ¿la industria argentina perdió empleo, producción y salario **justo en los sectores donde más crecieron las importaciones**?
Se pregunta si las dos cosas **coinciden**, no si una provocó la otra.

**Cómo se responde:** se comparan las 16 ramas industriales entre **2018 y 2025**, el último año completo en todas las fuentes (así importaciones y resultados miden el mismo período).
La medida principal es **cuánto crecieron las importaciones en dólares** de cada rama; los resultados, el cambio del empleo, la producción y el salario real (promedios anuales).

**Cómo está ordenada la página:** (A) la respuesta; (B) si la respuesta cambia al medir distinto, incluido separar las importaciones que **compiten** (bienes de consumo) de las que **abastecen** (insumos y máquinas); (C) exploración y complementos: las otras medidas, la base 2023, China y el modelo de panel.
"""
    )
    nota("Son coincidencias, no efectos causales. Las importaciones de una rama suben también cuando esa rama crece (importa insumos y "
         "maquinaria), y en el período hubo devaluaciones, recesión, pandemia y cambios de política a la vez.", titulo="Antes de leer los resultados:")


# ----------------------------------------------------------------------------------- A. respuesta
def _tarjetas(r, g):
    mas, menos = g.loc[MAS], g.loc[MENOS]
    pr = r.set_index("rama").loc[PRENDAS]
    al_reves = mas.puestos > menos.puestos
    titulo = ("¿Se perdió justo donde más crecieron las importaciones? No: en general, al revés" if al_reves
              else "¿Se perdió justo donde más crecieron las importaciones? Sí, en empleo")
    per = "2018 → 2025"

    def mm(v):
        return "MÁS" if v > 0 else "MENOS"

    tarjetas = [
        afiche(redondo(mas.puestos), (f"{mm(mas.puestos)} EMPLEOS", "DONDE MÁS SE IMPORTÓ"), "CRECIERON MÁS · 8 RAMAS", per,
               f"Exactamente <b>{fmt_miles(mas.puestos)}</b> puestos ({fmt_pct(mas.empleo)}). Sus importaciones crecieron {fmt_pct(mas.imp_usd, False)} (mediana).",
               OEDE_INDEC, ""),
        afiche(redondo(menos.puestos), (f"{mm(menos.puestos)} EMPLEOS", "DONDE MENOS SE IMPORTÓ"), "CRECIERON MENOS", per,
               f"8 ramas. Exactamente <b>{fmt_miles(menos.puestos)}</b> ({fmt_pct(menos.empleo)}).", OEDE_INDEC, ""),
        afiche(fmt_pct(menos.produccion), (f"{mm(menos.produccion)} PRODUCCIÓN", "DONDE MENOS SE IMPORTÓ"), "PRODUCCIÓN (MEDIANA)", per,
               f"Donde más se importó: <b>{fmt_pct(mas.produccion)}</b>.", "INDEC", ""),
        afiche(redondo(pr.puestos), ("MENOS EMPLEOS" if pr.puestos < 0 else "MÁS EMPLEOS", "EN PRENDAS Y CALZADO"), "LA EXCEPCIÓN", per,
               f"Sus importaciones crecieron <b>{fmt_pct(pr.imp_usd, False)}</b> en dólares y {fmt_pct(pr.imp_ton, False)} en toneladas.", OEDE_INDEC, ""),
        afiche(str(len(r)), ("RAMAS", "COMPARADAS"), "COINCIDENCIA, NO CAUSA", per,
               "Mide si las pérdidas coinciden con las importaciones, no si las provocaron.", OEDE_INDEC, "", "neu"),
    ]
    st.subheader("A. La respuesta, 2018 → 2025")
    st.markdown(f'<div class="hallazgos">{fila_hallazgo(1, titulo, tarjetas)}</div>', unsafe_allow_html=True)


def _respuesta_dispersion(r, c):
    f = c[(c.exposicion_col == "imp_usd") & (c.resultado_col == "empleo")].iloc[0]
    pr, tx = r.set_index("rama").loc[PRENDAS], r.set_index("rama").loc[TEXTILES]
    sentido = "a más importaciones, más empleo" if f.rho > 0 else "a más importaciones, menos empleo"

    with bloque("1. Importaciones y empleo, rama por rama"):
        fig = dispersion(r, "imp_usd", "empleo", "etiqueta", x_titulo="Crecimiento de las importaciones en dólares, 2018 → 2025 (%)",
                         y_titulo="Cambio del empleo, 2018 → 2025 (%)", alto=360, resaltar=[nombre(PRENDAS), nombre(TEXTILES)])
        # las ramas apiñadas cerca de 0 (importaciones +20-30%, empleo casi igual) van en un solo rótulo para que no se pisen los nombres
        apinadas = r.imp_usd.between(20, 30) & (r.empleo.abs() < 1.5)
        fig.data[0].text = [("" if a else e) for a, e in zip(apinadas, r.etiqueta)]
        fig.data[0].textposition = ["middle left" if x == TEXTILES else "top center" for x in r.rama]
        if apinadas.any():
            c0 = r[apinadas]
            fig.add_annotation(x=c0.imp_usd.mean(), y=c0.empleo.mean(), ax=60, ay=-4, axref="x", ayref="y", arrowcolor="#898781", arrowwidth=1,
                               text="<br>".join(c0.etiqueta), align="left", xanchor="left", font=dict(size=9))
        fig.update_xaxes(range=[r.imp_usd.min() - 15, r.imp_usd.max() + 20])
        figura(
            fig,
            que="Cada punto es una rama industrial. El eje horizontal dice cuánto crecieron sus importaciones en dólares entre 2018 y 2025; el vertical, cuánto cambió su empleo "
                "(promedio de 2025 contra promedio de 2018). Prendas y Textiles están en naranja porque son el centro del debate público.",
            como="Si la respuesta fuera «sí», los puntos bajarían hacia la derecha: más importaciones, más empleo perdido. La recta discontinua resume la tendencia.",
            observa=f"Los puntos suben hacia la derecha: la relación es {_fuerza(f.rho)} y en el sentido de «{sentido}» (ρ de Spearman = {fmt_num(f.rho, 2)}, p {fmt_p(f.p_valor)}). "
                    f"La excepción más clara es {nombre(PRENDAS)}: sus importaciones crecieron {fmt_pct(pr.imp_usd, False)} y perdió {fmt_miles(abs(pr.puestos))} puestos ({fmt_pct(pr.empleo)}). "
                    f"{nombre(TEXTILES)} parece poco expuesta en dólares ({fmt_pct(tx.imp_usd)}), pero en toneladas sus importaciones crecieron {fmt_pct(tx.imp_ton, False)} y perdió "
                    f"{fmt_miles(abs(tx.puestos))} puestos: se importa mucho más volumen a precios más bajos.",
            tener_en_cuenta=f"Con 16 ramas y corrigiendo por las pruebas hechas, la relación no se distingue del azar (p corregido = {fmt_num(f.p_corregido, 2)}). "
                            "Lo que sí se puede decir es que no aparece el patrón «más importaciones, más pérdidas».",
        )


def _respuesta_barras(r):
    d = r.assign(etiqueta=lambda x: x.etiqueta + " (" + x.imp_usd.map(lambda v: fmt_pct(v, True).replace(",0%", "%")) + ")")
    n_menos = int((r.grupo == MENOS).sum())
    perdedoras = r[r.puestos < 0]
    pct_menos = perdedoras[perdedoras.grupo == MENOS].puestos.sum() / perdedoras.puestos.sum() * 100
    top = r.sort_values("puestos").iloc[0]

    with bloque("2. Puestos ganados y perdidos, de la rama donde más crecieron las importaciones a la que menos"):
        fig = barras_signo(d, "puestos", "etiqueta", orden="imp_usd", x_titulo="Puestos de trabajo, 2018 → 2025", alto=380,
                           separador=(n_menos, "▲ importaciones crecieron más", "▼ crecieron menos"))
        fig.update_xaxes(range=[r.puestos.min() * 1.5, r.puestos.max() * 1.25])
        figura(
            fig,
            que="Cada barra son los puestos de trabajo que ganó (azul) o perdió (naranja) una rama entre 2018 y 2025. Las ramas están ordenadas por cuánto crecieron sus importaciones "
                "en dólares (entre paréntesis): arriba las que más, abajo las que menos. La línea punteada separa las 8 de arriba de las 8 de abajo.",
            como="Si la respuesta fuera «sí», las barras naranjas (pérdidas) se juntarían arriba de la línea. Si se juntan abajo, las pérdidas están donde las importaciones crecieron menos.",
            observa=f"{len(perdedoras)} ramas perdieron puestos, en total {fmt_miles(abs(perdedoras.puestos.sum()))}. El {fmt_num(pct_menos, 0)}% de esa pérdida está debajo de la línea, "
                    f"en ramas donde las importaciones crecieron menos. La pérdida más grande es la de {top.etiqueta} ({fmt_miles(abs(top.puestos))} puestos), "
                    f"{'la excepción: está arriba de la línea' if top.grupo == MAS else 'debajo de la línea'}.",
            tener_en_cuenta="Son promedios anuales: compara todo 2025 con todo 2018. El empleo industrial cae desde el máximo de 2023, así que contra el último trimestre "
                            "publicado las pérdidas son mayores (ver «Empleo y ramas»).",
        )


def _respuesta_grupos(r, g):
    filas = [dict(grupo=k, indicador=nom, v=g.loc[k, col]) for k in (MAS, MENOS)
             for nom, col in (("Empleo", "empleo"), ("Producción", "produccion"), ("Salario real", "salario"))]
    mas, menos, tot = g.loc[MAS], g.loc[MENOS], g.loc["Total industria"]
    q18 = empleo_trimestre(TOTAL, "2018")
    peor = [nom for nom, col in (("empleo", "empleo"), ("producción", "produccion"), ("salario real", "salario")) if mas[col] < menos[col]]

    with bloque("3. Las dos mitades de la industria"):
        fig = barras_agrupadas(pd.DataFrame(filas), "indicador", "grupo", "v", COLOR_GRUPO, y_titulo="Cambio %, 2018 → 2025", alto=300)
        figura(
            fig,
            que="Las 16 ramas partidas al medio por cuánto crecieron sus importaciones en dólares: 8 donde crecieron más (naranja) y 8 donde crecieron menos (azul). "
                "Empleo: cambio % del total de puestos de cada mitad; producción y salario real: mediana de las ramas de cada mitad.",
            como="Si la respuesta fuera «sí», la barra naranja quedaría por debajo de la azul en los tres indicadores.",
            observa=(f"La naranja queda por debajo solo en {', '.join(peor)}. " if peor else "La naranja no queda por debajo de la azul en ningún indicador. ")
                    + f"Las dos mitades perdieron salario real, y el total de la industria produjo {fmt_pct(tot.produccion)} y pagó salarios {fmt_pct(tot.salario)} (2025 contra 2018). "
                    f"El empleo total quedó en {fmt_pct(tot.empleo)} con promedios anuales; contra el {q18.trimestre_ultimo} la variación es {fmt_pct(q18.delta_pct)}, porque la caída es de 2024 en adelante.",
            tener_en_cuenta="Donde más crecieron: " + ", ".join(nombre(x.strip()) for x in mas.ramas.split(",")) +
                            ". Donde menos: " + ", ".join(nombre(x.strip()) for x in menos.ramas.split(",")) + ".",
        )


# ------------------------------------------------------------------------- B. robustez de la respuesta
def _robustez_medidas(c):
    d = c.assign(etiqueta=lambda x: x.exposicion.str.replace(r" \(.*\)", "", regex=True) + " · " + x.resultado)
    n_sig, n_bh, n_neg_sig = int((c.p_valor < 0.05).sum()), int((c.p_corregido < 0.05).sum()), int(((c.rho < 0) & (c.p_valor < 0.05)).sum())
    minimo = c.loc[c.p_corregido.idxmin()]

    st.subheader("B. ¿Cambia la respuesta si se mide distinto?")
    with bloque("4. Tres medidas de importaciones, tres resultados"):
        fig = coeficientes(d, "etiqueta", "rho", "ic_bajo", "ic_alto", "p_corregido", x_titulo="Correlación de Spearman (ρ) con su intervalo de confianza al 95%", alto=330)
        figura(
            fig,
            que="Las 9 correlaciones entre ramas que responden la pregunta: tres maneras de medir cuánto crecieron las importaciones (en dólares, en toneladas y en dólares por "
                "puesto de trabajo) contra los tres resultados, todo 2018 → 2025.",
            como="Cada punto es la correlación (de −1 a +1) y la barra gris el rango donde probablemente está el valor real (intervalo por bootstrap). Para un «sí» harían falta puntos "
                 "a la izquierda del cero con la barra entera a la izquierda. Naranja = resiste la corrección por comparaciones múltiples.",
            observa=f"{int((c.rho > 0).sum())} de 9 correlaciones son positivas y {'ninguna es negativa y significativa' if n_neg_sig == 0 else f'{n_neg_sig} es negativa y significativa'}. Sin corregir, {n_sig} {'da' if n_sig == 1 else 'dan'} p < 0,05; "
                    f"corrigiendo por las 9 pruebas, {_resisten(n_bh)} (la más cercana: {_minuscula(minimo.exposicion)} con {_minuscula(minimo.resultado)}, p corregido = {fmt_num(minimo.p_corregido, 2)}). "
                    "Ninguna medida muestra que las ramas donde más crecieron las importaciones hayan perdido más.",
            tener_en_cuenta="Los intervalos son muy anchos: con 16 ramas los datos son compatibles con una relación nula o positiva, y apenas con una negativa moderada. "
                            "«No se ve» no quiere decir «no existe».",
        )


def _robustez_sensibilidad(r, s, c):
    sin = s[s.tipo == "sin_rama"].assign(etiqueta=lambda x: "sin " + x.detalle.map(nombre))
    pond = s[s.tipo == "ponderada"].set_index("detalle")
    prev = s[s.tipo == "tendencia_previa"].set_index("detalle")
    base = c[(c.exposicion_col == "imp_usd") & (c.resultado_col == "empleo")].iloc[0]
    lo, hi = sin.loc[sin.estimacion.idxmin()], sin.loc[sin.estimacion.idxmax()]

    with bloque("5. Sacando cada rama de a una, ponderando por tamaño y mirando la tendencia previa"):
        fig = barras_h(sin, "estimacion", "etiqueta", color=AZUL, formato="{:+.2f}", x_titulo="ρ importaciones (USD) vs. empleo, sacando una rama", alto=380)
        fig.add_vline(x=base.rho, line_dash="dash", line_color=NARANJA, line_width=1.5)
        figura(
            fig,
            que="La correlación principal (crecimiento de las importaciones en dólares contra cambio del empleo) recalculada 16 veces, sacando cada vez una rama. "
                f"La línea naranja es el valor con las 16 ramas (ρ = {fmt_num(base.rho, 2)}).",
            como="Si alguna barra cruzara a valores negativos, la respuesta dependería de esa rama. Si todas quedan del mismo lado, la respuesta no depende de una sola rama.",
            observa=f"Todas quedan entre {fmt_num(lo.estimacion, 2)} ({lo.etiqueta}) y {fmt_num(hi.estimacion, 2)} ({hi.etiqueta}): ninguna cambia el signo. "
                    f"Sacar {nombre(PRENDAS)} la vuelve más fuerte, porque es la gran excepción.",
            tener_en_cuenta="Abajo, dos pruebas más: ponderar por el tamaño de cada rama y descontar la tendencia que cada rama traía desde antes de 2018.",
        )
        a, b, d = st.columns(3)
        a.metric("Ponderada por empleo (16 ramas)", f"p {fmt_p(pond.loc['16 ramas', 'p_valor'])}", f"pendiente {fmt_num(pond.loc['16 ramas', 'estimacion'], 2)} p.p. por 1%",
                 delta_color="off", delta_arrow="off", border=True,
                 help="Regresión del cambio del empleo sobre el crecimiento de las importaciones, dando a cada rama un peso según sus puestos de 2018.")
        b.metric("Ponderada, sin Alimentos y bebidas", f"p {fmt_p(pond.loc['sin Alimentos y bebidas', 'p_valor'])}",
                 f"pendiente {fmt_num(pond.loc['sin Alimentos y bebidas', 'estimacion'], 2)} p.p. por 1%", delta_color="off", delta_arrow="off", border=True,
                 help="La misma regresión sin la rama más grande, que es también la de mayor crecimiento de importaciones.")
        d.metric("Tendencia previa (empleo 2011-2017)", f"p {fmt_p(prev.loc['empleo 2011-2017', 'p_valor'])}",
                 f"importaciones: p {fmt_p(prev.loc['importaciones (USD)', 'p_valor'])}", delta_color="off", delta_arrow="off", border=True,
                 help="Regresión sobre rangos con dos variables: el crecimiento de las importaciones y cuánto cambió el empleo de la rama entre 2011 y 2017.")
        nota(f"Ponderando por tamaño, la relación positiva parece muy firme, pero es solo {nombre(ALIMENTOS)}: la rama más grande es también la de mayor crecimiento de importaciones "
             f"({fmt_pct(r.set_index('rama').loc[ALIMENTOS].imp_usd)}) y la que más empleo ganó. Y la tendencia previa explica más que las importaciones: las ramas que perdían "
             "empleo entre 2011 y 2017 son, en gran parte, las que lo pierden ahora.", titulo="Cómo leerlo:", color="blue")


def _uso_economico(r):
    u = leer("respuesta_uso_correlaciones.csv")
    filas = list(dict.fromkeys(u.exposicion))
    etiqueta = {e: f"{e} · {int(u[u.exposicion == e].n_ramas.iloc[0])} ramas" for e in filas}
    mat = u.pivot(index="exposicion", columns="resultado", values="rho").reindex(index=filas, columns=["Empleo", "Producción", "Salario real"])
    pc = u.pivot(index="exposicion", columns="resultado", values="p_corregido").reindex_like(mat)
    mat.index, pc.index = [etiqueta[e] for e in mat.index], [etiqueta[e] for e in pc.index]
    cons = u[(u.exposicion_col == "consumo_usd") & (u.resultado_col == "empleo")].iloc[0]
    ins = u[(u.exposicion_col == "insumos_usd") & (u.resultado_col == "empleo")].iloc[0]
    kg_prod = u[(u.exposicion_col == "consumo_ton") & (u.resultado_col == "produccion")].iloc[0]
    resisten = u[u.p_corregido < 0.05]
    lista = "; ".join(f"{_minuscula(x.exposicion)} con {_minuscula(x.resultado)}" for x in resisten.itertuples())

    with bloque("6. Lo que compite y lo que abastece: las importaciones según su uso"):
        fig = heatmap(mat, escala=ESCALA_RESULTADO, rango=1, decimales=2, sufijo="", alto=300, colorbar_titulo="ρ", marcas=pc < 0.05)
        figura(
            fig,
            que="La misma comparación entre ramas (2018 → 2025), pero separando lo que importa cada rama según su uso económico (clasificación BEC de Naciones Unidas): "
                "bienes de consumo, que compiten con lo que la rama vende; insumos y bienes de capital, que la abastecen.",
            como="Cada celda es la correlación de Spearman entre cuánto crecieron las importaciones de ese uso y cuánto cambió el resultado. Naranja: a más importaciones, peor resultado; "
                 "azul: mejor. El asterisco marca lo que resiste la corrección por comparaciones múltiples.",
            observa=f"El resultado de la sección A sale de los insumos: donde más crecieron las importaciones de insumos, más creció el empleo (ρ = {fmt_num(ins.rho, 2)}, "
                    f"p corregido = {fmt_num(ins.p_corregido, 3)}). Con los bienes de consumo esa relación desaparece (ρ = {fmt_num(cons.rho, 2)} con el empleo), y en toneladas "
                    f"aparece una señal negativa con la producción (ρ = {fmt_num(kg_prod.rho, 2)}) que no llega a ser significativa. "
                    + (f"Resiste la corrección: {lista}." if len(resisten) == 1 else f"Resisten la corrección: {lista}." if len(resisten) else "Ninguna resiste la corrección."),
            tener_en_cuenta="Una rama que crece importa más insumos y máquinas: por eso las importaciones totales suben con la actividad. Los bienes de capital solo aparecen en las "
                            "ramas que los producen (maquinaria, electrónica, transporte), por eso esa fila tiene menos ramas.",
        )


def _consumo_dispersion(r):
    d = r.dropna(subset=["consumo_usd"])
    pr = d.set_index("rama").loc[PRENDAS]
    u = leer("respuesta_uso_correlaciones.csv")
    f = u[(u.exposicion_col == "consumo_usd") & (u.resultado_col == "empleo")].iloc[0]
    g = leer("respuesta_uso_grupos.csv").set_index("grupo")
    mas, menos = g.loc["Consumo importado creció más"], g.loc["Consumo importado creció menos"]

    with bloque("7. Solo bienes de consumo: importaciones y empleo, rama por rama"):
        fig = dispersion(d, "consumo_usd", "empleo", "etiqueta", x_titulo="Crecimiento de las importaciones de bienes de consumo, 2018 → 2025 (%)",
                         y_titulo="Cambio del empleo, 2018 → 2025 (%)", alto=340, resaltar=[nombre(PRENDAS), nombre(TEXTILES)])
        fig.update_xaxes(range=[d.consumo_usd.min() - 15, d.consumo_usd.max() + 20])
        # nombres alternados arriba y abajo del punto, en el orden del eje horizontal, para que no se pisen
        orden = d.consumo_usd.rank(method="first").astype(int)
        fig.data[0].textposition = ["bottom center" if o % 2 else "top center" for o in orden]
        figura(
            fig,
            que="Como la sección 1, pero el eje horizontal mide solo las importaciones de bienes de consumo de cada rama: lo que compite directamente con lo que vende. "
                f"Son {len(d)} ramas ({nombre('23')} no importa bienes de consumo).",
            como="Si la respuesta fuera «sí», los puntos bajarían hacia la derecha.",
            observa=f"Los puntos no siguen ninguna dirección (ρ = {fmt_num(f.rho, 2)}, p {fmt_p(f.p_valor)}). Partiendo las ramas al medio, donde más creció el consumo importado "
                    f"el empleo varió {fmt_pct(mas.empleo)} ({fmt_miles(mas.puestos)} puestos) y donde menos, {fmt_pct(menos.empleo)} ({fmt_miles(menos.puestos)}). "
                    f"{nombre(PRENDAS)} sigue siendo el caso más visible: su consumo importado creció {fmt_pct(pr.consumo_usd, False)} y perdió {fmt_miles(abs(pr.puestos))} puestos.",
            tener_en_cuenta="Cada producto se asigna a la rama que lo fabrica según su capítulo del nomenclador: un auto importado cuenta en Automotores y una remera en Prendas.",
        )


# --------------------------------------------------------------------- C. exploración y complementos
def _exploracion_intro():
    st.subheader("C. Exploración y complementos")
    st.markdown(
        """
Las secciones siguientes son las del análisis original: permiten elegir **la base de comparación** (2018 o 2023), **la medida de exposición** y **el resultado**.
Usan el **último dato publicado** de cada resultado (no la ventana común 2018 → 2025), y suman dos medidas basadas en **China**:

- *Crecimiento de las importaciones (USD)* y *(toneladas)*: variación % del valor y del peso importado por la rama.
- *Aumento de la participación de China (p.p.)*: cuántos puntos porcentuales ganó China en lo importado por la rama.
- *Participación de China (nivel)*: qué parte de lo importado por la rama viene de China en 2025.
"""
    )


def _filtros(opc_expo, opc_res):
    with st.container(horizontal=True, vertical_alignment="bottom"):
        ventana = st.segmented_control("Base de comparación", ["2018", "2023"], default="2018", key="exp_ventana") or "2018"
        expo_col = st.selectbox("Medida de exposición a importaciones", list(opc_expo), format_func=opc_expo.get, key="exp_col")
        res_col = st.segmented_control("Resultado", list(opc_res), default="d_empleo", format_func=opc_res.get, key="exp_res") or "d_empleo"
    return ventana, expo_col, res_col


def _dispersion(ventana, expo_col, res_col, opc_expo, opc_res):
    expo, corr = leer("exposicion_vs_resultados.csv"), leer("correlaciones.csv")
    fila = corr[(corr.ventana == ventana) & (corr.exposicion_col == expo_col) & (corr.resultado_col == res_col)].iloc[0]
    d = expo[expo.ventana == ventana].assign(etiqueta=lambda x: x.rama.map(nombre))
    tx = d[d.etiqueta == "Textiles"].iloc[0]
    sentido = "a mayor exposición, peor resultado" if fila.rho < 0 else "a mayor exposición, mejor resultado"
    signif = "es estadísticamente significativa (p < 0,05)" if fila.p_valor < 0.05 else "no se distingue del azar con solo 16 ramas (p ≥ 0,05)"
    resiste = "y resiste" if fila.p_corregido < 0.05 else "pero no resiste"

    with bloque("8. Comparación entre ramas, con la medida y la base que elijas"):
        fig = dispersion(d, expo_col, res_col, "etiqueta", x_titulo=f"{opc_expo[expo_col]} ({UNIDAD[expo_col]})", y_titulo=opc_res[res_col],
                         alto=340, resaltar="Textiles")
        figura(
            fig,
            que=f"Cada punto es una rama. El eje horizontal es su exposición a las importaciones («{opc_expo[expo_col]}») y el vertical su resultado («{opc_res[res_col]}»), "
                f"tomando {ventana} como base. Textiles está resaltado en naranja porque es una de las ramas más discutidas.",
            como="Si las ramas más expuestas (a la derecha) tuvieran peores resultados, los puntos bajarían hacia la derecha: una recta con pendiente negativa y correlación "
                 "negativa. La recta discontinua es una guía por mínimos cuadrados. Abajo se resume la relación con la correlación de Spearman (ρ), que se calcula sobre rangos: "
                 "de −1 a +1, y un valor extremo no la domina como pasaría con la de Pearson.",
            observa=f"Con esta combinación se observa una relación {_fuerza(fila.rho)} en el sentido de «{sentido}» (ρ = {fmt_num(fila.rho, 2)}), que {signif}"
                    + (f" {resiste} la corrección por comparaciones múltiples (p corregido = {fmt_num(fila.p_corregido, 3)})" if fila.p_valor < 0.05 else "") + ". "
                    f"Textiles tiene una exposición de {fmt_num(tx[expo_col])} {UNIDAD[expo_col]} y un resultado de {fmt_pct(tx[res_col])}.",
            tener_en_cuenta="Dos trampas: (1) la exposición se mide al final del período, y una rama cuya producción ya cayó por otro motivo muestra más importaciones relativas por construcción; "
                            "(2) se prueban 24 combinaciones, así que 1 o 2 resultados «significativos» pueden aparecer solo por azar: por eso se muestra el p corregido.",
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Correlación de Spearman (ρ)", fmt_num(fila.rho, 2), border=True,
                  help="De -1 a +1. Negativa: a mayor exposición, peor resultado. Se calcula sobre rangos, por lo que un valor extremo no la domina.")
        c2.metric("p-valor", fmt_num(fila.p_valor, 3), border=True,
                  help="Probabilidad de ver una asociación así por puro azar si no hubiera ninguna. Menos de 0,05 se considera significativa.")
        c3.metric("p corregido", fmt_num(fila.p_corregido, 3), border=True,
                  help="El p-valor ajustado porque se probaron 24 combinaciones (método de Benjamini-Hochberg). Menos de 0,05: resiste la corrección.")
        c4.metric("Ramas", int(fila.n_ramas), border=True)


def _mapa_correlaciones(ventana, opc_expo, opc_res):
    corr = leer("correlaciones.csv")
    cv = corr[corr.ventana == ventana]
    mat = cv.pivot(index="exposicion", columns="resultado", values="rho").reindex(index=list(opc_expo.values()), columns=list(opc_res.values()))
    pc = cv.pivot(index="exposicion", columns="resultado", values="p_corregido").reindex_like(mat)
    n_sig, n_bh, n_neg = int((cv.p_valor < 0.05).sum()), int((cv.p_corregido < 0.05).sum()), int((mat < 0).sum().sum())
    fuerte = cv.loc[cv.rho.abs().idxmax()]
    es_china = cv.exposicion.str.contains("China")
    rho_china, rho_imp = cv[es_china].rho.mean(), cv[~es_china].rho.mean()

    with bloque("9. Todas las combinaciones de una vez"):
        fig = heatmap(mat, escala=ESCALA_RESULTADO, rango=1, decimales=2, sufijo="", alto=300, colorbar_titulo="ρ", marcas=pc < 0.05)
        figura(
            fig,
            que=f"La correlación de Spearman entre cada medida de exposición (filas) y cada resultado (columnas), para la base {ventana}. Son las 12 combinaciones posibles con esa base.",
            como="Naranja: a más exposición, peor resultado; azul: a más exposición, mejor resultado; gris: sin relación. El asterisco (*) marca las correlaciones que resisten la "
                 "corrección por comparaciones múltiples (p corregido < 0,05). Una asociación que aparece en una sola celda es más frágil que un patrón que se repite.",
            observa=f"Con base {ventana}, {n_neg} de las 12 correlaciones son negativas; {n_sig} {'da' if n_sig == 1 else 'dan'} p < 0,05 y {_resisten(n_bh)} la corrección. "
                    f"La más fuerte es «{fuerte.exposicion}» con «{fuerte.resultado}» (ρ = {fmt_num(fuerte.rho, 2)}, p {fmt_p(fuerte.p_valor)}). "
                    f"En promedio, las medidas de China dan ρ = {fmt_num(rho_china, 2)} y las de crecimiento de las importaciones ρ = {fmt_num(rho_imp, 2)}: "
                    f"{'China se asocia con peores resultados más que el crecimiento de las importaciones' if rho_china < rho_imp else 'el crecimiento de las importaciones se asocia con peores resultados más que China'}.",
            tener_en_cuenta="La participación de China en nivel dice en qué productos vende China (textiles, muebles, electrónica), sectores que caen en muchos países: mide la composición "
                            "de la industria más que un aumento de la competencia. Por eso China es un complemento y no la respuesta.",
        )


def _grupos(ventana, expo_col, opc_expo):
    grupos = leer("grupos_exposicion.csv")
    g = grupos[(grupos.ventana == ventana) & (grupos.exposicion == opc_expo[expo_col])]
    mayor, menor = g[g.grupo == "Mayor exposición"].iloc[0], g[g.grupo == "Menor exposición"].iloc[0]
    filas = []
    for r in g.itertuples():
        filas += [dict(grupo=r.grupo, indicador="Empleo", v=r.mediana_d_empleo),
                  dict(grupo=r.grupo, indicador="Salario real", v=r.mediana_d_salario),
                  dict(grupo=r.grupo, indicador="Producción (IPI)", v=r.mediana_d_ipi)]
    peor = []
    for nom, a, b in [("empleo", mayor.mediana_d_empleo, menor.mediana_d_empleo), ("salario real", mayor.mediana_d_salario, menor.mediana_d_salario),
                      ("producción", mayor.mediana_d_ipi, menor.mediana_d_ipi)]:
        peor.append(f"en {nom} los más expuestos {'evolucionaron peor' if a < b else 'evolucionaron mejor'} ({fmt_pct(a)} contra {fmt_pct(b)})")

    with bloque("10. Ramas de mayor vs. menor exposición, con la medida y la base que elijas"):
        fig = barras_agrupadas(pd.DataFrame(filas), "indicador", "grupo", "v", {"Mayor exposición": NARANJA, "Menor exposición": AZUL},
                               y_titulo="Mediana del cambio %", alto=290)
        figura(
            fig,
            que=f"Las 16 ramas partidas al medio según la medida de exposición elegida arriba («{opc_expo[expo_col]}», base {ventana}): 8 de mayor y 8 de menor exposición. "
                "Para cada mitad, la mediana del cambio porcentual en empleo, salario real y producción.",
            como="Se comparan barras del mismo indicador: si la naranja (mayor exposición) está por debajo de la azul, las ramas más expuestas evolucionaron peor. Se usa la mediana y no el "
                 "promedio para que una rama extrema no distorsione al grupo.",
            observa="En este corte, " + "; ".join(peor) + f". En puestos absolutos, las ramas de mayor exposición sumaron {fmt_miles(mayor.delta_puestos)} y las de menor {fmt_miles(menor.delta_puestos)}.",
            tener_en_cuenta="Con 8 ramas por grupo, la mediana puede cambiar mucho si una rama pasa de un grupo al otro: los resultados de esta sección son descriptivos, no una prueba estadística.",
        )
        with st.expander("Qué ramas hay en cada grupo"):
            st.markdown(f"**Mayor exposición:** {', '.join(nombre(x.strip()) for x in mayor.ramas.split(','))}")
            st.markdown(f"**Menor exposición:** {', '.join(nombre(x.strip()) for x in menor.ramas.split(','))}")


def _panel():
    regs = leer("regresiones_panel.csv")
    with bloque("11. Complemento: modelo de panel, dentro de cada rama año por año"):
        st.markdown('<div class="expl"><p>Responde otra pregunta, más cercana a la dinámica de corto plazo: cuando las importaciones de una rama suben respecto de lo habitual '
                    'para esa rama, ¿su empleo sube o baja ese mismo año?</p></div>', unsafe_allow_html=True)
        with st.container(horizontal=True):
            muestra = st.segmented_control("Muestra", ["Todas las ramas", "Sin refinación de petróleo"], default="Todas las ramas", key="reg_muestra") or "Todas las ramas"
            rezago = st.segmented_control("Momento de las importaciones", [0, 1], default=0, key="reg_rezago",
                                          format_func=lambda x: "Mismo año" if x == 0 else "Año anterior") or 0
        r = regs[(regs.muestra == muestra) & (regs.rezago_anios == rezago)].copy()
        r["etiqueta"] = r.resultado + " · " + r.importaciones.str.replace("Importaciones ", "imp. ")
        r = r.sort_values(["resultado", "importaciones"])
        n_sig, n_pos = int((r.p_valor < 0.05).sum()), int((r.efecto_10pct > 0).sum())
        emp = r[(r.resultado == "Empleo") & (r.importaciones == "Importaciones totales")].iloc[0]
        todas = regs[(regs.muestra == "Todas las ramas") & (regs.rezago_anios == rezago)]
        sin = regs[(regs.muestra == "Sin refinación de petróleo") & (regs.rezago_anios == rezago)]

        fig = coeficientes(r, "etiqueta", "efecto_10pct", "efecto_10pct_bajo", "efecto_10pct_alto", "p_valor",
                           x_titulo="Cambio % del resultado ante +10% de importaciones (IC 95%)", alto=300)
        figura(
            fig,
            que="Cuánto cambia el empleo, la producción o el salario real de una rama cuando sus importaciones aumentan 10%, comparando cada rama consigo misma entre 2016 y 2025 "
                "y descontando lo que le pasa a toda la industria en cada año (efectos fijos de rama y de año).",
            como="Cada punto es la estimación y la barra gris su intervalo de confianza al 95%. Naranja: la estimación es significativa al 5% (el intervalo no incluye el cero); gris: no se "
                 "distingue de cero. Un punto a la izquierda del cero indicaría que más importaciones se asocian con peor resultado; a la derecha, con mejor resultado.",
            observa=f"En esta muestra, {_significativas(n_sig, len(r))} y {n_pos} {'es positiva' if n_pos == 1 else 'son positivas'}. Para el empleo y las importaciones totales, +10% de importaciones se asocia con "
                    f"{fmt_pct(emp.efecto_10pct)} de empleo en la rama (intervalo de {fmt_pct(emp.efecto_10pct_bajo)} a {fmt_pct(emp.efecto_10pct_alto)}). "
                    f"Con todas las ramas, {_significativas(int((todas.p_valor < 0.05).sum()), len(todas))}; excluyendo refinación de petróleo, {int((sin.p_valor < 0.05).sum())} de {len(sin)}.",
            tener_en_cuenta="Que el resultado cambie tanto al sacar una sola rama (refinación, donde las importaciones cayeron y la producción subió) muestra que la conclusión es frágil. "
                            "Con 15 o 16 ramas los errores estándar son poco confiables.",
        )
        nota("Si las estimaciones dan positivas, no significa que importar cree empleo: una rama que crece necesita importar más "
             "insumos, repuestos y maquinaria, así que importaciones y empleo suben juntos. Para aislar la competencia de productos terminados haría falta "
             "separar importaciones por uso económico (bienes de consumo vs. insumos vs. bienes de capital), que no está en estos archivos.",
             titulo="Ojo con el signo positivo.")
        with st.expander("Ver todas las estimaciones (24 especificaciones)"):
            tabla = regs[["resultado", "importaciones", "muestra", "rezago_anios", "elasticidad", "p_valor", "efecto_10pct", "puestos_por_10pct", "n_obs", "n_ramas"]]
            tabla = tabla.rename(columns={"rezago_anios": "Rezago (años)", "elasticidad": "Elasticidad", "p_valor": "p-valor",
                                          "efecto_10pct": "Efecto de +10% (%)", "puestos_por_10pct": "Puestos por +10%", "n_obs": "Observaciones", "n_ramas": "Ramas"})
            st.dataframe(tabla, width="stretch", hide_index=True)


# -------------------------------------------------------------------------------------- síntesis
def _sintesis(r, g, c, s):
    mas, menos, tot = g.loc[MAS], g.loc[MENOS], g.loc["Total industria"]
    pr, tx = r.set_index("rama").loc[PRENDAS], r.set_index("rama").loc[TEXTILES]
    pond = s[s.tipo == "ponderada"].set_index("detalle")
    corr = leer("correlaciones.csv")
    china = corr[corr.exposicion.str.contains("China") & (corr.p_corregido < 0.05)]
    regs = leer("regresiones_panel.csv")
    todas = regs[regs.muestra == "Todas las ramas"]
    al_reves = mas.puestos > menos.puestos
    u = leer("respuesta_uso_correlaciones.csv")
    uins = u[(u.exposicion_col == "insumos_usd") & (u.resultado_col == "empleo")].iloc[0]
    ucons = u[(u.exposicion_col == "consumo_usd") & (u.resultado_col == "empleo")].iloc[0]
    sintesis([
        f"**La respuesta es {'no' if al_reves else 'sí, en empleo'}.** Entre 2018 y 2025, las 8 ramas donde más crecieron las importaciones {'sumaron' if mas.puestos > 0 else 'perdieron'} "
        f"{fmt_miles(abs(mas.puestos))} puestos ({fmt_pct(mas.empleo)}) y las 8 donde menos crecieron {'sumaron' if menos.puestos > 0 else 'perdieron'} {fmt_miles(abs(menos.puestos))} ({fmt_pct(menos.empleo)}). "
        f"En producción, la mediana fue {fmt_pct(mas.produccion)} contra {fmt_pct(menos.produccion)}.",
        f"**Lo que sí se perdió:** el total de la industria produjo {fmt_pct(tot.produccion)} y pagó salarios reales {fmt_pct(tot.salario)} (2025 contra 2018), en las dos mitades. "
        f"El empleo anual quedó en {fmt_pct(tot.empleo)}: su caída empieza después del máximo de 2023.",
        f"**Por qué «al revés»:** lo que más creció en las ramas que ganaron empleo fueron los insumos (ρ = {fmt_num(uins.rho, 2)} con el empleo). "
        f"Con los bienes de consumo, que son los que compiten, no hay relación con el empleo (ρ = {fmt_num(ucons.rho, 2)}).",
        f"**La excepción:** {nombre(PRENDAS)} (importaciones {fmt_pct(pr.imp_usd)} en dólares y {fmt_pct(pr.imp_ton)} en toneladas; {fmt_miles(pr.puestos)} puestos) y, mirando toneladas, "
        f"{nombre(TEXTILES)} ({fmt_pct(tx.imp_ton)} en toneladas; {fmt_miles(tx.puestos)} puestos). Son bienes de consumo: donde las importaciones compiten con lo que se produce.",
        f"**Qué tan firme es:** es una coincidencia medida, no un efecto. De las 9 pruebas de la respuesta, {_resisten(int((c.p_corregido < 0.05).sum()))} a la corrección por comparaciones múltiples; "
        f"la relación positiva ponderada depende de {nombre(ALIMENTOS)} (sin ella, p {fmt_p(pond.loc['sin Alimentos y bebidas', 'p_valor'])}), y la tendencia previa de cada rama explica más que las importaciones.",
        f"**Complementos:** de las 24 correlaciones del análisis original, {int((corr.p_corregido < 0.05).sum())} resiste la corrección"
        + (f": «{china.iloc[0].exposicion}» con «{china.iloc[0].resultado}», base {china.iloc[0].ventana}" if len(china) else "")
        + f". El modelo de panel con todas las ramas da {_significativas(int((todas.p_valor < 0.05).sum()), len(todas))}, con signo positivo: refleja que las ramas que crecen importan más insumos.",
        "**Para ir más allá:** pasar de «coincide» a «provoca» necesita otra fuente de variación (por ejemplo, lo que China le vende a otros países parecidos) "
        "y más detalle que 16 ramas. Ver «Método y límites».",
    ])


def mostrar():
    r, g, c, s = _respuesta()
    opc_expo, opc_res = _opciones()
    _introduccion()
    _tarjetas(r, g)
    _respuesta_dispersion(r, c)
    _respuesta_barras(r)
    _respuesta_grupos(r, g)
    _robustez_medidas(c)
    _robustez_sensibilidad(r, s, c)
    _uso_economico(r)
    _consumo_dispersion(r)
    _exploracion_intro()
    ventana, expo_col, res_col = _filtros(opc_expo, opc_res)
    _dispersion(ventana, expo_col, res_col, opc_expo, opc_res)
    _mapa_correlaciones(ventana, opc_expo, opc_res)
    _grupos(ventana, expo_col, opc_expo)
    _panel()
    _sintesis(r, g, c, s)
