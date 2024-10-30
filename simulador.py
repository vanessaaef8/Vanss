import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

# Estilos CSS
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
    }
    .stButton>button {
        color: black;
        background-color: white;
    }
    h1, h2, h3, h4, h5, h6, p, div, label {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True
)

# Título de la app
st.title("Simulador OptiMaxx Patrimonial - Allianz")

# Datos del cliente
with st.expander("Datos del Cliente"):
    nombre = st.text_input("Nombre")
    apellido_paterno = st.text_input("Apellido Paterno")
    if not nombre or not apellido_paterno:
        st.warning("Por favor, completa todos los campos para continuar.")
        st.stop()

edad = st.number_input("Edad", min_value=18, max_value=150, step=1)
edad_maxima = 150
edad_proyecto = st.number_input("Edad a proyectar", min_value=edad + 5, max_value=edad_maxima, step=1)

aportacion_inicial = st.number_input("Aportación inicial", min_value=1000.0, step=100.0)

etf_nombres = [
    "AZ QQQ NASDAQ 100", "AZ SPDR S&P 500 ETF TRUST", "AZ SPDR DJIA TRUST",
    "AZ VANGUARD EMERGING MARKET ETF", "AZ FINANCIAL SELECT SECTOR SPDR",
    "AZ HEALTH CARE SELECT SECTOR", "AZ DJ US HOME CONSTRUCT", "AZ SILVER TRUST",
    "AZ MSCI TAIWAN INDEX FD", "AZ MSCI UNITED KINGDOM", "AZ MSCI SOUTH KOREA IND",
    "AZ MSCI EMU", "AZ MSCI JAPAN INDEX FD", "AZ MSCI CANADA", "AZ MSCI GERMANY INDEX",
    "AZ MSCI AUSTRALIA INDEX", "AZ BARCLAYS AGGREGATE"
]

etf_tickers = [
    "QQQ", "SPY", "DIA", "VWO", "XLF", "XLV", "ITB", "SLV", "EWT",
    "EWU", "EWY", "EZU", "EWJ", "EWC", "EWG", "EWA", "AGG"
]

etf_seleccionado = st.selectbox("Selecciona un ETF para la inversión", etf_tickers)
etf_nombre_seleccionado = etf_nombres[etf_tickers.index(etf_seleccionado)]

anos_proyecto = st.slider("Número de años a proyectar", min_value=1, max_value=30, step=1)

def obtener_tasa_anual_promedio(ticker, anos_proyecto):
    datos = yf.Ticker(ticker).history(period=f"{anos_proyecto}y")
    precios_inicio = datos['Close'][0]
    precios_fin = datos['Close'][-1]
    tasa_promedio = ((precios_fin / precios_inicio) ** (1 / anos_proyecto)) - 1
    return tasa_promedio

tasa_anual = obtener_tasa_anual_promedio(etf_seleccionado, anos_proyecto)
valor_final = aportacion_inicial * (1 + tasa_anual) ** anos_proyecto

st.subheader("Proyección de Inversión")
st.write(f"Tasa de crecimiento anual promedio del ETF {etf_nombre_seleccionado}: {tasa_anual * 100:.2f}%")
st.write(
    f"Con una aportación inicial de ${aportacion_inicial:,.2f}, proyectando a {anos_proyecto} años, "
    f"se estima que tu inversión alcanzará un valor de ${valor_final:,.2f}."
)

años = np.arange(1, anos_proyecto + 1)
valores_proyectados = [aportacion_inicial * (1 + tasa_anual) ** i for i in años]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(años, valores_proyectados, color="green", marker="o")
ax.set_title(f"Proyección de Crecimiento del ETF: {etf_nombre_seleccionado}")
ax.set_xlabel("Años")
ax.set_ylabel("Valor de Inversión ($)")
ax.grid(True)
st.pyplot(fig)

