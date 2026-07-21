"""Estilo institucional compartido (CIEFD) para todas las páginas de la app."""
import os
from datetime import datetime

import streamlit as st

RUTA_LOGO = os.path.join(os.path.dirname(__file__), "assets", "logo_imss.png")

CSS_BASE = """
<style>
.stApp { background-color: #f4f5f0; }

.hero {
    background: #1f4d3a;
    padding: 1.8rem 2.2rem;
    border-radius: 10px;
    color: #faf6ec;
    margin-bottom: 1rem;
    border-left: 6px solid #d9c69c;
}
.hero .institucion {
    font-size: 2.4rem;
    font-weight: 900;
    letter-spacing: 3px;
    color: #d9c69c;
    line-height: 1.1;
    margin-bottom: 0.15rem;
}
.hero .institucion-nombre {
    font-size: 0.95rem;
    color: #e4ddc8;
    margin-bottom: 1.1rem;
}
.hero h1 {
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
    color: #ffffff;
}
.hero .subtitulo {
    font-size: 0.9rem;
    color: #d9c69c;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}
.hero p {
    font-size: 0.95rem;
    color: #e4ddc8;
    margin-bottom: 0;
    line-height: 1.5;
}
.hero code {
    background: rgba(255,255,255,0.14);
    padding: 2px 8px;
    border-radius: 4px;
    color: #faf6ec;
}

.meta-bar {
    background: #faf6ec;
    border: 1px solid #e0d6bd;
    border-radius: 8px;
    padding: 0.7rem 1.2rem;
    margin-bottom: 1.6rem;
    font-size: 0.85rem;
    color: #4a4030;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.4rem 1.5rem;
}
.meta-bar b { color: #1f4d3a; }

section[data-testid="stFileUploaderDropzone"] {
    border-radius: 8px;
    border: 1.5px dashed #6b9080;
    background-color: #f2efe4;
}

div[data-testid="stMetric"] {
    background-color: #faf6ec;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 1px 2px rgba(31,77,58,0.08);
    border: 1px solid #e0d6bd;
    border-top: 3px solid #1f4d3a;
}

.stTabs [data-baseweb="tab"] {
    font-weight: 600;
    color: #1f4d3a;
}

.seccion-final, .tarjeta {
    background: #faf6ec;
    border-radius: 10px;
    padding: 1.8rem;
    margin-top: 1rem;
    border: 1px solid #e0d6bd;
    border-left: 6px solid #d9c69c;
}

.tarjeta-nav {
    background: #ffffff;
    border-radius: 10px;
    padding: 1.4rem;
    border: 1px solid #e0d6bd;
    border-top: 4px solid #1f4d3a;
    height: 100%;
}
.tarjeta-nav h3 { color: #1f4d3a; margin-bottom: 0.4rem; }
.tarjeta-nav p { color: #4a4030; font-size: 0.9rem; }

.pie-pagina {
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid #e0d6bd;
    font-size: 0.78rem;
    color: #8b8168;
    text-align: center;
}
</style>
"""


def aplicar_estilo():
    st.markdown(CSS_BASE, unsafe_allow_html=True)


def mostrar_encabezado(titulo_pagina: str, descripcion: str, icono: str = "🗂️"):
    """Encabezado institucional con logo (si existe), sigla CIEFD y barra de metadatos."""
    aplicar_estilo()
    ahora = datetime.now()

    col_logo, col_texto = st.columns([1, 6], vertical_alignment="center")
    with col_logo:
        if os.path.exists(RUTA_LOGO):
            st.image(RUTA_LOGO, use_container_width=True)
        else:
            st.markdown(
                """
                <div style="border:1.5px dashed #6b9080; border-radius:8px;
                     padding:0.6rem; text-align:center; font-size:0.7rem;
                     color:#6b9080; background:#f2efe4;">
                    Logo IMSS<br>(pendiente)
                </div>
                """,
                unsafe_allow_html=True,
            )
    with col_texto:
        st.markdown(
            f"""
            <div class="hero" style="margin-top:0;">
                <div class="institucion">CIEFD</div>
                <div class="institucion-nombre">Centro de Investigación Educativa y Formación Docente</div>
                <div class="subtitulo">{icono} {titulo_pagina}</div>
                <p>{descripcion}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="meta-bar">
            <span>🏛️ Institución: <b>IMSS · CIEFD</b></span>
            <span>📅 Fecha: <b>{ahora.strftime('%d/%m/%Y')}</b></span>
            <span>🕒 Hora: <b>{ahora.strftime('%H:%M:%S')}</b></span>
            <span>⚙️ Versión del sistema: <b>2.0</b></span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return ahora


def mostrar_pie_pagina(ahora: datetime):
    st.markdown(
        f"""
        <div class="pie-pagina">
            IMSS · CIEFD — Centro de Investigación Educativa y Formación Docente<br>
            Página generada el {ahora.strftime('%d/%m/%Y a las %H:%M:%S')}
            · Plataforma CIEFD v2.0
            · Los datos procesados no se almacenan; el análisis ocurre únicamente
            durante esta sesión.
        </div>
        """,
        unsafe_allow_html=True,
    )
