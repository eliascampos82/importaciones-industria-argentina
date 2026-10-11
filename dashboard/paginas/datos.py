"""Página «Datos descargados»: qué archivos originales tiene el proyecto, de dónde salen, para qué se usan, cuánto pesan y dónde se descargan."""
from pathlib import Path

import openpyxl
import pandas as pd
import streamlit as st
import xlrd

from core.datos import PROJECT_ROOT
from core.formato import fmt_miles, fmt_num
from core.graficos import barras_h
from core.tema import AZUL
from core.ui import bloque, figura, nota, sintesis

RAW = PROJECT_ROOT / "data" / "raw"
INDEC_FTP = "https://www.indec.gob.ar/ftp/cuadros/"
OEDE = "https://www.argentina.gob.ar/sites/default/files/"
PAGINA_OEDE = "https://www.argentina.gob.ar/trabajo/estadisticas/oede-estadisticas-nacionales"
PAGINA_COMEX = "https://comex.indec.gob.ar/"

# Un conjunto de datos por fila. `archivos` es un patrón dentro de data/raw; las cifras (archivos, MB, filas) se calculan leyendo el disco.
CATALOGO = [
    dict(dataset="Importaciones por producto (NCM) y país", organismo="INDEC", archivos="comercio_exterior/importaciones/impo*.csv",
         cobertura="2016-2025, anual", usado=True,
         para_que="Cuánto importa cada rama, desde qué país (peso de China), en dólares CIF y en toneladas.",
         descarga="https://comex.indec.gob.ar/files/zips/imports_2025_Y.zip", pagina=PAGINA_COMEX,
         como="Un zip por año (cambiar 2025 por el año). El sitio no tiene botón de descarga: se baja con `python src/download_comex.py`."),
    dict(dataset="Importaciones: totales de control", organismo="INDEC", archivos="comercio_exterior/importaciones/itot*.csv",
         cobertura="2016-2025, anual", usado=True,
         para_que="Verificar que la descarga está completa (cantidad de registros y valor total).",
         descarga="https://comex.indec.gob.ar/files/zips/imports_2025_Y.zip", pagina=PAGINA_COMEX,
         como="Vienen dentro del mismo zip de importaciones."),
    dict(dataset="Exportaciones por producto y país", organismo="INDEC", archivos="comercio_exterior/exportaciones/expo*.csv",
         cobertura="2016-2025, anual", usado=True,
         para_que="Exportaciones y balanza comercial de cada rama.",
         descarga="https://comex.indec.gob.ar/files/zips/exports_2025_Y.zip", pagina=PAGINA_COMEX,
         como="Un zip por año (cambiar 2025 por el año); lo baja el mismo script `src/download_comex.py`."),
    dict(dataset="Exportaciones: totales de control", organismo="INDEC", archivos="comercio_exterior/exportaciones/etot*.csv",
         cobertura="2016-2025, anual", usado=True,
         para_que="Verificar que la descarga de exportaciones está completa.",
         descarga="https://comex.indec.gob.ar/files/zips/exports_2025_Y.zip", pagina=PAGINA_COMEX,
         como="Vienen dentro del mismo zip de exportaciones."),
    dict(dataset="Tabla de códigos de país (F.2668)", organismo="ARCA", archivos="comercio_exterior/Tablas-Paises-F2668.xls",
         cobertura="vigente", usado=True,
         para_que="Pasar el código de país de cada operación a su nombre (China, Brasil, etc.).",
         descarga=None, pagina="https://www.afip.gob.ar/operaciones-internacionales/",
         como="Se publica en el micrositio de Operaciones internacionales de ARCA; no se encontró un link directo estable al archivo."),
    dict(dataset="Exportaciones e importaciones por intensidad tecnológica", organismo="Ministerio de Economía (datos.gob.ar)",
         archivos="comercio_exterior/exportaciones_importaciones_intensidad_tecnologica.csv", cobertura="1995-2016, anual", usado=False,
         para_que="Descargado para ampliar el trabajo (clasificaciones de Lall y UNCTAD); hoy no se usa.",
         descarga="https://infra.datos.gob.ar/catalog/sspm/dataset/181/distribution/181.1/download/exportaciones-importaciones-intensidad.csv",
         pagina="https://datos.gob.ar/dataset/sspm-exportaciones-e-importaciones-por-intensidad-tecnologica",
         como="Descarga directa del CSV."),
    dict(dataset="Correspondencia de productos (HS) con uso económico (BEC)", organismo="Banco Mundial (WITS)",
         archivos="comercio_exterior/clasificaciones/hs*_a_bec.csv", cobertura="HS 2012, 2017 y 2022", usado=True,
         para_que="Clasificar lo importado en bienes de consumo, insumos y bienes de capital, para separar lo que compite con la industria de lo que la abastece.",
         descarga="https://wits.worldbank.org/data/public/concordance/Concordance_H5_to_BE.zip",
         pagina="https://wits.worldbank.org/product_concordance.html",
         como="Un zip por versión del HS (H4 = 2012, H5 = 2017, H6 = 2022): se cambia el código en el link. Se guardó el CSV de cada uno con un nombre propio."),
    dict(dataset="Importaciones de soja y subproductos", organismo="INDEC (comex)",
         archivos="comercio_exterior/impo_soja_y_sub_productos_acum_2002_2025.xlsx", cobertura="2002-2025, anual", usado=False,
         para_que="Descargado como material extra; hoy no se usa (la soja es agro, no manufactura).",
         descarga=None, pagina=PAGINA_COMEX,
         como="Cuadro del sistema comex de INDEC; no se encontró un link directo estable al archivo."),
    dict(dataset="Empleo asalariado registrado por rama, trimestral", organismo="Ministerio de Trabajo (OEDE)",
         archivos="empleo/nacional_serie_empleo_trimestral_8.xlsx", cobertura="1996-1T 2026, trimestral", usado=True,
         para_que="Puestos de trabajo de cada rama industrial (y el subtotal oficial «Industria» para controlar la suma).",
         descarga=OEDE + "nacional_serie_empleo_trimestral_8.xlsx", pagina=PAGINA_OEDE,
         como="Descarga directa. Si el navegador no lo baja, entrar desde la página del OEDE (el número final cambia con cada actualización)."),
    dict(dataset="Empleo trimestral (versión anterior)", organismo="Ministerio de Trabajo (OEDE)",
         archivos="empleo/nacional_serie_empleo_trimestral_7.xlsx", cobertura="1996-4T 2025, trimestral", usado=False,
         para_que="Versión anterior, reemplazada por la _8 (que llega al 1T 2026). Se conserva como respaldo.",
         descarga=OEDE + "nacional_serie_empleo_trimestral_7.xlsx", pagina=PAGINA_OEDE, como="Descarga directa."),
    dict(dataset="Empleo asalariado registrado, anual", organismo="Ministerio de Trabajo (OEDE)",
         archivos="empleo/nacional_serie_empleo_anual_2.xlsx", cobertura="1996-2025, anual", usado=False,
         para_que="Descargado; no se usa porque la serie trimestral es más actual.",
         descarga=OEDE + "nacional_serie_empleo_anual_2.xlsx", pagina=PAGINA_OEDE, como="Descarga directa."),
    dict(dataset="Empresas privadas activas por rama", organismo="Ministerio de Trabajo (OEDE)",
         archivos="empresas/nacional_serie_empresas_2.xlsx", cobertura="1996-2024, anual", usado=True,
         para_que="Cierres netos de empresas en cada rama.",
         descarga=OEDE + "nacional_serie_empresas_2.xlsx", pagina=PAGINA_OEDE, como="Descarga directa."),
    dict(dataset="Remuneraciones por rama, mensual", organismo="Ministerio de Trabajo (OEDE)",
         archivos="salarios/nacional_serie_remuneraciones_mensual_8.xlsx", cobertura="1995-mar 2026, mensual", usado=True,
         para_que="Salario de cada rama; dividido por el IPC da el salario real.",
         descarga=OEDE + "nacional_serie_remuneraciones_mensual_8.xlsx", pagina=PAGINA_OEDE,
         como="Descarga directa. Ojo: el archivo _9 del sitio trae por error el contenido de empleo; por eso se usa el _8."),
    dict(dataset="Remuneraciones por rama, anual", organismo="Ministerio de Trabajo (OEDE)",
         archivos="salarios/nacional_serie_remuneraciones_anual_2.xlsx", cobertura="1995-2025, anual", usado=False,
         para_que="Descargado; no se usa porque la serie mensual permite promedios de 12 meses.",
         descarga=OEDE + "nacional_serie_remuneraciones_anual_2.xlsx", pagina=PAGINA_OEDE, como="Descarga directa."),
    dict(dataset="Índice de salarios", organismo="INDEC", archivos="salarios/indice_salarios.csv", cobertura="oct 2015-jun 2026, mensual",
         usado=False, para_que="Descargado para comparar salarios registrados, no registrados y públicos; hoy no se usa.",
         descarga=INDEC_FTP + "sociedad/indice_salarios.csv", pagina="https://www.indec.gob.ar/indec/web/Nivel4-Tema-4-31-61",
         como="Descarga directa."),
    dict(dataset="Índice de precios al consumidor (IPC) por división", organismo="INDEC", archivos="precios/serie_ipc_divisiones.csv",
         cobertura="dic 2016-ago 2026, mensual", usado=True,
         para_que="Deflactar los salarios (pasar de pesos corrientes a salario real).",
         descarga=INDEC_FTP + "economia/serie_ipc_divisiones.csv", pagina="https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31",
         como="Descarga directa."),
    dict(dataset="Índice de producción industrial manufacturero (IPI)", organismo="INDEC",
         archivos="industria/ipi_manufacturero_serie_2016_2026.xls", cobertura="2016-jul 2026, mensual", usado=True,
         para_que="Producción física de cada rama y de sus subramas.",
         descarga=INDEC_FTP + "economia/sh_ipi_manufacturero_2026.xls", pagina="https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-6-14",
         como="En el sitio se llama sh_ipi_manufacturero_2026.xls; en el proyecto se guardó con otro nombre."),
    dict(dataset="Utilización de la capacidad instalada", organismo="INDEC", archivos="industria/capacidad_instalada_2016_2026.xls",
         cobertura="2016-2026, mensual", usado=True, para_que="Qué parte de las plantas está ociosa, por bloque de la industria.",
         descarga=INDEC_FTP + "economia/sh_capacidad_09_26.xls", pagina="https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-6-15",
         como="El nombre cambia con cada informe (sh_capacidad_MM_AA.xls); el link es el de septiembre de 2026."),
    dict(dataset="Encuesta de productos industriales (cuadros trimestrales)", organismo="INDEC",
         archivos="industria/productos_industriales_trimestral/cuadros_epi_*.xls", cobertura="2T 2024-2T 2026, trimestral", usado=False,
         para_que="Producción en unidades físicas por producto; descargada para ampliar el trabajo, hoy no se usa.",
         descarga=INDEC_FTP + "economia/cuadros_epi_06_26.xls", pagina="https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-6-18",
         como="Un archivo por trimestre (cuadros_epi_MM_AA.xls); el link es el del 2T 2026."),
    dict(dataset="Estimador mensual industrial (EMI), base 2012", organismo="Ministerio de Economía (datos.gob.ar)",
         archivos="industria/emi_mensual_base2012.csv", cobertura="1994-2015, mensual", usado=False,
         para_que="Serie industrial anterior al IPI; no se usa porque el análisis empieza en 2016.",
         descarga="https://infra.datos.gob.ar/catalog/sspm/dataset/13/distribution/13.3/download/emi-datos-mensuales-indice-base-2012.csv",
         pagina="https://datos.gob.ar/dataset/sspm-estimador-mensual-industrial-emi-indice-base-2012", como="Descarga directa del CSV."),
]


def _filas_csv(ruta: Path) -> int:
    with open(ruta, "rb") as f:
        return max(sum(1 for _ in f) - 1, 0)   # sin la fila de títulos


def _filas_excel(ruta: Path) -> tuple[int, int]:
    """(hojas, filas con al menos una celda con valor, sumando todas las hojas).

    No se usa `max_row`: algunas hojas de OEDE tienen formato aplicado hasta la fila 1.048.576 y la inflarían;
    por eso también se deja de leer una hoja después de 500 filas vacías seguidas."""
    def contar(filas) -> int:
        n = vacias = 0
        for fila in filas:
            if any(v not in (None, "") for v in fila):
                n, vacias = n + 1, 0
            else:
                vacias += 1
                if vacias > 500:
                    break
        return n

    if ruta.suffix == ".xls":
        wb = xlrd.open_workbook(ruta, on_demand=True)
        hojas = [contar(ws.row_values(i) for i in range(ws.nrows)) for ws in wb.sheets()]
    else:
        wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
        hojas = [contar(ws.iter_rows(values_only=True)) for ws in wb.worksheets]
    return len(hojas), sum(hojas)


@st.cache_data(ttl=3600)
def _inventario(firma: tuple) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Recorre data/raw y mide cada archivo del catálogo. `firma` (nombres y fechas de modificación) invalida la caché si cambian los archivos."""
    resumen, detalle = [], []
    for d in CATALOGO:
        archivos = sorted(RAW.glob(d["archivos"]))
        mb = filas = hojas = 0
        for a in archivos:
            tam = a.stat().st_size / 1e6
            if a.suffix == ".csv":
                n, h = _filas_csv(a), None
            else:
                h, n = _filas_excel(a)
                hojas += h
            mb += tam
            filas += n
            detalle.append({"Conjunto": d["dataset"], "Archivo": a.relative_to(RAW).as_posix(), "MB": tam, "Filas": n, "Hojas": h})
        resumen.append({**d, "n_archivos": len(archivos), "mb": mb, "filas": filas, "hojas": hojas,
                        "formato": "CSV" if d["archivos"].endswith(".csv") else "Excel"})
    return pd.DataFrame(resumen), pd.DataFrame(detalle)


def _cargar():
    firma = tuple((p.name, p.stat().st_mtime) for p in sorted(RAW.rglob("*")) if p.is_file())
    return _inventario(firma)


def _introduccion():
    st.markdown(
        """
Todos los datos del proyecto son **públicos y oficiales** y se guardaron sin modificar en la carpeta `data/raw`. Esta página es el inventario: qué archivo es cada uno,
**quién lo publica**, **para qué se usó** en el análisis, **cuántos datos tiene** y **dónde se descarga**. Las cantidades (archivos, megabytes y filas) se calculan
leyendo los archivos en el momento, no están escritas a mano.
"""
    )


def _indicadores(res: pd.DataFrame):
    usados = res[res.usado]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Conjuntos de datos", len(res), f"{len(usados)} usados en el análisis", delta_color="off", delta_arrow="off", border=True)
    c2.metric("Archivos descargados", fmt_miles(res.n_archivos.sum()), f"{fmt_miles(usados.n_archivos.sum())} usados", delta_color="off", delta_arrow="off", border=True)
    c3.metric("Tamaño total", f"{fmt_num(res.mb.sum())} MB", f"{fmt_num(usados.mb.sum())} MB usados", delta_color="off", delta_arrow="off", border=True)
    c4.metric("Filas de datos", fmt_miles(res.filas.sum()), f"{fmt_miles(usados.filas.sum())} en lo usado", delta_color="off", delta_arrow="off", border=True)
    return (f"El proyecto descargó {len(res)} conjuntos de datos ({fmt_miles(res.n_archivos.sum())} archivos, {fmt_num(res.mb.sum())} MB) "
            f"de {res.organismo.str.replace(' (comex)', '', regex=False).nunique()} organismos; {len(usados)} se usan en el análisis.")


def _tabla(res: pd.DataFrame):
    st.subheader("1. Catálogo de datos")
    f1, f2 = st.columns([2, 1])
    organismos = f1.multiselect("Organismo", sorted(res.organismo.unique()), placeholder="Todos")
    uso = f2.segmented_control("Uso", ["Todos", "Usados", "No usados"], default="Todos") or "Todos"
    t = res if not organismos else res[res.organismo.isin(organismos)]
    t = t if uso == "Todos" else t[t.usado == (uso == "Usados")]

    tabla = pd.DataFrame({
        "Conjunto de datos": t.dataset, "Organismo": t.organismo, "¿Se usa?": t.usado.map({True: "Sí", False: "No"}),
        "Cobertura": t.cobertura, "Archivos": t.n_archivos, "Tamaño (MB)": t.mb.round(2), "Filas": t.filas,
        "Descarga": t.descarga.fillna(""), "Página oficial": t.pagina,
    })
    st.dataframe(
        tabla, hide_index=True, width="stretch", height=min(38 + 35 * len(tabla), 560),
        column_config={
            "Conjunto de datos": st.column_config.TextColumn(width="large"),
            "Descarga": st.column_config.LinkColumn("Descarga", display_text="Descargar"),
            "Página oficial": st.column_config.LinkColumn("Página oficial", display_text="Abrir página"),
            "Tamaño (MB)": st.column_config.NumberColumn(format="localized"),
            "Filas": st.column_config.NumberColumn(format="localized"),
        },
    )
    st.caption("«Filas»: registros de datos en los CSV; en los Excel, filas con contenido de todas las hojas (incluye títulos y notas de los cuadros). "
               "«Descargar» baja el archivo tal como lo publica el organismo; si un link cambió, la página oficial lleva a la versión vigente.")
    sin_link = res[res.descarga.isna()].dataset.tolist()
    if sin_link:
        nota(f"No se encontró un link directo estable para: {', '.join(sin_link)}. Para esos se indica la página del organismo.")


def _grafico(res: pd.DataFrame):
    d = res.assign(etiqueta=[t if len(t) <= 42 else t[:40].rstrip() + "…" for t in res.dataset]).sort_values("mb")
    mayor = res.loc[res.mb.idxmax()]
    comex = res[res.organismo == "INDEC"].loc[lambda x: x.archivos.str.contains("comercio_exterior/(?:im|ex)portaciones/")]
    with bloque("Tamaño de cada conjunto de datos (MB)"):
        figura(
            barras_h(d, "mb", "etiqueta", color=AZUL, formato="{:,.2f}", x_titulo="MB", alto=60 + 19 * len(d)),
            "Cada barra es un conjunto de datos descargado y su largo, cuántos megabytes ocupa en la carpeta del proyecto.",
            "Sirve para ver dónde está el volumen: lo que pesa es lo que más tarda en descargarse y procesarse.",
            f"El más grande es «{mayor.dataset}» con {fmt_num(mayor.mb)} MB en {mayor.n_archivos} archivos. Entre importaciones y exportaciones "
            f"de INDEC suman {fmt_num(comex.mb.sum())} MB, el {fmt_num(100 * comex.mb.sum() / res.mb.sum(), 0)}% del total.",
            "Los archivos de comercio exterior no se suben al repositorio por su tamaño: se vuelven a bajar con el script src/download_comex.py.",
        )
    return f"El volumen está concentrado en comercio exterior: {fmt_num(100 * comex.mb.sum() / res.mb.sum(), 0)}% de los megabytes."


def _detalle(res: pd.DataFrame, det: pd.DataFrame):
    st.subheader("2. Ficha de cada conjunto")
    st.markdown("Elegí un conjunto de datos para ver para qué se usó, cómo se descarga y cada uno de sus archivos (por ejemplo, uno por año) con su tamaño y sus filas.")
    conjunto = st.selectbox("Conjunto de datos", res.dataset)
    r = res[res.dataset == conjunto].iloc[0]
    enlaces = [f"[Página oficial]({r.pagina})"] + ([f"[Descargar el archivo]({r.descarga})"] if pd.notna(r.descarga) else [])
    st.markdown(
        f"**Organismo:** {r.organismo} · **Cobertura:** {r.cobertura} · **¿Se usa en el análisis?** {'Sí' if r.usado else 'No'}\n\n"
        f"**Para qué:** {r.para_que}\n\n**Cómo se descarga:** {r.como}\n\n{' · '.join(enlaces)}"
    )
    d = det[det.Conjunto == conjunto].drop(columns="Conjunto")
    if d.empty:
        nota("Este conjunto no está en la carpeta de datos de esta computadora: hay que descargarlo.")
        return
    if d.Hojas.isna().all():
        d = d.drop(columns="Hojas")
    st.dataframe(d, hide_index=True, width="stretch",
                 column_config={"MB": st.column_config.NumberColumn(format="localized"),
                                "Filas": st.column_config.NumberColumn(format="localized"),
                                "Hojas": st.column_config.NumberColumn(format="%d")})


def _faltantes(res: pd.DataFrame):
    faltan = res[res.n_archivos == 0]
    if len(faltan):
        nota("Estos conjuntos no están en la carpeta de datos de esta computadora (hay que descargarlos): " + ", ".join(faltan.dataset) + ".")


def mostrar():
    res, det = _cargar()
    _introduccion()
    frases = [_indicadores(res)]
    _faltantes(res)
    _tabla(res)
    frases.append(_grafico(res))
    _detalle(res, det)
    no_usados = res[~res.usado]
    frases.append(f"Hay {len(no_usados)} conjuntos descargados que hoy no se usan ({fmt_num(no_usados.mb.sum())} MB): quedan como material para ampliar el trabajo.")
    frases.append("Todo sale de fuentes oficiales: INDEC, Ministerio de Trabajo (OEDE), ARCA y el portal datos.gob.ar del Ministerio de Economía.")
    sintesis(frases)
