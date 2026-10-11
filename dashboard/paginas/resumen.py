"""Página «Resumen»: pregunta, indicadores clave, hallazgos y la evidencia de contexto (industria y comercio exterior)."""

import pandas as pd
import streamlit as st

from core.consultas import (cambio, cambio_total, delta_empleo_rama, empleo_trimestre, panorama_ultimo_anio,
                            trimestre_texto)
from core.datos import RAMAS, TOTAL, leer, nombre
from core.formato import fmt_mes, fmt_miles, fmt_num, fmt_pct, fmt_signed
from core.graficos import lineas
from core.tema import AZUL, COLOR_METRICA, NARANJA
from core.tarjetas import afiche as _afiche, fila_hallazgo as _bloque, redondo as _redondo
from core.ui import bloque, figura, nota


def _introduccion():
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.markdown('<div class="etiqueta">Pregunta</div>', unsafe_allow_html=True)
        st.markdown("Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron "
                    "las importaciones?")
    with c2:
        st.markdown('<div class="etiqueta">Datos</div>', unsafe_allow_html=True)
        st.markdown("Fuentes oficiales: **INDEC** (comercio exterior, producción industrial, capacidad instalada y precios) y **Ministerio de Trabajo – OEDE** "
                    "(empleo, remuneraciones y empresas). Todo se llevó a **16 ramas industriales comparables** (ver «Método y límites»).")
    with c3:
        st.markdown('<div class="etiqueta">Enfoque</div>', unsafe_allow_html=True)
        st.markdown("Se describe qué pasó con la industria y con el comercio exterior, y se compara rama por rama, **entre 2018 y 2025**, cuánto crecieron las importaciones "
                    "con cómo cambiaron el empleo, la producción y el salario. Se miden **coincidencias**, no causas.")


def _indicadores():
    comercio = leer("resumen_comercio_anual.csv")
    c25, c24 = comercio.iloc[-1], comercio.iloc[-2]
    q23 = empleo_trimestre(TOTAL, "2023")
    ipi23, ipi18 = cambio_total("Producción (IPI)", "2023"), cambio_total("Producción (IPI)", "2018")
    sal23, sal18 = cambio_total("Salario real", "2023"), cambio_total("Salario real", "2018")

    st.subheader("Indicadores clave")
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Empleo industrial (puestos)", fmt_miles(q23.ultimo),
              f"{fmt_miles(q23.delta_abs)} vs {q23.trimestre_base} ({fmt_pct(q23.delta_pct)})", border=True)
    k2.metric("Producción (IPI) vs 2023", fmt_pct(ipi23.delta_pct), f"{fmt_pct(ipi18.delta_pct)} vs 2018", border=True)
    k3.metric("Salario real vs 2023", fmt_pct(sal23.delta_pct), f"{fmt_pct(sal18.delta_pct)} vs 2018", border=True)
    k4.metric("Importaciones 2025 (USD mil M)", fmt_num(c25.imp_cif / 1e9),
              f"{fmt_pct((c25.imp_cif / c24.imp_cif - 1) * 100)} vs 2024", delta_color="off", border=True)
    k5.metric("China en las importaciones", f"{fmt_num(c25.pct_china)}%",
              f"{fmt_num(c25.pct_china - c24.pct_china)} p.p. vs 2024", delta_color="off", border=True)
    st.caption(
        f"Cómo se calculan: el empleo compara el {q23.trimestre_ultimo} con el mismo trimestre de 2023 (así se elimina el efecto estacional). "
        "Producción y salario real comparan el promedio de los últimos 12 meses con el promedio del año base; se usan 12 meses porque la "
        "producción tiene estacionalidad fuerte y el salario incluye aguinaldo en junio y diciembre. Importaciones: valor CIF en dólares corrientes."
    )


def _hallazgos():
    expo = leer("exposicion_vs_resultados.csv")
    q23, q18 = empleo_trimestre(TOTAL, "2023"), empleo_trimestre(TOTAL, "2018")
    ipi23 = cambio_total("Producción (IPI)", "2023")
    t26, m26 = panorama_ultimo_anio()
    sal23, sal18 = cambio_total("Salario real", "2023"), cambio_total("Salario real", "2018")
    emp_prom, empresas = cambio_total("Empleo", "2023"), cambio_total("Empresas", "2023")
    t17, t1819 = cambio("17", "Producción (IPI)", "2023"), cambio("18-19", "Producción (IPI)", "2023")
    e17, e1819 = cambio("17", "Empleo", "2023"), cambio("18-19", "Empleo", "2023")
    x17 = expo[(expo.rama == "17") & (expo.ventana == "2023")].iloc[0]
    ramas = delta_empleo_rama(2018).sort_values("delta_abs")
    pierden, ganan = ramas[ramas.delta_abs < 0], ramas[ramas.delta_abs > 0].iloc[::-1]
    salarios = pd.Series({r: cambio(r, "Salario real", "2023").delta_pct for r in RAMAS}).sort_values()
    resp, grupos = leer("respuesta_por_rama.csv").set_index("rama"), leer("respuesta_grupos.csv").set_index("grupo")
    mas, menos = grupos.loc["Importaciones crecieron más"], grupos.loc["Importaciones crecieron menos"]
    rp, rt = resp.loc["18-19"], resp.loc["17"]
    R_PER = "2018 → 2025"
    emp26 = t26.loc[TOTAL]
    mas_perdio, mas_gano = next(pierden.itertuples()), next(ganan.itertuples())

    def mm(v: float, sube: str = "MÁS", baja: str = "MENOS") -> str:
        return sube if v > 0 else baja

    def n(texto: str, valor: str) -> str:
        """Resalta una cifra dentro del pie, como en el afiche."""
        return texto.replace(valor, f'<b>{valor}</b>', 1)

    def uno_de_cada(pct: float) -> str:
        m = 100 / abs(pct)
        return f"{'casi ' if m - int(m) > .15 else ''}1 de cada {round(m) if m - int(m) > .15 else int(m)}"

    OEDE, INDEC, AMBAS = "OEDE", "INDEC", "OEDE · INDEC"   # OEDE = Observatorio de Empleo del Ministerio de Trabajo
    per18 = f"{q18.trimestre_base} → {q18.trimestre_ultimo}"
    per23 = f"{q23.trimestre_base} → {q23.trimestre_ultimo}"

    bloques = [
        (_afiche(_redondo(q18.delta_abs), (f"{mm(q18.delta_abs)} EMPLEOS", "EN LA INDUSTRIA"), "EMPLEO INDUSTRIAL · ARGENTINA", per18,
                 n(f"Exactamente {fmt_miles(abs(q18.delta_abs))} ({fmt_pct(q18.delta_pct)}), del {q18.trimestre_base} al {q18.trimestre_ultimo}.",
                   fmt_miles(abs(q18.delta_abs))), OEDE, ""),
         [_afiche(f"{len(pierden)} de {len(ramas)}", ("RAMAS", "PIERDEN EMPLEO"), "RAMAS INDUSTRIALES", "DESDE 2018",
                  f"Solo {len(ganan)} sumaron puestos.", OEDE, "", "neu"),
          _afiche(_redondo(mas_perdio.delta_abs), ("MENOS EMPLEOS", f"EN {nombre(mas_perdio.Index).upper()}"), "LA MÁS GOLPEADA", "DESDE 2018",
                  n(f"{fmt_pct(mas_perdio.delta_pct)} de sus puestos ({fmt_miles(abs(mas_perdio.delta_abs))}).", fmt_pct(mas_perdio.delta_pct)), OEDE, ""),
          _afiche(_redondo(mas_gano.delta_abs), ("MÁS EMPLEOS", f"EN {nombre(mas_gano.Index).upper()}"), "LA QUE MÁS CRECIÓ", "DESDE 2018",
                  n(f"{fmt_pct(mas_gano.delta_pct)} de sus puestos ({fmt_miles(mas_gano.delta_abs)}).", fmt_pct(mas_gano.delta_pct)), OEDE, ""),
          _afiche(fmt_pct(q18.delta_pct), (f"{mm(q18.delta_pct)} EMPLEO", "QUE EN 2018"), "EMPLEO INDUSTRIAL", per18,
                  "Una industria que emplea menos, y de forma muy desigual." if q18.delta_abs < 0 else "Más empleo, pero desigual.", OEDE, "")]),
        (_afiche(fmt_pct(ipi23.delta_pct), (f"{mm(ipi23.delta_pct)} PRODUCCIÓN", "QUE EN 2023"), "PRODUCCIÓN INDUSTRIAL · IPI", "2023 → ÚLTIMOS 12 MESES",
                 "Cae la producción, se pierden puestos y cierran empresas." if ipi23.delta_pct < 0 and q23.delta_abs < 0 and empresas.delta_abs < 0
                 else "Promedio de los últimos 12 meses contra el promedio de 2023.", INDEC, ""),
         [_afiche(_redondo(q23.delta_abs), (f"{mm(q23.delta_abs)} EMPLEOS", "DESDE 2023"), "EMPLEO INDUSTRIAL", per23,
                  n(f"Exactamente {fmt_miles(abs(q23.delta_abs))} ({fmt_pct(q23.delta_pct)}).", fmt_miles(abs(q23.delta_abs))), OEDE, ""),
          _afiche(fmt_signed(empresas.delta_abs), (f"{mm(empresas.delta_abs)} EMPRESAS", "INDUSTRIALES"), "EMPRESAS ACTIVAS", "2023 → 2024",
                  n(f"Saldo neto: {fmt_pct(empresas.delta_pct)}.", fmt_pct(empresas.delta_pct)), OEDE, ""),
          _afiche(fmt_pct(emp_prom.delta_pct), (f"{mm(emp_prom.delta_pct, 'SUBE', 'CAE')} EL EMPLEO",
                                                "MENOS QUE LA PRODUCCIÓN" if ipi23.delta_pct < emp_prom.delta_pct < 0 else "PROMEDIO 12 MESES"),
                  "EMPLEO VS. PRODUCCIÓN", "CONTRA 2023", "Las empresas ajustaron más la producción que el personal."
                  if ipi23.delta_pct < emp_prom.delta_pct < 0 else "Promedio de 12 meses.", AMBAS, ""),
          _afiche(fmt_pct(emp26.empleo_pct), (f"{mm(emp26.empleo_pct)} EMPLEO", "QUE HACE UN AÑO"), "ÚLTIMO AÑO", f"{m26['trim_ant']} → {m26['trim_ult']}",
                  "La caída continúa." if emp26.empleo_pct < 0 else "Hay recuperación.", OEDE, "")]),
        (_afiche(fmt_pct(sal18.delta_pct), (f"{mm(sal18.delta_pct)} PODER", "DE COMPRA QUE EN 2018"), "SALARIO REAL INDUSTRIAL", "2018 → ÚLTIMOS 12 MESES",
                 "La caída principal fue entre 2017 y 2020; desde entonces se mantiene cerca del nivel de 2023.", AMBAS, ""),
         [_afiche(fmt_pct(sal23.delta_pct), (f"{mm(sal23.delta_pct)} SALARIO", "QUE EN 2023"), "SALARIO REAL", "2023 → ÚLTIMOS 12 MESES",
                  "Recuperación parcial." if sal23.delta_pct > 0 else "Sigue cayendo.", AMBAS, ""),
          _afiche(fmt_pct(emp26.salario_pct), (f"{mm(emp26.salario_pct, 'GANA', 'PIERDE')} SALARIO", f"EN {m26['fin_sal'].year}"), "SALARIO REAL",
                  f"HASTA {fmt_mes(m26['fin_sal']).upper()}", f"Contra el mismo período de {m26['fin_sal'].year - 1}.", AMBAS, ""),
          _afiche(fmt_pct(salarios.iloc[-1]), (f"{mm(salarios.iloc[-1])} SALARIO", f"EN {nombre(salarios.index[-1]).upper()}"), "LA QUE MÁS SUBIÓ",
                  "DESDE 2023", "Salario real de la rama.", AMBAS, ""),
          _afiche(fmt_pct(salarios.iloc[0]), (f"{mm(salarios.iloc[0])} SALARIO", f"EN {nombre(salarios.index[0]).upper()}"), "LA QUE MÁS CAYÓ",
                  "DESDE 2023", "Salario real de la rama.", AMBAS, "")]),
        (_afiche(fmt_pct(t17.delta_pct), (f"{mm(t17.delta_pct)} PRODUCCIÓN", "TEXTIL"), "TEXTILES Y CALZADO", "2023 → ÚLTIMOS 12 MESES",
                 "Cae la producción local mientras crecen las importaciones textiles." if t17.delta_pct < 0 < x17.d_imp_kg
                 else "Dos de las ramas donde más cayeron la producción y el empleo.", INDEC, ""),
         [_afiche(fmt_pct(t1819.delta_pct), (f"{mm(t1819.delta_pct)} PRODUCCIÓN", "EN PRENDAS Y CALZADO"), "PRENDAS, CUERO Y CALZADO", "DESDE 2023",
                  n(f"Y su empleo: {fmt_pct(e1819.delta_pct)}.", fmt_pct(e1819.delta_pct)), AMBAS, ""),
          _afiche(fmt_pct(e17.delta_pct), (f"{mm(e17.delta_pct)} EMPLEO", "TEXTIL"), "EMPLEO TEXTIL", "DESDE 2023",
                  f"Se perdió {uno_de_cada(e17.delta_pct)} puestos." if e17.delta_pct < 0 else "Contra 2023.", OEDE, ""),
          _afiche(fmt_pct(x17.d_imp_kg), (f"{mm(x17.d_imp_kg)} TEXTILES", "IMPORTADOS"), "IMPORTACIONES TEXTILES", "DESDE 2023",
                  "En toneladas.", INDEC, ""),
          _afiche(f"{'+' if x17.d_china_pp > 0 else ''}{fmt_num(x17.d_china_pp)} p.p.", (f"{mm(x17.d_china_pp)} CHINA", "EN TEXTILES IMPORTADOS"),
                  "PESO DE CHINA", "DESDE 2023", "Participación en lo importado.", INDEC, "")]),
        (_afiche(_redondo(mas.puestos), (f"{mm(mas.puestos)} EMPLEOS", "DONDE MÁS SE IMPORTÓ"), "CRECIERON MÁS · 8 RAMAS", R_PER,
                 n(f"Exactamente {fmt_miles(mas.puestos)} ({fmt_pct(mas.empleo)}). Sus importaciones crecieron {fmt_pct(mas.imp_usd, False)} (mediana).",
                   fmt_miles(mas.puestos)), AMBAS, ""),
         [_afiche(_redondo(menos.puestos), (f"{mm(menos.puestos)} EMPLEOS", "DONDE MENOS SE IMPORTÓ"), "CRECIERON MENOS", R_PER,
                  n(f"8 ramas. Exactamente {fmt_miles(menos.puestos)} ({fmt_pct(menos.empleo)}).", fmt_miles(menos.puestos)), AMBAS, ""),
          _afiche(_redondo(rp.puestos), (f"{mm(rp.puestos)} EMPLEOS", "EN PRENDAS Y CALZADO"), "LA EXCEPCIÓN", R_PER,
                  n(f"Sus importaciones crecieron {fmt_pct(rp.imp_usd, False)} en dólares y {fmt_pct(rp.imp_ton, False)} en toneladas.",
                    fmt_pct(rp.imp_usd, False)), AMBAS, ""),
          _afiche(fmt_pct(rt.imp_ton).replace(",0%", "%"), (f"{mm(rt.imp_ton)} TEXTILES", "IMPORTADOS"), "TEXTILES · TONELADAS", R_PER,
                  n(f"En dólares, solo {fmt_pct(rt.imp_usd)}. Perdió {fmt_miles(abs(rt.puestos))} empleos.", fmt_pct(rt.imp_usd)), AMBAS, ""),
          _afiche(str(len(resp)), ("RAMAS", "COMPARADAS"), "COINCIDENCIA, NO CAUSA", R_PER,
                  "Mide si las pérdidas coinciden con las importaciones, no si las provocaron.", AMBAS, "", "neu")]),
    ]

    titulos = [
        "Una industria que emplea menos, y de forma muy desigual" if q18.delta_abs < 0 else "Una industria que emplea más, pero de forma desigual",
        "Desde 2023, la industria retrocede" if ipi23.delta_pct < 0 else "Desde 2023, la industria crece",
        "El salario real no volvió a 2018" if sal18.delta_pct < 0 else "El salario real superó a 2018",
        "Textiles y calzado, los más golpeados",
        "¿Coincide con las importaciones? No, salvo en prendas y textiles" if mas.puestos > menos.puestos
        else "¿Coincide con las importaciones? Sí, en empleo",
    ]
    st.subheader("Hallazgos principales")
    html = "".join(_bloque(k + 1, t, [p] + d) for k, (t, (p, d)) in enumerate(zip(titulos, bloques)))
    st.markdown(f'<div class="hallazgos">{html}</div>', unsafe_allow_html=True)
    nota(f"Los hallazgos 1 a 4 usan el último dato publicado de cada fuente (empleo: {q18.trimestre_base} → {q18.trimestre_ultimo}). El 5 responde la pregunta "
         f"y compara promedios anuales 2018 → 2025, el último año completo en todas las fuentes, para que importaciones y empleo midan el mismo período. "
         f"Por eso las cifras cambian: con el último dato pierden empleo {len(pierden)} de {len(ramas)} ramas; con promedios anuales 2018 → 2025, {int((resp.puestos < 0).sum())} de {len(resp)}. "
         "La diferencia es la caída de 2024 a 2026.", titulo="Dos períodos distintos:", color="gray")


def _titulo_evidencia():
    st.subheader("Evidencia: la industria y el comercio exterior")
    st.markdown("Los tres gráficos siguientes dan el contexto de los hallazgos: cómo se movieron la industria y el comercio exterior en el período.")


def _grafico_industria():
    series = leer("series_indexadas.csv", ("periodo",))
    ind = series[(series.rama == TOTAL) & (series.periodo >= "2017-01-01")]

    def tramo(metrica):
        g = ind[ind.metrica == metrica].sort_values("periodo")
        return g.loc[g.indice.idxmin()], g.loc[g.indice.idxmax()], g.iloc[-1]

    emp_min, emp_max, emp_ult = tramo("Empleo")
    ipi_min, _, ipi_ult = tramo("Producción (IPI)")
    sal_min, sal_max, sal_ult = tramo("Salario real")
    rec = ind[(ind.metrica == "Producción (IPI)") & (ind.periodo > "2020-12-01") & (ind.periodo <= "2023-12-01")]
    ipi_rec = rec.loc[rec.indice.idxmax()]

    with bloque("1. La industria en un gráfico"):
        fig = lineas(ind, "periodo", "indice", "metrica", COLOR_METRICA, y_titulo="Índice (promedio 2023 = 100)", base100=True,
                     alto=300, orden=["Empleo", "Producción (IPI)", "Salario real"], formato="%{y:.1f}")
        figura(
            fig,
            que="Empleo registrado, producción física (IPI) y salario real del conjunto de la industria manufacturera, todos como promedio móvil de "
                "12 meses (4 trimestres en el caso del empleo) y expresados como índice, con el promedio de 2023 igual a 100.",
            como="La línea punteada es el nivel de 2023: una serie por encima estaba mejor que ese año y por debajo, peor. Como cada serie está en una unidad "
                 "distinta (puestos, volumen, pesos constantes), lo comparable es su trayectoria, no su nivel. Al ser promedios de 12 meses, los cambios aparecen "
                 "suavizados y algunos meses después de ocurrir. Cada serie llega hasta su último dato publicado.",
            observa=f"Las tres cayeron en 2020: la producción tocó su piso de {fmt_num(ipi_min.indice)} en {fmt_mes(ipi_min.periodo)} y el empleo el suyo de "
                    f"{fmt_num(emp_min.indice)} en el {trimestre_texto(emp_min.periodo)}. La recuperación llevó al empleo a su máximo ({fmt_num(emp_max.indice)} en el {trimestre_texto(emp_max.periodo)}) "
                    f"y a la producción a un máximo de {fmt_num(ipi_rec.indice)} en {fmt_mes(ipi_rec.periodo)}. Desde entonces la producción cae hasta {fmt_num(ipi_ult.indice)} "
                    f"({fmt_mes(ipi_ult.periodo)}) y el empleo hasta {fmt_num(emp_ult.indice)} ({trimestre_texto(emp_ult.periodo)}). El salario real parte de {fmt_num(sal_max.indice)} "
                    f"en {fmt_mes(sal_max.periodo)}, toca {fmt_num(sal_min.indice)} en {fmt_mes(sal_min.periodo)} y remonta a {fmt_num(sal_ult.indice)} en {fmt_mes(sal_ult.periodo)}.",
            tener_en_cuenta=f"El salario real empieza en {fmt_mes(sal_max.periodo)} porque necesita 12 meses de IPC (que se publica en continuo desde dic-2016).",
        )


def _grafico_comercio():
    comercio = leer("resumen_comercio_anual.csv")
    c25, c24 = comercio.iloc[-1], comercio.iloc[-2]
    y = comercio.assign(imp=comercio.imp_cif / 1e9, exp=comercio.exp_fob / 1e9)
    y["saldo"] = y.exp - y.imp
    var_imp = y.imp.pct_change() * 100
    i_min, i_max = y.loc[y.imp.idxmin()], y.loc[y.imp.idxmax()]
    caida = y.loc[var_imp.idxmin()]
    deficit = [str(int(a)) for a in y[y.saldo < 0].anio]

    with bloque("2. Comercio exterior de bienes"):
        d = pd.concat([y.assign(serie="Importaciones", v=y.imp), y.assign(serie="Exportaciones", v=y.exp)])
        fig = lineas(d, "anio", "v", "serie", {"Importaciones": NARANJA, "Exportaciones": AZUL}, y_titulo="USD miles de millones",
                     alto=290, formato="%{y:.1f}")
        fig.update_xaxes(type="category")
        figura(
            fig,
            que="Importaciones (valor CIF, que incluye flete y seguro) y exportaciones (valor FOB) argentinas de bienes, por año, en miles de millones de "
                "dólares corrientes. Incluye todos los bienes (combustibles, productos agropecuarios, manufacturas), no solo los industriales.",
            como="Cuando la línea naranja (importaciones) queda por encima de la azul (exportaciones), el país compró al exterior más de lo que vendió (déficit "
                 "comercial de bienes); cuando queda por debajo, hay superávit. Los valores son nominales, sin ajustar por inflación internacional.",
            observa=f"Las importaciones tuvieron un mínimo de USD {fmt_num(i_min.imp)} mil M en {int(i_min.anio)} y un máximo de USD {fmt_num(i_max.imp)} mil M en {int(i_max.anio)}. "
                    f"La mayor caída anual fue en {int(caida.anio)} ({fmt_pct(var_imp.loc[caida.name])}), mientras las exportaciones crecían: por eso el saldo "
                    f"pasó a ser positivo. Solo hubo déficit en {', '.join(deficit)}. En 2025 las importaciones subieron {fmt_pct((c25.imp_cif / c24.imp_cif - 1) * 100)} "
                    f"hasta USD {fmt_num(c25.imp_cif / 1e9)} mil M, con saldo positivo de USD {fmt_num(y.saldo.iloc[-1])} mil M.",
            tener_en_cuenta="Al comparar CIF con FOB el saldo queda algo subestimado (el CIF incluye costos de transporte). Es un cálculo orientativo, no la balanza oficial.",
        )


def _grafico_china():
    comercio = leer("resumen_comercio_anual.csv")
    c25, c24 = comercio.iloc[-1], comercio.iloc[-2]
    previo = comercio[comercio.anio < c25.anio].pct_china

    with bloque("3. China como origen de las importaciones"):
        fig = lineas(comercio.assign(serie="China", v=comercio.pct_china), "anio", "v", "serie", {"China": NARANJA},
                     y_titulo="% del valor importado", alto=270, formato="%{y:.1f}%")
        fig.update_xaxes(type="category")
        fig.update_yaxes(rangemode="tozero")
        figura(
            fig,
            que="Qué proporción del valor total importado cada año proviene de China, sobre el total de bienes importados.",
            como="Es una participación (parte del total), no un monto: puede subir aunque las compras a China no crezcan si caen las de otros orígenes. El eje "
                 "parte de cero para no exagerar los cambios.",
            observa=f"Entre {int(comercio.anio.min())} y {int(c24.anio)} la participación se movió en una franja estrecha, de {fmt_num(previo.min())}% a {fmt_num(previo.max())}% "
                    f"(el máximo fue en {int(comercio.loc[previo.idxmax()].anio)}). En {int(c25.anio)} saltó a {fmt_num(c25.pct_china)}%, el valor más alto de toda la serie y "
                    f"{fmt_num(c25.pct_china - c24.pct_china)} puntos porcentuales por encima de {int(c24.anio)}. El detalle por rama está en «Importaciones».",
            tener_en_cuenta="Es una participación en valor: China aparece con más peso en dólares que en toneladas (ver «Importaciones»).",
        )


def _guia():
    st.subheader("Cómo seguir leyendo")
    st.table(pd.DataFrame([
        ("Importaciones", "¿De dónde vienen las importaciones, qué ramas las reciben y cuánto avanzó China?"),
        ("Empleo y ramas", "¿Cuántos puestos ganó o perdió cada rama y cómo cambiaron su salario, producción y empresas?"),
        ("Importaciones vs. resultados", "¿Se perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones?"),
        ("Comparador de ramas", "¿Cómo le fue a una rama en particular frente al total de la industria?"),
        ("Método y límites", "¿Cómo se construyó el análisis, qué controles se hicieron y qué no se puede concluir?"),
    ], columns=["Página", "Qué responde"]).set_index("Página"))


def mostrar():
    _introduccion()
    _indicadores()
    _hallazgos()
    _titulo_evidencia()
    _grafico_industria()
    _grafico_comercio()
    _grafico_china()
    _guia()
