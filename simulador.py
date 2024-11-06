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
    nombre = st.text_input("Nombre")
    apellido_paterno = st.text_input("Apellido Paterno")
    edad = st.number_input("Edad", min_value=18, max_value=150, step=1)

# Validación de campos
    datos_completos = bool(nombre and apellido_paterno and edad)

# Inicializar opción
opcion = None

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

# Pestaña de "Proyección de Inversión"
with tab2:
    if datos_completos:
        etfs_seleccionados = st.multiselect(
            "Selecciona ETFs para ver su rendimiento histórico", etf_tickers,
            format_func=lambda x: etf_nombres[etf_tickers.index(x)]
        )  
        anos_proyecto = st.slider("Selecciona años de datos históricos", 1, 5, 1)

        if etfs_seleccionados:
            for etf in etfs_seleccionados:
                st.write(f"**Descripción del ETF ({etf}):** {etf_descripciones.get(etf, 'Descripción no disponible')}")

                # Obtener y graficar datos históricos
                ticker_data = yf.Ticker(etf)
                historical_data = ticker_data.history(period=f"{anos_proyecto}y")['Close']

                if not historical_data.empty:
                    plt.figure(figsize=(10, 6))
                    plt.plot(historical_data.index, historical_data, label=f"{etf_nombres[etf_tickers.index(etf)]}")
                    plt.xlabel("Fecha")
                    plt.ylabel("Precio de Cierre ($)")
                    plt.title(f"Precio Histórico del ETF: {etf_nombres[etf_tickers.index(etf)]}")
                    plt.legend()
                    st.pyplot(plt.gcf())
                    plt.clf()
                else:
                    st.warning(f"No se encontraron datos históricos para el ETF {etf}.")
                    
                # Calcular y mostrar tasa anual promedio
                try:
                    precios_inicio = historical_data[0]
                    precios_fin = historical_data[-1]
                    tasa_anual = ((precios_fin / precios_inicio) ** (1 / anos_proyecto)) - 1
                    st.write(f"**Tasa Anual Promedio de Crecimiento ({etf}):** {tasa_anual * 100:.2f}%")
                except Exception as e:
                    st.error(f"No se pudo calcular la tasa de crecimiento para {etf}. Error: {str(e)}")

                # Proyección de inversión
                aportacion_inicial = st.number_input("Monto de inversión inicial ($)", min_value=10000, step=1)
                if tasa_anual is not None:
                    valor_final = aportacion_inicial * (1 + tasa_anual) ** anos_proyecto
                    st.write(f"**Valor final de la inversión después de {anos_proyecto} años en {etf}:** ${valor_final:,.2f}")
                    
                    años = np.arange(1, anos_proyecto + 1)
                    valores_proyectados = [aportacion_inicial * (1 + tasa_anual) ** i for i in años]
                    
                    # Gráfica de proyección de crecimiento
                    plt.style.use('ggplot')
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(años, valores_proyectados, color="royalblue", marker="o", markersize=6)
                    ax.set_title(f"Proyección de Crecimiento del ETF: {etf_nombres[etf_tickers.index(etf)]}")
                    ax.set_xlabel("Años")
                    ax.set_ylabel("Valor de Inversión ($)")
                    st.pyplot(fig)

        # Botón de ayuda en la barra lateral
        st.sidebar.header("Ayuda")
        st.sidebar.write("Para más información, contacta a nuestro número de ayuda: 800-123-4567")
