import streamlit as st
import pandas as pd

# Título de la App
st.title("Simulador OptiMaxx Patrimonial - Allianz")

# Sección de Datos del Cliente
st.header("Datos del Cliente")
nombre = st.text_input("Nombre Completo")
edad = st.number_input("Edad", min_value=0, max_value=100, step=1)
edad_proyectar = st.number_input("Edad a Proyectar", min_value=0, max_value=100, step=1)

# Sección de Datos de la Póliza
st.header("Datos de la Póliza")
aportacion = st.number_input("Aportación Inicial ($)", min_value=0.0, step=1000.0)

# Sección de Aportaciones Subsecuentes
st.subheader("Aportaciones Subsecuentes")
num_aportaciones = st.number_input("Número de aportaciones", min_value=1, max_value=10, step=1)
aportaciones = []

for i in range(num_aportaciones):
    st.write(f"Aportación {i+1}")
    monto = st.number_input(f"Monto {i+1} ($)", min_value=0.0, step=1000.0, key=f"monto_{i}")
    año = st.selectbox(f"Año {i+1}", list(range(2024, 2035)), key=f"año_{i}")
    aportaciones.append({"Monto": monto, "Año": año})

# Conversión a DataFrame para visualización
df_aportaciones = pd.DataFrame(aportaciones)
if not df_aportaciones.empty:
    st.write("Resumen de Aportaciones:")
    st.dataframe(df_aportaciones)

# Sección de Portafolios
st.header("Asignación de Portafolios")
st.write("Distribución de Portafolios Básicos y Premier (Debe sumar 100%)")

portafolios = {
    "Allianz ETF Conservador Pesos": st.slider("Allianz ETF Conservador Pesos", 0, 100, 0),
    "Allianz ETF Balanceado Pesos": st.slider("Allianz ETF Balanceado Pesos", 0, 100, 0),
    "Allianz ETF Dinámico Pesos": st.slider("Allianz ETF Dinámico Pesos", 0, 100, 0),
    "Allianz ETF Real Pesos": st.slider("Allianz ETF Real Pesos", 0, 100, 0),
    "Allianz Global": st.slider("Allianz Global", 0, 100, 0)
}

# Validación de la suma de porcentajes
suma_porcentajes = sum(portafolios.values())
if suma_porcentajes != 100:
    st.warning(f"La suma de los porcentajes debe ser 100%. Actualmente es {suma_porcentajes}%.")

# Botón para calcular y mostrar los resultados
if st.button("Calcular"):
    if suma_porcentajes == 100:
        st.success("Cálculo realizado con éxito.")
        # Aquí podrías agregar la lógica para calcular el rendimiento o hacer proyecciones
        st.write("Aquí se mostrarían los resultados de las proyecciones.")
    else:
        st.error("Por favor, asegúrate de que la suma de los porcentajes sea igual a 100% antes de calcular.")
    
