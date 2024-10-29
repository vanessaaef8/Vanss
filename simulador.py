import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

# Cambiar el fondo a una imagen y el color del texto
st.markdown(
    """
    <style>
    .reportview-container {
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
edad_proyecto = st.number_input("Edad a proyectar", min_value=edad+5, max_value=edad_maxima, step=1)
if not isinstance(edad_proyecto, (int, float)):
    st.error("Por favor, ingresa un valor numérico para la edad a proyectar.")
    st.stop()

if edad_proyecto > edad_maxima:
    st.warning(f"La edad a proyectar no puede ser mayor a {edad_maxima} años.")
    st.stop()  # Detener la ejecución si la validación falla
    
# Datos de inversión inicial
st.header("Inversión Inicial")
aportacion_inicial = st.number_input("Aportación inicial", min_value=1000.0, step=100.0)
def validar_aportacion_inicial(aportacion_inicial):
    if aportacion_inicial <= 0:
        st.error("La aportación inicial debe ser un valor positivo.")
        return False
    return True

# Número de años para proyectar
anos_proyeccion = st.slider("Años de proyección", min_value=1, max_value=30, step=1)

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

for ticker in etf_tickers:
    data = yf.download(ticker, start="2013-12-31", end="2023-12-31")
    data.to_csv(f"{ticker}.csv")

def descargar_datos_historicos(etf_tickers):
    """Descarga los precios históricos de los últimos 10 años para una lista de tickers."""
    fecha_inicio, fecha_fin = obtener_fechas_ultimos_diez_anos()
    precios_historicos = {}
    
    for ticker in etf_tickers:
        try:
            accion = yf.Ticker(ticker)
            datos = accion.history(start=fecha_inicio, end=fecha_fin)
            precios_historicos[ticker] = datos
        except Exception as e:
            print(f"Error al descargar datos para {ticker}: {e}")
            precios_historicos[ticker] = None
    
    return precios_historicos
    
def obtener_info_etf(ticker):
    """Obtiene el nombre corto y la descripción larga de un ETF dado su ticker."""
    
    try:
        # Encuentra el índice del ticker en la lista
        index = etf_tickers.index(ticker)
        
        # Obtiene el nombre correspondiente
        nombre_corto = etf_nombres[index]
        
        # Genera una descripción larga (puedes personalizarla según tus necesidades)
        descripcion_larga = f"{nombre_corto} es un ETF que busca replicar el rendimiento del índice correspondiente a su ticker."
        
        return nombre_corto, descripcion_larga
    except ValueError:
        return None, f"Ticker '{ticker}' no encontrado."

tasa_rendimiento = rendimiento_anual[portafolio_seleccionado]
def validar_tasa_rendimiento(tasa):
    if tasa < -1:  # Consideramos -1 como un límite inferior razonable
        st.error("La tasa de rendimiento no puede ser menor a -1.")
    elif tasa > 0.5:  # Ajusta el límite superior según tus necesidades
        st.warning("La tasa de rendimiento ingresada es muy alta. Verifica si es correcta.")
    return tasa >= -1 and tasa <= 0.5
tasa_rendimiento = st.number_input("Tasa de rendimiento anual (en decimal)", min_value=-1.0, max_value=1.0, step=0.01)
if not validar_tasa_rendimiento(tasa_rendimiento):
    st.stop()

# Cálculo de proyección de rendimiento
valores = [aportacion_inicial]
for i in range(anos_proyeccion):
    nuevo_valor = valores[-1] * (1 + tasa_rendimiento)
    valores.append(nuevo_valor)
if not validar_aportacion_inicial(aportacion_inicial):
    st.stop()

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


    
