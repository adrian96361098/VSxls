import io
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sistema de Cruce y Consolidación de Bases de Datos",
    page_icon="🗂️",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Estilos — paleta institucional (azul marino / gris)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #f4f5f7; }

    .hero {
        background: #1f4d3a;
        padding: 2rem 2.2rem;
        border-radius: 10px;
        color: #faf6ec;
        margin-bottom: 1rem;
        border-left: 6px solid #d9c69c;
    }
    .hero .institucion {
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: 2px;
        color: #d9c69c;
        margin-bottom: 0.1rem;
    }
    .hero .institucion-nombre {
        font-size: 0.85rem;
        color: #e4ddc8;
        margin-bottom: 0.9rem;
    }
    .hero h1 {
        font-size: 1.7rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #ffffff;
        letter-spacing: 0.2px;
    }
    .hero .subtitulo {
        font-size: 0.95rem;
        color: #d9c69c;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.6rem;
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

    .seccion-final {
        background: #faf6ec;
        border-radius: 10px;
        padding: 1.8rem;
        margin-top: 1.5rem;
        border: 1px solid #e0d6bd;
        border-left: 6px solid #d9c69c;
    }

    .pie-pagina {
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid #e0d6bd;
        font-size: 0.78rem;
        color: #8b8168;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

ahora = datetime.now()

st.markdown(
    f"""
    <div class="hero">
        <div class="institucion">CIEFD</div>
        <div class="institucion-nombre">Centro de Investigación Educativa y Formación Docente</div>
        <div class="subtitulo">Herramienta de análisis de datos</div>
        <h1>🗂️ Sistema de Cruce y Consolidación de Bases de Datos</h1>
        <p>Compara dos archivos (CSV o Excel) a partir de una columna clave en
        común (por ejemplo <code>matricula</code> o <code>cardex</code>).
        El sistema genera automáticamente los cruces INNER, LEFT y RIGHT,
        identifica las discrepancias entre ambas fuentes, y produce una base
        de datos consolidada descargable en formato Excel.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="meta-bar">
        <span>🏛️ Institución: <b>CIEFD</b></span>
        <span>📅 Fecha del reporte: <b>{ahora.strftime('%d/%m/%Y')}</b></span>
        <span>🕒 Hora de generación: <b>{ahora.strftime('%H:%M:%S')}</b></span>
        <span>⚙️ Versión del sistema: <b>1.1</b></span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Carga de archivos
# ---------------------------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    archivo1 = st.file_uploader("📄 Archivo 1", type=["csv", "xlsx", "xls"])
with col2:
    archivo2 = st.file_uploader("📄 Archivo 2", type=["csv", "xlsx", "xls"])

if not archivo1 or not archivo2:
    st.info("👆 Sube ambos archivos (CSV o Excel) para comenzar el análisis.")
    st.stop()


def leer_archivo(archivo):
    """Lee CSV o Excel según la extensión del archivo subido."""
    nombre = archivo.name.lower()
    if nombre.endswith((".xlsx", ".xls")):
        return pd.read_excel(archivo, sheet_name=0)
    return pd.read_csv(archivo)


try:
    datos1 = leer_archivo(archivo1)
    datos2 = leer_archivo(archivo2)
except Exception as e:
    st.error(f"❌ Ocurrió un error al leer los archivos: {e}")
    st.stop()

# ---------------------------------------------------------------------------
# Selección de la columna de cruce
# ---------------------------------------------------------------------------
columnas_comunes = sorted(set(datos1.columns) & set(datos2.columns))

if not columnas_comunes:
    st.error(
        "❌ Los archivos no tienen ninguna columna en común. "
        "Revisa que los nombres de columnas coincidan exactamente."
    )
    st.stop()

preferidas = [c for c in ["matricula", "Matrícula", "cardex"] if c in columnas_comunes]
indice_default = columnas_comunes.index(preferidas[0]) if preferidas else 0

columna_cruce = st.selectbox(
    "🔑 Columna para cruzar los archivos",
    columnas_comunes,
    index=indice_default,
)

with st.expander("👀 Vista previa de los archivos cargados"):
    prev1, prev2 = st.columns(2)
    with prev1:
        st.caption(f"Archivo 1 — {len(datos1)} filas")
        st.dataframe(datos1.head(), use_container_width=True)
    with prev2:
        st.caption(f"Archivo 2 — {len(datos2)} filas")
        st.dataframe(datos2.head(), use_container_width=True)

# ---------------------------------------------------------------------------
# Cálculo de los joins
# ---------------------------------------------------------------------------
inner = pd.merge(datos1, datos2, on=columna_cruce, how="inner")
left = pd.merge(datos1, datos2, on=columna_cruce, how="left", indicator=True)
right = pd.merge(datos1, datos2, on=columna_cruce, how="right", indicator=True)

faltan_en_2 = left[left["_merge"] == "left_only"].drop(columns="_merge")
faltan_en_1 = right[right["_merge"] == "right_only"].drop(columns="_merge")

left = left.drop(columns="_merge")
right = right.drop(columns="_merge")

st.divider()

m1, m2, m3, m4 = st.columns(4)
m1.metric("🤝 Coincidencias (INNER)", len(inner))
m2.metric("📄 Solo en Archivo 1", len(faltan_en_2))
m3.metric("📄 Solo en Archivo 2", len(faltan_en_1))
m4.metric("📊 Total combinado (LEFT)", len(left))

st.divider()


def mostrar_tabla(df, mensaje_vacio="No hay filas que mostrar."):
    if df.empty:
        st.success(mensaje_vacio)
    else:
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "⬇️ Descargar como CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="resultado.csv",
            mime="text/csv",
            key=f"descarga_{id(df)}",
        )


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🤝 Inner Join",
        "⬅️ Left Join",
        "➡️ Right Join",
        "🚫 Faltan en Archivo 2",
        "🚫 Faltan en Archivo 1",
    ]
)

with tab1:
    st.caption(f"Registros con `{columna_cruce}` que existen en **ambos** archivos.")
    mostrar_tabla(inner)

with tab2:
    st.caption("Todos los registros del Archivo 1, con datos del Archivo 2 si coinciden.")
    mostrar_tabla(left)

with tab3:
    st.caption("Todos los registros del Archivo 2, con datos del Archivo 1 si coinciden.")
    mostrar_tabla(right)

with tab4:
    st.caption(f"Registros del Archivo 1 cuyo `{columna_cruce}` **no** se encontró en el Archivo 2.")
    mostrar_tabla(faltan_en_2, "🎉 Todos los registros del Archivo 1 tienen coincidencia.")

with tab5:
    st.caption(f"Registros del Archivo 2 cuyo `{columna_cruce}` **no** se encontró en el Archivo 1.")
    mostrar_tabla(faltan_en_1, "🎉 Todos los registros del Archivo 2 tienen coincidencia.")

# ---------------------------------------------------------------------------
# Base de datos consolidada y actualizada (descarga en .xlsx)
# ---------------------------------------------------------------------------
st.markdown('<div class="seccion-final">', unsafe_allow_html=True)
st.subheader("📦 Base de datos consolidada y actualizada")
st.markdown(
    "Genera **una sola tabla** con todos los registros de ambos archivos "
    f"(sin duplicar por `{columna_cruce}`). Donde un registro exista en los dos "
    "archivos, se usan los datos del archivo que elijas como más reciente, "
    "rellenando los espacios vacíos con el otro archivo."
)

prioridad = st.radio(
    "¿Cuál archivo es la fuente más reciente / confiable?",
    ["Archivo 2", "Archivo 1"],
    horizontal=True,
)


def construir_base_actualizada(d1, d2, col, prioridad):
    d1 = d1.drop_duplicates(subset=col).set_index(col)
    d2 = d2.drop_duplicates(subset=col).set_index(col)
    if prioridad == "Archivo 2":
        combinado = d2.combine_first(d1)
    else:
        combinado = d1.combine_first(d2)
    return combinado.reset_index()


base_actualizada = construir_base_actualizada(datos1, datos2, columna_cruce, prioridad)

st.caption(f"Resultado: **{len(base_actualizada)}** registros únicos por `{columna_cruce}`.")
st.dataframe(base_actualizada.head(20), use_container_width=True)

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    base_actualizada.to_excel(writer, index=False, sheet_name="Base actualizada")
buffer.seek(0)

st.download_button(
    "⬇️ Descargar base de datos actualizada (.xlsx)",
    data=buffer,
    file_name="base_datos_actualizada.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Pie de página
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="pie-pagina">
        CIEFD · Centro de Investigación Educativa y Formación Docente<br>
        Reporte generado automáticamente el {ahora.strftime('%d/%m/%Y a las %H:%M:%S')}
        · Sistema de Cruce y Consolidación de Bases de Datos v1.1
        · Los datos procesados no se almacenan; el análisis ocurre únicamente
        durante esta sesión.
    </div>
    """,
    unsafe_allow_html=True,
)
