"""Consultas frecuentes sobre las tablas procesadas (una fila por rama, indicador y ventana)."""
import pandas as pd

from core.datos import TOTAL, leer


def cambio(rama: str, metrica: str, ventana: str) -> pd.Series:
    """Variación de un indicador (Empleo, Producción (IPI), Salario real, Empresas) de una rama contra el año base."""
    c = leer("cambios_por_rama.csv")
    return c[(c.rama == rama) & (c.metrica == metrica) & (c.ventana == ventana)].iloc[0]


def cambio_total(metrica: str, ventana: str) -> pd.Series:
    return cambio(TOTAL, metrica, ventana)


def empleo_trimestre(rama: str, ventana: str) -> pd.Series:
    """Último trimestre publicado contra el mismo trimestre del año base (sin efecto estacional)."""
    q = leer("empleo_mismo_trimestre.csv")
    return q[(q.rama == rama) & (q.ventana == ventana)].iloc[0]


def panel_empleo(muestra: str, importaciones: str = "Importaciones totales", rezago: int = 0) -> pd.Series:
    """Estimación del modelo de panel para el empleo."""
    r = leer("regresiones_panel.csv")
    return r[(r.resultado == "Empleo") & (r.importaciones == importaciones) & (r.muestra == muestra) &
             (r.rezago_anios == rezago)].iloc[0]


def trimestre_texto(fecha: pd.Timestamp) -> str:
    """Timestamp de inicio de trimestre -> '1T 2026'."""
    return f"{(fecha.month - 1) // 3 + 1}T {fecha.year}"


def _acumulado_vs_anio_anterior(df: pd.DataFrame, valor: str) -> tuple[pd.Series, pd.Timestamp]:
    """Promedio de los meses transcurridos del último año contra los mismos meses del año anterior (% por rama)."""
    fin = df.periodo.max()
    actual = df[(df.periodo.dt.year == fin.year) & (df.periodo.dt.month <= fin.month)].groupby("rama")[valor].mean()
    previo = df[(df.periodo.dt.year == fin.year - 1) & (df.periodo.dt.month <= fin.month)].groupby("rama")[valor].mean()
    return (actual / previo - 1) * 100, fin


def panorama_ultimo_anio() -> tuple[pd.DataFrame, dict]:
    """Lo que va del último año (p. ej. 2026) contra el mismo período del año anterior, por rama y para el total.

    Empleo: último trimestre contra el mismo trimestre del año anterior. Producción y salario real: promedio de los meses
    transcurridos contra los mismos meses del año anterior (así no influye la estacionalidad ni el aguinaldo).
    """
    e = leer("empleo_por_rama.csv", ("periodo",)).pivot(index="rama", columns="periodo", values="puestos")
    ult = e.columns.max()
    ant = ult - pd.DateOffset(years=1)
    prod, fin_ipi = _acumulado_vs_anio_anterior(leer("ipi_por_rama.csv", ("periodo",)), "ipi")
    sal, fin_sal = _acumulado_vs_anio_anterior(leer("salario_real_por_rama.csv", ("periodo",)), "salario_real")
    t = pd.DataFrame({"empleo_abs": e[ult] - e[ant], "empleo_pct": (e[ult] / e[ant] - 1) * 100, "produccion_pct": prod, "salario_pct": sal})
    meta = dict(trim_ult=trimestre_texto(ult), trim_ant=trimestre_texto(ant), fin_ipi=fin_ipi, fin_sal=fin_sal, anio=fin_ipi.year)
    return t, meta


def _variacion_por_anio(df: pd.DataFrame, valor: str, anios: tuple) -> pd.DataFrame:
    """Variación % de cada año contra el anterior, por rama. El último año, si está incompleto, se compara con los mismos meses del anterior."""
    fin = df.periodo.max()
    salida = {}
    for y in anios:
        tope = fin.month if y == fin.year else 12
        actual = df[(df.periodo.dt.year == y) & (df.periodo.dt.month <= tope)].groupby("rama")[valor].mean()
        previo = df[(df.periodo.dt.year == y - 1) & (df.periodo.dt.month <= tope)].groupby("rama")[valor].mean()
        salida[y] = (actual / previo - 1) * 100
    return pd.DataFrame(salida)


def evolucion_por_anio(anios: tuple = (2024, 2025, 2026)) -> tuple[dict, dict]:
    """Año por año (cada uno contra el anterior): empleo, producción y salario real por rama. El último año es parcial y se indica en `meta`."""
    e = leer("empleo_por_rama.csv", ("periodo",))
    i = leer("ipi_por_rama.csv", ("periodo",))
    s = leer("salario_real_por_rama.csv", ("periodo",))
    tablas = {"Empleo": _variacion_por_anio(e, "puestos", anios), "Producción": _variacion_por_anio(i, "ipi", anios),
              "Salario real": _variacion_por_anio(s, "salario_real", anios)}
    meta = {"fin": {"Empleo": e.periodo.max(), "Producción": i.periodo.max(), "Salario real": s.periodo.max()}, "anios": anios}
    return tablas, meta


def delta_empleo_rama(anio_base: int) -> pd.DataFrame:
    """Puestos y % de cada rama: último trimestre publicado contra el mismo trimestre del año base (sin la fila del total)."""
    e = leer("empleo_por_rama.csv", ("periodo",)).pivot(index="rama", columns="periodo", values="puestos")
    ult = e.columns.max()
    base = ult - pd.DateOffset(years=ult.year - anio_base)
    return pd.DataFrame({"delta_abs": e[ult] - e[base], "delta_pct": (e[ult] / e[base] - 1) * 100}).drop(TOTAL)
