"""Página «Empleo y ramas»: qué pasó con empleo, salario real, producción y empresas en cada rama industrial."""
import numpy as np
import pandas as pd
import streamlit as st

from core.consultas import cambio_total, empleo_trimestre, evolucion_por_anio, panorama_ultimo_anio, trimestre_texto
from core.datos import TOTAL, leer, nombre
from core.formato import MESES, fmt_miles, fmt_num, fmt_pct, fmt_signed
from core.graficos import barras_signo, dispersion, heatmap
from core.tema import ESCALA_RESULTADO, GRIS
from core.ui import bloque, figura, sintesis


def _introduccion():
    st.markdown(
        """
Esta página muestra qué pasó con el **empleo registrado privado**, el **salario real**, la **producción** y la **cantidad de empresas** en cada una de
las 16 ramas industriales, y cuánto de eso se debe a un movimiento general de la industria o a cambios propios de cada rama.

Las secciones 1 y 3 comparan el **promedio de un año base** con el promedio de los **últimos 12 meses disponibles** (4 trimestres en el caso del empleo): así se evitan
distorsiones por estacionalidad y por el aguinaldo. Podés elegir contra qué año comparar: **2018**, el año previo a la pandemia (muestra qué cambió en el largo plazo),
o **2023**, el último año antes de que la industria empezara a caer (muestra lo que pasó últimamente). Las secciones 2 y 4 aclaran en su propio texto con qué período comparan.
"""
    )


def _ventana():
    return st.segmented_control("Comparar contra el promedio de", ["2018", "2023"], default="2023", key="emp_ventana") or "2023"


def _indicadores(ventana):
    q = empleo_trimestre(TOTAL, ventana)
    e, s = cambio_total("Empleo", ventana), cambio_total("Salario real", ventana)
    i, em = cambio_total("Producción (IPI)", ventana), cambio_total("Empresas", ventana)
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Empleo, prom. 4 trim. (puestos)", fmt_miles(e.delta_abs), fmt_pct(e.delta_pct), border=True)
    k2.metric(f"{q.trimestre_ultimo} vs {q.trimestre_base} (puestos)", fmt_miles(q.delta_abs), fmt_pct(q.delta_pct), border=True)
    k3.metric("Salario real", fmt_pct(s.delta_pct), f"hasta {s.fin}", delta_color="off", border=True)
    k4.metric("Producción (IPI)", fmt_pct(i.delta_pct), f"hasta {i.fin}", delta_color="off", border=True)
    k5.metric("Empresas activas", fmt_miles(em.delta_abs), f"{fmt_pct(em.delta_pct)} (hasta {em.fin})", border=True)
    st.caption(
        "Los cuatro indicadores son variaciones de toda la industria manufacturera. El segundo cuadro compara el mismo trimestre de ambos años, lo que "
        "elimina la estacionalidad del empleo; el primero usa promedios de 4 trimestres, que es la medida que usan los gráficos de abajo."
    )


def _mapa_calor(c, ventana):
    ancho = c[c.rama != TOTAL].pivot(index="rama", columns="metrica", values="delta_pct")
    ancho = ancho[["Empleo", "Producción (IPI)", "Salario real", "Empresas"]].sort_values("Empleo")
    n = {m: int((ancho[m] < 0).sum()) for m in ancho.columns}
    cuatro = [nombre(r) for r in ancho.index[(ancho < 0).all(axis=1)]]
    ipi = ancho["Producción (IPI)"]
    peor_ipi, mejor_ipi = nombre(ipi.idxmin()), nombre(ipi.idxmax())
    rango_ipi = (ipi.min(), ipi.max())
    ancho.index = [nombre(r) for r in ancho.index]

    with bloque("1. Mapa de calor: qué rama cambió cuánto"):
        fig = heatmap(ancho, escala=ESCALA_RESULTADO, rango=30, sufijo="%", decimales=1, colorbar_titulo="Δ%", alto=470)
        figura(
            fig,
            que=f"La variación porcentual de cuatro indicadores (empleo, producción, salario real y empresas activas) en cada una de las 16 ramas, comparando el promedio de "
                f"los últimos 12 meses con el promedio de {ventana}.",
            como="Naranja: el indicador empeoró; azul: mejoró; gris: casi no cambió. El color se satura en ±30% para que los extremos no oculten los cambios chicos, pero el "
                 "número de cada celda es el dato real. Las filas están ordenadas de la rama que más empleo perdió a la que más ganó. Una fila naranja de punta a punta es una "
                 "rama que empeora en todo; una fila con colores mezclados muestra que los indicadores no siempre se mueven juntos.",
            observa=f"Con base {ventana}, {n['Empleo']} de las 16 ramas perdieron empleo, {n['Producción (IPI)']} redujeron su producción, {n['Salario real']} tienen un salario real menor y "
                    f"{n['Empresas']} tienen menos empresas. " + (f"Caen en los cuatro indicadores a la vez: {', '.join(cuatro)}. " if cuatro else "Ninguna rama cae en los cuatro indicadores a la vez. ")
                    + f"La producción es el indicador con mayor dispersión: de {fmt_pct(rango_ipi[0])} en {peor_ipi} a {fmt_pct(rango_ipi[1])} en {mejor_ipi}.",
            tener_en_cuenta="Las ramas chicas (tabaco, otro equipo de transporte) tienen variaciones porcentuales más erráticas que las grandes; conviene mirar también el gráfico siguiente, "
                            "que muestra puestos absolutos.",
        )
    return (f"Con base {ventana}, {n['Empleo']} de 16 ramas perdieron empleo y {n['Producción (IPI)']} redujeron su producción; "
            + (f"caen en los cuatro indicadores: {', '.join(cuatro)}." if cuatro else "ninguna cae en los cuatro indicadores a la vez."))


def _puestos():
    e = leer("empleo_por_rama.csv", ("periodo",)).pivot(index="rama", columns="periodo", values="puestos")
    ult = e.columns.max()
    opciones = {trimestre_texto(ult - pd.DateOffset(years=k)): k for k in (1, 3, 8)}

    with bloque("2. Cuántos puestos de trabajo ganó o perdió cada rama"):
        elegido = st.segmented_control(f"Comparar el {trimestre_texto(ult)} contra el mismo trimestre de", list(opciones), default=list(opciones)[1], key="emp_puestos") or list(opciones)[1]
        base = ult - pd.DateOffset(years=opciones[elegido])
        d = (e[ult] - e[base]).drop(TOTAL)
        emp = pd.DataFrame({"delta_abs": d, "etiqueta": [nombre(r) for r in d.index]})
        perd, gan = d[d < 0].sum(), d[d > 0].sum()
        pierden, ganan = emp[emp.delta_abs < 0].sort_values("delta_abs"), emp[emp.delta_abs > 0].sort_values("delta_abs", ascending=False)
        top3 = pierden.delta_abs.head(3).sum() / perd * 100 if perd else 0
        tu, tb = trimestre_texto(ult), elegido

        fig = barras_signo(emp, "delta_abs", "etiqueta", x_titulo="Puestos de trabajo", formato="{:+,.0f}", alto=340)
        figura(
            fig,
            que=f"La variación de puestos de trabajo registrados de cada rama entre el {tb} y el {tu}.",
            como="Azul es que la rama sumó puestos y naranja que los perdió; la longitud de la barra es la cantidad. Se comparan trimestres iguales (1T contra 1T, por ejemplo) para que la estacionalidad "
                 "no distorsione. A diferencia del mapa de calor, acá una rama grande pesa más que una chica: sirve para ver dónde están realmente los puestos.",
            observa=f"Entre el {tb} y el {tu}, {len(pierden)} de 16 ramas perdieron empleo (en total {fmt_miles(-perd)} puestos menos) y {len(ganan)} {'ganó' if len(ganan) == 1 else 'ganaron'} ({fmt_miles(gan)} más). "
                    f"El resultado neto de la industria es {fmt_signed(perd + gan)} puestos. " + (f"Las tres que más perdieron ({', '.join(pierden.etiqueta.head(3))}) concentran {fmt_num(top3, 0)}% de los puestos perdidos. " if len(pierden) >= 3 else "")
                    + (f"Las que más ganaron son {', '.join(ganan.etiqueta.head(2))} ({fmt_miles(ganan.delta_abs.iloc[0])} y {fmt_miles(ganan.delta_abs.iloc[1])} puestos)." if len(ganan) >= 2 else ""),
            tener_en_cuenta="El resultado depende del trimestre de partida: la industria tuvo su nivel más alto reciente entre 2023 y principios de 2024, por eso comparar con 2023 muestra la caída actual y comparar con 2018 muestra el saldo "
                            "de varios años. Estos datos no permiten saber si los puestos que se crean en una rama son para las mismas personas ni si están en las mismas regiones.",
        )
    return f"Entre el {tb} y el {tu} la industria varió {fmt_signed(perd + gan)} puestos y las tres ramas que más perdieron concentran {fmt_num(top3, 0)}% de lo perdido."


def _produccion_vs_empleo(ventana):
    expo = leer("exposicion_vs_resultados.csv")
    e2 = expo[expo.ventana == ventana].assign(etiqueta=lambda x: x.rama.map(nombre))
    pendiente = np.polyfit(e2.d_ipi, e2.d_empleo, 1)[0]
    pierde_mas = e2[(e2.d_empleo < e2.d_ipi) & (e2.d_empleo < 0)]
    retiene = e2[(e2.d_ipi < -15) & (e2.d_empleo > -5)]

    with bloque("3. ¿Se perdió empleo donde cayó la producción?"):
        fig = dispersion(e2, "d_ipi", "d_empleo", "etiqueta", x_titulo="Δ% producción (IPI)", y_titulo="Δ% empleo", alto=340)
        lim = [min(e2.d_ipi.min(), e2.d_empleo.min()) - 2, max(e2.d_ipi.max(), e2.d_empleo.max()) + 2]
        fig.add_shape(type="line", x0=lim[0], y0=lim[0], x1=lim[1], y1=lim[1], line=dict(color=GRIS, dash="dot", width=1))
        fig.update_xaxes(range=[e2.d_ipi.min() - 4, e2.d_ipi.max() + 4])
        fig.update_yaxes(range=[e2.d_empleo.min() - 3, e2.d_empleo.max() + 3])
        figura(
            fig,
            que=f"Cada punto es una rama. El eje horizontal es el cambio porcentual de su producción y el vertical el cambio porcentual de su empleo, ambos contra el promedio de {ventana}.",
            como="La línea punteada diagonal marca «el empleo cambió igual que la producción». Un punto por encima: la producción cayó más que el empleo (la rama retuvo personal o "
                 "bajó su productividad). Un punto por debajo: el empleo cayó más que la producción (se produce lo mismo con menos gente). La recta discontinua es la tendencia "
                 "por mínimos cuadrados, una guía orientativa y no un modelo.",
            observa=f"La recta indica que, en promedio, por cada 10 puntos que cae la producción de una rama, su empleo varía {fmt_num(pendiente * 10)} puntos: "
                    + ("la producción se mueve más que el empleo. " if pendiente < 1 else "el empleo se mueve más que la producción. ")
                    + (f"Ramas donde el empleo cayó más que la producción: {', '.join(pierde_mas.etiqueta)}. " if len(pierde_mas) else "")
                    + (f"Ramas que redujeron su producción más de 15% pero perdieron menos de 5% de su empleo (retuvieron personal): {', '.join(retiene.etiqueta)}." if len(retiene) else ""),
            tener_en_cuenta="Son 16 puntos: la recta es sensible a una o dos ramas extremas. El empleo registrado solo cuenta trabajo asalariado privado formal.",
        )
    return f"Entre ramas, por cada 10 puntos que cae la producción el empleo varía en promedio {fmt_num(pendiente * 10)} puntos: la actividad se mueve más que el empleo." if pendiente < 1 else f"Entre ramas, por cada 10 puntos que cae la producción el empleo varía en promedio {fmt_num(pendiente * 10)} puntos."


def _ano_2026():
    t, m = panorama_ultimo_anio()
    anio, tot, r = m["anio"], t.loc[TOTAL], t.drop(TOTAL)
    mes_ipi, mes_sal = MESES[m["fin_ipi"].month - 1], MESES[m["fin_sal"].month - 1]
    pierden_emp = r.sort_values("empleo_abs").head(3)
    cae10, suben = r[r.produccion_pct < -10].sort_values("produccion_pct"), r[r.produccion_pct > 0].sort_values("produccion_pct", ascending=False)
    mat = r[["empleo_pct", "produccion_pct", "salario_pct"]].sort_values("empleo_pct").round(1) + 0.0  # + 0.0 evita mostrar «-0,0%»
    mat.columns = [f"Empleo<br>{m['trim_ult']} vs {m['trim_ant']}", f"Producción<br>ene-{mes_ipi} {anio} vs {anio - 1}", f"Salario real<br>ene-{mes_sal} {anio} vs {anio - 1}"]
    mat.index = [nombre(x) for x in mat.index]

    def nombres(d):
        return ", ".join(f"{nombre(x)} ({fmt_pct(v)})" for x, v in d.items())

    with bloque(f"4. Lo que va de {anio}, contra el mismo período de {anio - 1}"):
        fig = heatmap(mat, escala=ESCALA_RESULTADO, rango=20, sufijo="%", decimales=1, colorbar_titulo="Δ%", alto=470)
        figura(
            fig,
            que=f"Lo que va de {anio} contra el mismo período de {anio - 1}, rama por rama, en tres indicadores. El empleo compara el {m['trim_ult']} con el {m['trim_ant']}; la producción, el promedio de enero a "
                f"{mes_ipi} de ambos años; el salario real, el promedio de enero a {mes_sal}.",
            como="Naranja: el indicador empeoró; azul: mejoró. El color se satura en ±20%, pero el número de cada celda es el dato real. Se comparan períodos iguales de dos años seguidos para que la estacionalidad "
                 "y el aguinaldo no distorsionen. Las filas van de la rama que más empleo perdió a la que menos.",
            observa=f"En el total de la industria, el empleo varió {fmt_pct(tot.empleo_pct)} en un año ({fmt_miles(tot.empleo_abs)} puestos), la producción {fmt_pct(tot.produccion_pct)} y el salario real {fmt_pct(tot.salario_pct)}. "
                    f"{int((r.empleo_pct < 0).sum())} de 16 ramas perdieron empleo; las que más puestos perdieron son {", ".join(f"{nombre(x)} ({fmt_signed(v)})" for x, v in pierden_emp.empleo_abs.items())}. "
                    + (f"En producción caen más de 10%: {nombres(cae10.produccion_pct)}. " if len(cae10) else "")
                    + (f"Crecen: {nombres(suben.produccion_pct.head(4))}." if len(suben) else ""),
            tener_en_cuenta=f"Son pocos meses y datos recientes: el empleo llega al {m['trim_ult']} y el salario real a {mes_sal}-{m['fin_sal'].year}, y el Ministerio de Trabajo corrige los últimos trimestres cuando actualiza "
                            "la serie (con la última actualización se revisaron los trimestres de 2025). Las ramas chicas (tabaco, refinación de petróleo) tienen variaciones más erráticas.",
        )
    return (f"En lo que va de {anio}, el empleo cae {fmt_pct(tot.empleo_pct, False)} contra un año antes ({int((r.empleo_pct < 0).sum())} de 16 ramas pierden puestos) y la producción {fmt_pct(tot.produccion_pct)}.")


def _anio_por_anio():
    tablas, meta = evolucion_por_anio()
    anios = meta["anios"]
    ultimo = anios[-1]
    rango = {"Empleo": 12, "Producción": 20, "Salario real": 10}

    with bloque("5. Año por año: cada año contra el anterior"):
        ind = st.segmented_control("Indicador", list(tablas), default="Empleo", key="emp_anio") or "Empleo"
        fin = meta["fin"][ind]
        parcial = f"1T" if ind == "Empleo" else f"ene-{MESES[fin.month - 1]}"
        t = tablas[ind]
        tot, r = t.loc[TOTAL], t.drop(TOTAL)
        mat = r.sort_values(ultimo)
        mat.columns = [f"{y}<br>({parcial})" if y == ultimo else str(y) for y in mat.columns]
        mat.index = [nombre(x) for x in mat.index]
        peor, mejor = r[ultimo].idxmin(), r[ultimo].idxmax()
        n_neg = {y: int((r[y] < 0).sum()) for y in anios}

        fig = heatmap(mat, escala=ESCALA_RESULTADO, rango=rango[ind], sufijo="%", decimales=1, colorbar_titulo="Δ%", alto=470)
        figura(
            fig,
            que=f"Cómo cambió el {ind.lower()} de cada rama en {', '.join(str(a) for a in anios)}, cada año contra el anterior. {ultimo} es un año incompleto: se compara {parcial} de {ultimo} con el mismo período de {ultimo - 1}.",
            como="Naranja: el indicador empeoró respecto del año anterior; azul: mejoró. El color se satura en ±" + str(rango[ind]) + "%, pero el número de cada celda es el dato real. "
                 "Cada columna es un año: leyendo una fila de izquierda a derecha se ve cómo le fue a esa rama año tras año.",
            observa="En el total de la industria: " + "; ".join(f"{y}: {fmt_pct(tot[y])}" for y in anios) + ". "
                    + "Ramas que empeoran: " + ", ".join(f"{y}: {n} de 16" for y, n in n_neg.items()) + ". "
                    + f"En {ultimo}, la que más cae es {nombre(peor)} ({fmt_pct(r[ultimo][peor])}) y la que más mejora, {nombre(mejor)} ({fmt_pct(r[ultimo][mejor])}).",
            tener_en_cuenta=f"{ultimo} llega hasta {MESES[fin.month - 1]}-{fin.year}" + (" (primer trimestre)" if ind == "Empleo" else "") + ": las variaciones pueden cambiar cuando se publique el resto del año. "
                            "Los años completos comparan el promedio del año contra el del anterior.",
        )
    return f"Año por año, el {ind.lower()} del total varió " + ", ".join(f"{fmt_pct(tot[y])} en {y}" for y in anios) + "."


def _tabla(c, ventana):
    with st.expander("Ver y descargar la tabla completa"):
        tabla = (c[c.rama != TOTAL].assign(rama_nombre=lambda x: x.rama.map(nombre))
                 [["rama_nombre", "metrica", "base", "ultimo", "delta_abs", "delta_pct", "fin"]]
                 .rename(columns={"rama_nombre": "Rama", "metrica": "Indicador", "base": "Base (promedio año base)",
                                  "ultimo": "Último (12 meses)", "delta_abs": "Δ absoluto", "delta_pct": "Δ %", "fin": "Hasta"}))
        st.dataframe(tabla, width="stretch", hide_index=True)
        st.download_button("Descargar CSV", tabla.to_csv(index=False).encode("utf-8"), f"cambios_por_rama_base_{ventana}.csv", "text/csv")


def _cuando_cae() -> str:
    """Desde cuándo cae el empleo del total, con promedios anuales de años completos (lo que usa la pregunta central)."""
    e = leer("empleo_por_rama.csv", ("periodo",))
    e = e[e.rama == TOTAL].assign(anio=lambda x: x.periodo.dt.year)
    anual = e.groupby("anio").puestos.agg(["mean", "count"])
    anual = anual[anual["count"] == 4]["mean"]
    pico = int(anual.loc[2018:].idxmax())
    ult = int(anual.index.max())
    return (f"Con promedios anuales, el empleo industrial de {ult} está {fmt_pct((anual[ult] / anual[2018] - 1) * 100)} contra 2018; el máximo fue en {pico} y desde entonces varió "
            f"{fmt_pct((anual[ult] / anual[pico] - 1) * 100)}: la pérdida de empleo es de {pico + 1} en adelante. La pregunta central se responde en «Importaciones vs. resultados».")


def mostrar():
    cambios = leer("cambios_por_rama.csv")
    _introduccion()
    ventana = _ventana()
    c = cambios[cambios.ventana == ventana]
    _indicadores(ventana)
    conclusiones = [_mapa_calor(c, ventana), _puestos(), _produccion_vs_empleo(ventana), _ano_2026(), _anio_por_anio(), _cuando_cae()]
    _tabla(c, ventana)
    sintesis(conclusiones)
