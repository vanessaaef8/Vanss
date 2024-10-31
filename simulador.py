import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

# Configuración de la aplicación
st.set_page_config(page_title="Simulador OptiMaxx Patrimonial", page_icon=":chart_with_upwards_trend:", layout="wide")

# Estilo CSS personalizado
st.markdown(
    """
    <style>
    .appview-container, .main {
        background-color: #E8F0FE; /* Fondo claro */
        color: #1E3A8A; /* Color azul marino */
    }
    .sidebar .sidebar-content {
        background-color: #1E3A8A; /* Fondo azul oscuro para la barra lateral */
        color: white;
    }
    .stButton>button {
        color: white;
        background-color: #1E3A8A;
        border-radius: 5px;
    }
    .stTitle, .stHeader, h1, h2, h3, h4, h5, h6, p, label {
        color: #1E3A8A;
        font-family: Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sección de "Datos del Cliente"
st.sidebar.title("Simulador OptiMaxx Patrimonial")
st.sidebar.write("Por favor, ingresa tus datos para continuar.")

# Crear campos de entrada para los datos del cliente
nombre = st.text_input("Nombre")
apellido_paterno = st.text_input("Apellido Paterno")
edad = st.number_input("Edad", min_value=18, max_value=150, step=1)

# Validación de campos
datos_completos = nombre and apellido_paterno and edad

if datos_completos:
    # Menú de navegación en la barra lateral, aparece solo si se ingresan todos los datos
    opcion = st.sidebar.radio("Selecciona una sección", ("Inicio", "Proyección de Inversión", "Ayuda"))

# Sección de "Inicio"
if opcion == "Inicio":
    st.title("Simulador OptiMaxx Patrimonial - Allianz")
    st.write("¡Bienvenido! Configura tus datos para generar una proyección personalizada.")

# Sección "Proyección de Inversión"
if opcion == "Proyección de Inversión":
    st.title("Proyección de Inversión")

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

# Diccionario con descripciones de cada ETF
etf_descripciones = {
    "QQQ": "ETF de empresas tecnológicas que replican el índice NASDAQ 100.",
    "SPY": "ETF que replica el índice S&P 500, compuesto por las 500 empresas más grandes de EE.UU.",
    "DIA": "ETF que sigue el índice Dow Jones Industrial Average.",
    "VWO": "ETF que invierte en mercados emergentes.",
    "XLF": "ETF que sigue el sector financiero de Estados Unidos.",
    "XLV": "ETF que representa el sector de salud de Estados Unidos.",
    "ITB": "ETF enfocado en el sector de la construcción de viviendas en Estados Unidos.",
    "SLV": "ETF respaldado por plata física.",
    "EWT": "ETF que representa el mercado de valores de Taiwán.",
    "EWU": "ETF que invierte en empresas del Reino Unido.",
    "EWY": "ETF que invierte en empresas de Corea del Sur.",
    "EZU": "ETF que sigue el índice MSCI EMU, que representa el mercado europeo.",
    "EWJ": "ETF que invierte en el mercado japonés.",
    "EWC": "ETF que representa el mercado canadiense.",
    "EWG": "ETF que invierte en empresas de Alemania.",
    "EWA": "ETF que invierte en el mercado australiano.",
    "AGG": "ETF de bonos del mercado de renta fija de EE.UU."
}

etf_seleccionado = st.selectbox("Selecciona un ETF", etf_tickers, format_func=lambda x: etf_nombres[etf_tickers.index(x)])
anos_proyecto = st.slider("Número de años a proyectar", min_value=1, max_value=10, step=1)
etf_nombre_seleccionado = etf_nombres[etf_tickers.index(etf_seleccionado)]

# Mostrar descripción del ETF seleccionado
st.write(f"**Descripción del ETF seleccionado ({etf_nombre_seleccionado}):** {etf_descripciones.get(etf_seleccionado, 'Descripción no disponible.')}")

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

# Proyectar valores en base 100
años = np.arange(1, anos_proyecto + 1)
valores_proyectados = [100 * (1 + tasa_anual) ** i for i in años]  # Iniciando en 100

# Configuración del estilo de la gráfica
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10, 6))

# Plot de los valores proyectados en base 100
ax.plot(años, valores_proyectados, color="royalblue", marker="o", markersize=6, label="Proyección de Inversión")
ax.axhline(100, color="grey", linestyle="--", linewidth=1, label="Base 100")  # Línea de referencia en base 100

# Etiquetas y título
ax.set_title(f"Proyección de Crecimiento del ETF: {etf_nombre_seleccionado} en Base 100", fontsize=16, fontweight="bold")
ax.set_xlabel("Años", fontsize=12)
ax.set_ylabel("Valor de Inversión (Base 100)", fontsize=12)
ax.legend()

# Mostrar gráfica en Streamlit
st.pyplot(fig)

# Título y entrada de años de proyección
anos_proyecto = st.slider("Número de años a proyectar", min_value=1, max_value=30, step=1)

# Opciones de escenarios de tasa de crecimiento anual
escenario = st.selectbox("Selecciona un escenario", ["Optimista", "Esperado", "Pesimista"])

# Definir tasas de crecimiento para cada escenario (valores ejemplo, ajusta según datos reales)
if escenario == "Optimista":
    tasa_anual = tasa_anual * 1.2  # 20% más alta
elif escenario == "Esperado":
    tasa_anual = tasa_anual
else:
    tasa_anual = tasa_anual * 0.8  # 20% más baja

# Calcular proyecciones en base 100 para cada año
años = np.arange(1, anos_proyecto + 1)
valores_proyectados = [100 * (1 + tasa_anual) ** i for i in años]

# Configuración de la gráfica
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10, 6))

# Graficar proyección del escenario seleccionado
ax.plot(años, valores_proyectados, marker="o", markersize=6, label=f"Escenario {escenario}", color="royalblue")
ax.axhline(100, color="grey", linestyle="--", linewidth=1, label="Base 100")  # Línea de base

# Personalizar gráfica
ax.set_title(f"Proyección de Crecimiento - Escenario {escenario}", fontsize=16, fontweight="bold")
ax.set_xlabel("Años", fontsize=12)
ax.set_ylabel("Valor de Inversión (Base 100)", fontsize=12)
ax.legend()

# Mostrar gráfica
st.pyplot(fig)

# Sección "Ayuda"
if opcion == "Ayuda":
    st.title("Ayuda")
    st.write("Si necesitas ayuda, comunícate al número de contacto.")
else:
    st.warning("Por favor, completa todos los campos de datos para continuar.")
