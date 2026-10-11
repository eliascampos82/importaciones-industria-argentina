"""Tarjetas tipo afiche (cifra gigante + frase de dos renglones + pie con el detalle y la fuente), agrupadas en filas de hallazgos.

Las usan el Resumen y la página Importaciones vs. resultados. El CSS (`.hz`, `.afiche`, `.af-*`) está en `core/tema.py`.
Regla: las tarjetas son para hechos medidos (puestos, porcentajes), no para correlaciones.
"""
import re

from core.formato import fmt_signed


def redondo(x: float) -> str:
    """-45.383 -> '-45.000': en la tarjeta se lee de un golpe (la cifra exacta va en el pie)."""
    return fmt_signed(round(x, -3) if abs(x) >= 10_000 else round(x, -2) if abs(x) >= 1_000 else x)


def tono_de(valor: str) -> str:
    """Color de la cifra: naranja si cae, azul si sube, blanco si no es una variación (conteos, correlaciones)."""
    return "neg" if valor.startswith("-") else "pos" if valor.startswith("+") else "neu"


def afiche(valor: str, frase: tuple[str, str], tema: str, periodo: str, pie: str, fuente: str, tam: str, tono: str | None = None) -> dict:
    """Una tarjeta tipo afiche: tema y período arriba, barra de acento, cifra gigante, frase en dos renglones y pie con el detalle."""
    return dict(valor=valor, frase=frase, tema=tema, periodo=periodo, pie=pie, fuente=fuente, tam=tam, tono=tono or tono_de(valor))


def html_afiche(a: dict, extra: str = "") -> str:
    return (f'<div class="afiche {a["tam"]} {a["tono"]}{extra}">'
            f'<div class="af-cab"><span>{a["tema"]}</span><span>{a["periodo"]}</span></div>'
            f'<div class="af-cuerpo"><div class="af-barra"></div><div class="af-valor">{a["valor"]}</div>'
            f'<div class="af-frase">{a["frase"][0]}<br>{a["frase"][1]}</div></div>'
            f'<div class="af-pie"><div class="af-det">{a["pie"]}</div><div class="af-fuente">Fuente: {a["fuente"]}</div></div></div>')


def contenido(a: dict) -> int:
    """Cuánto texto lleva una tarjeta (cifra, frase y pie sin etiquetas HTML): define su ancho en la grilla."""
    # la frase pesa el doble: es lo que se corta en renglones feos si la tarjeta es angosta
    return len(a["valor"]) + 2 * max(len(a["frase"][0]), len(a["frase"][1])) + len(re.sub(r"<[^>]+>", "", a["pie"])) // 2


def fila_hallazgo(i: int, titulo: str, tarjetas: list[dict]) -> str:
    """Un hallazgo = encabezado (número y título) + una fila de 5 tarjetas en una grilla de 12 columnas.
    El dato principal (la primera) y la tarjeta con más contenido de las demás ocupan 3 columnas; las otras 3, 2 columnas."""
    mas_contenido = 1 + max(range(len(tarjetas) - 1), key=lambda k: contenido(tarjetas[k + 1]))
    for k, a in enumerate(tarjetas):
        a["tam"] = "ancho" if k in (0, mas_contenido) else "angosto"
    return (f'<section class="hz"><div class="hz-cab"><span class="hz-num">{i:02d}</span><span class="hz-tit">{titulo}</span></div>'
            f'<div class="hz-grilla">{"".join(html_afiche(a) for a in tarjetas)}</div></section>')
