"""Paleta y estilo de los gráficos (Plotly), compatibles con tema claro y oscuro.

Los colores categóricos van en orden fijo y cada entidad conserva su color en todos los gráficos:
azul = la rama o serie en foco, naranja = la serie de comparación (total industria / China).
"""
AZUL = "#2a78d6"
NARANJA = "#eb6834"
AQUA = "#1baf7a"
AMARILLO = "#eda100"
MAGENTA = "#e87ba4"
VERDE = "#008300"
VIOLETA = "#7c6fd8"
GRIS = "#898781"
GRIS_CLARO = "#b9b8b0"

GRILLA = "rgba(128,128,128,0.22)"

COLOR_ORIGEN = {"Brasil": AZUL, "China": NARANJA, "Estados Unidos": AQUA, "Alemania": AMARILLO, "Resto del mundo": GRIS_CLARO}
COLOR_METRICA = {"Empleo": AZUL, "Producción (IPI)": NARANJA, "Salario real": AQUA, "Empresas": AMARILLO}

# escala divergente: azul (baja) - neutro - naranja (sube)
ESCALA_DIVERGENTE = [[0.0, AZUL], [0.5, "rgba(200,200,195,0.35)"], [1.0, NARANJA]]
# escala divergente para resultados: naranja (empeora) - neutro - azul (mejora)
ESCALA_RESULTADO = [[0.0, NARANJA], [0.5, "rgba(200,200,195,0.35)"], [1.0, AZUL]]


def layout(titulo: str | None = None, alto: int = 320, leyenda: bool = True, **extra) -> dict:
    # Sin título se fija texto vacío: si el título queda sin texto, Streamlit deja que Plotly dibuje "undefined".
    top = 34 if (titulo or leyenda) else 16
    base = dict(
        height=alto,
        margin=dict(l=8, r=12, t=top + (16 if titulo and leyenda else 0), b=8),
        title=dict(text=titulo or "", x=0, xanchor="left", font=dict(size=14)),
        font=dict(size=11),
        hoverlabel=dict(font_size=11),
        showlegend=leyenda,
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0, title_text="", font=dict(size=11), traceorder="normal"),
    )
    base.update(extra)
    return base


def estilo_ejes(fig, x_titulo: str | None = None, y_titulo: str | None = None):
    fig.update_xaxes(title_text=x_titulo or "", title_font=dict(size=11), gridcolor=GRILLA, zeroline=False, showline=True, linecolor=GRILLA)
    fig.update_yaxes(title_text=y_titulo or "", title_font=dict(size=11), gridcolor=GRILLA, zeroline=False, showline=False)
    return fig


ESTILO_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@400;500&display=swap');
html { font-size: 15px; }

/* página: aire arriba (para que no quede pegada a la barra de pestañas) y ancho de lectura */
[data-testid="stMainBlockContainer"] { padding: 5.5rem 3rem 3rem; max-width: 1400px; }
[data-testid="stVerticalBlock"] { gap: 1rem; }
[data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"] { gap: .4rem; }

/* jerarquía de títulos: título de página > encabezado de sección */
[data-testid="stHeading"] h1 { font-size: 2.1rem !important; font-weight: 700; line-height: 1.15; padding: 0; margin: 0; }
[data-testid="stHeading"] h3 { font-size: 1.4rem !important; font-weight: 650; line-height: 1.25; padding: 0 0 .4rem; margin: 0;
                               border-bottom: 1px solid rgba(128,128,128,.28); }
[data-testid="stElementContainer"]:has([data-testid="stHeading"] h3) { margin-top: 1.3rem; }
.subtitulo { font-size: 1.1rem; line-height: 1.45; color: #898781; margin: .35rem 0 .6rem; }
/* hallazgos del Resumen: tarjetas tipo afiche (fondo oscuro fijo, cifra gigante condensada, frase en mayúsculas).
   Cada hallazgo es una sección con encabezado y una línea que la separa de la siguiente; adentro, una fila de 5 tarjetas
   en una grilla de 12 columnas: las 2 con más contenido ocupan 3 columnas y las demás 2 (ancho según contenido, nunca vacías). */
.hallazgos { display: flex; flex-direction: column; gap: 2.6rem; margin: .6rem 0 1rem; }
.hz-cab { display: flex; align-items: baseline; gap: .9rem; padding-bottom: .55rem; margin-bottom: 1rem; border-bottom: 2px solid rgba(128,128,128,.5); }
.hz-num { font-family: 'IBM Plex Mono', ui-monospace, monospace; font-size: .95rem; font-weight: 500; color: #eb6834; letter-spacing: .08em; }
.hz-tit { font-size: 1.2rem; font-weight: 700; line-height: 1.3; }
.hz-grilla { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 1rem; align-items: stretch; }
.hz-grilla .ancho { grid-column: span 3; } .hz-grilla .angosto { grid-column: span 2; }
.afiche { background: #151311; color: #f3efe8; border: 1px solid rgba(255,255,255,.3); box-shadow: 0 0 0 1px rgba(0,0,0,.25); border-radius: 12px; padding: 1rem 1.05rem .9rem;
          display: flex; flex-direction: column; min-width: 0; --acento: #ff5c3d; }
.afiche.pos { --acento: #4f9cf0; } .afiche.neu { --acento: #f3efe8; }
.af-cab { display: flex; flex-direction: column; font-family: 'IBM Plex Mono', ui-monospace, monospace; font-size: .72rem; letter-spacing: .1em;
          text-transform: uppercase; color: #d2cbbf; line-height: 1.45; }
.af-cab span:last-child { color: #a29a8d; }
.af-cuerpo { padding: .8rem 0 .75rem; }
.af-barra { width: 2.4rem; height: 4px; background: var(--acento); margin-bottom: .6rem; }
.afiche.neu .af-barra { background: #ff5c3d; }
.af-valor { font-family: 'Anton', 'Impact', 'Arial Narrow Bold', sans-serif; font-weight: 400; color: var(--acento); line-height: 1;
            font-size: 2.7rem; letter-spacing: 0; white-space: nowrap; }
.af-frase { font-family: 'Anton', 'Impact', 'Arial Narrow Bold', sans-serif; font-weight: 400; text-transform: uppercase; line-height: 1.12;
            font-size: 1.12rem; margin-top: .45rem; letter-spacing: .02em; }
.ancho .af-valor { font-size: 3.3rem; } .ancho .af-frase { font-size: 1.3rem; }
.af-pie { margin-top: auto; border-top: 1px solid rgba(243,239,232,.18); padding-top: .6rem; }
.af-det { font-size: .92rem; line-height: 1.45; color: #efe9df; }
.af-det b { color: var(--acento); font-weight: 700; } .afiche.neu .af-det b { color: #ff5c3d; }
.af-fuente { font-family: 'IBM Plex Mono', ui-monospace, monospace; font-size: .7rem; color: #a29a8d; margin-top: .45rem; white-space: nowrap; }
/* notebooks chicas: sigue la fila de 5, con letra un poco menor para que nada se corte */
@media (max-width: 1250px) {
  .hz-grilla { gap: .75rem; } .afiche { padding: .9rem .85rem .8rem; }
  .af-valor { font-size: 2.2rem; } .af-frase { font-size: 1rem; } .ancho .af-valor { font-size: 2.8rem; } .ancho .af-frase { font-size: 1.15rem; }
  .af-cab { font-size: .66rem; letter-spacing: .06em; } .af-det { font-size: .86rem; } .af-fuente { white-space: normal; }
}
/* pantallas medianas: dos renglones completos, las 2 anchas arriba (3+3) y las 3 angostas abajo (2+2+2), sin huecos */
@media (max-width: 950px) {
  .hz-grilla { grid-template-columns: repeat(6, minmax(0, 1fr)); }
  .hz-grilla .ancho { grid-column: span 3; order: 0; } .hz-grilla .angosto { grid-column: span 2; order: 1; }
  .hz-grilla .angosto .af-valor { font-size: 2.4rem; }
}
@media (max-width: 640px) { .hz-grilla { grid-template-columns: 1fr; } .hz-grilla .ancho, .hz-grilla .angosto { grid-column: auto; } }
.etiqueta { font-size: .78rem; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; color: #898781; margin-bottom: 1.3rem; }

/* barra superior: nombre del proyecto a la izquierda y pestañas de solo texto centradas. Se ocultan el botón Deploy y el menú «⋮»
   de Streamlit (tapaban las últimas pestañas); el costado derecho se anula para que las pestañas usen todo el ancho. */
[data-testid="stHeader"] { border-bottom: 1px solid rgba(128,128,128,.18); }
[data-testid="stAppDeployButton"], [data-testid="stMainMenu"] { display: none !important; }
[data-testid="stToolbar"] > div > div:nth-child(3) { flex: 0 0 0 !important; min-width: 0 !important; width: 0 !important; padding: 0 !important; overflow: hidden; }
[data-testid="stToolbar"] > div > div:nth-child(1) { flex: 0 0 auto; display: flex; align-items: center; padding-left: 1.6rem; }
[data-testid="stToolbar"] > div > div:nth-child(1)::before {
  content: "Importaciones e industria\\A Argentina · 2016-2026"; white-space: pre; font-size: .82rem; font-weight: 700; line-height: 1.25;
  letter-spacing: .01em; border-left: 3px solid #eb6834; padding-left: .6rem; }
[data-testid="stToolbar"] > div > div:nth-child(2) { flex: 1 1 auto; }
[data-testid="stToolbar"] .rc-overflow { justify-content: center; gap: .15rem; }
[data-testid="stTopNavLink"] > span:has([data-testid="stIconMaterial"]) { display: none; }   /* sin íconos: más limpio y entra todo */
[data-testid="stTopNavLink"] { background: transparent !important; border-radius: 0; padding: .55rem .75rem; opacity: .68;
                               box-shadow: inset 0 -2px 0 transparent; transition: opacity .15s, box-shadow .15s; }
[data-testid="stTopNavLink"] p { font-size: .9rem; font-weight: 550; letter-spacing: .005em; }
[data-testid="stTopNavLink"]:hover { opacity: 1; box-shadow: inset 0 -2px 0 rgba(128,128,128,.35); }
[data-testid="stTopNavLink"][aria-current="page"] { opacity: 1; box-shadow: inset 0 -2px 0 #eb6834; }
[data-testid="stTopNavLink"][aria-current="page"] p { font-weight: 700; }
@media (max-width: 1100px) {
  [data-testid="stToolbar"] > div > div:nth-child(1)::before { content: none; }
  [data-testid="stToolbar"] > div > div:nth-child(1) { padding-left: .6rem; }
  [data-testid="stToolbar"] .rc-overflow { gap: 0; }
  [data-testid="stTopNavLink"] { padding: .55rem .45rem; }
  [data-testid="stTopNavLink"] p { font-size: .84rem; }
}

/* presentación: cada sección es una diapositiva a todo el ancho (bordes negativos que cancelan el padding lateral de la página), no una tarjeta */
/* cada diapositiva mide exactamente una pantalla (el alto visible menos la barra de pestañas) y el scroll se engancha de a una,
   así nunca se ve un pedazo de la anterior o de la siguiente. Si el contenido no entra, la diapositiva crece (min-height) en vez de cortarlo. */
:root { --barra: 56px; --alto-slide: calc(100dvh - var(--barra)); }
[data-testid="stMain"]:has(.st-key-slide_portada) { scroll-snap-type: y mandatory; scroll-padding-top: var(--barra); }
[data-testid="stMainBlockContainer"]:has(.st-key-slide_portada) { padding-top: var(--barra) !important; padding-bottom: 0 !important; }
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]:has(.st-key-slide_portada) { gap: 0 !important; }
[class*="st-key-slide_"] { position: relative !important; width: calc(100% + 6rem) !important; max-width: calc(100% + 6rem) !important; margin: 0 -3rem !important;
                           box-sizing: border-box !important; padding: clamp(1.6rem, 6vh, 4.6rem) max(4rem, calc(50% - 560px)); min-height: var(--alto-slide);
                           scroll-snap-align: start; scroll-snap-stop: always; display: flex; flex-direction: column;
                           justify-content: center; gap: .5rem; border: 0; border-top: 1px solid rgba(128,128,128,.16); border-radius: 0; background: transparent; }
.st-key-slide_preguntas, .st-key-slide_resultado { background: rgba(128,128,128,.035); }
.st-key-slide_recorrido { padding-bottom: 3.6rem; }

/* portada: ocupa toda la pantalla, con su propio fondo e independiente del tema claro/oscuro */
.st-key-slide_portada { border-top: 0; padding: clamp(2rem, 9vh, 7rem) max(4rem, calc(50% - 560px)) clamp(1.4rem, 4vh, 3rem); color: #fff;
                        align-items: center;
                        background: radial-gradient(circle at 1px 1px, rgba(255,255,255,.10) 1.4px, transparent 0) 0 0/30px 30px,
                                    linear-gradient(125deg, #0e1b33 0%, #1f3864 45%, #7a3418 130%); }
/* título y pregunta centrados: los bloques con max-width necesitan margen automático a los costados, no alcanza con text-align */
.st-key-slide_portada .slide-kicker, .st-key-slide_portada .hero-titulo, .st-key-slide_portada .hero-sub { text-align: center; margin-left: auto; margin-right: auto; }
.st-key-slide_portada .hero-pie { align-self: stretch; }
.hero-fuentes-etq { font-size: .78rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #9dc2f5; margin-bottom: .35rem; }
.slide-badge { position: absolute; top: clamp(1rem, 3.5vh, 1.8rem); right: max(2.2rem, calc(50% - 560px + 1.8rem)); font-size: .8rem; font-weight: 600; letter-spacing: .1em;
              color: rgba(128,128,128,.7); }
.st-key-slide_portada .slide-badge { color: rgba(255,255,255,.55); }
.slide-kicker { font-size: .85rem; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: #2a78d6; margin: 0 0 .9rem; }
.st-key-slide_portada .slide-kicker { color: #9dc2f5; }
.slide-titulo { font-size: clamp(1.9rem, 3.2vw, 2.9rem); font-weight: 730; line-height: 1.15; letter-spacing: -.01em; margin: 0 0 clamp(1.2rem, 4vh, 2.6rem); max-width: 48rem; }
.slide-texto { font-size: 1.25rem; line-height: 1.6; color: #898781; max-width: 46rem; margin: -1rem 0 2.4rem; }
.hero-titulo { font-size: clamp(2.3rem, min(5.4vw, 9.5vh), 5.2rem); font-weight: 780; line-height: 1.06; letter-spacing: -.02em; margin: .5rem 0 clamp(1rem, 3vh, 1.8rem); max-width: 50rem; color: #fff; }
.nowrap { white-space: nowrap; }
.hero-sub { font-size: clamp(1.05rem, 1.7vw, 1.45rem); line-height: 1.55; color: rgba(255,255,255,.8); max-width: 36rem; margin: 0 0 clamp(1.4rem, 5vh, 3.5rem); }
.hero-pie { margin-top: auto; padding-top: clamp(1rem, 3.5vh, 2.4rem); border-top: 1px solid rgba(255,255,255,.22);
           display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 1.2rem; }
.hero-autor { font-size: 1.2rem; line-height: 1.4; color: #fff; }
.hero-rol { font-size: .95rem; line-height: 1.5; color: rgba(255,255,255,.68); margin-top: .2rem; }
.hero-fuentes { font-size: .85rem; letter-spacing: .04em; color: rgba(255,255,255,.62); line-height: 1.6; text-align: right; }
.postura { border: 1px solid rgba(128,128,128,.3); border-radius: 16px; padding: 2.2rem 2.3rem; background: rgba(128,128,128,.06); height: 100%; }
.postura-etq { font-size: .8rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #eb6834; margin-bottom: .9rem; }
.postura-frase { font-size: 1.9rem; font-weight: 700; line-height: 1.22; margin-bottom: 1rem; }
.postura-texto { font-size: 1.15rem; line-height: 1.55; color: #898781; }
.cierre-slide { font-size: 1.4rem; font-weight: 600; line-height: 1.5; text-align: center; margin-top: 2.8rem; }
.pregunta-num { font-size: 3.8rem; font-weight: 760; line-height: 1; color: #2a78d6; opacity: .85; margin-bottom: .7rem; }
.pregunta-tit { font-size: 1.6rem; font-weight: 700; line-height: 1.25; margin-bottom: .8rem; }
.pregunta-txt { font-size: 1.15rem; line-height: 1.6; color: #898781; }
.cifra { font-size: 2.8rem; font-weight: 750; line-height: 1.1; margin-bottom: .5rem; }
.cifra-etq { font-size: 1rem; line-height: 1.4; color: #898781; }
.gran-numero { font-size: 4.6rem; font-weight: 800; line-height: 1.05; letter-spacing: -.02em; margin-bottom: .7rem; }
.gran-numero.az { color: #2a78d6; } .gran-numero.na { color: #eb6834; } .gran-numero.gr { color: #898781; }
.gran-tit { font-size: 1.45rem; font-weight: 700; line-height: 1.25; margin-bottom: .7rem; }
.gran-etq { font-size: 1.15rem; line-height: 1.55; color: #898781; }
.st-key-cta { margin-bottom: 1.6rem; }
.st-key-slide_recorrido [data-testid="stHorizontalBlock"] { margin-bottom: .8rem; }
.st-key-cta a { border: 1px solid #2a78d6; border-radius: 999px; justify-content: center; padding: .5rem 1.1rem; font-weight: 600; }
.st-key-cta a:hover { background: rgba(42,120,214,.12); }
[data-testid="stPageLink"] p { font-size: 1.05rem; }

/* texto corrido: ancho de lectura cómodo (los recuadros de gráficos y las tarjetas usan todo el ancho) */
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] > [data-testid="stMarkdown"] { max-width: 64rem; }
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] > [data-testid="stMarkdown"]:has(.hallazgos) { max-width: none; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { line-height: 1.65; }
[data-testid="stMarkdownContainer"] ol, [data-testid="stMarkdownContainer"] ul { padding-left: 1.4rem; }
[data-testid="stMarkdownContainer"] ol li { margin-bottom: .75rem; }
[data-testid="stMarkdownContainer"] ul li { margin-bottom: .3rem; }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { font-size: .92rem !important; line-height: 1.55; }

/* indicadores */
[data-testid="stMetric"] [data-testid="stMetricValue"], [data-testid="stMetric"] [data-testid="stMetricValue"] * { font-size: 2rem !important; line-height: 1.25; }
[data-testid="stMetric"] [data-testid="stMetricLabel"] p { font-size: .95rem; margin: 0; }
[data-testid="stMetric"] [data-testid="stMetricDelta"] { font-size: .9rem; }

/* recuadros de gráficos (tamaños fijos en px para que no dependan de la escala general) */
.bloque-titulo { font-size: 14.3px; font-weight: 600; line-height: 1.3; margin: 0 0 .9rem; }  /* el margen inferior compensa el margen negativo de Streamlit */
.expl p { font-size: 12px; line-height: 1.45; margin: 0 0 .6rem; }
.expl p:last-child { margin-bottom: 1rem; }
.expl p.nota { color: #898781; font-style: italic; }
/* informe («Conclusiones»): hojas A4 blancas, con tipografía de documento, iguales en tema claro y oscuro */
[class*="st-key-hoja_"] { background: #fff; width: min(210mm, 100%); min-height: 297mm; margin: 0 auto 1.6rem; padding: 16mm 20mm 10mm;
                          box-sizing: border-box; box-shadow: 0 1px 2px rgba(0,0,0,.3), 0 10px 30px rgba(0,0,0,.18); gap: .3rem; }
[class*="st-key-hoja_"] > [data-testid="stElementContainer"]:last-child { margin-top: auto; }
div.doc { font-family: Cambria, "Times New Roman", Georgia, serif; font-size: 10.5pt; line-height: 1.45; color: #1b1b1b; text-align: justify; hyphens: auto; }
div.doc p { font-size: 10.5pt; line-height: 1.45; margin: 0 0 .75rem; color: #1b1b1b; }
div.doc b, div.doc i, div.doc li, div.doc td { color: #1b1b1b; }
div.doc .h1 { font-family: Calibri, Carlito, "Segoe UI", Arial, sans-serif; font-size: 15pt; font-weight: 700; color: #1f3864; margin: .5rem 0 .55rem;
              padding-bottom: 2px; border-bottom: 1px solid #b4c0d8; text-align: left; }
div.doc .h2 { font-family: Calibri, Carlito, "Segoe UI", Arial, sans-serif; font-size: 12pt; font-weight: 700; color: #2f5496; margin: .35rem 0 .45rem; text-align: left; }
div.doc ol.lista, div.doc ul.lista { margin: 0 0 .75rem; padding-left: 1.5rem; }
div.doc ol.lista li, div.doc ul.lista li { font-size: 10.5pt; line-height: 1.45; margin: 0 0 .3rem; }
div.doc p.leyenda { font-size: 9pt; line-height: 1.35; color: #555; text-align: left; margin: .1rem 0 1.2rem; }
div.doc p.leyenda b { color: #555; }
div.doc p.titulo-tabla { font-family: Calibri, Carlito, "Segoe UI", Arial, sans-serif; font-size: 9.5pt; font-weight: 700; color: #1f3864; text-align: left; margin: .2rem 0 .3rem; }
div.doc table.tabla { width: 100%; border-collapse: collapse; margin: 0 0 .2rem; font-family: Calibri, Carlito, "Segoe UI", Arial, sans-serif; font-size: 9pt; }
div.doc table.tabla th { background: #1f3864; color: #fff !important; font-weight: 600; padding: 3px 6px; border: 0; line-height: 1.25; vertical-align: bottom; }
div.doc table.tabla.sin-cortes td.izq { white-space: nowrap; }
div.doc table.tabla td { padding: 2px 6px; border: 0; border-bottom: 1px solid #d5d9e2; line-height: 1.3; }
div.doc table.tabla tbody tr:nth-child(even) td { background: #f3f5fa; }
div.doc .espacio { height: .45rem; }
div.doc .izq { text-align: left; } div.doc .der { text-align: right; } div.doc .cen { text-align: center; }
div.doc .indice .fila { display: flex; align-items: baseline; gap: 6px; font-size: 10.5pt; line-height: 1.3; }
div.doc .indice .punteado { flex: 1; border-bottom: 1px dotted #999; transform: translateY(-3px); }
div.doc .portada { padding: 4mm 0 5mm; border-bottom: 3px solid #1f3864; margin-bottom: 8mm; text-align: left; }
div.doc .portada .sup { font-family: Calibri, Carlito, "Segoe UI", Arial, sans-serif; font-size: 10pt; letter-spacing: .18em; text-transform: uppercase; color: #2f5496; margin: 0 0 .6rem; }
div.doc .portada .titulo { font-family: Calibri, Carlito, "Segoe UI", Arial, sans-serif; font-size: 27pt; line-height: 1.12; font-weight: 700; color: #1f3864; margin: 0 0 .7rem; }
div.doc .portada .subtitulo-doc { font-size: 13pt; line-height: 1.35; color: #444; margin: 0 0 1.1rem; }
div.doc .portada p.autor { font-size: 10.5pt; color: #333; margin: 0; text-align: left; }
div.doc .pie-hoja { display: flex; justify-content: space-between; font-family: Calibri, Carlito, "Segoe UI", Arial, sans-serif; font-size: 8.5pt; color: #777;
                    border-top: 1px solid #ccd; padding-top: 4px; margin-top: .6rem; }
/* impresión / «Guardar como PDF»: cada hoja del informe es una página A4 */
@media print {
  @page { size: A4; margin: 0; }
  html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stMainBlockContainer"] { height: auto !important; overflow: visible !important; position: static !important; }
  [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebar"] { display: none !important; }
  [data-testid="stMainBlockContainer"] { padding: 0 !important; max-width: none !important; }
  [data-testid="stElementContainer"]:has([data-testid="stHeading"]), [data-testid="stElementContainer"]:has(.subtitulo) { display: none !important; }
  [data-testid="stVerticalBlock"]:has([class*="st-key-hoja_"]) { gap: 0 !important; }
  [class*="st-key-hoja_8"] { break-after: auto !important; page-break-after: auto !important; }
  [class*="st-key-hoja_"] { box-shadow: none !important; margin: 0 !important; width: 210mm !important; height: 296mm !important; min-height: 0 !important; overflow: hidden;
                            break-after: page; page-break-after: always; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
</style>
"""


def aplicar_estilo():
    """Reduce la escala de la interfaz para que cada bloque se vea completo en una notebook."""
    import streamlit as st
    st.markdown(ESTILO_CSS, unsafe_allow_html=True)
