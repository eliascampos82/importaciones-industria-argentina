"""Controles de los datos procesados: que coincidan con los totales oficiales y que la respuesta sea coherente.

Correr desde la carpeta del proyecto:  .\\.venv\\Scripts\\python.exe -m pytest
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from loaders import load_empleo_industria_oficial  # noqa: E402
from ramas import RAMAS, TOTAL  # noqa: E402

P = RAIZ / "data" / "processed"


def leer(nombre, **kw):
    return pd.read_csv(P / nombre, dtype={"rama": str, "ventana": str}, **kw)


def test_comercio_exterior_coincide_con_los_totales_de_control_del_indec():
    control = leer("control_comex.csv")
    assert control.coincide_imp.all() and control.coincide_exp.all()


def test_suma_de_ramas_de_empleo_es_igual_al_subtotal_oficial():
    e = leer("empleo_por_rama.csv", parse_dates=["periodo"])
    suma = e[e.rama != TOTAL].groupby("periodo").puestos.sum()
    oficial = load_empleo_industria_oficial().set_index("periodo").puestos_oficial
    comun = suma.index.intersection(oficial.index)
    assert len(comun) > 100
    assert np.allclose(suma[comun], oficial[comun])


def test_hay_16_ramas_en_cada_tabla_por_rama():
    for archivo in ("respuesta_por_rama.csv", "exposicion_vs_resultados.csv"):
        d = leer(archivo)
        assert set(d.rama) == set(RAMAS), archivo


def test_importaciones_por_uso_suman_lo_mismo_que_el_total_por_rama():
    uso = leer("importaciones_por_uso.csv").groupby(["rama", "anio"]).imp_cif.sum()
    com = leer("comercio_por_rama_anio.csv").set_index(["rama", "anio"]).imp_cif
    assert np.allclose(uso.sort_index(), com.loc[uso.sort_index().index])


def test_casi_todo_lo_importado_tiene_uso_economico():
    uso = leer("importaciones_por_uso.csv")
    sin = uso[uso.uso == "Sin clasificar"].imp_cif.sum() / uso.imp_cif.sum()
    assert sin < 0.005


def test_grupos_de_la_respuesta_suman_el_total():
    r, g = leer("respuesta_por_rama.csv"), leer("respuesta_grupos.csv").set_index("grupo")
    assert (r.grupo.value_counts() == 8).all()
    mas, menos, tot = g.loc["Importaciones crecieron más"], g.loc["Importaciones crecieron menos"], g.loc["Total industria"]
    assert mas.puestos + menos.puestos == pytest.approx(tot.puestos)
    assert tot.puestos == pytest.approx(r.puestos.sum())


@pytest.mark.parametrize("archivo, n", [("correlaciones.csv", 24), ("respuesta_correlaciones.csv", 9), ("respuesta_uso_correlaciones.csv", 12)])
def test_correlaciones_validas_y_p_corregido_no_menor_que_p(archivo, n):
    c = leer(archivo)
    assert len(c) == n
    assert c.rho.between(-1, 1).all()
    assert (c.p_corregido >= c.p_valor - 1e-12).all()
