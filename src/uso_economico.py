"""Clasificación de las importaciones por uso económico (BEC: Broad Economic Categories, Naciones Unidas).

Para qué: las importaciones totales de una rama mezclan lo que **compite** con su producción (bienes de consumo
terminados) con lo que la **abastece** (insumos, partes, máquinas). Cuando una rama crece importa más insumos y
máquinas, así que las importaciones totales suben con la actividad y tapan la competencia. Separar por uso permite
medir la exposición solo con los bienes de consumo.

Tablas de correspondencia HS 6 dígitos -> BEC rev. 4 del Banco Mundial (WITS), guardadas en
data/raw/comercio_exterior/clasificaciones/. El NCM argentino de 8 dígitos usa el HS en sus primeros 6, con la
versión del HS vigente cada año: HS2012 hasta 2016, HS2017 de 2017 a 2021 y HS2022 desde 2022. Si un código no
está en la tabla de su versión se busca en las otras.

Grandes categorías (correspondencia de BEC con el Sistema de Cuentas Nacionales):
  - Consumo: alimentos y bebidas para hogares (112, 122, 12), bienes de consumo durables, semidurables y no
    durables (61, 62, 63), equipo de transporte no industrial (522) y autos de pasajeros (51), que compiten con
    la producción automotriz local.
  - Capital: máquinas y equipo (41) y equipo de transporte industrial (521).
  - Insumos: el resto, incluidas partes y accesorios (42, 53) y combustibles (31, 32).
"""
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "comercio_exterior" / "clasificaciones"
TABLAS = {"HS2012": "hs2012_a_bec.csv", "HS2017": "hs2017_a_bec.csv", "HS2022": "hs2022_a_bec.csv"}

CONSUMO, INSUMOS, CAPITAL, SIN_CLASIFICAR = "Consumo", "Insumos", "Capital", "Sin clasificar"
USOS = (CONSUMO, INSUMOS, CAPITAL)
_BEC_A_USO = {
    **{c: CONSUMO for c in ("112", "122", "12", "61", "62", "63", "522", "51")},
    **{c: CAPITAL for c in ("41", "521")},
    **{c: INSUMOS for c in ("111", "121", "21", "22", "31", "32", "321", "322", "42", "53")},
}


def version_hs(anio: int) -> str:
    return "HS2012" if anio <= 2016 else "HS2017" if anio <= 2021 else "HS2022"


def _tabla(version: str) -> pd.Series:
    t = pd.read_csv(RAW / TABLAS[version], dtype=str, encoding="cp1252")  # los archivos de WITS vienen en codificación de Windows
    t.columns = ["hs6", "hs_desc", "bec", "bec_desc"]
    t["hs6"] = t["hs6"].str.strip().str.zfill(6)
    t["uso"] = t["bec"].str.strip().map(_BEC_A_USO).fillna(SIN_CLASIFICAR)
    return t.drop_duplicates("hs6").set_index("hs6")["uso"]


def uso_por_hs6(anio: int) -> pd.Series:
    """hs6 -> uso, priorizando la versión del HS vigente ese año y completando con las otras."""
    principal = version_hs(anio)
    tabla = _tabla(principal)
    for v in TABLAS:
        if v != principal:
            otra = _tabla(v)
            tabla = pd.concat([tabla, otra[~otra.index.isin(tabla.index)]])
    return tabla


def importaciones_por_uso(imp: pd.DataFrame, anio: int) -> pd.DataFrame:
    """Importaciones de un año (salida de loaders.load_importaciones) agregadas por rama y uso: CIF y kilos."""
    d = imp[imp["rama"].notna() & (imp["rama"] != "NO_IND")].copy()
    d["uso"] = d["ncm"].str[:6].map(uso_por_hs6(anio)).fillna(SIN_CLASIFICAR)
    return (d.groupby(["rama", "uso"], as_index=False)
             .agg(imp_cif=("cif_usd", "sum"), imp_kg=("peso_neto_kg", "sum"))
             .assign(anio=anio))
