import streamlit as st
import pandas as pd

from algoritmo import (
    a_estrella
)

# =====================================================
# CONFIGURACION DE PAGINA
# =====================================================

st.set_page_config(
    page_title="Asignación de Llantas con A*",
    page_icon="🚗",
    layout="wide"
)

# =====================================================
# TITULO
# =====================================================

st.title("Asignación Óptima de Llantas con A*")

st.markdown("""
Este sistema utiliza el algoritmo A* para encontrar
la asignación óptima de ruedas a empresas minimizando
el costo total.
""")

# =====================================================
# COSTOS INICIALES
# =====================================================

costos_iniciales = {
    "Empresa 1": {"T": 20, "H": 30, "V": 20, "W": 40},
    "Empresa 2": {"T": 50, "H": 50, "V": 40, "W": 50},
    "Empresa 3": {"T": 60, "H": 55, "V": 50, "W": 60},
    "Empresa 4": {"T": 100, "H": 80, "V": 60, "W": 70},
}

# =====================================================
# TABLA EDITABLE
# =====================================================

st.subheader("Tabla de Costos (USD)")

df = pd.DataFrame(costos_iniciales).T

df_editado = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed",
    column_config={
        col: st.column_config.NumberColumn(
            col,
            min_value=0,
            format="$%d USD"
        )
        for col in df.columns
    }
)

# =====================================================
# CONVERTIR A DICCIONARIO
# =====================================================

costos_actualizados = df_editado.T.to_dict()

# =====================================================
# BOTON
# =====================================================

st.subheader("Ejecutar Algoritmo")

if st.button("Ejecutar A*"):

    try:

        resultado = a_estrella(costos_actualizados)

        solucion = resultado["solucion"]
        costo_total = resultado["costo_total"]
        pasos = resultado["pasos"]

        st.success("Algoritmo ejecutado correctamente")

        # =================================================
        # EXPLORACION
        # =================================================

        st.subheader("Exploración de Estados")

        total_niveles = 4

        for i, paso in enumerate(pasos):

            with st.expander(f"Paso {i+1}"):

                st.write("Asignaciones actuales")

                if paso["asignaciones"]:

                    asignaciones_df = pd.DataFrame(
                        list(paso["asignaciones"].items()),
                        columns=["Rueda", "Empresa"]
                    )

                    st.table(asignaciones_df)

                else:
                    st.info("Estado inicial")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "g(n)",
                    f"${paso['g']}"
                )

                col2.metric(
                    "h(n)",
                    f"${paso['h']}"
                )

                col3.metric(
                    "f(n)",
                    f"${paso['f']}"
                )

                st.progress(
                    min((paso["nivel"] / total_niveles), 1.0)
                )

        # =================================================
        # RESULTADO FINAL
        # =================================================

        st.subheader("Solución Óptima")

        for tipo, empresa in solucion.items():

            costo = costos_actualizados[empresa][tipo]

            st.success(
                f"Rueda {tipo} → {empresa} | "
                f"Costo: ${costo}"
            )

        st.metric(
            label="Costo Total Mínimo",
            value=f"${costo_total} USD"
        )

        # =================================================
        # TABLA FINAL
        # =================================================

        st.subheader("Resumen Final")

        resumen = pd.DataFrame({
            "Tipo de Rueda": list(solucion.keys()),
            "Empresa Asignada": list(solucion.values()),
            "Costo": [
                costos_actualizados[empresa][tipo]
                for tipo, empresa in solucion.items()
            ]
        })

        st.table(resumen)

    except Exception as e:

        st.error(f"Ocurrió un error: {e}")
        