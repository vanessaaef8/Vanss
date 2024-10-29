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

def obtener_fechas_ultimos_diez_anos():
    """Obtiene las fechas de inicio y fin para los últimos 10 años."""
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=365 * 10)  # 10 años
    return fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d")

def descargar_datos_historicos(tickers):
    """Descarga los precios históricos de los últimos 10 años para una lista de tickers."""
    fecha_inicio, fecha_fin = obtener_fechas_ultimos_diez_anos()
    precios_historicos = {}
    
    for ticker in tickers:
        try:
            accion = yf.Ticker(ticker)
            datos = accion.history(start=fecha_inicio, end=fecha_fin)
            precios_historicos[ticker] = datos
        except Exception as e:
            print(f"Error al descargar datos para {ticker}: {e}")
            precios_historicos[ticker] = None
    
    return precios_historicos

def obtener_data(ticker):
    """Obtiene el nombre corto y la descripción larga de un ETF dado su ticker."""
    try:
        accion = yf.Ticker(ticker)
        info = accion.info
        nombre_corto = info.get('shortName', 'No disponible')
        descripcion_larga = info.get('longBusinessSummary', 'Descripción no disponible')
        descripcion_traducida = traducir_texto(descripcion_larga)  # Traducir la descripción
        return nombre_corto, descripcion_traducida
    except Exception as e:
        print(f"Error al obtener datos para {ticker}: {e}")
        return 'No disponible', 'Descripción no disponible'

def traducir_texto(texto):
    """Traduce un texto al español utilizando Google Translate."""
    try:
        traduccion = translator.translate(texto, dest='es')
        return traduccion.text
    except Exception as e:
        print(f"Error al traducir el texto: {e}")
        return 'Traducción no disponible'

def obtener_precio_actual(ticker):
    """Obtiene el precio de cierre más reciente de un ETF o acción dado su ticker."""
    try:
        # Crear el objeto del ticker
        accion = yf.Ticker(ticker)
        # Descargar el precio de cierre del último día de negociación
        precio_actual = accion.history(period='1d')['Close'].iloc[-1]
        return precio_actual
    except Exception as e:
        print(f"Error al obtener el precio actual para {ticker}: {e}")
        return None

def rendimiento_logaritmico(precios_historicos):
    """Calcula el rendimiento logarítmico anualizado a partir de los precios históricos."""
    precios = precios_historicos['Close']
    primer_precio = precios.iloc[0]
    ultimo_precio = precios.iloc[-1]
    
    rendimiento_log = np.log(ultimo_precio / primer_precio)
    rendimiento_log_anualizado = rendimiento_log / 10  # Dividir entre 10 años
    
    return rendimiento_log_anualizado

def calcular_riesgo_promedio(precios_historicos):
    """Calcula el riesgo promedio (desviación estándar anualizada) basado en precios de cierre históricos."""
    precios = precios_historicos['Close']
    rendimientos_diarios = np.log(precios / precios.shift(1)).dropna()
    desviacion_diaria = rendimientos_diarios.std()
    riesgo_promedio_anualizado = desviacion_diaria * np.sqrt(252)  # 252 días de negociación en un año
    return riesgo_promedio_anualizado

def calcular_ratio_riesgo_rendimiento(rendimiento_anualizado, riesgo_promedio):
    """Calcula el ratio riesgo-rendimiento."""
    if riesgo_promedio > 0:
        return rendimiento_anualizado / riesgo_promedio
    else:
        return None

def rendimiento_y_riesgo_por_periodo(precios_historicos, periodo):
    """Calcula el rendimiento y riesgo para un periodo específico."""
    try:
        if periodo == '1m':
            datos_periodo = precios_historicos.last('1M')
        elif periodo == '3m':
            datos_periodo = precios_historicos.last('3M')
        elif periodo == '6m':
            datos_periodo = precios_historicos.last('6M')
        elif periodo == '1y':
            datos_periodo = precios_historicos.last('1Y')
        elif periodo == 'YTD':
            datos_periodo = precios_historicos[precios_historicos.index >= datetime.now().replace(month=1, day=1)]
        elif periodo == '3y':
            datos_periodo = precios_historicos.last('3Y')
        elif periodo == '5y':
            datos_periodo = precios_historicos.last('5Y')
        elif periodo == '10y':
            datos_periodo = precios_historicos.last('10Y')
        else:
            raise ValueError("Periodo no reconocido.")

        # Calcular el rendimiento logarítmico
        rendimiento_log = np.log(datos_periodo['Close'].iloc[-1] / datos_periodo['Close'].iloc[0])
        rendimiento_anualizado = rendimiento_log / (datos_periodo.shape[0] / 252)  # Ajustar por días de negociación

        # Calcular el riesgo
        rendimientos_diarios = np.log(datos_periodo['Close'] / datos_periodo['Close'].shift(1)).dropna()
        desviacion_diaria = rendimientos_diarios.std()
        riesgo_anualizado = desviacion_diaria * np.sqrt(252)

        return rendimiento_anualizado, riesgo_anualizado
    except Exception as e:
        print(f"Error al calcular rendimiento y riesgo para el periodo {periodo}: {e}")
        return None, None

# Variable para almacenar la información de los ETFs
ETFs_Data = []

# Descargar precios históricos para todos los tickers
precios_historicos_todos = descargar_datos_historicos(etf_tickers)

# Iterar sobre los ETFs y obtener la información
for nombre, ticker in zip(etf_nombres, etf_tickers):
    nombre_corto, descripcion_larga = obtener_data(ticker)
    
    # Obtener los precios históricos del ticker actual
    precios_historicos = precios_historicos_todos.get(ticker)
    
    # Obtener el precio actual
    precio_actual = obtener_precio_actual(ticker)

    # Calcular el rendimiento logarítmico anualizado
    if precios_historicos is not None and not precios_historicos.empty:
        rendimiento_log_geom = rendimiento_logaritmico(precios_historicos)
        riesgo_promedio = calcular_riesgo_promedio(precios_historicos)
        ratio_riesgo_rendimiento = calcular_ratio_riesgo_rendimiento(rendimiento_log_geom, riesgo_promedio)

        # Calcular rendimiento y riesgo para diferentes periodos
        periodos = ['1m', '3m', '6m', '1y', 'YTD', '3y', '5y', '10y']
        rendimientos = {}
        riesgos = {}
        
        for periodo in periodos:
            rendimiento, riesgo = rendimiento_y_riesgo_por_periodo(precios_historicos, periodo)
            rendimientos[periodo] = rendimiento
            riesgos[periodo] = riesgo

    else:
        rendimiento_log_geom = None
        riesgo_promedio = None
        ratio_riesgo_rendimiento = None
        rendimientos = {periodo: None for periodo in periodos}
        riesgos = {periodo: None for periodo in periodos}
    
    # Añadir la información a la lista de ETFs
    ETFs_Data.append({
        "nombre": nombre,
        "simbolo": ticker,
        "nombre_corto": nombre_corto,
        "descripcion_larga": descripcion_larga,
        "precios_historicos": precios_historicos,
        "precio_actual": precio_actual,
        "rendimiento_log_geom": rendimiento_log_geom,
        "riesgo_promedio": riesgo_promedio,
        "ratio_riesgo_rendimiento": ratio_riesgo_rendimiento,
        "rendimientos": rendimientos,
        "riesgos": riesgos
    })

# Mostrar resultados en tabla
df_resultado = pd.DataFrame({"Año": list(range(anos_proyeccion + 1)), "Valor proyectado": valores})
st.write(df_resultado)

# Suponiendo que df_resultado ya está definido
st.subheader("Gráfica de Rendimiento Proyectado")

# Establecer un estilo para la gráfica
plt.style.use('seaborn-darkgrid')

# Crear la figura y el eje
fig, ax = plt.subplots(figsize=(10, 6))  # Ajustar tamaño de la figura

# Graficar los datos
ax.plot(df_resultado["Año"], df_resultado["Valor proyectado"], 
        marker='o', color='royalblue', linewidth=2, markersize=8, label='Valor Proyectado')

# Etiquetas y título
ax.set_xlabel("Año", fontsize=14)
ax.set_ylabel("Valor Proyectado ($)", fontsize=14)
ax.set_title(f"Proyección del Portafolio seleccionado: {portafolio_seleccionado}", fontsize=16)
ax.legend()  # Agregar leyenda

# Añadir cuadrícula
ax.grid(True)

# Formato de los ejes
ax.tick_params(axis='both', which='major', labelsize=12)

# Mostrar la gráfica en Streamlit
st.pyplot(fig)

# Mensaje final personalizado
st.success(f"{nombre} {apellido_paterno}, según el análisis, a los {edad_proyecto} años tendrás un valor estimado de inversión de ${valores[-1]:,.2f} en el portafolio seleccionado.")


    
