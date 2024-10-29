import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Título de la app
st.title("Simulador OptiMaxx Patrimonial - Allianz")

# Datos del cliente
st.header("Datos del Cliente")
col1, col2, col3 = st.columns(3)
with col1:
    nombre = st.text_input("Nombre")
with col2:
    apellido_paterno = st.text_input("Apellido Paterno")
with col3:
    apellido_materno = st.text_input("Apellido Materno")

# Verificar si se han llenado todos los campos de nombre
if not nombre or not apellido_paterno or not apellido_materno:
    st.warning("Por favor, completa todos los campos de nombre, apellido paterno y apellido materno para continuar.")
    st.stop()  # Detener la ejecución hasta que se completen los campos

edad = st.number_input("Edad", min_value=18, max_value=100, step=1)
edad_proyecto = st.number_input("Edad a proyectar", min_value=edad, max_value=100, step=1)

# Datos de inversión inicial
st.header("Inversión Inicial")
aportacion_inicial = st.number_input("Aportación inicial", min_value=1000.0, step=100.0)

# Selección de Portafolio Allianz
st.header("Selección de Portafolio Allianz")
portafolios = [
    "Allianz ETF Conservador Pesos",
    "Allianz ETF Conservador Dólares",
    "Allianz ETF Conservador Euros",
    "Allianz ETF Balanceado Pesos",
    "Allianz ETF Balanceado Dólares",
    "Allianz ETF Balanceado Euros",
    "Allianz ETF Dinámico Pesos",
    "Allianz ETF Dinámico Dólares",
    "Allianz ETF Dinámico Euros",
    "Allianz ETF Real Pesos",
    "Allianz Global"
]
portafolio_seleccionado = st.selectbox("Selecciona el portafolio recomendado", portafolios)

# Número de años para proyectar
anos_proyeccion = st.slider("Años de proyección", min_value=1, max_value=30, step=1)

# Rendimientos según portafolio (ajusta los valores cuando los tengas)
rendimiento_anual = {
    "Allianz ETF Conservador Pesos": 0.00,
    "Allianz ETF Conservador Dólares": 0.00,
    "Allianz ETF Conservador Euros": 0.00,
    "Allianz ETF Balanceado Pesos": 0.00,
    "Allianz ETF Balanceado Dólares": 0.00,
    "Allianz ETF Balanceado Euros": 0.00,
    "Allianz ETF Dinámico Pesos": 0.00,
    "Allianz ETF Dinámico Dólares": 0.00,
    "Allianz ETF Dinámico Euros": 0.00,
    "Allianz ETF Real Pesos": 0.00,
    "Allianz Global": 0.00
}
tasa_rendimiento = rendimiento_anual[portafolio_seleccionado]

# Cálculo de proyección de rendimiento
valores = [aportacion_inicial]
for i in range(anos_proyeccion):
    nuevo_valor = valores[-1] * (1 + tasa_rendimiento)
    valores.append(nuevo_valor)

# Mostrar resultados en tabla
df_resultado = pd.DataFrame({"Año": list(range(anos_proyeccion + 1)), "Valor proyectado": valores})
st.write(df_resultado)

# Gráfica de rendimiento
st.subheader("Gráfica de Rendimiento Proyectado")
fig, ax = plt.subplots()
ax.plot(df_resultado["Año"], df_resultado["Valor proyectado"], marker='o')
ax.set_xlabel("Año")
ax.set_ylabel("Valor Proyectado ($)")
ax.set_title(f"Proyección del Portafolio seleccionado: {portafolio_seleccionado}")
st.pyplot(fig)

# Mensaje final personalizado
st.success(f"{nombre} {apellido_paterno}, según el análisis, a los {edad_proyecto} años tendrás un valor estimado de inversión de ${valores[-1]:,.2f} en el portafolio {portafolio_seleccionado} que puedes ver en la gráfica.")


    
