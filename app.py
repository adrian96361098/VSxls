import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Comparador de Archivos",
    page_icon="🔗",
    layout="wide",
)

st.title("🔗 Comparador y Cruce de Archivos")
st.markdown(
    "Sube dos archivos (CSV o Excel) que compartan una columna en común "
    "(por ejemplo **`matricula`** o **`cardex`**) y esta herramienta te "
    "mostrará automáticamente los cruces (INNER, LEFT, RIGHT) y las filas "
    "que no coincidieron entre ambos."
)

st.divider()

# --- Carga de archivos ---
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


# --- Lectura con manejo de errores ---
try:
    datos1 = leer_archivo(archivo1)
    datos2 = leer_archivo(archivo2)
except Exception as e:
    st.error(f"❌ Ocurrió un error al leer los archivos: {e}")
    st.stop()

# --- Selección de la columna de cruce ---
columnas_comunes = sorted(set(datos1.columns) & set(datos2.columns))

if not columnas_comunes:
    st.error(
        "❌ Los archivos no tienen ninguna columna en común. "
        "Revisa que los nombres de columnas coincidan exactamente."
    )
    st.stop()

# Sugerir "matricula" o "cardex" como opción por defecto si existen
preferidas = [c for c in ["matricula", "cardex"] if c in columnas_comunes]
indice_default = columnas_comunes.index(preferidas[0]) if preferidas else 0

columna_cruce = st.selectbox(
    "🔑 Columna para cruzar los archivos",
    columnas_comunes,
    index=indice_default,
)

# --- Vista previa rápida ---
with st.expander("👀 Vista previa de los archivos cargados"):
    prev1, prev2 = st.columns(2)
    with prev1:
        st.caption(f"Archivo 1 — {len(datos1)} filas")
        st.dataframe(datos1.head(), use_container_width=True)
    with prev2:
        st.caption(f"Archivo 2 — {len(datos2)} filas")
        st.dataframe(datos2.head(), use_container_width=True)

# --- Cálculo de los joins ---
inner = pd.merge(datos1, datos2, on=columna_cruce, how="inner")
left = pd.merge(datos1, datos2, on=columna_cruce, how="left", indicator=True)
right = pd.merge(datos1, datos2, on=columna_cruce, how="right", indicator=True)

# Filas del archivo 1 que no encontraron pareja en el archivo 2
faltan_en_2 = left[left["_merge"] == "left_only"].drop(columns="_merge")
# Filas del archivo 2 que no encontraron pareja en el archivo 1
faltan_en_1 = right[right["_merge"] == "right_only"].drop(columns="_merge")

left = left.drop(columns="_merge")
right = right.drop(columns="_merge")

st.divider()

# --- Resumen con métricas ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Coincidencias (INNER)", len(inner))
m2.metric("Solo en Archivo 1", len(faltan_en_2))
m3.metric("Solo en Archivo 2", len(faltan_en_1))
m4.metric("Total combinado (LEFT)", len(left))

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


# --- Resultados en pestañas ---
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
