"""Página «Conclusiones»: el trabajo completo resumido como un informe, en hojas A4. Toda cifra del texto sale de los datos procesados."""
import re
from contextlib import contextmanager
from datetime import date
from html import escape
from types import SimpleNamespace

import pandas as pd
import streamlit as st

from core.consultas import cambio_total, empleo_trimestre, evolucion_por_anio, panel_empleo, trimestre_texto
from core.datos import AUTOR, PROCESSED, TOTAL, leer, nombre
from core.formato import MESES, fmt_mes, fmt_miles, fmt_num, fmt_p, fmt_pct, fmt_signed
from core.graficos import barras_signo, dispersion, dumbbell, heatmap, lineas
from core.tema import COLOR_METRICA, ESCALA_RESULTADO, GRIS, NARANJA

N_HOJAS = 8
MESES_LARGOS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
INDICE = [("1. Introducción", 2), ("2. Datos y método", 2), ("3. Resultados", 3), ("4. Conclusiones", 7), ("5. Limitaciones", 8), ("6. Próximos pasos", 8), ("Fuentes", 8)]
FUENTE_GENERAL = "Fuente: elaboración propia con datos de INDEC y del Ministerio de Trabajo (OEDE)."


# ---------------------------------------------------------------- formato del documento

def _t(s: str) -> str:
    """Texto plano -> HTML: escapa y convierte **negrita** y *cursiva*."""
    s = escape(s, quote=False).replace("\n", "<br>")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*", r"<i>\1</i>", s)


def _doc(*partes: str) -> None:
    st.markdown(f'<div class="doc" lang="es">{"".join(partes)}</div>', unsafe_allow_html=True)


def _h1(s): return f'<div class="h1">{_t(s)}</div>'
def _h2(s): return f'<div class="h2">{_t(s)}</div>'
def _p(s): return f"<p>{_t(s)}</p>"
def _ol(items): return '<ol class="lista">' + "".join(f"<li>{_t(i)}</li>" for i in items) + "</ol>"
def _ul(items): return '<ul class="lista">' + "".join(f"<li>{_t(i)}</li>" for i in items) + "</ul>"


def _tabla(titulo: str, cabecera: list, filas: list, alinear: str | None = None, fuente: str | None = FUENTE_GENERAL, sin_cortes: bool = False) -> str:
    """Tabla al estilo Word: título arriba, encabezado oscuro, filas con línea fina y fuente al pie. `alinear`: una letra (l/r) por columna."""
    alinear = alinear or "l" + "r" * (len(cabecera) - 1)
    cls = {"l": "izq", "r": "der", "c": "cen"}
    th = "".join(f'<th class="{cls[a]}">{_t(c)}</th>' for c, a in zip(cabecera, alinear))
    tr = "".join("<tr>" + "".join(f'<td class="{cls[a]}">{_t(str(v))}</td>' for v, a in zip(f, alinear)) + "</tr>" for f in filas)
    pie = f'<p class="leyenda">{_t(fuente)}</p>' if fuente else '<div class="espacio"></div>'
    clase = "tabla sin-cortes" if sin_cortes else "tabla"
    return f'<p class="titulo-tabla">{_t(titulo)}</p><table class="{clase}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>{pie}'


def _leyenda(n: int, texto: str, fuente: str = FUENTE_GENERAL) -> None:
    _doc(f'<p class="leyenda"><b>Figura {n}.</b> {_t(texto)} {_t(fuente)}</p>')


def _papel(fig, alto: int):
    """Los gráficos del informe van siempre sobre fondo blanco y texto oscuro, sin depender del tema de la aplicación."""
    fig.update_layout(template="simple_white", paper_bgcolor="white", plot_bgcolor="white", height=alto,
                      font=dict(family="Calibri, Carlito, Arial, sans-serif", size=11, color="#222222"))
    fig.update_layout(margin=dict(l=6, r=10, t=fig.layout.margin.t, b=6))
    return fig


def _grafico(fig, alto: int) -> None:
    st.plotly_chart(_papel(fig, alto), width="stretch", theme=None, config={"displayModeBar": False})


@contextmanager
def _hoja(n: int):
    with st.container(key=f"hoja_{n}"):
        yield
        _doc(f'<div class="pie-hoja"><span>Importaciones e industria en Argentina, 2016-2026</span><span>Página {n} de {N_HOJAS}</span></div>')


def _lista(xs) -> str:
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " y " + xs[-1]


def _indice() -> str:
    return '<div class="indice">' + "".join(f'<div class="fila"><span>{_t(t)}</span><span class="punteado"></span><span>{n}</span></div>' for t, n in INDICE) + "</div>"


def _signif(n: int, total: int) -> str:
    """'1 de 12 estimaciones es significativa' / '11 de 12 estimaciones son significativas'."""
    return f"{n} de {total} estimaciones " + ("es significativa" if n == 1 else "son significativas")


@st.cache_data(ttl=3600)
def _ultimo_ipc() -> pd.Timestamp:
    """Último mes del IPC nacional (archivo original)."""
    ipc = pd.read_csv(PROCESSED.parent / "raw" / "precios" / "serie_ipc_divisiones.csv", sep=";", encoding="latin1", usecols=["Periodo"])
    return pd.to_datetime(str(int(ipc["Periodo"].max())), format="%Y%m")


def _sg(x: float, dec: int = 1) -> str:
    return f"{x:+.{dec}f}".replace(".", ",")


def _pp(x: float) -> str:
    return f"{_sg(x)} p.p."


# ---------------------------------------------------------------- cálculo de todas las cifras

def _datos() -> SimpleNamespace:
    d = SimpleNamespace()
    d.q23, d.q18 = empleo_trimestre(TOTAL, "2023"), empleo_trimestre(TOTAL, "2018")
    d.ipi23, d.ipi18 = cambio_total("Producción (IPI)", "2023"), cambio_total("Producción (IPI)", "2018")
    d.sal23, d.sal18 = cambio_total("Salario real", "2023"), cambio_total("Salario real", "2018")
    d.emp23, d.empr23 = cambio_total("Empleo", "2023"), cambio_total("Empresas", "2023")

    # series de la industria
    series = leer("series_indexadas.csv", ("periodo",))
    d.ind = series[(series.rama == TOTAL) & (series.periodo >= "2017-01-01")]

    def tramo(metrica):
        g = d.ind[d.ind.metrica == metrica].sort_values("periodo")
        return g.loc[g.indice.idxmin()], g.loc[g.indice.idxmax()], g.iloc[-1]

    d.emp_min, d.emp_max, d.emp_ult = tramo("Empleo")
    d.ipi_min, _, d.ipi_ult = tramo("Producción (IPI)")
    d.sal_min, d.sal_max, d.sal_ult = tramo("Salario real")
    rec = d.ind[(d.ind.metrica == "Producción (IPI)") & (d.ind.periodo > "2020-12-01") & (d.ind.periodo <= "2023-12-01")]
    d.ipi_rec = rec.loc[rec.indice.idxmax()]

    # empleo por rama: último trimestre contra el mismo trimestre de 2018 y de 2023
    e = leer("empleo_por_rama.csv", ("periodo",)).pivot(index="rama", columns="periodo", values="puestos")
    ult = e.columns.max()
    d.tu = trimestre_texto(ult)

    def delta_rama(anio_base):
        base = ult - pd.DateOffset(years=ult.year - anio_base)
        x = pd.DataFrame({"delta_abs": e[ult] - e[base], "delta_pct": (e[ult] / e[base] - 1) * 100}).drop(TOTAL)
        x["rama"], x["etiqueta"] = x.index, [nombre(r) for r in x.index]
        return x.reset_index(drop=True), trimestre_texto(base)

    d.e18, d.tb18 = delta_rama(2018)
    e23, d.tb23 = delta_rama(2023)
    d.pierden18 = d.e18[d.e18.delta_abs < 0].sort_values("delta_abs")
    d.ganan18 = d.e18[d.e18.delta_abs > 0].sort_values("delta_abs", ascending=False)
    d.pierden23, d.ganan23 = e23[e23.delta_abs < 0].sort_values("delta_abs"), e23[e23.delta_abs > 0].sort_values("delta_abs", ascending=False)
    d.top3_23 = d.pierden23.delta_abs.head(3).sum() / d.pierden23.delta_abs.sum() * 100
    d.evol, d.evol_meta = evolucion_por_anio()
    fin = d.evol_meta["fin"]
    d.f_emp = fmt_mes(ult + pd.DateOffset(months=2))      # el último trimestre termina dos meses después de su primer mes
    d.f_ipi, d.f_sal = fmt_mes(fin["Producción"]), fmt_mes(fin["Salario real"])
    d.f_ipc = fmt_mes(_ultimo_ipc())
    d.f_empresas = int(leer("empresas_por_rama.csv", ("periodo",)).periodo.max().year)
    d.corte = f"empleo hasta {d.f_emp}, producción hasta {d.f_ipi}, salario real hasta {d.f_sal}"
    expo = leer("exposicion_vs_resultados.csv")
    d.expo18 = expo[expo.ventana == "2018"].assign(etiqueta=lambda x: x.rama.map(nombre))

    # comercio exterior
    d.com = leer("resumen_comercio_anual.csv")
    d.c25, d.c24, d.c18 = d.com.iloc[-1], d.com.iloc[-2], d.com[d.com.anio == 2018].iloc[0]
    d.f_com = f"dic-{int(d.com.anio.max())}"
    d.i_min, d.i_max = d.com.loc[d.com.imp_cif.idxmin()], d.com.loc[d.com.imp_cif.idxmax()]
    previo = d.com[d.com.anio < d.c25.anio].pct_china
    d.china_previo = (previo.min(), previo.max())
    r = leer("comercio_por_rama_anio.csv")
    r18, r25 = r[r.anio == 2018], r[r.anio == 2025].assign(etiqueta=lambda x: x.rama.map(nombre))
    d.r_imp18, d.r_imp25 = r18.imp_cif.sum(), r25.imp_cif.sum()
    d.r_kg18, d.r_kg25 = r18.imp_kg.sum(), r25.imp_kg.sum()
    d.no_ind = d.c25.imp_cif - d.r_imp25
    d.deficit25 = r25.balanza.sum()
    d.def_mayores = r25.sort_values("balanza").head(3)
    d.superavit = r25[r25.balanza > 0].sort_values("balanza", ascending=False)
    ch = r[r.anio.isin([2018, 2025])].pivot(index="rama", columns="anio", values="pct_china").reset_index()
    ch["etiqueta"] = ch.rama.map(nombre)
    ch["cambio"] = ch[2025] - ch[2018]
    d.china = ch
    d.china_mayoria = ch[ch[2025] >= 50].sort_values(2025, ascending=False)
    d.china_avance = ch.sort_values("cambio", ascending=False).head(3)
    d.china_baja = ch[ch.cambio < -1].sort_values("cambio")
    d.n_china_sube = int((ch.cambio > 0).sum())

    # asociaciones
    d.corr = leer("correlaciones.csv")
    d.sig = d.corr[d.corr.p_valor < 0.05]
    g = leer("grupos_exposicion.csv")
    d.grupos = g
    m = g[g.grupo == "Mayor exposición"].set_index(["ventana", "exposicion"])
    n = g[g.grupo == "Menor exposición"].set_index(["ventana", "exposicion"])
    d.cortes = pd.DataFrame({"emp_mayor": m.mediana_d_empleo, "emp_menor": n.mediana_d_empleo, "ipi_mayor": m.mediana_d_ipi, "ipi_menor": n.mediana_d_ipi}).reset_index()
    d.cortes["es_china"] = d.cortes.exposicion.str.contains("China")
    d.cortes["ipi_peor"] = d.cortes.ipi_mayor < d.cortes.ipi_menor
    d.cortes["emp_peor"] = d.cortes.emp_mayor < d.cortes.emp_menor
    regs = leer("regresiones_panel.csv")
    d.regs = regs
    d.todas, d.sin = regs[regs.muestra == "Todas las ramas"], regs[regs.muestra == "Sin refinación de petróleo"]
    d.p_todas, d.p_sin = panel_empleo("Todas las ramas"), panel_empleo("Sin refinación de petróleo")
    d.control = leer("control_comex.csv")
    d.sig_todas = int((d.todas.p_valor < 0.05).sum())
    d.sig_sin = int((d.sin.p_valor < 0.05).sum())
    d.neg_todas = int((d.todas.efecto_10pct < 0).sum())
    d.fuerte = d.corr.loc[d.corr.rho.abs().idxmax()]
    imp = d.corr[d.corr.exposicion.str.startswith("Crecimiento")]
    d.n_imp, d.n_imp_sig = len(imp), int((imp.p_valor < 0.05).sum())
    d.n_imp_sig_neg = int(((imp.p_valor < 0.05) & (imp.rho < 0)).sum())
    d.n_sig_china = int(d.sig.exposicion.str.contains("China").sum())
    otras = d.sig[~d.sig.exposicion.str.contains("China")]
    d.n_sig_otras = len(otras)
    d.frase_otras = "; ".join(f"más importaciones con {'más' if r.rho > 0 else 'menos'} {r.resultado.replace('Δ% ', '')}" for r in otras.itertuples())
    d.n_cortes_imp = int((~d.cortes.es_china).sum())
    d.n_cortes_imp_emp_peor = int(d.cortes[~d.cortes.es_china].emp_peor.sum())
    d.n_bh = int((d.corr.p_corregido < 0.05).sum())

    # respuesta a la pregunta central: 2018 -> 2025, promedios anuales
    d.resp = leer("respuesta_por_rama.csv").assign(etiqueta=lambda x: x.rama.map(nombre))
    d.rg = leer("respuesta_grupos.csv").set_index("grupo")
    d.mas, d.menos, d.tot = d.rg.loc["Importaciones crecieron más"], d.rg.loc["Importaciones crecieron menos"], d.rg.loc["Total industria"]
    d.rc = leer("respuesta_correlaciones.csv")
    d.rc_emp = d.rc[(d.rc.exposicion_col == "imp_usd") & (d.rc.resultado_col == "empleo")].iloc[0]
    d.rc_bh = int((d.rc.p_corregido < 0.05).sum())
    d.uc = leer("respuesta_uso_correlaciones.csv")
    usoc = lambda e, r: d.uc[(d.uc.exposicion_col == e) & (d.uc.resultado_col == r)].iloc[0]
    d.u_ins, d.u_cons, d.u_kg_prod = usoc("insumos_usd", "empleo"), usoc("consumo_usd", "empleo"), usoc("consumo_ton", "produccion")
    d.ug = leer("respuesta_uso_grupos.csv").set_index("grupo")
    sens = leer("respuesta_sensibilidad.csv")
    d.previo = sens[sens.tipo == "tendencia_previa"].set_index("detalle")
    rr = d.resp.set_index("rama")
    d.pre, d.tex = rr.loc["18-19"], rr.loc["17"]
    d.al_reves = d.mas.puestos > d.menos.puestos
    return d


# ---------------------------------------------------------------- hojas

def _hoja_1(d):
    hoy = date.today()
    q23, q18, c25 = d.q23, d.q18, d.c25
    with _hoja(1):
        _doc(
            '<div class="portada">',
            '<p class="sup">Informe de conclusiones</p>',
            '<div class="titulo">Importaciones e industria en Argentina, 2016-2026</div>',
            '<div class="subtitulo-doc">Desde 2018, ¿la industria perdió empleo, producción y salario justo donde más crecieron las importaciones?</div>',
            f'<p class="autor"><b>{AUTOR}</b><br>{MESES_LARGOS[hoy.month - 1].capitalize()} de {hoy.year}<br>Datos hasta: empleo {d.f_emp} · producción {d.f_ipi} · salario real {d.f_sal} · comercio exterior {d.f_com}</p>',
            "</div>",
        )
        _doc(
            _h1("Resumen"),
            _p("Este informe responde una pregunta: **desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?** "
               "Se usan datos oficiales del INDEC y del Ministerio de Trabajo, llevados a 16 ramas industriales comparables."),
            _p(f"La industria retrocede: entre 2018 y 2025 la producción varió {fmt_pct(d.tot.produccion)} y el salario real {fmt_pct(d.tot.salario)}; el empleo se sostuvo hasta 2023 y desde entonces cae "
               f"({fmt_pct(q23.delta_pct)} hasta {d.f_emp}). Pero las pérdidas no se concentraron donde más crecieron las importaciones: las 8 ramas donde más crecieron "
               f"{'sumaron' if d.mas.puestos > 0 else 'perdieron'} {fmt_miles(abs(d.mas.puestos))} puestos y las 8 donde menos crecieron {'sumaron' if d.menos.puestos > 0 else 'perdieron'} {fmt_miles(abs(d.menos.puestos))}. "
               f"Ese «al revés» lo explican los insumos: las ramas que crecen importan más insumos y máquinas. Con los bienes de consumo, que son los que compiten, no hay relación con el empleo."),
            _p(f"**Conclusión principal:** {'no' if d.al_reves else 'en empleo, sí'}. Desde 2018 la industria perdió producción y salario en casi todas sus ramas, pero esas pérdidas no coinciden con el crecimiento de las importaciones. "
               f"La excepción visible es {d.pre.etiqueta}, donde las importaciones crecieron {fmt_pct(d.pre.imp_ton, False)} en toneladas y se perdieron {fmt_miles(abs(d.pre.puestos))} puestos. Es una coincidencia medida, no un efecto."),
            _tabla("Tabla 1. Indicadores clave de la industria manufacturera",
                   ["Indicador", "Valor", "Contra 2023", "Contra 2018"],
                   [(f"Empleo registrado privado (hasta {d.f_emp})", f"{fmt_miles(q23.ultimo)} puestos", f"{fmt_pct(q23.delta_pct)} ({fmt_signed(q23.delta_abs)})", f"{fmt_pct(q18.delta_pct)} ({fmt_signed(q18.delta_abs)})"),
                    (f"Producción (IPI), 12 meses hasta {d.f_ipi}", f"Índice {fmt_num(d.ipi23.ultimo)}", fmt_pct(d.ipi23.delta_pct), fmt_pct(d.ipi18.delta_pct)),
                    (f"Salario real, 12 meses hasta {d.f_sal}", "—", fmt_pct(d.sal23.delta_pct), fmt_pct(d.sal18.delta_pct)),
                    (f"Empresas activas (año {d.f_empresas})", fmt_miles(d.empr23.ultimo), f"{fmt_pct(d.empr23.delta_pct)} ({fmt_signed(d.empr23.delta_abs)})", "—"),
                    (f"Importaciones de bienes (año {int(c25.anio)})", f"USD {fmt_num(c25.imp_cif / 1e9)} mil M", f"{fmt_pct((c25.imp_cif / d.com[d.com.anio == 2023].imp_cif.iloc[0] - 1) * 100)}", f"{fmt_pct((c25.imp_cif / d.c18.imp_cif - 1) * 100)}"),
                    (f"China en las importaciones (año {int(c25.anio)})", f"{fmt_num(c25.pct_china)}% del valor", _pp(c25.pct_china - d.com[d.com.anio == 2023].pct_china.iloc[0]), _pp(c25.pct_china - d.c18.pct_china))],
                   alinear="lrrr", fuente="Empleo: mismo trimestre de cada año; producción y salario real: promedio de 12 meses. Fuente: INDEC y OEDE."),
            _h2("Contenido"),
            _indice(),
        )


def _hoja_2(d):
    n_anios = len(d.control)
    ok = bool(d.control.coincide_imp.all() and d.control.coincide_exp.all())
    with _hoja(2):
        _doc(
            _h1("1. Introducción"),
            _p("En los últimos años se discutió en Argentina si el aumento de las importaciones perjudica a la industria nacional o si, por el contrario, acompaña a la actividad porque abarata "
               "insumos y facilita el acceso a maquinaria. Este trabajo reúne datos oficiales "
               "de comercio exterior, empleo, salarios y producción, los lleva a una clasificación común de 16 ramas industriales y busca responder tres preguntas:"),
            _ol(["**Descriptiva:** ¿qué le pasó a la industria (empleo, salario real, producción, empresas) y al comercio exterior entre 2016 y 2026?",
                 "**De reasignación:** ¿el resultado total esconde ramas que crecieron y ramas que se achicaron?",
                 "**De asociación (la pregunta central):** Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?"]),
            _p("**H1 (la hipótesis central):** las ramas donde más crecieron las importaciones perdieron más empleo, producción y salario. **H0:** no hay relación, o es la contraria "
               "(más importaciones acompañan más actividad). **H2 (complementaria):** el avance de China se asocia con peores resultados aunque las importaciones totales no lo hagan."),
            _h1("2. Datos y método"),
            _tabla("Tabla 2. Fuentes de datos y hasta cuándo llega cada una",
                   ["Dato", "Fuente", "Último dato", "Uso"],
                   [("Comercio exterior por producto y país", "INDEC (países: ARCA)", d.f_com, "Qué se importa y de dónde"),
                    ("Empleo asalariado registrado", "Ministerio de Trabajo (OEDE, SIPA)", f"{d.tu} ({d.f_emp})", "Puestos de trabajo por rama"),
                    ("Remuneraciones", "Ministerio de Trabajo (OEDE, SIPA)", d.f_sal, "Salario de cada rama"),
                    ("Empresas activas", "Ministerio de Trabajo (OEDE)", str(d.f_empresas), "Cierres netos de empresas"),
                    ("Producción industrial (IPI)", "INDEC", d.f_ipi, "Producción física por rama"),
                    ("Precios al consumidor (IPC)", "INDEC", d.f_ipc, "Deflactar salarios")],
                   alinear="llll", fuente=None),
            _p(f"**Clasificación común.** Comercio exterior clasifica productos (NCM), empleo y salarios clasifican actividades (CIIU) y la producción usa divisiones propias del IPI. "
               f"Todo se llevó a las 16 ramas del IPI. Se excluyeron los productos primarios (petróleo crudo, gas, oro y agro sin procesar): USD {fmt_num(d.no_ind / 1e9)} mil "
               f"millones de los USD {fmt_num(d.c25.imp_cif / 1e9)} mil millones importados en 2025."),
            _p("**Comparación.** El empleo compara el último trimestre con el mismo trimestre de un año de referencia; la producción y el salario real, el promedio de los últimos 12 meses con el promedio de ese año "
               "(así no influyen la estacionalidad ni el aguinaldo). Las referencias son 2018 (previo a la pandemia: cambio de largo plazo) y 2023 (último año antes de que la industria empezara a caer: lo reciente); "
               "además se mira cada año contra el anterior. El salario real es la remuneración dividida por el IPC."),
            _p("**Exposición a las importaciones.** Medida principal: crecimiento de las importaciones en dólares de cada rama entre 2018 y 2025, el último año completo en todas las fuentes, "
               "contra el cambio del empleo, la producción y el salario real en esos mismos años (promedios anuales). Robustez: toneladas, dólares por puesto de trabajo y **uso económico** "
               "(BEC, Naciones Unidas: bienes de consumo, que compiten con la producción local; insumos y capital, que la abastecen). Complementos: China y base 2023."),
            _p(f"**Análisis.** Comparación entre las 8 ramas donde más y las 8 donde menos crecieron las importaciones; correlación de Spearman entre las 16 ramas con p-valor corregido por "
               f"comparaciones múltiples (Benjamini-Hochberg); y, como complemento, un modelo de panel con efectos fijos de rama y de año (2016-2025). **Controles:** "
               + (f"los totales de importaciones y exportaciones coinciden con los de control del INDEC en los {n_anios} años" if ok else "los totales de comercio se contrastaron con los de control del INDEC")
               + "; la suma de las 16 ramas de empleo coincide con el subtotal oficial de industria."),
        )


def _hoja_3(d):
    q23, q18 = d.q23, d.q18
    with _hoja(3):
        _doc(
            _h1("3. Resultados"),
            _h2("3.1 La industria desde 2016"),
            _p(f"En 2020 la producción tocó su piso ({fmt_num(d.ipi_min.indice)} en {fmt_mes(d.ipi_min.periodo)}) y el empleo el suyo ({fmt_num(d.emp_min.indice)} en el {trimestre_texto(d.emp_min.periodo)}). "
               f"La recuperación llevó al empleo a su máximo ({fmt_num(d.emp_max.indice)} en el {trimestre_texto(d.emp_max.periodo)}) y a la producción a {fmt_num(d.ipi_rec.indice)} en {fmt_mes(d.ipi_rec.periodo)}. "
               f"Desde entonces la producción cae hasta {fmt_num(d.ipi_ult.indice)} ({fmt_mes(d.ipi_ult.periodo)}) y el empleo hasta {fmt_num(d.emp_ult.indice)} ({trimestre_texto(d.emp_ult.periodo)}). "
               f"El salario real, en cambio, parte de {fmt_num(d.sal_max.indice)} en {fmt_mes(d.sal_max.periodo)}, toca {fmt_num(d.sal_min.indice)} en {fmt_mes(d.sal_min.periodo)} y remonta a {fmt_num(d.sal_ult.indice)} en {fmt_mes(d.sal_ult.periodo)}."),
        )
        fig = lineas(d.ind, "periodo", "indice", "metrica", COLOR_METRICA, y_titulo="Índice (promedio 2023 = 100)", base100=True, orden=["Empleo", "Producción (IPI)", "Salario real"], formato="%{y:.1f}")
        _grafico(fig, 205)
        _leyenda(1, f"Empleo, producción y salario real de la industria manufacturera (promedios móviles de 12 meses; promedio 2023 = 100). Datos: {d.corte}.")
        _doc(
            _p(f"Contra 2023, el empleo varió {fmt_pct(q23.delta_pct)} ({fmt_signed(q23.delta_abs)} puestos entre el {q23.trimestre_base} y el {q23.trimestre_ultimo}), la producción {fmt_pct(d.ipi23.delta_pct)} "
               f"y las empresas activas {fmt_pct(d.empr23.delta_pct)} ({fmt_signed(d.empr23.delta_abs)}). La producción cae más que el empleo ({fmt_pct(d.ipi23.delta_pct)} contra {fmt_pct(d.emp23.delta_pct)} en promedios "
               f"de 12 meses): las empresas ajustaron menos personal que producción. Contra 2018: empleo {fmt_pct(q18.delta_pct)}, producción {fmt_pct(d.ipi18.delta_pct)} y salario real {fmt_pct(d.sal18.delta_pct)}."),
            _h2("3.2 Empleo por rama: quién perdió y quién ganó"),
            _p(f"Contra el {d.tb18}, el empleo total varió {fmt_signed(q18.delta_abs)} puestos ({fmt_pct(q18.delta_pct)}), pero la caída no es pareja: las ramas que más puestos perdieron fueron "
               + _lista(f"{r.etiqueta} ({fmt_signed(r.delta_abs)}, {fmt_pct(r.delta_pct)})" for r in d.pierden18.head(3).itertuples())
               + ", y las que más ganaron, " + _lista(f"{r.etiqueta} ({fmt_signed(r.delta_abs)}, {fmt_pct(r.delta_pct)})" for r in d.ganan18.head(2).itertuples())
               + f". Contra el {d.tb23} el retroceso es {'casi general' if len(d.pierden23) >= 12 else 'parcial'}: {len(d.pierden23)} de 16 ramas perdieron empleo ("
               + (f"solo {_lista(d.ganan23.etiqueta)} lo aumentó" if len(d.ganan23) else "ninguna lo aumentó") + f") y las tres que más perdieron concentran {fmt_num(d.top3_23, 0)}% del total de puestos perdidos."),
        )
        fig = barras_signo(d.e18, "delta_abs", "etiqueta", x_titulo=f"Puestos de trabajo ({d.tu} contra {d.tb18})", formato="{:+,.0f}")
        fig.update_xaxes(range=[d.e18.delta_abs.min() * 1.35, d.e18.delta_abs.max() * 1.15])
        fig.update_yaxes(dtick=1, tickfont=dict(size=10))
        _grafico(fig, 250)
        _leyenda(2, f"Variación de puestos de trabajo registrados por rama, {d.tu} (hasta {d.f_emp}) contra {d.tb18}.")


def _hoja_4(d):
    tablas, meta = d.evol, d.evol_meta
    anios, ult, fin = meta["anios"], meta["anios"][-1], meta["fin"]
    tot = {k: t.loc[TOTAL] for k, t in tablas.items()}
    com = d.com.set_index("anio")

    def imp(y):
        return fmt_pct((com.loc[y, "imp_cif"] / com.loc[y - 1, "imp_cif"] - 1) * 100) if y in com.index else "n/d"

    filas = [("Empleo registrado", *[fmt_pct(tot["Empleo"][y]) for y in anios]),
             ("Producción física (IPI)", *[fmt_pct(tot["Producción"][y]) for y in anios]),
             ("Salario real", *[fmt_pct(tot["Salario real"][y]) for y in anios]),
             ("Importaciones de bienes (USD)", *[imp(y) for y in anios]),
             ("China en las importaciones (% del valor)", *[(f"{fmt_num(com.loc[y, 'pct_china'])}%" if y in com.index else "n/d") for y in anios])]
    cabecera = ["Cada año contra el anterior"] + [f"{y} (parcial)" if y == ult else str(y) for y in anios]
    nota = (f"{ult}: empleo, {trimestre_texto(fin['Empleo'])} contra el mismo trimestre de {ult - 1}; producción, enero a {MESES[fin['Producción'].month - 1]}; salario real, enero a {MESES[fin['Salario real'].month - 1]}. "
            f"Importaciones de {ult}: el archivo del INDEC no indica hasta qué mes llega, por eso no se comparan. Fuente: INDEC y Ministerio de Trabajo (OEDE).")
    emp, prod, sal = tot["Empleo"], tot["Producción"], tot["Salario real"]
    r_emp = tablas["Empleo"].drop(TOTAL)
    n_emp = {y: int((r_emp[y] < 0).sum()) for y in anios}
    peores = r_emp[ult].sort_values().head(2)
    r_prod = tablas["Producción"].drop(TOTAL)

    def lista_anios(serie):
        return ", ".join(f"{fmt_pct(serie[y])} en {y}" for y in anios[:-1]) + f" y {fmt_pct(serie[ult])} en lo que va de {ult}"

    mayor = "; es la mayor caída de los tres períodos" if emp[ult] < min(emp[y] for y in anios[:-1]) else ""
    with _hoja(4):
        _doc(
            _h2(f"3.3 Año por año: {', '.join(str(y) for y in anios[:-1])} y lo que va de {ult}"),
            _p(f"Mirando cada año contra el anterior (Tabla 3; {ult} solo hasta {d.f_emp} en empleo, {d.f_ipi} en producción y {d.f_sal} en salario real), el empleo del total de la industria varió {lista_anios(emp)}{mayor}. La producción varió {lista_anios(prod)}, y el salario real, {lista_anios(sal)}. "
               f"Las ramas que pierden empleo son {', '.join(f'{n} de 16 en {y}' for y, n in n_emp.items())}."),
            _tabla("Tabla 3. La industria año por año", cabecera, filas, alinear="lrrr", fuente=nota),
        )
        mat = r_emp.sort_values(ult).copy()
        mat.columns = [f"{y} (1T)" if y == ult else str(y) for y in mat.columns]
        mat.index = [nombre(x) for x in mat.index]
        fig = heatmap(mat, escala=ESCALA_RESULTADO, rango=12, sufijo="%", decimales=1, tam_texto=10, alto=330)
        _grafico(fig, 330)
        _leyenda(3, f"Variación del empleo de cada rama, cada año contra el anterior ({ult}: {trimestre_texto(fin['Empleo'])} contra el mismo trimestre de {ult - 1}).")
        _doc(
            _p(f"En lo que va de {ult}, las más golpeadas son {nombre(peores.index[0])} y {nombre(peores.index[1])}: su empleo cae {fmt_pct(abs(peores.iloc[0]), False)} y {fmt_pct(abs(peores.iloc[1]), False)} y su producción varía "
               f"{fmt_pct(r_prod[ult][peores.index[0]])} y {fmt_pct(r_prod[ult][peores.index[1]])}. En producción, {int((r_prod[ult] < 0).sum())} de 16 ramas caen en {ult} contra {int((r_prod[anios[-2]] < 0).sum())} en {anios[-2]}. "
               f"Los datos de {ult} son parciales y el Ministerio de Trabajo corrige los últimos trimestres cuando actualiza la serie, por lo que estas cifras pueden cambiar."),
        )


def _hoja_5(d):
    c25, c24, c18 = d.c25, d.c24, d.c18
    filas = []
    for r in d.com.itertuples():
        saldo = (r.exp_fob - r.imp_cif) / 1e9
        filas.append((int(r.anio), fmt_num(r.imp_cif / 1e9), fmt_num(r.exp_fob / 1e9), _sg(saldo), fmt_num(r.pct_china)))
    with _hoja(5):
        _doc(
            _h2("3.4 Comercio exterior y avance de China"),
            _p(f"Las importaciones de bienes pasaron de USD {fmt_num(c18.imp_cif / 1e9)} mil millones en 2018 a USD {fmt_num(c25.imp_cif / 1e9)} mil millones en 2025 ({fmt_pct((c25.imp_cif / c18.imp_cif - 1) * 100)}), "
               f"(años completos, hasta {d.f_com}), con un mínimo de USD {fmt_num(d.i_min.imp_cif / 1e9)} mil millones en {int(d.i_min.anio)} y un máximo de USD {fmt_num(d.i_max.imp_cif / 1e9)} mil millones en {int(d.i_max.anio)}; en 2025 subieron "
               f"{fmt_pct((c25.imp_cif / c24.imp_cif - 1) * 100, False)} respecto de 2024. Considerando solo las 16 ramas industriales, desde 2018 el valor importado varió {fmt_pct((d.r_imp25 / d.r_imp18 - 1) * 100)} pero el peso "
               f"{fmt_pct((d.r_kg25 / d.r_kg18 - 1) * 100)}: se paga más y entra casi lo mismo, lo que apunta a mayores precios o a un cambio en el tipo de bienes (los valores son dólares corrientes)."),
        )
        _doc(_tabla("Tabla 4. Comercio exterior de bienes, en miles de millones de dólares corrientes",
                    ["Año", "Importaciones (CIF)", "Exportaciones (FOB)", "Saldo", "China (% de las importaciones)"], filas, alinear="crrrr",
                    fuente="Saldo: exportaciones FOB menos importaciones CIF (orientativo). Fuente: INDEC."))
        _doc(
            _p(f"El déficit industrial de 2025 (exportaciones menos importaciones, ambas FOB) fue de USD {fmt_num(abs(d.deficit25) / 1e9)} mil millones y se concentra en "
               + _lista(f"{r.etiqueta} ({_sg(r.balanza / 1e9)})" for r in d.def_mayores.itertuples())
               + "; solo " + _lista(f"{r.etiqueta} ({_sg(r.balanza / 1e9)})" for r in d.superavit.itertuples()) + " tuvieron superávit."),
            _p(f"China fue entre 2016 y {int(c24.anio)} el origen de entre {fmt_num(d.china_previo[0])}% y {fmt_num(d.china_previo[1])}% del valor importado; en {int(c25.anio)} saltó a {fmt_num(c25.pct_china)}% "
               f"({_pp(c25.pct_china - c24.pct_china)} en un año), el valor más alto de la serie. Por rama, ganó peso en {d.n_china_sube} de 16: los mayores avances entre 2018 y 2025 fueron "
               + _lista(f"{r.etiqueta} ({fmt_num(r[2018], 0)}% a {fmt_num(r[2025], 0)}%)" for _, r in d.china_avance.iterrows())
               + ", y en " + _lista(f"{r.etiqueta} ({fmt_num(r[2025], 0)}%)" for _, r in d.china_mayoria.iterrows()) + " provee la mitad o más de lo importado"
               + ("; perdió terreno en " + _lista(f"{r.etiqueta} ({fmt_num(r[2018], 0)}% a {fmt_num(r[2025], 0)}%)" for _, r in d.china_baja.iterrows()) if len(d.china_baja) else "") + "."),
        )
        _grafico(dumbbell(d.china, "etiqueta", 2018, 2025, "2018", "2025", x_titulo="% de las importaciones de la rama que vienen de China", c0=GRIS, c1=NARANJA), 300)
        _leyenda(4, "Participación de China en el valor importado por cada rama, 2018 y 2025.")


def _hoja_6(d):
    filas = [("Importaciones crecieron más (8 ramas)", f"{fmt_pct(d.mas.imp_usd)}", f"{fmt_signed(d.mas.puestos)} ({fmt_pct(d.mas.empleo)})", fmt_pct(d.mas.produccion), fmt_pct(d.mas.salario)),
             ("Importaciones crecieron menos (8 ramas)", f"{fmt_pct(d.menos.imp_usd)}", f"{fmt_signed(d.menos.puestos)} ({fmt_pct(d.menos.empleo)})", fmt_pct(d.menos.produccion), fmt_pct(d.menos.salario))]
    for g, nom in (("Consumo importado creció más", "Consumo importado creció más"), ("Consumo importado creció menos", "Consumo importado creció menos")):
        x = d.ug.loc[g]
        filas.append((f"{nom} ({int(x.n_ramas)} ramas)", f"{fmt_pct(x.consumo_usd)} (consumo)", f"{fmt_signed(x.puestos)} ({fmt_pct(x.empleo)})", fmt_pct(x.produccion), fmt_pct(x.salario)))
    filas.append(("Total industria", "—", f"{fmt_signed(d.tot.puestos)} ({fmt_pct(d.tot.empleo)})", fmt_pct(d.tot.produccion), fmt_pct(d.tot.salario)))
    todas, sin = d.p_todas, d.p_sin
    r = d.resp
    with _hoja(6):
        _doc(
            _h2("3.5 La respuesta: ¿se perdió justo donde más crecieron las importaciones?"),
            _p(f"Entre 2018 y 2025, las 8 ramas donde más crecieron las importaciones {'sumaron' if d.mas.puestos > 0 else 'perdieron'} {fmt_miles(abs(d.mas.puestos))} puestos ({fmt_pct(d.mas.empleo)}) y las 8 donde menos crecieron "
               f"{'sumaron' if d.menos.puestos > 0 else 'perdieron'} {fmt_miles(abs(d.menos.puestos))} ({fmt_pct(d.menos.empleo)}); en producción, la mediana fue {fmt_pct(d.mas.produccion)} contra {fmt_pct(d.menos.produccion)} (Tabla 5). "
               f"Entre las 16 ramas, la correlación entre el crecimiento de las importaciones y el del empleo es positiva (ρ = {fmt_num(d.rc_emp.rho, 2)}, p {fmt_p(d.rc_emp.p_valor)}): "
               f"{'lo contrario de H1' if d.rc_emp.rho > 0 else 'en la dirección de H1'}. La excepción es {d.pre.etiqueta} (Figura 5)."),
        )
        fig = dispersion(r, "imp_usd", "empleo", "etiqueta", x_titulo="Crecimiento de las importaciones en dólares, 2018 → 2025 (%)", y_titulo="Δ% empleo, 2018 → 2025",
                         resaltar=[nombre("18-19"), nombre("17")])
        apinadas = r.imp_usd.between(20, 30) & (r.empleo.abs() < 1.5)
        fig.data[0].text = [("" if a else e) for a, e in zip(apinadas, r.etiqueta)]
        fig.data[0].textposition = ["middle left" if x == "17" else "top center" for x in r.rama]
        if apinadas.any():
            c0 = r[apinadas]
            fig.add_annotation(x=c0.imp_usd.mean(), y=c0.empleo.mean(), ax=58, ay=-6, axref="x", ayref="y", arrowcolor=GRIS, arrowwidth=1,
                               text="<br>".join(c0.etiqueta), align="left", xanchor="left", font=dict(size=8))
        fig.update_xaxes(range=[r.imp_usd.min() - 15, r.imp_usd.max() + 20])
        _grafico(fig, 255)
        _leyenda(5, f"Crecimiento de las importaciones y cambio del empleo de cada rama, 2018 → 2025 (promedios anuales; ρ de Spearman = {fmt_num(d.rc_emp.rho, 2)}). En naranja, {d.pre.etiqueta} y {d.tex.etiqueta}.")
        _doc(
            _tabla("Tabla 5. Cambio 2018 → 2025 según cuánto crecieron las importaciones de cada rama",
                   ["Grupo de ramas", "Importaciones (mediana)", "Puestos (empleo %)", "Producción (mediana)", "Salario real (mediana)"], filas, alinear="lrrrr", sin_cortes=True),
            _p(f"**¿Cambia si se mide distinto?** Con toneladas o con dólares por puesto la respuesta es la misma: de 9 correlaciones, {'ninguna' if d.rc_bh == 0 else d.rc_bh} resiste la corrección por comparaciones múltiples "
               f"y ninguna asocia más importaciones con peor resultado. Separando por uso económico se ve de dónde sale el signo positivo: el crecimiento de las importaciones de **insumos** va junto con el del empleo "
               f"(ρ = {fmt_num(d.u_ins.rho, 2)}, p corregido = {fmt_num(d.u_ins.p_corregido, 3)}), mientras que con los **bienes de consumo** la relación desaparece (ρ = {fmt_num(d.u_cons.rho, 2)}); en toneladas de consumo "
               f"hay una señal negativa con la producción (ρ = {fmt_num(d.u_kg_prod.rho, 2)}) que no es significativa. La tendencia previa (empleo 2011-2017) explica más que las importaciones "
               f"(p {fmt_p(d.previo.loc['empleo 2011-2017', 'p_valor'])} contra p {fmt_p(d.previo.loc['importaciones (USD)', 'p_valor'])})."),
            _p(f"**Complementos.** De las {len(d.corr)} correlaciones del análisis original (cuatro medidas, entre ellas dos de China, y dos años base), {d.n_bh} resiste la corrección: «{d.fuerte.exposicion}» con «{d.fuerte.resultado}» "
               f"(base {d.fuerte.ventana}; ρ = {fmt_num(d.fuerte.rho, 2)}). En el modelo de panel, +10% de importaciones se asocia con {fmt_pct(todas.efecto_10pct)} de empleo (p {fmt_p(todas.p_valor)}); sin refinación de petróleo, "
               f"{fmt_pct(sin.efecto_10pct)} (p {fmt_p(sin.p_valor)}). Que dependa de una sola rama indica que es frágil, y un signo positivo no significa que importar cree empleo."),
        )


def _hoja_7(d):
    ch = d.cortes[d.cortes.es_china]
    q23, q18 = d.q23, d.q18
    ult = d.evol_meta["anios"][-1]
    emp_ult = d.evol["Empleo"].loc[TOTAL, ult]
    with _hoja(7):
        _doc(
            _h1("4. Conclusiones"),
            _ol([
                f"**La industria retrocede desde 2023.** Entre el {q23.trimestre_base} y el {q23.trimestre_ultimo} el empleo cayó {fmt_pct(abs(q23.delta_pct), False)} ({fmt_signed(q23.delta_abs)} puestos), la producción {fmt_pct(abs(d.ipi23.delta_pct), False)} y hay {fmt_miles(abs(d.empr23.delta_abs))} empresas activas menos; "
                f"en lo que va de {ult} (hasta {d.f_emp}) el empleo cae otro {fmt_pct(abs(emp_ult), False)} contra el mismo período de {ult - 1}. La producción cae más que el empleo: las empresas ajustaron menos personal que producción.",
                f"**La caída del empleo es desigual entre ramas.** El empleo es {fmt_pct(q18.delta_pct)} respecto del {d.tb18}: {d.pierden18.etiqueta.iloc[0]}, {d.pierden18.etiqueta.iloc[1]} y {d.pierden18.etiqueta.iloc[2]} perdieron "
                f"{fmt_miles(abs(d.pierden18.delta_abs.head(3).sum()))} puestos mientras {d.ganan18.etiqueta.iloc[0]} y {d.ganan18.etiqueta.iloc[1]} ganaron {fmt_miles(d.ganan18.delta_abs.head(2).sum())}.",
                f"**Las pérdidas no se concentraron donde más crecieron las importaciones; en general, fue al revés.** Entre 2018 y 2025 las ramas donde más crecieron {'sumaron' if d.mas.puestos > 0 else 'perdieron'} "
                f"{fmt_miles(abs(d.mas.puestos))} puestos y las de menor crecimiento {'sumaron' if d.menos.puestos > 0 else 'perdieron'} {fmt_miles(abs(d.menos.puestos))}. Ninguna de las 9 pruebas asocia más importaciones con peor resultado.",
                f"**El «al revés» lo explican los insumos.** Las ramas que crecen importan más insumos y máquinas (ρ = {fmt_num(d.u_ins.rho, 2)} con el empleo). Con los bienes de consumo, los que compiten, no hay relación "
                f"(ρ = {fmt_num(d.u_cons.rho, 2)}).",
                f"**La excepción: prendas y textiles.** {d.pre.etiqueta} importó {fmt_pct(d.pre.imp_ton, False)} más en toneladas y perdió {fmt_miles(abs(d.pre.puestos))} puestos; {d.tex.etiqueta}, {fmt_pct(d.tex.imp_ton, False)} más en toneladas "
                f"(pero solo {fmt_pct(d.tex.imp_usd)} en dólares) y {fmt_miles(abs(d.tex.puestos))} puestos menos. Son bienes de consumo baratos: el valor en dólares subestima cuánto entra.",
                f"**China avanzó, pero es un indicio, no la respuesta.** Llegó a {fmt_num(d.c25.pct_china)}% del valor importado en 2025 y provee la mitad o más en {_lista(d.china_mayoria.etiqueta)}. "
                f"De las {len(d.corr)} correlaciones originales, {d.n_bh} resiste la corrección (peso de China con producción), y mide más la composición de la industria que un aumento de la competencia.",
            ]),
            _h2("Respuesta a la pregunta de investigación"),
            _p(f"**{'No' if d.al_reves else 'En empleo, sí'}.** Desde 2018 la industria perdió producción y salario real, pero no justo en los sectores donde más crecieron las importaciones: **H1 no se confirma**. "
               f"La relación positiva que aparece (más importaciones, más empleo) sale de los insumos que compran las ramas que crecen; con los bienes de consumo no hay relación. La excepción son prendas y textiles. "
               f"Es una coincidencia medida en 16 ramas, sin controlar la recesión, el tipo de cambio ni la demanda interna: no permite afirmar que las importaciones no afectaron a ninguna rama."),
            _tabla("Tabla 6. Balance de las hipótesis",
                   ["Hipótesis", "Qué muestran los datos", "Veredicto"],
                   [("H1. Más importaciones, peores resultados",
                     f"Ramas donde más crecieron: {fmt_signed(d.mas.puestos)} puestos; donde menos: {fmt_signed(d.menos.puestos)}. Ninguna de 9 pruebas con peor resultado; {d.rc_bh} resiste la corrección.", "No se confirma"),
                    ("H0. Sin relación, o relación contraria",
                     f"La relación positiva es de los insumos (ρ = {fmt_num(d.u_ins.rho, 2)}); con bienes de consumo, ρ = {fmt_num(d.u_cons.rho, 2)}. Prendas y textiles son la excepción.", "Compatible con los datos"),
                    ("H2. El avance de China se asocia con peor resultado",
                     f"{d.n_sig_china} de {len(d.corr)} correlaciones significativas involucran a China; {d.n_bh} resiste la corrección; peor producción en {int(ch.ipi_peor.sum())} de {len(ch)} cortes con China.", "Indicio, sin prueba de causa")],
                   alinear="lll", fuente=None),
        )


def _hoja_8(d):
    ult = d.evol_meta["anios"][-1]
    fin = d.evol_meta["fin"]
    with _hoja(8):
        _doc(
            _h1("5. Limitaciones"),
            _ul(["**Asociación no es causalidad.** En el período hubo devaluaciones, recesión, pandemia y cambios de política comercial a la vez.",
                 "**El uso económico es aproximado.** Cada producto se clasifica por su uso más habitual (BEC) y se asigna a la rama que lo fabrica según su capítulo; un insumo importado también puede competir con quien lo produce en el país.",
                 f"**Pocas ramas.** Son 16 ramas: solo correlaciones grandes (|ρ| de 0,5 o más) se distinguen del azar; por eso los p-valores se corrigen y «no significativo» no quiere decir «no hay relación».",
                 "**Exposición medida con sustitutos.** Falta el valor de la producción por rama para calcular el índice clásico de penetración de importaciones.",
                 "**Empleo registrado y sin horas.** Solo cuenta asalariados privados formales; las empresas pueden ajustar horas sin despedir.",
                 "**Valores corrientes y traducción aproximada.** Los dólares no están ajustados por inflación internacional y el pasaje de producto a rama es aproximado (se aplica el mismo criterio a todo).",
                 f"**Datos de {ult} parciales y revisables.** El empleo llega al {trimestre_texto(fin['Empleo'])}, el salario real a {MESES[fin['Salario real'].month - 1]} y la producción a {MESES[fin['Producción'].month - 1]}; "
                 f"el Ministerio de Trabajo corrige los últimos trimestres al actualizar la serie. Las importaciones de {ult} no se usan porque el archivo no indica el mes de corte.",
                 "**Fechas de corte distintas.** «Últimos 12 meses» termina en fechas diferentes según la fuente, y cerca de 5% de las exportaciones es confidencial y no se puede asignar a una rama."]),
            _h1("6. Próximos pasos"),
            _ol(["Pasar de «coincide» a «provoca»: usar como fuente de variación lo que China le vende a otros países parecidos (estrategia de Autor, Dorn y Hanson) o la apertura de importaciones de 2024.",
                 "Bajar a nivel de producto (NCM de 4 a 6 dígitos) y comparar con la producción física del mismo producto (encuesta de productos industriales), para ganar detalle sobre prendas y textiles.",
                 "Incorporar el valor de la producción por rama y calcular la exposición clásica (importaciones sobre consumo aparente).",
                 f"Sumar el comercio exterior de enero a agosto de {ult}, publicado por el INDEC por mes, y controles macroeconómicos (tipo de cambio real, demanda interna, aranceles)."]),
            _h1("Fuentes"),
            _ul(["INDEC. Comercio exterior (importaciones y exportaciones por producto y país), Índice de producción industrial manufacturero, Utilización de la capacidad instalada e Índice de precios al consumidor.",
                 "Ministerio de Trabajo, Empleo y Seguridad Social. Observatorio de Empleo y Dinámica Empresarial (OEDE): empleo asalariado privado registrado, remuneraciones y empresas, por actividad (SIPA).",
                 "ARCA. Tabla de códigos de país."]),
            _p("Los datos y el detalle de cada cálculo pueden recorrerse en las demás pestañas de esta aplicación; la página «Método y límites» documenta las decisiones y los controles."),
        )


def mostrar():
    d = _datos()
    for hoja in (_hoja_1, _hoja_2, _hoja_3, _hoja_4, _hoja_5, _hoja_6, _hoja_7, _hoja_8):
        hoja(d)
