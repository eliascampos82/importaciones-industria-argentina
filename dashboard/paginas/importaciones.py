"""Página «Importaciones»: origen, ramas receptoras, avance de China, valor/volumen/precio y balanza comercial por rama."""
import pandas as pd
import streamlit as st

from core.datos import RAMAS, leer, nombre
from core.formato import fmt_num, fmt_pct
from core.graficos import barras_apiladas, barras_signo, dumbbell, heatmap, lineas
from core.tema import AMARILLO, AQUA, AZUL, COLOR_ORIGEN, ESCALA_DIVERGENTE, GRIS, NARANJA
from core.ui import bloque, figura, sintesis

ORIGENES = ["Brasil", "China", "Estados Unidos", "Alemania"]
ORDEN_ORIGEN = ORIGENES + ["Resto del mundo"]


def _introduccion():
    st.markdown(
        """
Esta página describe las **importaciones argentinas de bienes entre 2016 y 2025** (INDEC, sistema de comercio exterior): de qué países vienen,
qué ramas industriales las reciben, dónde avanzó China y cuál es la balanza comercial de cada rama. Los años están validados contra los totales
de control de INDEC (ver «Método y límites»).

Los valores son **CIF** (incluyen flete y seguro) en **dólares corrientes**, es decir, sin descontar la inflación internacional. Las **toneladas**
sirven para separar dos fenómenos que el valor mezcla: importar *más cantidad* o importar *lo mismo a otro precio*. El selector de abajo cambia
la unidad de las secciones 1, 2 y 3.

**Para la pregunta central:** la sección 3 muestra la medida que usa la respuesta (cuánto crecieron las importaciones de cada rama desde 2018) y la sección 7
separa lo que se importa según su uso: **bienes de consumo**, que compiten con lo que fabrica la industria, e **insumos y bienes de capital**, que la abastecen.
"""
    )


def _medida():
    m = st.segmented_control("Medir las importaciones en", ["Valor (USD)", "Toneladas"], default="Valor (USD)", key="imp_metrica") or "Valor (USD)"
    return m == "Valor (USD)"


def _por_origen(imp, columna):
    d = imp.assign(origen=imp.pais.where(imp.pais.isin(ORIGENES), "Resto del mundo"))
    g = d.groupby(["anio", "origen"], as_index=False)[columna].sum()
    g["v"] = g[columna] / 1e9
    g["pct"] = g.v / g.groupby("anio").v.transform("sum") * 100
    return g


def _origen_niveles(imp, es_valor):
    col = "cif_usd" if es_valor else "peso_neto_kg"
    unidad = "USD miles de millones" if es_valor else "millones de toneladas"
    lab = "USD mil M" if es_valor else "M de toneladas"
    g = _por_origen(imp, col)
    tot = g.groupby("anio").v.sum()
    china = g[g.origen == "China"].set_index("anio").v
    a_min, a_max = tot.idxmin(), tot.idxmax()

    with bloque("1. Cuánto se importa y de dónde"):
        figura(
            barras_apiladas(g, "anio", "v", "origen", COLOR_ORIGEN, ORDEN_ORIGEN, y_titulo=unidad, alto=290),
            que=f"El total importado cada año ({'valor CIF' if es_valor else 'peso neto'}), partido entre los cuatro orígenes más importantes (Brasil, China, Estados Unidos y "
                "Alemania) y el resto del mundo.",
            como="La altura total de la barra es lo importado en el año; cada color es el aporte de un origen. Sirve para ver cuánto se importó en total y "
                 "qué origen explica los cambios; para comparar pesos relativos conviene el gráfico siguiente, que lleva todo a porcentajes.",
            observa=f"El total tuvo su mínimo en {a_min} ({fmt_num(tot[a_min])} {lab}) y su máximo en {a_max} ({fmt_num(tot[a_max])} {lab}); en 2025 fue "
                    f"{fmt_pct((tot[2025] / tot[2018] - 1) * 100)} respecto de 2018. Lo importado desde China pasó de {fmt_num(china[2016])} a {fmt_num(china[2025])} {lab} entre 2016 y 2025 "
                    f"({fmt_pct((china[2025] / china[2016] - 1) * 100)}), un aumento {'mayor' if china[2025] / china[2016] > tot[2025] / tot[2016] else 'menor'} que el del total ({fmt_pct((tot[2025] / tot[2016] - 1) * 100)}).",
            tener_en_cuenta="En valor, los movimientos de un año a otro mezclan cantidad y precio, además de la evolución del dólar; por eso conviene contrastar con el modo «Toneladas».",
        )
    return (f"En 2025 se importó {fmt_pct((tot[2025] / tot[2018] - 1) * 100)} más que en 2018 (en {'valor' if es_valor else 'toneladas'}); "
            f"lo proveniente de China creció {fmt_pct((china[2025] / china[2016] - 1) * 100)} desde 2016.")


def _origen_participacion(imp, es_valor):
    col = "cif_usd" if es_valor else "peso_neto_kg"
    g = _por_origen(imp, col)
    g = g[g.origen.isin(ORIGENES)]
    p = g.pivot(index="anio", columns="origen", values="pct")
    ch_val = _por_origen(imp, "cif_usd").query("origen == 'China' and anio == 2025").pct.iloc[0]
    ch_kg = _por_origen(imp, "peso_neto_kg").query("origen == 'China' and anio == 2025").pct.iloc[0]
    ranking = p.loc[2025].sort_values(ascending=False)

    with bloque("2. Cuánto pesa cada origen"):
        fig = lineas(g, "anio", "pct", "origen", COLOR_ORIGEN, y_titulo="% del total importado", alto=290, formato="%{y:.1f}%", orden=ORIGENES)
        fig.update_xaxes(type="category")
        figura(
            fig,
            que=f"La participación de cada origen en el total importado del año, medida en {'valor' if es_valor else 'toneladas'}. El resto de los países no se muestra "
                "(es lo que falta para llegar al 100%).",
            como="Una línea que sube significa que ese origen gana lugar frente a los demás, aunque sus compras absolutas no crezcan. Brasil y China son "
                 "los orígenes principales; Estados Unidos y Alemania son referencias más estables.",
            observa=f"China pasó de {fmt_num(p.China.loc[2016])}% en 2016 a {fmt_num(p.China.loc[2025])}% en 2025 (mínimo de {fmt_num(p.China.min())}% en {p.China.idxmin()}). "
                    f"En 2025 el orden es {ranking.index[0]} ({fmt_num(ranking.iloc[0])}%), {ranking.index[1]} ({fmt_num(ranking.iloc[1])}%), {ranking.index[2]} ({fmt_num(ranking.iloc[2])}%) y "
                    f"{ranking.index[3]} ({fmt_num(ranking.iloc[3])}%). Brasil se movió entre {fmt_num(p.Brasil.min())}% y {fmt_num(p.Brasil.max())}%; Estados Unidos "
                    f"perdió lugar hasta {fmt_num(p['Estados Unidos'].loc[2025])}% en 2025.",
            tener_en_cuenta=f"En 2025 China representa {fmt_num(ch_val)}% del valor pero {fmt_num(ch_kg)}% de las toneladas: lo que se compra a China es, en promedio, "
                            "más caro por kilo (manufacturas) que el conjunto de las importaciones. Por eso su peso cambia según la unidad.",
        )
    return f"China concentra {fmt_num(ch_val)}% del valor importado en 2025 pero solo {fmt_num(ch_kg)}% de las toneladas."


def _mapa_ramas(com, es_valor):
    col = "imp_cif" if es_valor else "imp_kg"
    piv = com.pivot(index="rama", columns="anio", values=col)
    crec = (piv.div(piv[2018], axis=0) - 1) * 100
    crec = crec[[a for a in crec.columns if a >= 2019]]
    crec = crec.loc[[r for r in RAMAS if r in crec.index]].sort_values(2025, ascending=False)
    n_pand = int((crec[2020] < 0).sum())
    n_25 = int((crec[2025] > 0).sum())
    sube, baja = crec[2025].head(3), crec[2025].tail(2)
    crec.index = [nombre(r) for r in crec.index]
    sube.index, baja.index = [nombre(r) for r in sube.index], [nombre(r) for r in baja.index]

    with bloque("3. Cuánto crecieron las importaciones de cada rama respecto de 2018"):
        fig = heatmap(crec, escala=ESCALA_DIVERGENTE, rango=100, sufijo="%", decimales=0, colorbar_titulo="% vs 2018", alto=470)
        figura(
            fig,
            que=f"La variación porcentual anual de las importaciones ({'en dólares' if es_valor else 'en toneladas'}) de cada rama industrial contra su propio valor de 2018, "
                "que es el año base. Cada fila es una rama y cada columna un año; las filas están ordenadas por lo ocurrido en 2025.",
            como="Naranja: la rama importa más que en 2018; azul: importa menos. El color se satura en ±100% para que los extremos no tapen al resto, pero el número de cada "
                 "celda es el dato real. Leyendo una fila de izquierda a derecha se ve la trayectoria de esa rama; leyendo una columna, cuáles ramas empujan en ese año.",
            observa=f"En 2020, {n_pand} de las 16 ramas importaban menos que en 2018 (recesión y pandemia). En 2025, {n_25} de 16 superan el nivel de 2018. Los mayores aumentos son "
                    f"{sube.index[0]} ({fmt_pct(sube.iloc[0], False)}), {sube.index[1]} ({fmt_pct(sube.iloc[1], False)}) y {sube.index[2]} ({fmt_pct(sube.iloc[2], False)}); "
                    f"caen {baja.index[0]} ({fmt_pct(baja.iloc[0], False)}) y {baja.index[1]} ({fmt_pct(baja.iloc[1], False)}).",
            tener_en_cuenta="Una rama puede aparecer estable en dólares y creciendo en toneladas si bajaron los precios (ver la sección 5). Los valores en dólares son corrientes.",
        )
    return f"En 2025, {n_25} de 16 ramas importan más que en 2018, con subas fuertes en {sube.index[0]} y {sube.index[1]}."


def _china_por_rama(com):
    c = com[com.anio.isin([2018, 2025])].pivot(index="rama", columns="anio", values="pct_china").reset_index()
    c["etiqueta"] = c.rama.map(nombre)
    c["cambio"] = c[2025] - c[2018]
    mayor = c.sort_values("cambio", ascending=False).head(3)
    mayoria = c[c[2025] >= 50].sort_values(2025, ascending=False)
    n_sube = int((c.cambio > 0).sum())
    baja = c[c.cambio < -0.5].sort_values("cambio")
    grandes = com[com.anio == 2025].sort_values("imp_cif", ascending=False).head(2).merge(c[["rama", "etiqueta"]], on="rama")

    with bloque("4. Dónde más avanzó China"):
        fig = dumbbell(c, "etiqueta", 2018, 2025, "2018", "2025", x_titulo="% de las importaciones de la rama que vienen de China",
                       alto=340, c0=GRIS, c1=NARANJA)
        figura(
            fig,
            que="Qué porcentaje del valor importado por cada rama industrial proviene de China, en 2018 (punto gris) y en 2025 (punto naranja).",
            como="Cada fila une los dos puntos: una línea larga hacia la derecha indica que China ganó mucho terreno en esa rama, y hacia la izquierda que lo perdió. "
                 "La posición horizontal es el nivel (cuánto de lo que importa la rama viene de China); la longitud de la línea es el cambio.",
            observa=f"China ganó peso en {n_sube} de las 16 ramas. Los mayores avances fueron " + ", ".join(f"{r.etiqueta} ({fmt_num(r[2018], 0)}% → {fmt_num(r[2025], 0)}%)" for _, r in mayor.iterrows())
                    + ". En 2025 China provee la mitad o más de lo importado en " + ", ".join(f"{r.etiqueta} ({fmt_num(r[2025], 0)}%)" for _, r in mayoria.iterrows())
                    + (". Perdió terreno en " + ", ".join(f"{r.etiqueta} ({fmt_num(r.cambio, 1)} p.p.)" for _, r in baja.iterrows()) if len(baja) else "") + ".",
            tener_en_cuenta="Los porcentajes no pesan igual en todas las ramas: las que más importan en dólares son " + " y ".join(
                f"{r.etiqueta} (USD {fmt_num(r.imp_cif / 1e9)} mil M, {fmt_num(r.pct_china, 0)}% de China)" for r in grandes.itertuples()) + ".",
        )
    return (f"China ganó participación en {n_sube} de 16 ramas y provee más de la mitad de lo importado en "
            f"{', '.join(mayoria.etiqueta)}.")


def _precio_kilo(fila):
    return fila.imp_cif / fila.imp_kg


def _valor_volumen_precio(com):
    with bloque("5. Valor, volumen y precio de las importaciones de una rama"):
        sel = st.selectbox("Rama", RAMAS, index=RAMAS.index("17"), format_func=nombre, key="imp_rama")
        r = com[com.rama == sel].sort_values("anio")
        b = r[r.anio == 2018].iloc[0]
        u = r[r.anio == 2025].iloc[0]
        serie = pd.concat([
            pd.DataFrame({"anio": r.anio, "serie": "Valor (USD)", "v": r.imp_cif / b.imp_cif * 100}),
            pd.DataFrame({"anio": r.anio, "serie": "Toneladas", "v": r.imp_kg / b.imp_kg * 100}),
            pd.DataFrame({"anio": r.anio, "serie": "Precio por kilo", "v": (r.imp_cif / r.imp_kg) / _precio_kilo(b) * 100}),
        ])
        d_val, d_kg, d_pre = (u.imp_cif / b.imp_cif - 1) * 100, (u.imp_kg / b.imp_kg - 1) * 100, (_precio_kilo(u) / _precio_kilo(b) - 1) * 100
        if d_kg > d_val + 5:
            lectura = "Las toneladas subieron más que el valor: se está importando más volumen a un precio por kilo menor."
        elif d_val > d_kg + 5:
            lectura = "El valor subió más que las toneladas: el precio por kilo (o el tipo de producto importado) se encareció."
        else:
            lectura = "Valor y toneladas se movieron parecido: el precio por kilo casi no cambió."
        minimo = r.loc[r.imp_cif.idxmin()]
        fig = lineas(serie, "anio", "v", "serie", {"Valor (USD)": AZUL, "Toneladas": NARANJA, "Precio por kilo": AQUA},
                     y_titulo="Índice (2018 = 100)", base100=True, alto=300, formato="%{y:.0f}",
                     orden=["Valor (USD)", "Toneladas", "Precio por kilo"])
        fig.update_xaxes(type="category")
        figura(
            fig,
            que=f"Para la rama «{nombre(sel)}», tres series de importaciones con 2018 = 100: el valor en dólares, el peso en toneladas y el precio implícito por kilo "
                "(valor dividido por toneladas).",
            como="Las tres líneas parten de 100 en 2018. Si la de toneladas queda por encima de la de valor, el precio por kilo cayó (línea verde por debajo de 100); si queda "
                 "por debajo, el precio por kilo subió. El precio implícito cambia tanto por los precios internacionales como por el tipo de producto que se importa.",
            observa=f"Entre 2018 y 2025 el valor importado varió {fmt_pct(d_val)}, las toneladas {fmt_pct(d_kg)} y el precio por kilo {fmt_pct(d_pre)}. {lectura} "
                    f"El piso de importaciones en valor fue en {int(minimo.anio)}, a {fmt_num(minimo.imp_cif / b.imp_cif * 100, 0)} sobre 100.",
            tener_en_cuenta="Cambiá la rama en el selector: el patrón varía mucho entre ramas, y en las de insumos o productos muy heterogéneos el precio por kilo es poco informativo.",
        )


def _balanza(com):
    with bloque("6. Balanza comercial por rama"):
        anios = sorted(com.dropna(subset=["balanza"]).anio.unique())
        anio = st.segmented_control("Año", anios, default=anios[-1], key="bal_anio") or anios[-1]
        b = com[com.anio == anio].dropna(subset=["balanza"]).assign(etiqueta=lambda x: x.rama.map(nombre), v=lambda x: x.balanza / 1e6)
        deficit, superavit = b[b.v < 0].sort_values("v"), b[b.v > 0].sort_values("v", ascending=False)
        total = b.v.sum() / 1e3
        fig = barras_signo(b, "v", "etiqueta", x_titulo="USD millones", formato="{:+,.0f}", alto=340)
        figura(
            fig,
            que=f"Exportaciones FOB menos importaciones FOB de cada rama industrial en {anio}, en millones de dólares. Azul es superávit (la rama exporta más de lo que importa) "
                "y naranja es déficit.",
            como="Cuanto más larga la barra, mayor el saldo, en un sentido u otro. Las ramas están ordenadas de mayor déficit a mayor superávit. Un déficit grande no es "
                 "por sí solo bueno o malo: indica dependencia de insumos o bienes importados en esa rama.",
            observa=f"En {anio}, {len(deficit)} de las 16 ramas tienen déficit. Los más grandes son " + ", ".join(f"{r.etiqueta} ({fmt_num(r.v, 0)})" for r in deficit.head(3).itertuples())
                    + "; " + (f"solo {' y '.join(superavit.etiqueta)} tienen superávit" if len(superavit) else "ninguna tiene superávit")
                    + f". La suma de las 16 ramas es de USD {fmt_num(total)} mil M.",
            tener_en_cuenta="Es el saldo de las 16 ramas industriales: excluye combustibles sin refinar y otros productos primarios, por eso no coincide con el saldo total del Resumen. "
                            "Desde 2018 INDEC oculta cerca de 5% de las exportaciones por secreto estadístico (no se asignan a ninguna rama) y el FOB de importaciones solo existe desde 2019, "
                            "por lo que el selector empieza ese año.",
        )
    return (f"En {anio} la suma de los saldos de las 16 ramas es de USD {fmt_num(total)} mil M: "
            f"{len(deficit)} ramas con déficit, encabezadas por {deficit.iloc[0].etiqueta} y {deficit.iloc[1].etiqueta}.")


COLOR_USO = {"Consumo": NARANJA, "Insumos": AZUL, "Capital": AMARILLO}


def _uso_economico():
    u = leer("importaciones_por_uso.csv")
    u = u[u.uso.isin(COLOR_USO)]
    with bloque("7. Qué tipo de bienes se importan: consumo, insumos y capital"):
        opciones = ["todas"] + RAMAS
        sel = st.selectbox("Rama", opciones, format_func=lambda r: "Las 16 ramas industriales" if r == "todas" else nombre(r), key="imp_uso_rama")
        d = u if sel == "todas" else u[u.rama == sel]
        g = d.groupby(["anio", "uso"], as_index=False).imp_cif.sum().assign(v=lambda x: x.imp_cif / 1e9)
        piv = g.pivot(index="anio", columns="uso", values="imp_cif").fillna(0)
        peso = piv.div(piv.sum(axis=1), axis=0) * 100
        crec = (piv.loc[2025] / piv.loc[2018].replace(0, float("nan")) - 1) * 100
        quien = "las 16 ramas" if sel == "todas" else f"«{nombre(sel)}»"
        partes = [f"{k.lower()} {fmt_pct(crec[k])}" for k in COLOR_USO if k in crec and pd.notna(crec[k])]
        fig = barras_apiladas(g, "anio", "v", "uso", COLOR_USO, orden=[k for k in COLOR_USO if k in set(g.uso)], y_titulo="USD miles de millones (CIF)", alto=300)
        figura(
            fig,
            que=f"Las importaciones de {quien} cada año, separadas según su uso económico (clasificación BEC de Naciones Unidas): bienes de consumo, insumos (materias primas, partes, "
                "combustibles) y bienes de capital (máquinas y equipo).",
            como="Cada barra es un año y cada color, un tipo de bien. Los bienes de consumo son los que compiten con lo que vende la industria local; los insumos y el capital crecen cuando "
                 "la industria produce más, porque los compra para producir.",
            observa=(f"Los bienes de consumo fueron {fmt_num(peso.loc[2018].get('Consumo', 0), 0)}% de lo importado en 2018 y {fmt_num(peso.loc[2025].get('Consumo', 0), 0)}% en 2025, "
                     f"con un mínimo de {fmt_num(peso.get('Consumo', peso.iloc[:, 0] * 0).min(), 0)}% en {int(peso.get('Consumo', peso.iloc[:, 0] * 0).idxmin())}. "
                     f"Entre 2018 y 2025 variaron: {', '.join(partes)}." if partes else "Esta rama casi no importa estos bienes."),
            tener_en_cuenta="Cada producto se clasifica por su uso más habitual y se asigna a la rama que lo fabrica: un auto de pasajeros cuenta como consumo en Automotores y el acero como insumo "
                            "en Metálicas básicas, aunque también compita con las acerías locales. Valores en dólares corrientes.",
        )
    total = u.groupby(["anio", "uso"]).imp_cif.sum().unstack()
    pc = total["Consumo"] / total.sum(axis=1) * 100
    return (f"Los bienes de consumo, que son los que compiten con la producción local, fueron {fmt_num(pc[2018], 0)}% de lo importado por las 16 ramas en 2018 y {fmt_num(pc[2025], 0)}% en 2025; "
            f"en el medio bajaron hasta {fmt_num(pc.min(), 0)}% en {int(pc.idxmin())}. La mayor parte de lo que importa la industria son insumos.")


def mostrar():
    imp = leer("importaciones_rama_pais_anio.csv")
    com = leer("comercio_por_rama_anio.csv")

    _introduccion()
    es_valor = _medida()
    conclusiones = [
        _origen_niveles(imp, es_valor),
        _origen_participacion(imp, es_valor),
        _mapa_ramas(com, es_valor),
        _china_por_rama(com),
    ]
    _valor_volumen_precio(com)
    conclusiones.append(_balanza(com))
    conclusiones.append(_uso_economico())
    sintesis(conclusiones)
