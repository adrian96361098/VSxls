import streamlit as st

from estilo import mostrar_encabezado, mostrar_pie_pagina

st.set_page_config(
    page_title="Plataforma CIEFD",
    page_icon="🗂️",
    layout="wide",
)

ahora = mostrar_encabezado(
    titulo_pagina="Plataforma de Análisis de Datos Docentes",
    descripcion=(
        "Bienvenido a la plataforma del CIEFD. Usa el menú de la izquierda "
        "para navegar entre los apartados disponibles."
    ),
    icono="🏠",
)

st.markdown("### 📂 Apartados disponibles")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="tarjeta-nav">
            <h3>🔗 Comparador de Archivos</h3>
            <p>Cruza dos bases de datos (CSV o Excel) por una columna clave,
            identifica coincidencias y discrepancias, y genera una base
            de datos consolidada y actualizada lista para descargar.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="tarjeta-nav">
            <h3>📊 Dashboard Docente</h3>
            <p>Sube tu base de personal docente y obtén un informe por
            unidad con el número de docentes activos e inactivos,
            gráficas y un reporte descargable en Excel.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")
st.info("👈 Selecciona un apartado en el menú lateral para comenzar.")

mostrar_pie_pagina(ahora)
