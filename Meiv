import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import requests
import json
import sqlite3
from scipy.stats import norm

# Función para calcular cuánto necesitas al retiro
def calcular_meta_retiro(edad_actual, edad_retiro, ahorro_mensual, tasa_inflacion=0.04):
    años = edad_retiro - edad_actual
    ahorro_total = ahorro_mensual * 12 * años
    monto_necesario = ahorro_total * (1 + tasa_inflacion)**años
    return round(monto_necesario, 2)

# Función para recomendar portafolio
def recomendar_portafolio(horizonte, riesgo="balanceado"):
    if horizonte >= 15:  # Largo plazo
        return {"CETES": 0.2, "Fondos Indexados": 0.5, "Criptomonedas": 0.3}
    elif horizonte >= 7:  # Medio plazo
        return {"CETES": 0.4, "Fondos Indexados": 0.4, "Criptomonedas": 0.2}
    else:  # Corto plazo
        return {"CETES": 0.7, "Fondos Indexados": 0.2, "Criptomonedas": 0.1}

# Función para obtener tasa de CETES desde Yahoo Finance
def obtener_tasa_cetes():
    try:
        data = yf.download("MX0R.MX", period="1d")
        return data["Adj Close"][-1] / 100
    except:
        return 0.10  # Tasa fija si falla la API

# Función para obtener precio de criptomonedas desde CoinGecko
def obtener_precio_crypto(crypto="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[crypto]["usd"]
    return None

# Función para obtener rendimiento de fondos indexados (ejemplo SPY)
def obtener_rendimiento_fondos():
    try:
        data = yf.download("SPY", period="1y")
        rendimiento = (data["Adj Close"][-1] - data["Adj Close"][0]) / data["Adj Close"][0]
        return rendimiento
    except:
        return 0.07  # Rendimiento promedio anual estimado

# Función para guardar configuración del usuario en SQLite
def guardar_configuracion(usuario, edad, ahorro, preferencias):
    conn = sqlite3.connect("config.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            usuario TEXT,
            edad INTEGER,
            ahorro REAL,
            preferencias TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO usuarios (usuario, edad, ahorro, preferencias)
        VALUES (?, ?, ?, ?)
    """, (usuario, edad, ahorro, preferencias))
    conn.commit()
    conn.close()

# Simulación de Monte Carlo para el crecimiento del portafolio
def simulacion_monte_carlo(inversion_inicial, años, rendimiento_promedio, volatilidad):
    simulaciones = []
    for _ in range(1000):  # 1000 escenarios
        valores = [inversion_inicial]
        for _ in range(años):
            crecimiento = np.random.normal(rendimiento_promedio, volatilidad)
            valores.append(valores[-1] * (1 + crecimiento))
        simulaciones.append(valores)
    return simulaciones

# Interfaz de Streamlit
st.title("Calculadora de Retiro e Inversiones")
st.sidebar.header("Configuración Inicial")

# Entrada de datos
edad_actual = st.sidebar.number_input("Tu edad actual:", min_value=18, max_value=100, value=25)
edad_retiro = st.sidebar.number_input("Edad de retiro:", min_value=30, max_value=100, value=65)
ahorro_mensual = st.sidebar.number_input("Ahorro mensual ($):", min_value=0, value=5000)
tasa_inflacion = st.sidebar.slider("Inflación anual (%):", min_value=0.0, max_value=10.0, value=4.0) / 100
usuario = st.sidebar.text_input("Nombre de usuario:")

# Selección de instrumentos de inversión
inversiones = st.sidebar.multiselect(
    "Elige los instrumentos de inversión:",
    ["CETES", "Fondos Indexados", "Criptomonedas", "Bonos Corporativos"],
    default=["CETES", "Fondos Indexados", "Criptomonedas"]
)

# Cálculos principales
años_para_retiro = edad_retiro - edad_actual
monto_necesario = calcular_meta_retiro(edad_actual, edad_retiro, ahorro_mensual, tasa_inflacion)
recomendacion = recomendar_portafolio(años_para_retiro)

# Guardar configuración
if st.sidebar.button("Guardar configuración"):
    guardar_configuracion(usuario, edad_actual, ahorro_mensual, str(inversiones))
    st.sidebar.success(f"Configuración guardada para {usuario}.")

# Mostrar resultados
st.header("Proyección Financiera")
st.write(f"Tienes **{años_para_retiro} años** para ahorrar e invertir.")
st.write(f"Necesitarás aproximadamente **${monto_necesario:,.2f}** al momento de tu retiro considerando una inflación del {tasa_inflacion*100:.2f}%.")

# Recomendación de portafolio
st.header("Recomendación de Portafolio")
for instrumento, porcentaje in recomendacion.items():
    if instrumento in inversiones:
        st.write(f"- {instrumento}: **{porcentaje*100:.0f}%**")

# Gráfica de distribución del portafolio
fig = go.Figure(data=[go.Pie(labels=list(recomendacion.keys()), values=list(recomendacion.values()))])
fig.update_layout(title="Distribución Recomendada")
st.plotly_chart(fig)

# Simulación del crecimiento del portafolio
st.header("Simulación del Crecimiento")
cetes_rate = obtener_tasa_cetes()
fondos_rate = obtener_rendimiento_fondos()
crypto_rate = 0.15  # Rendimiento estimado, alta volatilidad

portafolio = []
saldo_actual = 0

for año in range(años_para_retiro):
    cetes = saldo_actual * recomendacion["CETES"] * (1 + cetes_rate)
    fondos = saldo_actual * recomendacion["Fondos Indexados"] * (1 + fondos_rate)
    crypto = saldo_actual * recomendacion["Criptomonedas"] * (1 + crypto_rate)
    saldo_actual += ahorro_mensual * 12
    saldo_actual += cetes + fondos + crypto
    portafolio.append(saldo_actual)

# Gráfica de proyección
df = pd.DataFrame({
    "Año": range(edad_actual, edad_retiro),
    "Saldo Proyectado": portafolio
})

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df["Año"], y=df["Saldo Proyectado"], mode="lines+markers", name="Proyección"))
fig2.update_layout(title="Proyección del Portafolio", xaxis_title="Año", yaxis_title="Saldo ($)")
st.plotly_chart(fig2)

# Simulación de Monte Carlo
st.header("Simulación de Monte Carlo para el Portafolio")
simulaciones = simulacion_monte_carlo(saldo_actual, años_para_retiro, 0.07, 0.2)

# Gráfica de simulación
fig3 = go.Figure()
for simulacion in simulaciones[:10]:  # Mostrar solo las primeras 10 simulaciones
    fig3.add_trace(go.Scatter(x=df["Año"], y=simulacion, mode="lines", name="Simulación"))
fig3.update_layout(title="Simulaciones de Crecimiento del Portafolio (Monte Carlo)", xaxis_title="Año", yaxis_title="Saldo ($)")
st.plotly_chart(fig3)

st.write("**Nota:** Las tasas de rendimiento son estimaciones basadas en datos históricos y pueden variar.")
