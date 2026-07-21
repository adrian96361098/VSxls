import io
import os
import sys

import altair as alt
import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from estilo import mostrar_encabezado, mostrar_pie_pagina  # noqa: E402

st.set_page_config(
    page_title="Dashboard Docente · CIEFD",
    page_icon="📊",
    layout="wide",
)

ahora = mostrar_encabezado(
    titulo_pagina="Dashboard Docente",
    descripcion=(
        "Sube tu base de personal docente y genera automáticamente un "
        "informe por unidad que muestra cuántos docentes están "
        "<b>activos</b> y cuántos <b>inactivos</b>, con gráficas y "
        "descarga en Excel."
    ),
    icono="📊",
)

# ---------------------------------------------------------------------------
# Carga de archivo
# ---------------------------------------------------------------------------
archivo = st.file_uploader("📄 Base de datos de docentes", type=["csv", "xlsx", "xls"])

if not archivo:
    st.info("👆 Sube un archivo (CSV o Excel) con tu base de personal docente para comenzar.")
    mostrar_pie_pagina(ahora)
    st.stop()


def leer_archivo(archivo):
    nombre = archivo.name.lower()
    if nombre.endswith((".xlsx", ".xls")):
        return pd.read_excel(archivo, sheet_name=0)
    return pd.read_csv(archivo)


try:
    datos = leer_archivo(archivo)
except Exception as e:
    st.error(f"❌ Ocurrió un error al leer el archivo: {e}")
    st.stop()

if datos.empty:
    st.warning("⚠️ El archivo no tiene registros.")
    st.stop()


def sugerir_columna(columnas, palabras_clave, evitar=None):
    """Sugiere la columna más probable según palabras clave en su nombre."""
    evitar = evitar or []
    candidatas = [
        c for c in columnas
        if any(p in str(c).lower() for p in palabras_clave)
        and not any(e in str(c).lower() for e in evitar)
    ]
    return candidatas[0] if candidatas else columnas[0]


columnas = list(datos.columns)
col_unidad_sugerida = sugerir_columna(columnas, ["unidad"])
col_estado_sugerida = sugerir_columna(columnas, ["estado del docente", "estatus", "estado"], evitar=["delegacion"])

st.divider()
sel1, sel2 = st.columns(2)
with sel1:
    columna_unidad = st.selectbox(
        "🏢 Columna de Unidad",
        columnas,
        index=columnas.index(col_unidad_sugerida),
    )
with sel2:
    columna_estado = st.selectbox(
        "🟢 Columna de Estado del docente",
        columnas,
        index=columnas.index(col_estado_sugerida),
    )

valores_estado = sorted(datos[columna_estado].dropna().astype(str).unique())

if not valores_estado:
    st.warning("⚠️ La columna de estado seleccionada no tiene valores.")
    st.stop()

sugeridos_activos = [
    v for v in valores_estado
    if "activ" in v.lower() and "inactiv" not in v.lower()
]

valores_activos = st.multiselect(
    "✅ ¿Qué valores de esa columna cuentan como 'Activo'?",
    valores_estado,
    default=sugeridos_activos or valores_estado[:1],
)

with st.expander("👀 Vista previa de los datos cargados"):
    st.caption(f"{len(datos)} registros en total")
    st.dataframe(datos.head(10), use_container_width=True)

# ---------------------------------------------------------------------------
# Cálculo del informe por unidad
# ---------------------------------------------------------------------------
datos = datos.copy()
datos["_condicion"] = datos[columna_estado].astype(str).apply(
    lambda v: "Activo" if v in valores_activos else "Inactivo"
)

informe = (
    datos.groupby([columna_unidad, "_condicion"])
    .size()
    .unstack(fill_value=0)
)
for col in ["Activo", "Inactivo"]:
    if col not in informe.columns:
        informe[col] = 0

informe["Total"] = informe["Activo"] + informe["Inactivo"]
informe["% Activos"] = (informe["Activo"] / informe["Total"] * 100).round(1)
informe = informe.sort_values("Total", ascending=False).reset_index()
informe = informe[[columna_unidad, "Activo", "Inactivo", "Total", "% Activos"]]

st.divider()

total_docentes = len(datos)
total_activos = int((datos["_condicion"] == "Activo").sum())
total_inactivos = total_docentes - total_activos
total_unidades = informe[columna_unidad].nunique()

m1, m2, m3, m4 = st.columns(4)
m1.metric("👥 Total de docentes", total_docentes)
m2.metric("🟢 Activos", total_activos)
m3.metric("🔴 Inactivos", total_inactivos)
m4.metric("🏢 Unidades", total_unidades)

st.divider()

st.subheader("📋 Informe por unidad")
st.dataframe(
    informe.style.format({"% Activos": "{:.1f}%"}),
    use_container_width=True,
)

# ---------------------------------------------------------------------------
# Gráfica
# ---------------------------------------------------------------------------
st.subheader("📈 Activos vs. Inactivos por unidad")

datos_grafica = informe.melt(
    id_vars=[columna_unidad],
    value_vars=["Activo", "Inactivo"],
    var_name="Condición",
    value_name="Docentes",
)

grafica = (
    alt.Chart(datos_grafica)
    .mark_bar()
    .encode(
        x=alt.X(f"{columna_unidad}:N", sort="-y", title="Unidad"),
        y=alt.Y("Docentes:Q", title="Número de docentes"),
        color=alt.Color(
            "Condición:N",
            scale=alt.Scale(domain=["Activo", "Inactivo"], range=["#1f4d3a", "#c98a3a"]),
        ),
        tooltip=[columna_unidad, "Condición", "Docentes"],
    )
    .properties(height=420)
)
st.altair_chart(grafica, use_container_width=True)

# ---------------------------------------------------------------------------
# Descarga del informe
# ---------------------------------------------------------------------------
st.markdown('<div class="seccion-final">', unsafe_allow_html=True)
st.subheader("⬇️ Descargar informe")
st.markdown("El archivo incluye el resumen por unidad y el detalle completo de cada docente con su condición.")

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    informe.to_excel(writer, index=False, sheet_name="Resumen por unidad")
    datos.drop(columns="_condicion").assign(
        Condición=datos["_condicion"]
    ).to_excel(writer, index=False, sheet_name="Detalle docentes")
buffer.seek(0)

st.download_button(
    "⬇️ Descargar informe por unidad (.xlsx)",
    data=buffer,
    file_name="informe_docentes_por_unidad.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
st.markdown('</div>', unsafe_allow_html=True)

mostrar_pie_pagina(ahora)
