"""Bloques de presentación compartidos por las páginas: recuadro de gráfico, interpretación y síntesis."""
from contextlib import contextmanager
from html import escape

import streamlit as st


@contextmanager
def bloque(titulo: str):
    """Recuadro con borde que contiene el título, los controles, el gráfico y su explicación."""
    with st.container(border=True):
        st.markdown(f'<div class="bloque-titulo">{escape(titulo)}</div>', unsafe_allow_html=True)
        yield


def _abrir(que: str) -> str:
    """Convierte la descripción del gráfico en la frase que abre la explicación."""
    return que if que.startswith("Cada ") else "El gráfico muestra " + que[0].lower() + que[1:]


def interpretacion(que: str, como: str, observa: str | None = None, tener_en_cuenta: str | None = None) -> None:
    """Explicación de un gráfico en texto corrido: qué muestra y cómo leerlo, qué se observa en los datos y una aclaración final."""
    parrafos = [f"<p>{escape(_abrir(que) + ' ' + como)}</p>"]
    if observa:
        parrafos.append(f"<p>{escape(observa)}</p>")
    if tener_en_cuenta:
        parrafos.append(f'<p class="nota">{escape(tener_en_cuenta)}</p>')
    st.markdown(f'<div class="expl">{"".join(parrafos)}</div>', unsafe_allow_html=True)


def figura(fig, que: str, como: str, observa: str | None = None, tener_en_cuenta: str | None = None,
           proporcion: tuple = (5, 4)) -> None:
    """Gráfico a la izquierda y su interpretación a la derecha (en pantallas angostas se apilan). Va dentro de un `bloque`."""
    grafico, texto = st.columns(proporcion, gap="medium", vertical_alignment="center")
    with grafico:
        st.plotly_chart(fig, width="stretch")
    with texto:
        interpretacion(que, como, observa, tener_en_cuenta)


def nota(*parrafos: str, titulo: str | None = None, color: str = "orange") -> None:
    """Advertencia o aclaración en texto cursiva y de color, sin recuadro. `titulo` (opcional) abre el primer párrafo en negrita."""
    for i, p in enumerate(parrafos):
        cabecera = f"***{titulo}*** " if (i == 0 and titulo) else ""
        st.markdown(f":{color}[{cabecera}*{p}*]")


def sintesis(puntos: list[str], titulo: str = "Síntesis de la página") -> None:
    """Cierre de página: los puntos que el lector debería llevarse, en pocas líneas."""
    with bloque(titulo):
        st.markdown("\n".join(f"- {p}" for p in puntos))
