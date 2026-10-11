"""Página «Presentación»: el trabajo contado como una presentación, en diapositivas a pantalla completa (portada, tema, preguntas, datos, resultado y recorrido)."""
import streamlit as st

from core.consultas import empleo_trimestre, trimestre_texto
from core.datos import AUTOR, RAMAS, TOTAL, leer
from core.formato import fmt_miles, fmt_num, fmt_pct

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
TOTAL_SLIDES = 6

# descripción de cada pestaña, en el orden en que se recomienda recorrerlas
RECORRIDO = [
    ("Resumen", "Los indicadores clave, los cinco hallazgos principales y tres gráficos de contexto."),
    ("Importaciones", "De dónde vienen, qué ramas las reciben, cuánto avanzó China y la balanza de cada rama."),
    ("Empleo y ramas", "Cuántos puestos ganó o perdió cada rama y cómo cambiaron su salario, producción y empresas."),
    ("Importaciones vs. resultados", "La pregunta central: si se perdió empleo, producción y salario justo donde más crecieron las importaciones."),
    ("Comparador de ramas", "Una rama de punta a punta, comparada con el total de la industria."),
    ("Método y límites", "Fuentes, controles de calidad, decisiones de método y qué no se puede concluir."),
]


def _badge(n: int) -> None:
    st.markdown(f'<div class="slide-badge">{n:02d} / {TOTAL_SLIDES:02d}</div>', unsafe_allow_html=True)


def _kicker(tema: str, titulo: str) -> None:
    st.markdown(f'<div class="slide-kicker">{tema}</div><div class="slide-titulo">{titulo}</div>', unsafe_allow_html=True)


def _vigencia() -> str:
    """Hasta cuándo llega cada serie, leído de los datos procesados (cambia solo cuando se actualizan)."""
    def ultimo(archivo: str):
        return leer(archivo, ("periodo",)).periodo.max()

    ipi, sal = ultimo("ipi_por_rama.csv"), ultimo("salario_real_por_rama.csv")
    return (f"Empleo al {trimestre_texto(ultimo('empleo_por_rama.csv'))} · Salarios a {MESES[sal.month - 1][:3]} {sal.year}<br>"
            f"Producción a {MESES[ipi.month - 1][:3]} {ipi.year} · Comercio exterior {leer('comercio_por_rama_anio.csv').anio.max()}")


def _portada() -> None:
    with st.container(key="slide_portada"):
        _badge(1)
        st.markdown(
            '<div class="slide-kicker">Proyecto de análisis de datos</div>'
            '<div class="hero-titulo">Importaciones e industria en Argentina, <span class="nowrap">2016-2026</span></div>'
            '<div class="hero-sub">Desde 2018, ¿la industria argentina perdió empleo, producción y salario justo en los sectores donde más crecieron '
            'las importaciones? Un análisis con datos oficiales.</div>'
            '<div class="hero-pie">'
            f'<div><div class="hero-autor"><b>{AUTOR}</b></div><div class="hero-rol">Análisis y desarrollo del dashboard</div></div>'
            '<div class="hero-fuentes"><div class="hero-fuentes-etq">Datos oficiales · últimos publicados</div>'
            f'{_vigencia()}<br>INDEC · Ministerio de Trabajo (OEDE) · ARCA</div>'
            '</div>',
            unsafe_allow_html=True,
        )


def _tema() -> None:
    with st.container(key="slide_tema"):
        _badge(2)
        _kicker("El tema", "Un debate con dos posturas enfrentadas")
        a, b = st.columns(2, gap="large")
        with a:
            st.markdown('<div class="postura"><div class="postura-etq">Postura 1</div><div class="postura-frase">Importar más destruye industria y empleo.</div>'
                        '<div class="postura-texto">Sostiene que los productos importados, sobre todo los que vienen de China, desplazan a la producción nacional.</div></div>',
                        unsafe_allow_html=True)
        with b:
            st.markdown('<div class="postura"><div class="postura-etq">Postura 2</div><div class="postura-frase">Importar acompaña a la actividad.</div>'
                        '<div class="postura-texto">Sostiene que las importaciones abaratan los insumos y traen la maquinaria que las fábricas necesitan para producir.</div></div>',
                        unsafe_allow_html=True)
        st.markdown('<div class="cierre-slide">Este trabajo no toma partido: <b>mide qué dicen los datos</b>.</div>', unsafe_allow_html=True)


def _preguntas() -> None:
    with st.container(key="slide_preguntas"):
        _badge(3)
        _kicker("Las preguntas", f"Tres preguntas sobre la industria manufacturera y sus {len(RAMAS)} ramas")
        columnas = st.columns(3, gap="large")
        textos = [
            ("01", "¿Qué pasó?", "Cómo evolucionaron el empleo, el salario real, la producción y las empresas de la industria, y el comercio exterior del país."),
            ("02", "¿Dónde pasó?", "Si el total esconde ramas que crecieron y ramas que se achicaron: textiles, alimentos, automotores, maquinaria y otras once."),
            ("03", "¿Hay relación con las importaciones?", "Si los sectores que más perdieron son los mismos donde más crecieron las importaciones o más avanzó China, separando lo que compite (consumo) de lo que abastece (insumos). Se miden coincidencias, no causas."),
        ]
        for col, (n, t, d) in zip(columnas, textos):
            with col:
                st.markdown(f'<div class="pregunta-num">{n}</div><div class="pregunta-tit">{t}</div><div class="pregunta-txt">{d}</div>', unsafe_allow_html=True)


def _datos() -> None:
    control, por_uso = leer("control_comex.csv"), leer("importaciones_por_uso.csv")
    clasificado = por_uso[por_uso.uso != "Sin clasificar"].imp_cif.sum() / por_uso.imp_cif.sum() * 100
    registros = int(control.registros_imp.sum() + control.registros_exp.sum())
    cifras = [(fmt_miles(registros), f"registros de comercio exterior, {int(control.anio.min())}-{int(control.anio.max())}"),
              (str(len(RAMAS)), "ramas industriales comparables"),
              ("3", "fuentes oficiales: INDEC, Trabajo y ARCA"),
              ("2018-2025", "el período que se compara, rama por rama"),
              (f"{fmt_num(int(clasificado * 10) / 10, 1)}%", "de lo importado, clasificado por uso: consumo, insumos y capital")]
    with st.container(key="slide_datos"):
        _badge(4)
        _kicker("Los datos", "Datos oficiales llevados a un solo idioma")
        st.markdown('<div class="slide-texto">Comercio exterior, empleo, salarios y producción vienen clasificados de forma distinta. '
                    'Los traduje a 16 ramas industriales para poder compararlos, y verifiqué que los totales coincidan con los oficiales.</div>', unsafe_allow_html=True)
        for col, (n, t) in zip(st.columns(5, gap="medium"), cifras):
            col.markdown(f'<div class="cifra">{n}</div><div class="cifra-etq">{t}</div>', unsafe_allow_html=True)


def _resultado() -> None:
    comercio = leer("resumen_comercio_anual.csv")
    c25 = comercio.iloc[-1]
    q23 = empleo_trimestre(TOTAL, "2023")
    g = leer("respuesta_grupos.csv").set_index("grupo")
    mas, menos, tot = g.loc["Importaciones crecieron más"], g.loc["Importaciones crecieron menos"], g.loc["Total industria"]
    pr = leer("respuesta_por_rama.csv").set_index("rama").loc["18-19"]
    u = leer("respuesta_uso_correlaciones.csv")
    cons = u[(u.exposicion_col == "consumo_usd") & (u.resultado_col == "empleo")].iloc[0]
    with st.container(key="slide_resultado"):
        _badge(5)
        _kicker("Qué encontré", "La respuesta, en tres cifras")
        a, b, c = st.columns(3, gap="large")
        a.markdown(f'<div class="gran-numero na">{fmt_pct(tot.produccion)}</div><div class="gran-tit">La industria produce menos</div>'
                   f'<div class="gran-etq">Entre 2018 y 2025 la producción varió {fmt_pct(tot.produccion)} y el salario real {fmt_pct(tot.salario)}. '
                   f'El empleo cae desde 2023: {fmt_pct(q23.delta_pct)} hasta el {q23.trimestre_ultimo}.</div>', unsafe_allow_html=True)
        b.markdown(f'<div class="gran-numero az">{fmt_miles(round(mas.puestos, -3)) if mas.puestos < 0 else "+" + fmt_miles(round(mas.puestos, -3))}</div>'
                   f'<div class="gran-tit">Empleos donde más se importó</div>'
                   f'<div class="gran-etq">Donde menos crecieron las importaciones: {fmt_miles(round(menos.puestos, -3))}. No se perdió justo donde más se importó: '
                   f'lo que crece con el empleo son los insumos, y con los bienes de consumo no hay relación (ρ = {fmt_num(cons.rho, 2)}).</div>', unsafe_allow_html=True)
        c.markdown(f'<div class="gran-numero na">{fmt_miles(round(pr.puestos, -2))}</div><div class="gran-tit">La excepción: prendas y calzado</div>'
                   f'<div class="gran-etq">Importó {fmt_pct(pr.imp_ton, False)} más en toneladas y perdió {fmt_miles(abs(pr.puestos))} puestos. '
                   f'China ya es {fmt_num(c25.pct_china)}% de todo lo importado, el máximo de la serie.</div>', unsafe_allow_html=True)
        st.markdown('<div class="cierre-slide">Los datos muestran <b>coincidencias, no causas</b>.</div>', unsafe_allow_html=True)


def _recorrido(paginas: dict) -> None:
    with st.container(key="slide_recorrido"):
        _badge(6)
        _kicker("Cómo recorrerlo", "Explorá el trabajo")
        with st.container(key="cta"):
            b1, b2, _ = st.columns([1, 1, 2], gap="medium")
            b1.page_link(paginas["Resumen"], label="Empezar por el resumen", icon=":material/arrow_forward:", width="stretch")
            b2.page_link(paginas["Conclusiones"], label="Leer el informe", icon=":material/description:", width="stretch")
        for fila in (RECORRIDO[:3], RECORRIDO[3:]):
            for col, (titulo, texto) in zip(st.columns(3, gap="medium"), fila):
                with col, st.container(border=True):
                    st.page_link(paginas[titulo], label=f"**{titulo}**", icon=paginas[titulo].icon, width="stretch")
                    st.caption(texto)
        st.caption(f"{AUTOR} · Datos: INDEC, Ministerio de Trabajo (OEDE) y ARCA · Todas las cifras se calculan a partir de los datos procesados del proyecto.")


# La rueda del mouse avanza de a una diapositiva. Solo con CSS (scroll-snap) un giro corto de la rueda vuelve a la misma diapositiva.
# El listener se registra una sola vez y no hace nada en las otras páginas (no hay diapositivas); si una diapositiva es más alta
# que la pantalla (pantallas muy bajas) se deja el scroll normal para poder leerla entera.
_RUEDA_JS = """
<script>
(() => {
  if (window.__ruedaSlides) return;
  window.__ruedaSlides = true;
  let bloqueado = false, acumulado = 0;
  document.addEventListener('wheel', (e) => {
    const main = document.querySelector('[data-testid="stMain"]');
    const slides = [...document.querySelectorAll('[class*="st-key-slide_"]')];
    if (!main || !slides.length || e.ctrlKey || !main.contains(e.target)) return;
    const barra = main.getBoundingClientRect().top + 56;
    const actual = slides.reduce((mejor, s, i) =>
      Math.abs(s.getBoundingClientRect().top - barra) < Math.abs(slides[mejor].getBoundingClientRect().top - barra) ? i : mejor, 0);
    const r = slides[actual].getBoundingClientRect();
    const visible = main.clientHeight - 56;
    if (r.height > visible + 4 && ((e.deltaY > 0 && r.bottom > main.clientHeight + 4) || (e.deltaY < 0 && r.top < barra - 4))) return;
    e.preventDefault();
    if (bloqueado) return;
    acumulado += e.deltaY;
    if (Math.abs(acumulado) < 30) return;   // los trackpads mandan muchos movimientos chicos
    const destino = Math.max(0, Math.min(slides.length - 1, actual + (acumulado > 0 ? 1 : -1)));
    acumulado = 0;
    bloqueado = true;
    slides[destino].scrollIntoView({behavior: 'smooth', block: 'start'});
    setTimeout(() => { bloqueado = false; }, 750);
  }, {passive: false});
})();
</script>
"""


def mostrar(paginas: dict) -> None:
    st.html(_RUEDA_JS, unsafe_allow_javascript=True)
    _portada()
    _tema()
    _preguntas()
    _datos()
    _resultado()
    _recorrido(paginas)
