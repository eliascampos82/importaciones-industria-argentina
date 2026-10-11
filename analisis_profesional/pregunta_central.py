"""Respuesta directa a la pregunta central (ver 05_pruebas_de_robustez.md, parte A).

Pregunta: «Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los
sectores donde más crecieron las importaciones?»

Ventana común 2018 -> 2025 (último año completo en todas las fuentes): promedios anuales de
data/processed/panel_rama_anio.csv. Lee solo data/processed/ (no modifica nada).

Uso, desde la carpeta del proyecto:
    .\\.venv\\Scripts\\python.exe analisis_profesional/pregunta_central.py
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.ramas import RAMA_LABELS  # noqa: E402

P = Path(__file__).resolve().parents[1] / "data" / "processed"
panel = pd.read_csv(P / "panel_rama_anio.csv", dtype={"rama": str})
empleo = pd.read_csv(P / "empleo_por_rama.csv", dtype={"rama": str}, parse_dates=["periodo"])
expo26 = pd.read_csv(P / "exposicion_vs_resultados.csv", dtype={"rama": str})
INI, FIN = 2018, 2025
rng = np.random.default_rng(2018)
sys.stdout.reconfigure(encoding="utf-8")  # acentos en la consola de Windows


def titulo(t):
    print(f"\n=== {t} ===")


a, b = panel[panel.anio == INI].set_index("rama"), panel[panel.anio == FIN].set_index("rama")
pct = lambda col: (b[col] / a[col] - 1) * 100
t = pd.DataFrame({
    "empleo": pct("puestos"), "puestos": b.puestos - a.puestos, "produccion": pct("ipi"), "salario": pct("salario_real"),
    "imp_usd": pct("imp_cif"), "imp_ton": pct("imp_kg"), "imp_por_puesto": (b.imp_cif - a.imp_cif) / a.puestos,
    "puestos_2018": a.puestos,
})
# tendencia previa: empleo 2011 -> 2017
pre = empleo[empleo.periodo.dt.year.isin([2011, 2017])].groupby([empleo.periodo.dt.year, "rama"]).puestos.mean().unstack(0)
t["empleo_previo"] = (pre[2017] / pre[2011] - 1) * 100

EXPO = {"imp_usd": "Importaciones en USD (Δ%)", "imp_ton": "Importaciones en toneladas (Δ%)", "imp_por_puesto": "Aumento de importaciones por puesto (USD)"}
RES = {"empleo": "Empleo", "produccion": "Producción", "salario": "Salario real"}

titulo(f"1. Tabla por rama, {INI} -> {FIN} (ordenada por crecimiento de importaciones en USD)")
v = t.sort_values("imp_usd", ascending=False).copy()
v.index = [RAMA_LABELS[r][:34] for r in v.index]
print(v[["imp_usd", "imp_ton", "imp_por_puesto", "empleo", "puestos", "produccion", "salario"]].round(1).to_string())

titulo("2. Correlaciones de Spearman (9 pruebas) con corrección de Benjamini-Hochberg e IC 95% por bootstrap")
filas = []
for e, en in EXPO.items():
    for r, rn in RES.items():
        rho, p = spearmanr(t[e], t[r])
        boot = []
        for _ in range(5000):
            i = rng.integers(0, len(t), len(t))
            s = t.iloc[i]
            if s[e].nunique() > 1 and s[r].nunique() > 1:
                boot.append(spearmanr(s[e], s[r])[0])
        filas.append((en, rn, rho, p, *np.nanpercentile(boot, [2.5, 97.5])))
c = pd.DataFrame(filas, columns=["exposicion", "resultado", "rho", "p", "ic_bajo", "ic_alto"])
c["p_bh"] = multipletests(c.p, method="fdr_bh")[1]
print(c.round(3).to_string(index=False))

titulo("3. ¿Dónde se perdieron los puestos? Ramas por encima y por debajo de la mediana de crecimiento de importaciones (USD)")
t["grupo"] = np.where(t.imp_usd > t.imp_usd.median(), "Importaciones crecieron más", "Importaciones crecieron menos")
g = t.groupby("grupo").agg(ramas=("puestos", "size"), puestos=("puestos", "sum"), puestos_2018=("puestos_2018", "sum"),
                           produccion_mediana=("produccion", "median"), salario_mediana=("salario", "median"))
g["empleo_pct"] = g.puestos / g.puestos_2018 * 100
print(g.round(1).to_string())
print(f"Total industria (16 ramas): {t.puestos.sum():+,.0f} puestos ({t.puestos.sum() / t.puestos_2018.sum() * 100:+.1f}%)")
perd = t[t.puestos < 0]
print(f"Ramas que perdieron puestos: {len(perd)}; de esos {-perd.puestos.sum():,.0f} puestos, "
      f"{-perd[perd.grupo == 'Importaciones crecieron menos'].puestos.sum() / -perd.puestos.sum() * 100:.0f}% en ramas donde las importaciones crecieron menos")

titulo("4. Regresión ponderada por empleo de 2018: Δ% empleo ~ crecimiento de importaciones (errores robustos HC3)")
for e in ("imp_usd", "imp_ton"):
    for pond in (False, True):
        X = sm.add_constant(t[[e]])
        m = (sm.WLS(t.empleo, X, weights=t.puestos_2018) if pond else sm.OLS(t.empleo, X)).fit(cov_type="HC3")
        print(f"{EXPO[e]:34s} {'ponderada' if pond else 'sin ponderar':12s} pendiente = {m.params[e]:+.3f} p.p. por cada 1% más de importaciones  "
              f"(IC95 {m.conf_int().loc[e, 0]:+.3f} a {m.conf_int().loc[e, 1]:+.3f}, p = {m.pvalues[e]:.3f})")

titulo("5. Controlando la tendencia previa (empleo 2011-2017): regresión sobre rangos")
R = t[["empleo", "imp_usd", "imp_ton", "empleo_previo"]].rank()
for e in ("imp_usd", "imp_ton"):
    m = sm.OLS(R.empleo, sm.add_constant(R[[e, "empleo_previo"]])).fit(cov_type="HC3")
    print(f"{EXPO[e]:34s} coef (rangos) = {m.params[e]:+.2f} (p = {m.pvalues[e]:.3f}); tendencia previa = {m.params.empleo_previo:+.2f} (p = {m.pvalues.empleo_previo:.3f})")

titulo("6. Sensibilidad de la correlación principal (importaciones USD vs empleo)")
for r in t.index:
    s = t.drop(r)
    print(f"sin {RAMA_LABELS[r][:34]:34s} rho = {spearmanr(s.imp_usd, s.empleo)[0]:+.2f}  p = {spearmanr(s.imp_usd, s.empleo)[1]:.3f}")
e26 = expo26[expo26.ventana == 2018]
print(f"\nCon resultados hasta 2026 (dashboard): rho = {spearmanr(e26.d_imp_cif, e26.d_empleo)[0]:+.2f}  p = {spearmanr(e26.d_imp_cif, e26.d_empleo)[1]:.3f}")
