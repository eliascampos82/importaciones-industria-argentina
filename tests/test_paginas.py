"""Cada pestaña del dashboard carga sin errores, incluidos los selectores principales.

Correr desde la carpeta del proyecto:  .\\.venv\\Scripts\\python.exe -m pytest
"""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

DASHBOARD = Path(__file__).resolve().parents[1] / "dashboard"

# la presentación necesita el diccionario de páginas de Inicio.py: se prueban sus diapositivas sin la de recorrido
APP = f"""
import sys
sys.path.insert(0, r"{DASHBOARD}")
import streamlit as st
from core.tema import aplicar_estilo
from paginas import comparador, datos, empleo_ramas, exposicion, importaciones, informe, metodologia, presentacion, resumen
aplicar_estilo()
pag = st.session_state["pag"]
if pag == "presentacion":
    for diapositiva in (presentacion._portada, presentacion._tema, presentacion._preguntas, presentacion._datos, presentacion._resultado):
        diapositiva()
else:
    dict(comparador=comparador, datos=datos, empleo_ramas=empleo_ramas, exposicion=exposicion, importaciones=importaciones,
         informe=informe, metodologia=metodologia, resumen=resumen)[pag].mostrar()
"""
PAGINAS = ["presentacion", "resumen", "importaciones", "empleo_ramas", "exposicion", "comparador", "informe", "metodologia", "datos"]


def correr(pag: str, **estado) -> AppTest:
    at = AppTest.from_string(APP, default_timeout=180)
    at.session_state["pag"] = pag
    for k, v in estado.items():
        at.session_state[k] = v
    at.run()
    return at


@pytest.mark.parametrize("pag", PAGINAS)
def test_la_pagina_carga_sin_errores(pag):
    at = correr(pag)
    assert not at.exception, at.exception[0].message if at.exception else ""


@pytest.mark.parametrize("ventana", ["2018", "2023"])
@pytest.mark.parametrize("medida", ["d_imp_cif", "d_imp_kg", "d_china_pp", "pct_china"])
def test_importaciones_vs_resultados_con_cada_filtro(ventana, medida):
    at = correr("exposicion", exp_ventana=ventana, exp_col=medida)
    assert not at.exception


@pytest.mark.parametrize("rama", ["15", "16", "17", "18-19", "20-22", "23", "24", "25", "26", "27", "28", "29", "30-33", "34", "35", "36-38"])
def test_comparador_con_cada_rama(rama):
    at = correr("comparador", cmp_rama=rama)
    assert not at.exception, at.exception[0].message if at.exception else ""


@pytest.mark.parametrize("rama", ["todas", "17", "23", "29"])
def test_importaciones_por_uso_con_cada_rama(rama):
    at = correr("importaciones", imp_uso_rama=rama)
    assert not at.exception, at.exception[0].message if at.exception else ""
