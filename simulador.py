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

# Seleccionar un ETF
selected_etf = st.selectbox("Selecciona un ETF", etf_nombres)

# Obtener el ticker del ETF seleccionado
selected_ticker = etf_tickers[etf_nombres.index(selected_etf)]

# Funciones para obtener datos y calcular rendimiento/riesgo...

def obtener_fechas_ultimos_diez_anos():
    """Obtiene las fechas de inicio y fin para los últimos 10 años."""
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=365 * 10)  # 10 años
    return fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d")

def descargar_datos_historicos(ticker):
    """Descarga los precios históricos de los últimos 10 años para un ticker."""
    fecha_inicio, fecha_fin = obtener_fechas_ultimos_diez_anos()
    try:
        accion = yf.Ticker(ticker)
        datos = accion.history(start=fecha_inicio, end=fecha_fin)
        return datos
    except Exception as e:
        print(f"Error al descargar datos para {ticker}: {e}")
        return None

# Descargar precios históricos para el ETF seleccionado
precios_historicos = descargar_datos_historicos(selected_ticker)

# Comprobar si se descargaron los precios
if precios_historicos is not None and not precios_historicos.empty:
    # Calcular el rendimiento y riesgo
    rendimiento_log = np.log(precios_historicos['Close'].iloc[-1] / precios_historicos['Close'].iloc[0])
    rendimiento_anualizado = rendimiento_log / (precios_historicos.shape[0] / 252)  # Ajustar por días de negociación

    # Proyección de valor a través de los años
    anos_proyeccion = edad_proyecto - edad
    valor_proyectado = []
    
    for i in range(anos_proyeccion + 1):
        valor = aportacion_inicial * (1 + rendimiento_anualizado) ** i
        valor_proyectado.append(valor)
    
    # Mostrar resultados en tabla
    df_resultado = pd.DataFrame({"Año": list(range(anos_proyeccion + 1)), "Valor proyectado": valor_proyectado})
    st.write(df_resultado)

    # Gráfica de Rendimiento Proyectado
    st.subheader("Gráfica de Rendimiento Proyectado")
    plt.style.use('seaborn-darkgrid')
    
    fig, ax = plt.subplots(figsize=(10, 6))  # Ajustar tamaño de la figura
    ax.plot(df_resultado["Año"], df_resultado["Valor proyectado"], 
            marker='o', color='royalblue', linewidth=2, markersize=8, label='Valor Proyectado')
    
    # Etiquetas y título
    ax.set_xlabel("Año", fontsize=14)
    ax.set_ylabel("Valor Proyectado ($)", fontsize=14)
    ax.set_title(f"Proyección del Portafolio seleccionado: {selected_ticker}", fontsize=16)
    ax.legend()  # Agregar leyenda
    ax.grid(True)
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)

    # Mensaje final personalizado
    st.success(f"{nombre} {apellido_paterno}, según el análisis, a los {edad_proyecto} años tendrás un valor estimado de inversión de ${valor_proyectado[-1]:,.2f} en el portafolio seleccionado.")
else:
    st.error("No se pudieron obtener los datos históricos para el ETF seleccionado.")
