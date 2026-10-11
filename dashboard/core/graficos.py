"""Constructores de gráficos Plotly compartidos por las páginas."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from core.tema import (AZUL, ESCALA_DIVERGENTE, ESCALA_RESULTADO, GRILLA, GRIS, GRIS_CLARO, NARANJA, estilo_ejes, layout)


def marca_vertical(fig, fecha, texto: str):
    """Línea vertical punteada (p. ej. dic-2023) con etiqueta arriba."""
    fig.add_shape(type="line", x0=fecha, x1=fecha, y0=0, y1=1, yref="paper",
                  line=dict(color=GRIS, width=1, dash="dot"))
    fig.add_annotation(x=fecha, y=1, yref="paper", text=texto, showarrow=False, xanchor="left",
                       yanchor="top", font=dict(size=11, color=GRIS))
    return fig


def lineas(df, x, y, serie, colores: dict, titulo=None, y_titulo=None, alto=290, base100=False,
           formato="%{y:,.1f}", marca=None, ancho_linea=2.2, orden=None):
    """Varias líneas (una por valor de `serie`), color fijo por entidad."""
    fig = go.Figure()
    for s in (orden or list(df[serie].unique())):
        d = df[df[serie] == s].sort_values(x)
        fig.add_trace(go.Scatter(x=d[x], y=d[y], mode="lines", name=s,
                                 line=dict(color=colores.get(s, GRIS), width=ancho_linea),
                                 hovertemplate=f"{formato}<extra>{s}</extra>"))
    if base100:
        fig.add_hline(y=100, line_dash="dot", line_color=GRIS, line_width=1)
    if marca:
        marca_vertical(fig, *marca)
    fig.update_layout(**layout(titulo, alto, leyenda=df[serie].nunique() > 1), hovermode="x unified")
    return estilo_ejes(fig, None, y_titulo)


def barras_signo(df, valor, etiqueta, titulo=None, formato="{:+,.0f}", x_titulo=None, alto=None,
                 color_pos=AZUL, color_neg=NARANJA, orden: str | None = None, separador: tuple | None = None):
    """Barras horizontales ordenadas; azul = sube/gana, naranja = baja/pierde.

    `orden`: columna por la que se ordenan las barras (por defecto, el mismo valor; la mayor queda arriba).
    `separador`: (posición, texto arriba, texto abajo) dibuja una línea punteada entre dos grupos de barras;
    la posición cuenta barras desde abajo (p. ej. 8 = entre la octava y la novena).
    """
    d = df.sort_values(orden or valor, ascending=True).copy()
    colores = [color_pos if v >= 0 else color_neg for v in d[valor]]
    texto = [formato.format(v).replace(",", "X").replace(".", ",").replace("X", ".") for v in d[valor]]
    fig = go.Figure(go.Bar(x=d[valor], y=d[etiqueta], orientation="h", marker_color=colores,
                           text=texto, textposition="outside", cliponaxis=False,
                           hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>"))
    if separador:
        pos, arriba, abajo = separador
        fig.add_hline(y=pos - 0.5, line_dash="dot", line_color=GRIS, line_width=1.2)
        for texto, y, ancla in ((arriba, pos - 0.5, "bottom"), (abajo, pos - 0.5, "top")):
            fig.add_annotation(x=1, xref="paper", y=y, text=texto, showarrow=False, xanchor="right", yanchor=ancla,
                               font=dict(size=10, color=GRIS))
    fig.update_layout(**layout(titulo, alto or (40 + 19 * len(d)), leyenda=False), bargap=0.3)
    fig.update_xaxes(zeroline=True, zerolinecolor=GRIS)
    return estilo_ejes(fig, x_titulo, None)


def barras_h(df, valor, etiqueta, color=AZUL, titulo=None, formato="{:,.1f}", x_titulo=None, alto=None):
    d = df.sort_values(valor, ascending=True)
    texto = [formato.format(v).replace(",", "X").replace(".", ",").replace("X", ".") for v in d[valor]]
    fig = go.Figure(go.Bar(x=d[valor], y=d[etiqueta], orientation="h", marker_color=color, text=texto,
                           textposition="outside", cliponaxis=False,
                           hovertemplate="<b>%{y}</b><br>%{text}<extra></extra>"))
    fig.update_layout(**layout(titulo, alto or (40 + 19 * len(d)), leyenda=False), bargap=0.3)
    return estilo_ejes(fig, x_titulo, None)


NEUTRO_OPACO = "#e6e5e0"
TEXTO_OSCURO = "#1c1c1a"


def _rgb(color: str) -> tuple:
    c = color.lstrip("#")
    return tuple(int(c[k:k + 2], 16) for k in (0, 2, 4))


def _color_en(escala, t: float) -> tuple:
    """Color RGB de la escala (hex opacos) en la posición t (0-1), interpolando entre paradas."""
    for (p0, c0), (p1, c1) in zip(escala, escala[1:]):
        if t <= p1:
            f = (t - p0) / (p1 - p0) if p1 > p0 else 0
            return tuple(a + (b - a) * f for a, b in zip(_rgb(c0), _rgb(c1)))
    return _rgb(escala[-1][1])


def _luminancia(rgb) -> float:
    lin = [(v / 255) / 12.92 if v / 255 <= 0.03928 else (((v / 255) + 0.055) / 1.055) ** 2.4 for v in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def _texto_legible(rgb) -> str:
    """Blanco u oscuro, el que mayor contraste (WCAG) tenga con el fondo de la celda."""
    lf = _luminancia(rgb)
    contraste_blanco = 1.05 / (lf + 0.05)
    contraste_oscuro = (lf + 0.05) / (_luminancia(_rgb(TEXTO_OSCURO)) + 0.05)
    return "#ffffff" if contraste_blanco > contraste_oscuro else TEXTO_OSCURO


def heatmap(matriz: pd.DataFrame, titulo=None, escala=ESCALA_DIVERGENTE, rango=None, sufijo="%", decimales=0,
            alto=None, colorbar_titulo=None, texto_matriz: pd.DataFrame | None = None, marcas: pd.DataFrame | None = None, tam_texto=12):
    """Mapa de calor centrado en 0: filas = ramas, columnas = años o métricas.

    Cada celda lleva su número con el color de texto (blanco u oscuro) que mejor contraste con el fondo de esa celda,
    así se lee igual en tema claro y oscuro: por eso el tramo neutro de la escala se dibuja opaco.
    `marcas` (opcional, booleana y del mismo tamaño) agrega un asterisco a las celdas marcadas.
    """
    escala = [[p, NEUTRO_OPACO if c.startswith("rgba") else c] for p, c in escala]
    z = matriz.values.astype(float)
    tm = (texto_matriz if texto_matriz is not None else matriz).values.astype(float)
    rango = rango or float(np.nanpercentile(np.abs(z), 90))
    x, y = [str(c) for c in matriz.columns], list(matriz.index)
    ast = marcas.reindex_like(matriz).fillna(False).values.astype(bool) if marcas is not None else np.zeros(z.shape, bool)
    textos = [[("" if np.isnan(v) else f"{v:+.{decimales}f}{sufijo}".replace(".", ",") + (" *" if ast[i, k] else ""))
               for k, v in enumerate(fila)] for i, fila in enumerate(tm)]
    fig = go.Figure(go.Heatmap(
        z=z, x=x, y=y, colorscale=escala, zmid=0, zmin=-rango, zmax=rango, customdata=textos,
        xgap=2, ygap=2, colorbar=dict(title=colorbar_titulo or "", thickness=10, len=0.8),
        hovertemplate="<b>%{y}</b><br>%{x}: %{customdata}<extra></extra>"))
    for i, fila in enumerate(z):
        for k, v in enumerate(fila):
            if np.isnan(v) or not textos[i][k]:
                continue
            t = min(max((v + rango) / (2 * rango), 0), 1)
            fig.add_annotation(x=k, y=i, text=textos[i][k], showarrow=False,
                               font=dict(size=tam_texto, color=_texto_legible(_color_en(escala, t))))
    fig.update_layout(**layout(titulo, alto or (60 + 26 * len(matriz)), leyenda=False))
    fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
    fig.update_xaxes(side="top", type="category", gridcolor="rgba(0,0,0,0)")
    return fig


def dumbbell(df, etiqueta, v0, v1, n0, n1, titulo=None, x_titulo=None, alto=None, c0=GRIS, c1=NARANJA, sufijo="%"):
    """Dos puntos por fila unidos por una línea (antes / después)."""
    d = df.sort_values(v1, ascending=True)
    fig = go.Figure()
    for _, r in d.iterrows():
        fig.add_shape(type="line", x0=r[v0], x1=r[v1], y0=r[etiqueta], y1=r[etiqueta],
                      line=dict(color=GRILLA.replace("0.22", "0.6"), width=2))
    fig.add_trace(go.Scatter(x=d[v0], y=d[etiqueta], mode="markers", name=n0,
                             marker=dict(color=c0, size=9),
                             hovertemplate=f"<b>%{{y}}</b><br>{n0}: %{{x:.1f}}{sufijo}<extra></extra>"))
    fig.add_trace(go.Scatter(x=d[v1], y=d[etiqueta], mode="markers", name=n1,
                             marker=dict(color=c1, size=9),
                             hovertemplate=f"<b>%{{y}}</b><br>{n1}: %{{x:.1f}}{sufijo}<extra></extra>"))
    fig.update_layout(**layout(titulo, alto or (70 + 17 * len(d))))
    return estilo_ejes(fig, x_titulo, None)


def dispersion(df, x, y, etiqueta, titulo=None, x_titulo=None, y_titulo=None, alto=340, recta=True,
               resaltar: str | list | None = None):
    """Un punto por rama, con etiquetas y recta de mínimos cuadrados (orientativa). `resaltar`: una rama o una lista, en naranja."""
    resaltadas = [resaltar] if isinstance(resaltar, str) else (resaltar or [])
    colores = [NARANJA if e in resaltadas else AZUL for e in df[etiqueta]]
    fig = go.Figure(go.Scatter(x=df[x], y=df[y], mode="markers+text", text=df[etiqueta],
                               textposition="top center", textfont=dict(size=9),
                               marker=dict(color=colores, size=9, line=dict(width=1.5, color="rgba(255,255,255,0.8)")),
                               hovertemplate="<b>%{text}</b><br>x: %{x:,.1f}<br>y: %{y:,.1f}<extra></extra>"))
    if recta and df[[x, y]].dropna().shape[0] >= 4:
        d = df[[x, y]].dropna()
        b, a = np.polyfit(d[x], d[y], 1)
        xs = np.array([d[x].min(), d[x].max()])
        fig.add_trace(go.Scatter(x=xs, y=a + b * xs, mode="lines", line=dict(color=GRIS, dash="dash", width=1.5),
                                 hoverinfo="skip", showlegend=False))
    fig.add_hline(y=0, line_color=GRIS, line_width=1)
    fig.add_vline(x=0, line_color=GRIS, line_width=1)
    fig.update_layout(**layout(titulo, alto, leyenda=False))
    return estilo_ejes(fig, x_titulo, y_titulo)


def barras_agrupadas(df, categoria, serie, valor, colores: dict, titulo=None, y_titulo=None, alto=290, sufijo="%"):
    fig = go.Figure()
    for s in df[serie].unique():
        d = df[df[serie] == s]
        fig.add_trace(go.Bar(x=d[categoria], y=d[valor], name=s, marker_color=colores.get(s, GRIS),
                             text=[f"{v:+.1f}{sufijo}".replace(".", ",") for v in d[valor]], textposition="outside",
                             cliponaxis=False, hovertemplate=f"<b>%{{x}}</b> ({s})<br>%{{y:+.1f}}{sufijo}<extra></extra>"))
    fig.add_hline(y=0, line_color=GRIS, line_width=1)
    fig.update_layout(**layout(titulo, alto), barmode="group", bargap=0.3)
    return estilo_ejes(fig, None, y_titulo)


def barras_apiladas(df, x, y, serie, colores: dict, orden: list, titulo=None, y_titulo=None, alto=290):
    fig = go.Figure()
    for s in orden:
        d = df[df[serie] == s].sort_values(x)
        fig.add_trace(go.Bar(x=d[x], y=d[y], name=s, marker_color=colores.get(s, GRIS),
                             hovertemplate=f"<b>{s}</b><br>%{{x}}: %{{y:,.1f}}<extra></extra>"))
    fig.update_layout(**layout(titulo, alto), barmode="stack", bargap=0.25)
    fig.update_xaxes(type="category")
    return estilo_ejes(fig, None, y_titulo)


def coeficientes(df, etiqueta, valor, bajo, alto_ic, p_valor, titulo=None, x_titulo=None, alto=None):
    """Estimaciones con intervalo de confianza; naranja = significativa al 5%, gris = no distinguible de cero."""
    d = df.iloc[::-1]
    colores = [NARANJA if p < 0.05 else GRIS for p in d[p_valor]]
    fig = go.Figure(go.Scatter(
        x=d[valor], y=d[etiqueta], mode="markers",
        error_x=dict(type="data", symmetric=False, array=(d[alto_ic] - d[valor]).values,
                     arrayminus=(d[valor] - d[bajo]).values, color=GRIS_CLARO, thickness=2, width=6),
        marker=dict(color=colores, size=10),
        customdata=np.stack([d[p_valor], d[bajo], d[alto_ic]], axis=-1),
        hovertemplate="<b>%{y}</b><br>estimación: %{x:+.2f}<br>IC 95%: %{customdata[1]:+.2f} a %{customdata[2]:+.2f}"
                      "<br>p = %{customdata[0]:.3f}<extra></extra>"))
    fig.add_vline(x=0, line_color=GRIS, line_width=1.5)
    fig.update_layout(**layout(titulo, alto or (70 + 28 * len(d)), leyenda=False))
    return estilo_ejes(fig, x_titulo, None)
