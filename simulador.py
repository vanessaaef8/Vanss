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

# Crear las pestañas
tab1, tab2 = st.tabs(["Datos del Cliente", "Proyección de Inversión"])

# Pestaña de "Datos del Cliente"
with tab1:
    st.sidebar.title("Simulador OptiMaxx Patrimonial")
    st.sidebar.write("Por favor, ingresa tus datos para continuar.")
    
    # Crear campos de entrada para los datos del cliente
    nombre = st.text_input("Nombre")
    apellido_paterno = st.text_input("Apellido Paterno")
    edad = st.number_input("Edad", min_value=18, max_value=150, step=1)
    
    # Validación de campos
    datos_completos = bool(nombre and apellido_paterno and edad)

# Inicializar opción
opcion = None

# Pestaña de "Proyección de Inversión"
with tab2:
    # Verificar que se hayan completado los datos del cliente
    if datos_completos:
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
        anos_proyecto = st.slider("Número de años a proyectar", min_value=1, max_value=5, step=1)
        etf_nombre_seleccionado = etf_nombres[etf_tickers.index(etf_seleccionado)]
        
        # Mostrar descripción del ETF seleccionado
        st.write(f"**Descripción del ETF seleccionado ({etf_nombre_seleccionado}):** {etf_descripciones.get(etf_seleccionado, 'Descripción no disponible.')}")

        def obtener_tasa_anual_promedio(ticker, anos_proyecto):
            try:
                datos = yf.Ticker(ticker).history(period=f"{anos_proyecto}y")
                precios_inicio = datos['Close'][0]
                precios_fin = datos['Close'][-1]
                tasa_promedio = ((precios_fin / precios_inicio) ** (1 / anos_proyecto)) - 1
                return tasa_promedio
            except Exception as e:
                st.error(f"No se pudo obtener datos para el ticker {ticker}. Error: {str(e)}")
                return None
                
        tasa_anual = obtener_tasa_anual_promedio(etf_seleccionado, anos_proyecto)
        
        # Campo de entrada para el monto de inversión inicial
        aportacion_inicial = st.number_input("Monto de inversión inicial ($)", min_value=10000, step=1)
        
        # Verificamos que la tasa anual sea válida antes de proceder
        if tasa_anual is not None:
            # Calculamos el valor final de la inversión
            valor_final = aportacion_inicial * (1 + tasa_anual) ** anos_proyecto
            st.write(f"**Valor final de la inversión después de {anos_proyecto} años:** ${valor_final:,.2f}")
            
            # Calculamos los valores proyectados basados en el monto inicial
            años = np.arange(1, anos_proyecto + 1)
            valores_proyectados = [aportacion_inicial * (1 + tasa_anual) ** i for i in años]
        
            # Configuración de la gráfica para mostrar la inversión proyectada
            plt.style.use('ggplot')
            fig, ax = plt.subplots(figsize=(10, 6))
        
            ax.plot(años, valores_proyectados, color="royalblue", marker="o", markersize=6, label="Proyección de Inversión")
            ax.set_title(f"Proyección de Crecimiento del ETF: {etf_nombre_seleccionado}", fontsize=16, fontweight="bold")
            ax.set_xlabel("Años", fontsize=12)
            ax.set_ylabel("Valor de Inversión ($)", fontsize=12)
            ax.legend()
        
            # Mostrar gráfica en Streamlit
            st.pyplot(fig)
        else:
            st.error("No se pudo obtener la tasa de crecimiento. Verifica el ticker o el periodo seleccionado.")
        
        # Opciones de escenarios de tasa de crecimiento anual
        if tasa_anual is not None:
            escenario = st.selectbox("Selecciona un escenario", ["Optimista", "Esperado", "Pesimista"])

            # Definir tasas de crecimiento para cada escenario (valores ejemplo, ajusta según datos reales)
            if escenario == "Optimista":
                tasa_anual_ajustada = tasa_anual * 1.2  # 20% más alta
            elif escenario == "Esperado":
                tasa_anual_ajustada = tasa_anual
            else:
                tasa_anual_ajustada = tasa_anual * 0.8  # 20% más baja

            # Calcular proyecciones en base 100 para cada año
            años = np.arange(1, anos_proyecto + 1)
            valores_proyectados = [100 * (1 + tasa_anual_ajustada) ** i for i in años]

            # Configuración de la gráfica
            plt.style.use('ggplot')
            fig, ax = plt.subplots(figsize=(10, 6))

            # Graficar proyección del escenario seleccionado
            ax.plot(años, valores_proyectados, marker="o", markersize=6, label=f"Escenario {escenario}", color="royalblue")
            ax.axhline(100, color="grey", linestyle="--", linewidth=1, label="Base
