"""Página «Comparador de ramas»: una rama de punta a punta contra el total de la industria."""
import pandas as pd
import streamlit as st

from core.consultas import cambio, empleo_trimestre
from core.datos import RAMA_A_UCI, RAMAS, TOTAL, UCI_APROXIMADO, leer, nombre
from core.formato import fmt_mes, fmt_miles, fmt_num, fmt_pct
from core.graficos import lineas, marca_vertical
from core.tema import AMARILLO, AQUA, AZUL, GRIS, MAGENTA, NARANJA, VERDE, VIOLETA
from core.ui import bloque, figura, nota, sintesis

DIC_2023 = pd.Timestamp("2023-12-01")


def _introduccion():
    st.markdown(
        """
Elegí una rama y mirala de punta a punta: su empleo, salario real y producción **contra el total de la industria**, más lo que pasó con sus importaciones,
su capacidad instalada y sus empresas. Sirve para ver si lo que le ocurrió a una rama es propio de ella o es parte de un movimiento general.

Las series de empleo, salario y producción son promedios móviles de 12 meses (4 trimestres en empleo) con **promedio de 2023 = 100**. Las comparaciones con
importaciones y empresas usan índices con **2018 = 100**. La línea vertical punteada marca diciembre de 2023.
"""
    )


def _indicadores(sel):
    q = empleo_trimestre(sel, "2023")
    ipi23, ipi18 = cambio(sel, "Producción (IPI)", "2023"), cambio(sel, "Producción (IPI)", "2018")
    sal23, sal18 = cambio(sel, "Salario real", "2023"), cambio(sel, "Salario real", "2018")
    c = leer("comercio_por_rama_anio.csv")
    c_ult = c[(c.rama == sel) & (c.anio == c.anio.max())].iloc[0]
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Puestos de trabajo", fmt_miles(q.ultimo), f"{fmt_miles(q.delta_abs)} vs {q.trimestre_base} ({fmt_pct(q.delta_pct)})", border=True)
    k2.metric("Producción vs 2023", fmt_pct(ipi23.delta_pct), f"vs 2018: {fmt_pct(ipi18.delta_pct)}", delta_color="off", border=True)
    k3.metric("Salario real vs 2023", fmt_pct(sal23.delta_pct), f"vs 2018: {fmt_pct(sal18.delta_pct)}", delta_color="off", border=True)
    k4.metric(f"Importaciones {int(c_ult.anio)} (USD M)", fmt_miles(c_ult.imp_cif / 1e6), f"{fmt_num(c_ult.pct_china, 0)}% desde China", delta_color="off", border=True)


def _frente_a_la_pregunta(sel):
    """La rama elegida frente a la pregunta central: cuánto crecieron sus importaciones 2018 -> 2025 y qué pasó con su empleo."""
    r = leer("respuesta_por_rama.csv").set_index("rama")
    x = r.loc[sel]
    puesto = int(r.imp_usd.rank(ascending=False).loc[sel])
    st.markdown('<div class="etiqueta">Frente a la pregunta central · 2018 → 2025 (promedios anuales)</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Importaciones de la rama (USD)", fmt_pct(x.imp_usd), f"puesto {puesto} de {len(r)} por crecimiento", delta_color="off", delta_arrow="off", border=True,
              help="Crecimiento del valor importado por la rama entre 2018 y 2025. El puesto ordena las 16 ramas de mayor a menor crecimiento.")
    k2.metric("Bienes de consumo importados", fmt_pct(x.consumo_usd) if pd.notna(x.consumo_usd) else "no importa",
              "lo que compite con la rama", delta_color="off", delta_arrow="off", border=True,
              help="Crecimiento de las importaciones de bienes de consumo (clasificación BEC) de la rama: los que compiten con lo que vende.")
    k3.metric("Empleo de la rama", fmt_pct(x.empleo), f"{fmt_miles(x.puestos)} puestos", border=True)
    k4.metric("Grupo", "Crecieron más" if x.grupo == "Importaciones crecieron más" else "Crecieron menos",
              "ver Importaciones vs. resultados", delta_color="off", delta_arrow="off", border=True,
              help="Las 16 ramas partidas al medio por el crecimiento de sus importaciones en dólares. Ver «Importaciones vs. resultados».")


def _cruce(sel):
    panel = leer("panel_rama_anio.csv")
    p = panel[panel.rama == sel].sort_values("anio")
    b = p[p.anio == 2018].iloc[0]
    partes = [("Importaciones (toneladas)", p.imp_kg / b.imp_kg * 100), ("Empleo", p.puestos / b.puestos * 100), ("Producción (IPI)", p.ipi / b.ipi * 100)]
    if b.salario_real == b.salario_real:
        partes.append(("Salario real", p.salario_real / b.salario_real * 100))
    cruce = pd.concat([pd.DataFrame({"anio": p.anio, "serie": n, "v": v}) for n, v in partes]).dropna()
    ult = cruce[cruce.anio == cruce.anio.max()].set_index("serie").v
    imp, prod, emp = ult["Importaciones (toneladas)"], ult["Producción (IPI)"], ult["Empleo"]
    if imp > 100 and prod < 100:
        patron = "las importaciones suben mientras la producción cae: es compatible con que la producción local esté siendo reemplazada por producto importado, aunque estos datos no lo prueban"
    elif imp <= 100 and prod < 100:
        patron = "las importaciones y la producción caen juntas: la caída parece más ligada a la actividad interna que a una mayor competencia importada"
    elif imp > 100:
        patron = "las importaciones y la producción crecen juntas: las compras al exterior acompañan a la actividad (insumos, maquinaria) más que reemplazarla"
    else:
        patron = "la producción se sostiene mientras las importaciones bajan"
    texto_sal = f", el salario real {fmt_num(ult['Salario real'], 0)}" if "Salario real" in ult else ""

    with bloque("1. Importaciones, producción, empleo y salario de la rama"):
        fig = lineas(cruce, "anio", "v", "serie",
                     {"Importaciones (toneladas)": VIOLETA, "Empleo": AZUL, "Producción (IPI)": NARANJA, "Salario real": AQUA},
                     y_titulo="Índice (2018 = 100)", base100=True, alto=300, formato="%{y:.0f}")
        fig.update_xaxes(type="category")
        figura(
            fig,
            que=f"Para «{nombre(sel)}», cuatro variables anuales en un mismo gráfico: importaciones en toneladas, empleo, producción (IPI) y salario real, todas con promedio de 2018 = 100.",
            como="Todas parten de 100 en 2018; por encima es más que ese año y por debajo, menos. Mirar las líneas en conjunto permite distinguir dos historias: si las importaciones (violeta) "
                 "suben mientras producción y empleo bajan, es el patrón típico de una rama que pierde mercado interno; si todas suben o bajan juntas, las importaciones siguen a la actividad.",
            observa=f"En {int(cruce.anio.max())}, las importaciones están en {fmt_num(imp, 0)}, la producción en {fmt_num(prod, 0)}, el empleo en {fmt_num(emp, 0)}{texto_sal}. En esta rama, {patron}.",
            tener_en_cuenta="Los salarios reales solo existen desde 2017 (el IPC nacional continuo empieza en dic-2016). Los promedios anuales alisan lo ocurrido dentro del año.",
        )
    return f"Con 2018 = 100, las importaciones (toneladas) están en {fmt_num(imp, 0)} y la producción en {fmt_num(prod, 0)}: {patron}."


def _panel_rama_total(sel, label, colores, metrica, titulo, que, como, tener):
    series = leer("series_indexadas.csv", ("periodo",))
    d = series[(series.metrica == metrica) & (series.periodo >= "2017-01-01")]
    d = pd.concat([d[d.rama == sel].assign(serie=label), d[d.rama == TOTAL].assign(serie="Total industria")])
    r, t = d[d.serie == label].sort_values("periodo"), d[d.serie == "Total industria"].sort_values("periodo")
    r_ult, t_ult = r.iloc[-1], t.iloc[-1]
    r_min = r.loc[r.indice.idxmin()]
    brecha = r_ult.indice - t_ult.indice
    lectura = ("por debajo del total" if brecha < -1 else "por encima del total" if brecha > 1 else "en línea con el total")

    with bloque(titulo):
        fig = lineas(d, "periodo", "indice", "serie", colores, y_titulo="Índice (promedio 2023 = 100)", base100=True, alto=290,
                     formato="%{y:.1f}", orden=[label, "Total industria"])
        marca_vertical(fig, DIC_2023, "dic-2023")
        figura(
            fig, que=que, como=como,
            observa=f"Al último dato ({fmt_mes(r_ult.periodo)}), la rama está en {fmt_num(r_ult.indice)} y el total de la industria en {fmt_num(t_ult.indice)}: {lectura} "
                    f"({fmt_num(abs(brecha))} puntos de diferencia). El punto más bajo de la rama desde 2017 fue {fmt_num(r_min.indice)} en {fmt_mes(r_min.periodo)}.",
            tener_en_cuenta=tener,
        )
    return r_ult.indice, t_ult.indice, lectura


def _capacidad(sel, label, colores):
    grupo_uci = RAMA_A_UCI.get(sel)
    with bloque("5. Capacidad instalada utilizada"):
        if not grupo_uci:
            nota("INDEC no publica un bloque de capacidad instalada comparable para esta rama.", color="blue")
            return
        uci = leer("capacidad_instalada.csv", ("periodo",))
        u = uci[uci.bloque.isin([grupo_uci, "Nivel general"])].copy()
        u["serie"] = u.bloque.map(lambda x: label if x == grupo_uci else "Total industria")
        u = u[u.periodo >= "2017-01-01"]
        r, t = u[u.serie == label].sort_values("periodo"), u[u.serie == "Total industria"].sort_values("periodo")
        r_ult, t_ult, r_min = r.iloc[-1], t.iloc[-1], r.loc[r.uci.idxmin()]
        fig = lineas(u, "periodo", "uci", "serie", colores, y_titulo="% de la capacidad", alto=290, formato="%{y:.1f}%", orden=[label, "Total industria"])
        marca_vertical(fig, DIC_2023, "dic-2023")
        aprox = f" Como el bloque de INDEC agrupa varias ramas, la comparación es aproximada para {label.lower()}." if sel in UCI_APROXIMADO else ""
        figura(
            fig,
            que=f"El porcentaje de la capacidad instalada que la industria utiliza, para el bloque «{grupo_uci}» de INDEC y para el total de la industria.",
            como="Mide cuánta de la planta y el equipamiento disponibles se usa. Un valor bajo y en caída indica planta ociosa: las empresas producen menos de lo que podrían, "
                 "situación que suele asociarse con poca inversión y, si se prolonga, con cierres o despidos. Un valor alto indica que hay poco margen para producir más sin ampliar la capacidad.",
            observa=f"Al último dato ({fmt_mes(r_ult.periodo)}), el bloque usa {fmt_num(r_ult.uci)}% de su capacidad contra {fmt_num(t_ult.uci)}% del total industrial "
                    f"({fmt_num(r_ult.uci - t_ult.uci)} puntos de diferencia). El valor más bajo desde 2017 fue {fmt_num(r_min.uci)}% en {fmt_mes(r_min.periodo)}.",
            tener_en_cuenta="Es un porcentaje y no un índice: los niveles entre bloques no son comparables por sí solos (cada industria tiene un uso «normal» distinto); importa la trayectoria." + aprox,
        )


def _empresas(sel, label, colores):
    empresas = leer("empresas_por_rama.csv", ("periodo",))
    e = empresas[empresas.periodo >= "2015-01-01"].assign(anio=lambda x: x.periodo.dt.year)
    e = pd.concat([e[e.rama == sel].assign(serie=label), e[e.rama == TOTAL].assign(serie="Total industria")])
    base = e[e.anio == 2018].set_index("serie").empresas
    e["v"] = e.empresas / e.serie.map(base) * 100
    r, t = e[e.serie == label].sort_values("anio"), e[e.serie == "Total industria"].sort_values("anio")
    r_ult, t_ult = r.iloc[-1], t.iloc[-1]

    with bloque("6. Empresas activas"):
        fig = lineas(e, "anio", "v", "serie", colores, y_titulo="Índice (2018 = 100)", base100=True, alto=290, formato="%{y:.1f}", orden=[label, "Total industria"])
        fig.update_xaxes(type="category")
        figura(
            fig,
            que="La cantidad de empresas privadas con al menos un empleado registrado, en la rama y en toda la industria, por año, con 2018 = 100.",
            como="Una caída significa cierres netos: empresas que dejan de tener empleados registrados (cierran, se achican a cero o pasan a la informalidad) sin ser reemplazadas por otras nuevas. "
                 "Es distinto de perder puestos en empresas que siguen funcionando, que se ve en el gráfico de empleo.",
            observa=f"En {int(r_ult.anio)}, la rama tiene {fmt_miles(r_ult.empresas)} empresas, un índice de {fmt_num(r_ult.v)} contra {fmt_num(t_ult.v)} del total industrial. "
                    f"{'La rama perdió más empresas que la industria.' if r_ult.v < t_ult.v - 1 else 'La rama perdió menos empresas que la industria (o ganó).' if r_ult.v > t_ult.v + 1 else 'La rama evolucionó igual que la industria.'}",
            tener_en_cuenta="Llega hasta el último año publicado (2024). Es un conteo: no distingue entre empresas grandes y chicas.",
        )


def _subramas(sel):
    nombres = leer("ipi_subramas_nombres.csv")
    hijas = nombres[nombres.rama_padre == sel]
    if not len(hijas):
        return
    idx = leer("ipi_subramas_indexadas.csv", ("periodo",))
    colores = dict(zip(hijas.nombre, [AZUL, NARANJA, AQUA, AMARILLO, MAGENTA, VERDE, VIOLETA, GRIS]))
    s = idx.merge(hijas[["codigo", "nombre"]], on="codigo")
    s = s[s.periodo >= "2017-01-01"]
    top = list(hijas.nombre)[:8]
    s = s[s.nombre.isin(top)]
    ult = s.sort_values("periodo").groupby("nombre").indice.last().sort_values()

    with bloque("7. Detalle de producción por producto"):
        fig = lineas(s, "periodo", "indice", "nombre", colores, y_titulo="Índice (promedio 2023 = 100)", base100=True, alto=300, formato="%{y:.1f}", orden=top)
        marca_vertical(fig, DIC_2023, "dic-2023")
        figura(
            fig,
            que="La producción (IPI) de los subsectores que componen la rama, cada uno como promedio móvil de 12 meses con promedio de 2023 = 100.",
            como="Permite ver si la caída (o suba) de la rama es pareja o se concentra en algunos productos. Cada color es un subsector; el orden de las líneas al final del período "
                 "muestra cuáles están mejor y cuáles peor que en 2023.",
            observa=f"Al último dato, el subsector más rezagado es {ult.index[0]} ({fmt_num(ult.iloc[0])}) y el que mejor está es {ult.index[-1]} ({fmt_num(ult.iloc[-1])}). "
                    f"{'La diferencia entre ambos muestra que la evolución de la rama no es pareja.' if ult.iloc[-1] - ult.iloc[0] > 15 else 'Los subsectores se mueven de manera parecida.'}",
            tener_en_cuenta="Son series de producción física, sin precios. Algunos subsectores son muy chicos y más volátiles.",
        )


def mostrar():
    _introduccion()
    sel = st.selectbox("Rama", RAMAS, index=RAMAS.index("18-19"), format_func=nombre, key="cmp_rama")
    label = nombre(sel)
    colores = {label: AZUL, "Total industria": NARANJA}
    _indicadores(sel)
    _frente_a_la_pregunta(sel)
    concl = [_cruce(sel)]

    r_e, t_e, lect_e = _panel_rama_total(
        sel, label, colores, "Empleo", "2. Empleo: la rama contra el total de la industria",
        que=f"El empleo asalariado privado registrado de «{label}» y de toda la industria manufacturera, con promedio de 2023 = 100.",
        como="Si la línea azul (la rama) queda por debajo de la naranja (el total), la rama perdió empleo más rápido, o creció menos, que la industria en su conjunto; si queda por encima, "
             "le fue mejor. La línea vertical marca el fin de 2023: ahí el promedio móvil abarca justo el año base y ambas series valen 100.",
        tener="Es empleo registrado: no incluye informalidad ni cuentapropistas. Trimestral, por eso la línea tiene menos puntos.")
    r_p, t_p, lect_p = _panel_rama_total(
        sel, label, colores, "Producción (IPI)", "3. Producción: la rama contra el total de la industria",
        que=f"El volumen físico producido por «{label}» (índice de producción industrial de INDEC) y por toda la industria, con promedio de 2023 = 100.",
        como="Es producción en cantidades, no en dinero. Si cae más que el empleo, la rama produce menos por persona ocupada; si el empleo cae más que la producción, produce lo mismo con menos gente.",
        tener="Como todo IPI, no incluye precios ni servicios asociados a la industria.")
    r_s, t_s, lect_s = _panel_rama_total(
        sel, label, colores, "Salario real", "4. Salario real: la rama contra el total de la industria",
        que=f"La remuneración registrada por puesto de «{label}» y de toda la industria, deflactada por el IPC y ponderada por puestos de trabajo, con promedio de 2023 = 100.",
        como="Muestra si el poder de compra de los salarios de la rama evolucionó mejor o peor que el del total. Interesa la trayectoria: las diferencias de nivel entre ramas existen "
             "desde antes y no aparecen acá, porque cada serie está indexada a su propio promedio de 2023.",
        tener="Incluye aguinaldo (junio y diciembre): por eso se usan promedios de 12 meses. Son salarios registrados; no reflejan la informalidad.")
    _capacidad(sel, label, colores)
    _empresas(sel, label, colores)
    _subramas(sel)

    concl += [f"El empleo de la rama está {lect_e} ({fmt_num(r_e)} contra {fmt_num(t_e)}, con 2023 = 100).",
              f"La producción de la rama está {lect_p} ({fmt_num(r_p)} contra {fmt_num(t_p)}).",
              f"El salario real de la rama está {lect_s} ({fmt_num(r_s)} contra {fmt_num(t_s)})."]
    sintesis(concl, titulo=f"Síntesis: {label}")
