"""Pruebas de robustez de la revisión profesional (ver 05_pruebas_de_robustez.md).

Uso, desde la carpeta del proyecto:
    .\\.venv\\Scripts\\python.exe analisis_profesional/pruebas_robustez.py
Lee solo data/processed/ (no modifica nada).
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests

P = Path(__file__).resolve().parents[1] / "data" / "processed"
corr = pd.read_csv(P / "correlaciones.csv")
panel = pd.read_csv(P / "panel_rama_anio.csv", dtype={"rama": str})
expo = pd.read_csv(P / "exposicion_vs_resultados.csv", dtype={"rama": str})
comercio = pd.read_csv(P / "comercio_por_rama_anio.csv", dtype={"rama": str})
empleo = pd.read_csv(P / "empleo_por_rama.csv", dtype={"rama": str}, parse_dates=["periodo"])
sys.stdout.reconfigure(encoding="utf-8")  # acentos en la consola de Windows


def titulo(t):
    print(f"\n=== {t} ===")


titulo("1. Corrección por comparaciones múltiples (24 correlaciones)")
print(f"p < 0,05 sin corregir: {(corr.p_valor < .05).sum()} de {len(corr)}")
for metodo in ("bonferroni", "holm", "fdr_bh"):
    rechaza = multipletests(corr.p_valor, alpha=.05, method=metodo)[0]
    print(f"{metodo:10s}: sobreviven {rechaza.sum()} ->", corr.loc[rechaza, ["ventana", "exposicion_col", "resultado_col", "rho"]].values.tolist())

titulo("2. Panel de empleo dejando afuera cada rama de a una")
d = panel.assign(x=np.log1p(panel.imp_cif / 1e6), y=np.log(panel.puestos)).dropna(subset=["x", "y"])
for rama in sorted(d.rama.unique()):
    e = d[d.rama != rama]
    m = smf.ols("y ~ x + C(rama) + C(anio)", e).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(e.rama)[0]})
    print(f"sin {rama:6s} coef = {m.params.x:+.3f}  p = {m.pvalues.x:.3f}")

titulo("3. Exposición estilo Autor-Dorn-Hanson: aumento de importaciones por trabajador (USD por puesto)")
for base in (2018, 2023):
    L = empleo[empleo.periodo.dt.year == base].groupby("rama").puestos.mean()
    a, b = comercio[comercio.anio == base].set_index("rama"), comercio[comercio.anio == comercio.anio.max()].set_index("rama")
    g = expo[expo.ventana == base].set_index("rama")
    for nombre, x in (("total", (b.imp_cif - a.imp_cif) / L), ("China", (b.imp_china_cif - a.imp_china_cif) / L)):
        for res in ("d_empleo", "d_ipi", "d_salario"):
            z = pd.concat([x.rename("x"), g[res]], axis=1).dropna()
            rho, p = spearmanr(z.x, z[res])
            print(f"base {base}  ΔM/L {nombre:5s} vs {res:9s}  rho = {rho:+.2f}  p = {p:.3f}")

titulo("4. Placebo y persistencia: ¿las ramas ya venían cayendo antes de 2018?")
g = expo[expo.ventana == 2018].set_index("rama")
for ini, fin in ((2008, 2015), (2011, 2017)):
    A = empleo[empleo.periodo.dt.year == ini].groupby("rama").puestos.mean()
    B = empleo[empleo.periodo.dt.year == fin].groupby("rama").puestos.mean()
    previo = ((B / A - 1) * 100).drop("TOTAL", errors="ignore").rename("previo")
    for col in ("pct_china", "d_china_pp", "d_imp_cif", "d_empleo"):
        z = pd.concat([previo, g[col]], axis=1).dropna()
        rho, p = spearmanr(z.previo, z[col])
        print(f"empleo {ini}-{fin} vs {col:10s}  rho = {rho:+.2f}  p = {p:.3f}")
