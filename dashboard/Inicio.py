"""Punto de entrada del dashboard: define las páginas y la navegación. Cada página vive en paginas/<nombre>.py."""
import streamlit as st

from core.tema import aplicar_estilo
from paginas import comparador, datos, empleo_ramas, exposicion, importaciones, informe, metodologia, presentacion, resumen

st.set_page_config(page_title="Importaciones e industria en Argentina", page_icon=":material/factory:", layout="wide")
aplicar_estilo()



def _presentacion():
    presentacion.mostrar({p.title: p for p in PAGINAS})


PAGINAS = [
    st.Page(_presentacion, title="Presentación", icon=":material/home:", default=True),
    st.Page(resumen.mostrar, title="Resumen", icon=":material/dashboard:", url_path="resumen"),
    st.Page(importaciones.mostrar, title="Importaciones", icon=":material/local_shipping:", url_path="importaciones"),
    st.Page(empleo_ramas.mostrar, title="Empleo y ramas", icon=":material/groups:", url_path="empleo-y-ramas"),
    st.Page(exposicion.mostrar, title="Importaciones vs. resultados", icon=":material/compare_arrows:", url_path="importaciones-vs-resultados"),
    st.Page(comparador.mostrar, title="Comparador de ramas", icon=":material/monitoring:", url_path="comparador"),
    st.Page(informe.mostrar, title="Conclusiones", icon=":material/description:", url_path="conclusiones"),
    st.Page(metodologia.mostrar, title="Método y límites", icon=":material/fact_check:", url_path="metodo"),
    st.Page(datos.mostrar, title="Datos", icon=":material/database:", url_path="datos"),
]
pagina = st.navigation(PAGINAS, position="top")

SUBTITULOS = {
    "Resumen": "Empleo, salarios, producción e importaciones de la industria argentina · INDEC y Ministerio de Trabajo · 2016-2026",
    "Importaciones": "De dónde vienen las importaciones, qué ramas industriales las reciben y cuánto avanzó China",
    "Empleo y ramas": "Qué pasó con el empleo, el salario real, la producción y las empresas en cada una de las 16 ramas industriales",
    "Importaciones vs. resultados": "Si se perdió empleo, producción y salario justo en los sectores donde más crecieron las importaciones",
    "Comparador de ramas": "Una rama de punta a punta, contra el total de la industria",
    "Conclusiones": "El trabajo completo resumido como informe: preguntas, método, resultados, conclusiones y límites",
    "Método y límites": "Fuentes, decisiones de método, controles de calidad y alcance de las conclusiones",
    "Datos": "Cada archivo original del proyecto: de dónde sale, para qué se usó, cuántos datos tiene y dónde se descarga",
}

if pagina.title != "Presentación":  # la presentación lleva su propia portada en vez de título y subtítulo
    st.title(f"{pagina.icon} {pagina.title}")  # el ícono va dentro del texto: `st.title(icon=...)` no existe en todas las versiones de Streamlit
    st.markdown(f'<p class="subtitulo">{SUBTITULOS.get(pagina.title, "")}</p>', unsafe_allow_html=True)
pagina.run()
