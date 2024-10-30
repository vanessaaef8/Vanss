import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

# Cambiar el fondo a una imagen y el color del texto
st.markdown(
    """
    <style>
    .appview-container, .main {
        background-image: url('https://blog.monex.com.mx/hs-fs/hubfs/C-3.jpg?width=900&height=599&name=C-3.jpg'); /* Cambia la URL por la de tu imagen */
        background-size: cover; /* Asegura que la imagen cubra todo el fondo */
        color: white; /* Color del texto */
    }
    .sidebar .sidebar-content {
        background-color: rgba(0, 0, 0, 0.8); /* Fondo oscuro y semitransparente para la barra lateral */
        color: white; /* Color del texto de la barra lateral */
    }
    .stButton>button {
        color: black; /* Color del texto del botón */
        background-color: white; /* Fondo del botón */
    }
    h1, h2, h3, h4, h5, h6, p, div, label {
        color: white !important; /* Cambia el color del texto en encabezados y párrafos a blanco */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título de la app
st.title("Simulador OptiMaxx Patrimonial - Allianz")

# Datos del cliente
st.header("Datos del Cliente")
col1, col2 = st.columns(2)
with col1:
    nombre = st.text_input("Nombre")
with col2:
    apellido_paterno = st.text_input("Apellido Paterno")

# Verificar si se han llenado todos los campos de nombre
if not nombre or not apellido_paterno:
    st.warning("Por favor, completa todos los campos para continuar.")
    st.stop()  # Detener la ejecución hasta que se completen los campos

edad = st.number_input("Edad", min_value=18, max_value=150, step=1)
if not isinstance(edad, (int, float)):
    st.error("Por favor, ingresa un valor numérico para la edad.")
    st.stop()

# Validación de la edad a proyectar
edad_maxima = 150
edad_proyecto = st.number_input("Edad a proyectar", min_value=edad + 5, max_value=edad_maxima, step=1)
if not isinstance(edad_proyecto, (int, float)):
    st.error("Por favor, ingresa un valor numérico para la edad a proyectar.")
    st.stop()

if edad_proyecto > edad_maxima:
    st.warning(f"La edad a proyectar no puede ser mayor a {edad_maxima} años.")
    st.stop()  # Detener la ejecución si la validación falla
    
# Datos de inversión inicial
st.header("Inversión Inicial")
aportacion_inicial = st.number_input("Aportación inicial", min_value=1000.0, step=100.0)

if aportacion_inicial <= 0:
    st.error("La aportación inicial debe ser un valor positivo.")
    st.stop()

# Lista de nombres de ETFs y sus símbolos
etf_nombres = [
    "AZ QQQ NASDAQ 100",
    "AZ SPDR S&P 500 ETF TRUST",
    "AZ SPDR DJIA TRUST",
    "AZ VANGUARD EMERGING MARKET ETF",
    "AZ FINANCIAL SELECT SECTOR SPDR",
    "AZ HEALTH CARE SELECT SECTOR",
    "AZ DJ US HOME CONSTRUCT",
    "AZ SILVER TRUST",
    "AZ MSCI TAIWAN INDEX FD",
    "AZ MSCI UNITED KINGDOM",
    "AZ MSCI SOUTH KOREA IND",
    "AZ MSCI EMU",
    "AZ MSCI JAPAN INDEX FD",
    "AZ MSCI CANADA",
    "AZ MSCI GERMANY INDEX",
    "AZ MSCI AUSTRALIA INDEX",
    "AZ BARCLAYS AGGREGATE"
]

# Tickers correspondientes a los ETFs
etf_tickers = [
    "QQQ",
    "SPY",
    "DIA",
    "VWO",
    "XLF",
    "XLV",
    "ITB",
    "SLV",
    "EWT",
    "EWU",
    "EWY",
    "EZU",
    "EWJ",
    "EWC",
    "EWG",
    "EWA",
    "AGG"
]

# Seleccionar ETF
etf_seleccionado = st.selectbox("Selecciona un ETF para la inversión", etf_tickers)
etf_nombre_seleccionado = etf_nombres[etf_tickers.index(etf_seleccionado)]

# Parámetros de entrada
aportacion_inicial = st.number_input("Aportación inicial en USD", min_value=1000.0, value=1000.0, step=500.0)
anos_proyecto = st.slider("Número de años a proyectar", min_value=1, max_value=30, value=10)

# Función para descargar precios históricos y calcular la tasa de crecimiento anual promedio
def obtener_tasa_anual_promedio(ticker):
    """Calcula la tasa anual de crecimiento promedio basada en los datos históricos."""
    datos = yf.Ticker(ticker).history(period="10y")  # 10 años de datos
    precios_inicio = datos['Close'][0]
    precios_fin = datos['Close'][-1]
    tasa_promedio = ((precios_fin / precios_inicio) ** (1 / 10)) - 1  # Tasa anual promedio
    return tasa_promedio

# Calcular la tasa anual promedio
tasa_anual = obtener_tasa_anual_promedio(etf_seleccionado)

# Calcular proyección de inversión usando interés compuesto
valor_final = aportacion_inicial * (1 + tasa_anual) ** anos_proyecto

# Mostrar proyección y detalles al usuario
st.subheader("Proyección de Inversión")
st.write(f"Tasa de crecimiento anual promedio del ETF {etf_nombre_seleccionado}: {tasa_anual * 100:.2f}%")
st.write(
    f"Con una aportación inicial de ${aportacion_inicial:,.2f}, proyectando a {anos_proyecto} años, "
    f"se estima que tu inversión alcanzará un valor de ${valor_final:,.2f}."
)

# Generar gráfica de crecimiento
años = np.arange(1, anos_proyecto + 1)
valores_proyectados = [aportacion_inicial * (1 + tasa_anual) ** i for i in años]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(años, valores_proyectados, color="green", marker="o")
ax.set_title(f"Proyección de Crecimiento del ETF: {etf_nombre_seleccionado}")
ax.set_xlabel("Años")
ax.set_ylabel("Valor de Inversión ($)")
ax.grid(True)

# Mostrar gráfica en Streamlit
st.pyplot(fig)
