"""Carga (con caché) de los datos procesados y nombres cortos de las ramas."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "src"))
from ramas import RAMA_A_UCI, RAMA_LABELS, RAMAS, TOTAL, TOTAL_LABEL, UCI_APROXIMADO  # noqa: E402,F401

PROCESSED = PROJECT_ROOT / "data" / "processed"
AUTOR = "Francisco Elias Campos"

RAMA_CORTA = {
    "15": "Alimentos y bebidas", "16": "Tabaco", "17": "Textiles", "18-19": "Prendas, cuero y calzado",
    "20-22": "Madera, papel e impresión", "23": "Refinación de petróleo", "24": "Químicos",
    "25": "Caucho y plástico", "26": "Minerales no metálicos", "27": "Metálicas básicas",
    "28": "Productos de metal", "29": "Maquinaria y equipo", "30-33": "Electrónica, eléctricos, instrumentos",
    "34": "Automotores", "35": "Otro equipo de transporte", "36-38": "Muebles y otras manufacturas",
    TOTAL: TOTAL_LABEL,
}


def nombre(rama: str) -> str:
    return RAMA_CORTA.get(rama, rama)


@st.cache_data(ttl=3600, max_entries=64)
def leer(archivo: str, fechas: tuple = ()) -> pd.DataFrame:
    return pd.read_csv(PROCESSED / archivo, dtype={"rama": str, "codigo": str, "rama_padre": str, "ventana": str},
                       parse_dates=list(fechas))
