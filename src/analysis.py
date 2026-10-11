"""Series suavizadas, ventanas de comparación, comercio exterior y modelos por rama.

Decisiones metodológicas (importan para no sacar conclusiones falsas):
  - Salario real = remuneración nominal "por todo concepto" / IPC. Esa remuneración incluye el
    aguinaldo (junio y diciembre), así que un mes suelto no es comparable con otro: se compara
    siempre promedios de 12 meses.
  - El IPI tiene estacionalidad fuerte (diciembre y enero son meses bajos): también promedios de 12 meses.
  - Empleo trimestral: promedios de 4 trimestres.
  - Los "totales" son sobre la industria manufacturera (CIIU 15-37), no sobre toda la economía.
  - El salario de una rama (y del total) es promedio ponderado por puestos de trabajo de cada CIIU2.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests

from ramas import TOTAL

BASES = (2018, 2023)
MESES_ES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


# ------------------------------------------------------------- series base por rama
def empleo_por_rama(emp: pd.DataFrame) -> pd.DataFrame:
    por_rama = emp.groupby(["rama", "periodo"], as_index=False).puestos.sum()
    total = emp.groupby("periodo", as_index=False).puestos.sum().assign(rama=TOTAL)
    return pd.concat([por_rama, total], ignore_index=True)


def empresas_por_rama(emp2: pd.DataFrame) -> pd.DataFrame:
    df = emp2.copy()
    df["periodo"] = pd.to_datetime(df["anio"].astype(str) + "-01-01")
    por_rama = df.groupby(["rama", "periodo"], as_index=False).empresas.sum()
    total = df.groupby("periodo", as_index=False).empresas.sum().assign(rama=TOTAL)
    return pd.concat([por_rama, total], ignore_index=True)


def salario_real_ponderado(sal: pd.DataFrame, emp: pd.DataFrame, ipc: pd.DataFrame) -> pd.DataFrame:
    """Salario real por rama y total, ponderado por puestos de cada CIIU2 (mensual desde dic-2016)."""
    df = sal.merge(ipc, on="periodo", how="inner")
    df["salario_real"] = df["salario_nominal"] / df["ipc"] * 100

    pesos = emp[["ciiu2", "periodo", "puestos"]].rename(columns={"periodo": "trim", "puestos": "peso"})
    df["trim"] = df["periodo"].dt.to_period("Q").dt.to_timestamp()
    # el empleo llega hasta el último trimestre publicado: para meses posteriores se usa ese peso
    df = pd.merge_asof(df.sort_values("trim"), pesos.sort_values("trim"),
                       on="trim", by="ciiu2", direction="backward")
    df["wx"] = df["salario_real"] * df["peso"]

    por_rama = df.groupby(["rama", "periodo"], as_index=False).agg(wx=("wx", "sum"), w=("peso", "sum"))
    total = df.groupby("periodo", as_index=False).agg(wx=("wx", "sum"), w=("peso", "sum")).assign(rama=TOTAL)
    out = pd.concat([por_rama, total], ignore_index=True)
    out["salario_real"] = out["wx"] / out["w"]
    return out[["rama", "periodo", "salario_real"]]


def ipi_por_rama(ipi: pd.DataFrame) -> pd.DataFrame:
    return ipi[ipi["nivel"].isin(["rama", "total"])][["rama", "periodo", "ipi"]].reset_index(drop=True)


# ------------------------------------------------------------ series suavizadas / indexadas
def suavizar_e_indexar(df: pd.DataFrame, valor: str, ventana: int, base_year: int = 2023) -> pd.DataFrame:
    """Media móvil de `ventana` períodos, indexada a 100 = promedio del año base."""
    df = df.sort_values(["rama", "periodo"]).copy()
    df["suavizado"] = df.groupby("rama")[valor].transform(lambda s: s.rolling(ventana, min_periods=ventana).mean())
    base = df[df["periodo"].dt.year == base_year].groupby("rama")[valor].mean().rename("base")
    df = df.join(base, on="rama")
    df["indice"] = df["suavizado"] / df["base"] * 100
    return df.dropna(subset=["indice"])[["rama", "periodo", "suavizado", "indice"]]


def series_indexadas(empleo, salario, ipi) -> pd.DataFrame:
    partes = [
        suavizar_e_indexar(empleo, "puestos", 4).assign(metrica="Empleo"),
        suavizar_e_indexar(salario, "salario_real", 12).assign(metrica="Salario real"),
        suavizar_e_indexar(ipi, "ipi", 12).assign(metrica="Producción (IPI)"),
    ]
    return pd.concat(partes, ignore_index=True)


# --------------------------------------------------------------------- ventanas de cambio
def _fin_texto(periodo: pd.Timestamp, frecuencia: str) -> str:
    if frecuencia == "T":
        return f"{(periodo.month - 1) // 3 + 1}T {periodo.year}"
    if frecuencia == "M":
        return f"{MESES_ES[periodo.month - 1]} {periodo.year}"
    return str(periodo.year)


def _cambios(df, valor, n_final, frecuencia, metrica, unidad):
    filas = []
    for base_year in BASES:
        for rama, g in df.groupby("rama"):
            g = g.sort_values("periodo")
            g_base = g[g["periodo"].dt.year == base_year]
            if g_base.empty:
                continue
            g_ult = g.tail(n_final)
            base, ultimo = g_base[valor].mean(), g_ult[valor].mean()
            filas.append(dict(
                rama=rama, ventana=str(base_year), metrica=metrica, unidad=unidad,
                base=base, ultimo=ultimo, delta_abs=ultimo - base, delta_pct=(ultimo / base - 1) * 100,
                fin=_fin_texto(g_ult["periodo"].max(), frecuencia),
            ))
    return pd.DataFrame(filas)


def cambios_por_rama(empleo, salario, ipi, empresas) -> pd.DataFrame:
    """Promedio del año base vs. promedio de los últimos 12 meses (4 trimestres / último año) disponibles."""
    return pd.concat([
        _cambios(empleo, "puestos", 4, "T", "Empleo", "puestos de trabajo"),
        _cambios(salario, "salario_real", 12, "M", "Salario real", "pesos constantes"),
        _cambios(ipi, "ipi", 12, "M", "Producción (IPI)", "índice base 2004=100"),
        _cambios(empresas, "empresas", 1, "A", "Empresas", "empresas activas"),
    ], ignore_index=True)


def empleo_mismo_trimestre(empleo: pd.DataFrame) -> pd.DataFrame:
    """Último trimestre publicado vs. el mismo trimestre de los años base (sin efecto estacional)."""
    ultimo = empleo["periodo"].max()
    mismo = empleo[empleo["periodo"].dt.month == ultimo.month]
    filas = []
    for base_year in BASES:
        b = mismo[mismo["periodo"].dt.year == base_year].set_index("rama")["puestos"]
        u = mismo[mismo["periodo"] == ultimo].set_index("rama")["puestos"]
        d = pd.DataFrame({"base": b, "ultimo": u}).dropna()
        d["delta_abs"] = d["ultimo"] - d["base"]
        d["delta_pct"] = (d["ultimo"] / d["base"] - 1) * 100
        d["ventana"] = str(base_year)
        d["trimestre_base"] = _fin_texto(pd.Timestamp(year=base_year, month=ultimo.month, day=1), "T")
        d["trimestre_ultimo"] = _fin_texto(ultimo, "T")
        filas.append(d.reset_index())
    return pd.concat(filas, ignore_index=True)


def ipi_subramas(ipi: pd.DataFrame):
    """Detalle de producción por subrama (ej. calzado, muebles, informática): nombres, serie indexada y cambios."""
    sub = ipi[ipi["nivel"] == "subrama"]
    nombres = (sub.drop_duplicates("codigo").set_index("codigo")[["nombre", "rama"]]
               .rename(columns={"rama": "rama_padre"}).reset_index())
    serie = sub[["codigo", "periodo", "ipi"]].rename(columns={"codigo": "rama"})
    indexada = suavizar_e_indexar(serie, "ipi", 12).rename(columns={"rama": "codigo"})
    cambios = _cambios(serie, "ipi", 12, "M", "Producción (IPI)", "índice base 2004=100").rename(columns={"rama": "codigo"})
    return nombres, indexada, cambios


# ---------------------------------------------------------------- comercio exterior por rama
def comercio_anual(imp_rama_pais: pd.DataFrame, exp_rama: pd.DataFrame) -> pd.DataFrame:
    """Importaciones (CIF, FOB, kg), importaciones desde China y exportaciones FOB, por rama y año."""
    imp = imp_rama_pais[imp_rama_pais["rama"] != "NO_IND"]
    total = imp.groupby(["rama", "anio"], as_index=False).agg(
        imp_cif=("cif_usd", "sum"), imp_fob=("fob_usd", lambda s: s.sum(min_count=1)), imp_kg=("peso_neto_kg", "sum"))
    china = (imp[imp["pais"] == "China"].groupby(["rama", "anio"], as_index=False)
             .agg(imp_china_cif=("cif_usd", "sum"), imp_china_kg=("peso_neto_kg", "sum")))
    out = total.merge(china, on=["rama", "anio"], how="left").fillna({"imp_china_cif": 0, "imp_china_kg": 0})
    out["pct_china"] = out["imp_china_cif"] / out["imp_cif"] * 100
    exp = (exp_rama[~exp_rama["rama"].isin(["NO_IND", "CONFIDENCIAL"])][["rama", "anio", "fob_usd"]]
           .rename(columns={"fob_usd": "exp_fob"}))
    out = out.merge(exp, on=["rama", "anio"], how="left")
    out["balanza"] = out["exp_fob"] - out["imp_fob"]          # FOB - FOB (las importaciones FOB existen desde 2019)
    return out


def panel_anual(empleo, salario, ipi, comercio) -> pd.DataFrame:
    """Panel rama x año (solo años completos): puestos, salario real, IPI, importaciones y exportaciones."""
    def anual(df, valor, n_min):
        d = df[df["rama"] != TOTAL].assign(anio=lambda x: x["periodo"].dt.year)
        g = d.groupby(["rama", "anio"])[valor].agg(["mean", "count"]).reset_index()
        return g[g["count"] >= n_min].rename(columns={"mean": valor}).drop(columns="count")

    panel = (anual(empleo, "puestos", 4)
             .merge(anual(ipi, "ipi", 12), on=["rama", "anio"], how="outer")
             .merge(anual(salario, "salario_real", 12), on=["rama", "anio"], how="outer"))
    return panel.merge(comercio, on=["rama", "anio"], how="left")


def regresiones_panel(panel: pd.DataFrame) -> pd.DataFrame:
    """Efectos fijos de rama y de año: log(resultado) ~ log(1 + importaciones en millones de USD).

    Los efectos fijos de año absorben lo que le pasa a toda la industria a la vez (devaluaciones, recesiones,
    política macro); los de rama, las diferencias permanentes entre ramas. Lo que queda es la relación entre
    el movimiento de las importaciones de una rama y el de su empleo/producción/salario, respecto de las demás
    ramas ese mismo año. Errores estándar agrupados por rama.
    """
    resultados = [("Empleo", "puestos"), ("Producción (IPI)", "ipi"), ("Salario real", "salario_real")]
    regresores = [("Importaciones totales", "imp_cif"), ("Importaciones desde China", "imp_china_cif")]
    muestras = [("Todas las ramas", None), ("Sin refinación de petróleo", "23")]
    total_puestos = panel[panel["anio"] == panel["anio"].max()]["puestos"].sum()

    filas = []
    for res_lab, res in resultados:
        for reg_lab, reg in regresores:
            for mue_lab, excluir in muestras:
                for rezago in (0, 1):
                    d = panel.sort_values(["rama", "anio"]).copy()
                    d["x"] = np.log1p(d[reg] / 1e6)
                    if rezago:
                        d["x"] = d.groupby("rama")["x"].shift(rezago)
                    d["y"] = np.log(d[res])
                    if excluir:
                        d = d[d["rama"] != excluir]
                    d = d.dropna(subset=["x", "y"])
                    m = smf.ols("y ~ x + C(rama) + C(anio)", data=d).fit(
                        cov_type="cluster", cov_kwds={"groups": pd.factorize(d["rama"])[0]})
                    coef, se = m.params["x"], m.bse["x"]
                    ic = m.conf_int().loc["x"]

                    def por10(b):        # % de cambio en el resultado por cada +10% de importaciones
                        return b * np.log(1.10) * 100

                    filas.append(dict(
                        resultado=res_lab, importaciones=reg_lab, muestra=mue_lab, rezago_anios=rezago,
                        elasticidad=coef, error_estandar=se, p_valor=m.pvalues["x"],
                        ic_bajo=ic[0], ic_alto=ic[1],
                        efecto_10pct=por10(coef), efecto_10pct_bajo=por10(ic[0]), efecto_10pct_alto=por10(ic[1]),
                        puestos_por_10pct=por10(coef) / 100 * total_puestos if res == "puestos" else np.nan,
                        n_obs=int(m.nobs), n_ramas=d["rama"].nunique(),
                    ))
    return pd.DataFrame(filas)


# ------------------------------------------------------------------------- exposición
def exposicion_vs_resultados(cambios: pd.DataFrame, comercio: pd.DataFrame) -> pd.DataFrame:
    """Una fila por rama y ventana: cuánto crecieron las importaciones y cómo evolucionaron empleo, salario, producción."""
    ancho = (cambios[cambios["rama"] != TOTAL]
             .pivot_table(index=["rama", "ventana"], columns="metrica", values="delta_pct").reset_index()
             .rename(columns={"Empleo": "d_empleo", "Salario real": "d_salario",
                              "Producción (IPI)": "d_ipi", "Empresas": "d_empresas"}))
    puestos = (cambios[(cambios["metrica"] == "Empleo") & (cambios["rama"] != TOTAL)]
               [["rama", "ventana", "delta_abs"]].rename(columns={"delta_abs": "d_puestos"}))
    base = ancho.merge(puestos, on=["rama", "ventana"])

    ultimo = comercio["anio"].max()
    filas = []
    for ventana in base["ventana"].unique():
        a = comercio[comercio["anio"] == int(ventana)].set_index("rama")
        b = comercio[comercio["anio"] == ultimo].set_index("rama")
        filas.append(pd.DataFrame({
            "ventana": ventana,
            "d_imp_cif": (b["imp_cif"] / a["imp_cif"] - 1) * 100,
            "d_imp_kg": (b["imp_kg"] / a["imp_kg"] - 1) * 100,
            "d_china_pp": b["pct_china"] - a["pct_china"],
            "pct_china": b["pct_china"],
            "imp_cif_ultimo": b["imp_cif"],
        }).reset_index())
    return base.merge(pd.concat(filas), on=["rama", "ventana"], how="left")


EXPOSICIONES = [("d_imp_cif", "Crecimiento de las importaciones (USD)"),
                ("d_imp_kg", "Crecimiento de las importaciones (toneladas)"),
                ("d_china_pp", "Aumento de la participación de China (p.p.)"),
                ("pct_china", "Participación de China en las importaciones (nivel)")]
RESULTADOS = [("d_empleo", "Δ% empleo"), ("d_salario", "Δ% salario real"), ("d_ipi", "Δ% producción (IPI)")]


def correlaciones(base: pd.DataFrame) -> pd.DataFrame:
    """Correlación de Spearman (por rangos, robusta a outliers) entre exposición y resultados, entre ramas.

    `p_corregido`: Benjamini-Hochberg sobre todas las pruebas juntas. Con 24 pruebas al 5% se esperan 1 o 2
    «significativas» por azar; el p corregido descuenta eso.
    """
    filas = []
    for ventana, g in base.groupby("ventana"):
        for expo, expo_lab in EXPOSICIONES:
            for res, res_lab in RESULTADOS:
                x = g[[expo, res]].dropna()
                if len(x) < 5:
                    continue
                rho, p = spearmanr(x[expo], x[res])
                filas.append(dict(ventana=ventana, exposicion=expo_lab, exposicion_col=expo,
                                  resultado=res_lab, resultado_col=res, rho=rho, p_valor=p, n_ramas=len(x)))
    out = pd.DataFrame(filas)
    out["p_corregido"] = multipletests(out["p_valor"], method="fdr_bh")[1]
    return out


def grupos_por_exposicion(base: pd.DataFrame) -> pd.DataFrame:
    """Ramas partidas por la mediana de cada medida de exposición: mediana de los cambios en cada grupo."""
    filas = []
    for ventana, g in base.groupby("ventana"):
        for expo, expo_lab in EXPOSICIONES:
            g2 = g.dropna(subset=[expo]).copy()
            corte = g2[expo].median()
            g2["grupo"] = np.where(g2[expo] >= corte, "Mayor exposición", "Menor exposición")
            for grupo, gg in g2.groupby("grupo"):
                filas.append(dict(
                    ventana=ventana, exposicion=expo_lab, grupo=grupo, n_ramas=len(gg),
                    mediana_d_empleo=gg["d_empleo"].median(), mediana_d_salario=gg["d_salario"].median(),
                    mediana_d_ipi=gg["d_ipi"].median(), delta_puestos=gg["d_puestos"].sum(),
                    ramas=", ".join(sorted(gg["rama"])),
                ))
    return pd.DataFrame(filas)


# ------------------------------------------------------------- respuesta a la pregunta central
# «Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más
# crecieron las importaciones?» Ventana común 2018 -> 2025: último año completo en todas las fuentes, así
# exposición y resultados miden el mismo período. Medida principal: crecimiento % de las importaciones en USD.
INICIO, FIN = 2018, 2025
MEDIDAS_RESPUESTA = [("imp_usd", "Importaciones en dólares (Δ%)"),
                     ("imp_ton", "Importaciones en toneladas (Δ%)"),
                     ("imp_por_puesto", "Aumento de importaciones por puesto (USD)")]
RESULTADOS_RESPUESTA = [("empleo", "Empleo"), ("produccion", "Producción"), ("salario", "Salario real")]
GRUPO_MAS, GRUPO_MENOS = "Importaciones crecieron más", "Importaciones crecieron menos"


def respuesta_por_rama(panel: pd.DataFrame, empleo: pd.DataFrame, por_uso: pd.DataFrame | None = None) -> pd.DataFrame:
    """Una fila por rama: crecimiento de las importaciones y cambio de empleo, producción y salario, 2018 -> 2025.

    Grupo: las 16 ramas partidas en la mediana del crecimiento de las importaciones en USD (8 y 8).
    `empleo_previo`: cambio del empleo 2011 -> 2017, para ver si las ramas ya venían cayendo antes.
    `por_uso` (salida de uso_economico.importaciones_por_uso, todos los años): agrega el crecimiento de las importaciones
    de bienes de consumo, insumos y capital, y qué parte de lo importado por la rama eran bienes de consumo en 2018.
    Una rama sin importaciones de consumo (refinación) queda sin dato en las columnas de consumo.
    """
    a = panel[panel["anio"] == INICIO].set_index("rama")
    b = panel[panel["anio"] == FIN].set_index("rama")
    pct = lambda col: (b[col] / a[col] - 1) * 100
    e = empleo[empleo["rama"] != TOTAL]
    previo = e[e["periodo"].dt.year.isin([2011, 2017])].groupby([e["periodo"].dt.year, "rama"])["puestos"].mean().unstack(0)
    out = pd.DataFrame({
        "imp_usd": pct("imp_cif"), "imp_ton": pct("imp_kg"), "imp_por_puesto": (b["imp_cif"] - a["imp_cif"]) / a["puestos"],
        "empleo": pct("puestos"), "puestos": b["puestos"] - a["puestos"], "puestos_inicio": a["puestos"],
        "produccion": pct("ipi"), "salario": pct("salario_real"), "empleo_previo": (previo[2017] / previo[2011] - 1) * 100,
    })
    out["grupo"] = np.where(out["imp_usd"] > out["imp_usd"].median(), GRUPO_MAS, GRUPO_MENOS)
    if por_uso is not None:
        cif = por_uso.pivot_table(index="rama", columns=["uso", "anio"], values="imp_cif", aggfunc="sum").fillna(0)
        kg = por_uso.pivot_table(index="rama", columns=["uso", "anio"], values="imp_kg", aggfunc="sum").fillna(0)
        cambio = lambda t, uso: (t[(uso, FIN)] / t[(uso, INICIO)].replace(0, np.nan) - 1) * 100
        out["consumo_usd"], out["consumo_ton"] = cambio(cif, "Consumo"), cambio(kg, "Consumo")
        out["insumos_usd"], out["capital_usd"] = cambio(cif, "Insumos"), cambio(cif, "Capital")
        out["consumo_por_puesto"] = (cif[("Consumo", FIN)] - cif[("Consumo", INICIO)]) / out["puestos_inicio"]
        out["consumo_peso"] = cif[("Consumo", INICIO)] / cif.xs(INICIO, level="anio", axis=1).sum(axis=1) * 100
        out.loc[out["consumo_peso"] == 0, ["consumo_usd", "consumo_ton", "consumo_por_puesto"]] = np.nan
    return out.rename_axis("rama").reset_index()


def respuesta_grupos(resp: pd.DataFrame, ipi: pd.DataFrame, salario: pd.DataFrame) -> pd.DataFrame:
    """Los dos grupos de ramas y el total de la industria: puestos, empleo %, producción y salario 2018 -> 2025.

    Grupos: producción y salario como mediana de las ramas (una rama extrema no domina). Total: las series oficiales del total.
    """
    filas = []
    for grupo, g in resp.groupby("grupo"):
        filas.append(dict(grupo=grupo, n_ramas=len(g), puestos=g["puestos"].sum(), empleo=g["puestos"].sum() / g["puestos_inicio"].sum() * 100,
                          produccion=g["produccion"].median(), salario=g["salario"].median(), imp_usd=g["imp_usd"].median(),
                          ramas=", ".join(g.sort_values("imp_usd", ascending=False)["rama"])))

    def total_anual(df, valor):
        t = df[df["rama"] == TOTAL].groupby(df["periodo"].dt.year)[valor].mean()
        return (t[FIN] / t[INICIO] - 1) * 100

    filas.append(dict(grupo="Total industria", n_ramas=len(resp), puestos=resp["puestos"].sum(),
                      empleo=resp["puestos"].sum() / resp["puestos_inicio"].sum() * 100,
                      produccion=total_anual(ipi, "ipi"), salario=total_anual(salario, "salario_real"), imp_usd=np.nan, ramas=""))
    return pd.DataFrame(filas)


def respuesta_correlaciones(resp: pd.DataFrame, repeticiones: int = 5000, semilla: int = 2018) -> pd.DataFrame:
    """Spearman entre cada medida de crecimiento de las importaciones y cada resultado (9 pruebas).

    Intervalo de confianza al 95% por bootstrap (remuestreando ramas) y p corregido por Benjamini-Hochberg.
    """
    rng = np.random.default_rng(semilla)
    filas = []
    for expo, expo_lab in MEDIDAS_RESPUESTA:
        for res, res_lab in RESULTADOS_RESPUESTA:
            rho, p = spearmanr(resp[expo], resp[res])
            boot = []
            for _ in range(repeticiones):
                s = resp.iloc[rng.integers(0, len(resp), len(resp))]
                if s[expo].nunique() > 1 and s[res].nunique() > 1:
                    boot.append(spearmanr(s[expo], s[res])[0])
            bajo, alto = np.nanpercentile(boot, [2.5, 97.5])
            filas.append(dict(exposicion_col=expo, exposicion=expo_lab, resultado_col=res, resultado=res_lab,
                              rho=rho, p_valor=p, ic_bajo=bajo, ic_alto=alto, principal=expo == "imp_usd"))
    out = pd.DataFrame(filas)
    out["p_corregido"] = multipletests(out["p_valor"], method="fdr_bh")[1]
    return out


def respuesta_sensibilidad(resp: pd.DataFrame) -> pd.DataFrame:
    """¿Cambia la respuesta principal (importaciones USD vs. empleo) si se mide distinto?

    tipo = «sin_rama» (sacando cada rama de a una), «ponderada» (regresión ponderada por empleo de 2018, errores HC3)
    y «tendencia_previa» (regresión sobre rangos con el empleo 2011-2017 como control).
    """
    filas = []
    for rama in resp["rama"]:
        s = resp[resp["rama"] != rama]
        rho, p = spearmanr(s["imp_usd"], s["empleo"])
        filas.append(dict(tipo="sin_rama", detalle=rama, estimacion=rho, p_valor=p, n_ramas=len(s)))
    for detalle, s in (("16 ramas", resp), ("sin Alimentos y bebidas", resp[resp["rama"] != "15"])):
        m = sm.WLS(s["empleo"], sm.add_constant(s[["imp_usd"]]), weights=s["puestos_inicio"]).fit(cov_type="HC3")
        filas.append(dict(tipo="ponderada", detalle=detalle, estimacion=m.params["imp_usd"], p_valor=m.pvalues["imp_usd"], n_ramas=len(s)))
    r = resp[["empleo", "imp_usd", "empleo_previo"]].rank()
    m = sm.OLS(r["empleo"], sm.add_constant(r[["imp_usd", "empleo_previo"]])).fit(cov_type="HC3")
    for var, detalle in (("imp_usd", "importaciones (USD)"), ("empleo_previo", "empleo 2011-2017")):
        filas.append(dict(tipo="tendencia_previa", detalle=detalle, estimacion=m.params[var], p_valor=m.pvalues[var], n_ramas=len(resp)))
    return pd.DataFrame(filas)


MEDIDAS_USO = [("consumo_usd", "Bienes de consumo (USD)"), ("consumo_ton", "Bienes de consumo (toneladas)"),
               ("insumos_usd", "Insumos (USD)"), ("capital_usd", "Bienes de capital (USD)")]
GRUPO_CONSUMO_MAS, GRUPO_CONSUMO_MENOS = "Consumo importado creció más", "Consumo importado creció menos"


def respuesta_uso_correlaciones(resp: pd.DataFrame) -> pd.DataFrame:
    """Spearman entre el crecimiento de las importaciones de cada uso económico y cada resultado, 2018 -> 2025.

    Es la prueba de si la respuesta cambia al separar lo que compite (consumo) de lo que abastece (insumos, capital).
    Solo ramas con importaciones de ese uso en 2018; p corregido por Benjamini-Hochberg sobre estas 12 pruebas.
    """
    filas = []
    for expo, expo_lab in MEDIDAS_USO:
        for res, res_lab in RESULTADOS_RESPUESTA:
            x = resp[[expo, res]].replace([np.inf, -np.inf], np.nan).dropna()
            rho, p = spearmanr(x[expo], x[res])
            filas.append(dict(exposicion_col=expo, exposicion=expo_lab, resultado_col=res, resultado=res_lab, rho=rho, p_valor=p, n_ramas=len(x)))
    out = pd.DataFrame(filas)
    out["p_corregido"] = multipletests(out["p_valor"], method="fdr_bh")[1]
    return out


def respuesta_uso_grupos(resp: pd.DataFrame) -> pd.DataFrame:
    """Ramas partidas en la mediana del crecimiento de las importaciones de bienes de consumo (sin las que no importan consumo)."""
    d = resp.dropna(subset=["consumo_usd"]).copy()
    d["grupo_consumo"] = np.where(d["consumo_usd"] > d["consumo_usd"].median(), GRUPO_CONSUMO_MAS, GRUPO_CONSUMO_MENOS)
    filas = []
    for grupo, g in d.groupby("grupo_consumo"):
        filas.append(dict(grupo=grupo, n_ramas=len(g), puestos=g["puestos"].sum(), empleo=g["puestos"].sum() / g["puestos_inicio"].sum() * 100,
                          produccion=g["produccion"].median(), salario=g["salario"].median(), consumo_usd=g["consumo_usd"].median(),
                          ramas=", ".join(g.sort_values("consumo_usd", ascending=False)["rama"])))
    return pd.DataFrame(filas)
