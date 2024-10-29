import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
edad_proyecto = st.number_input("Edad a proyectar", min_value=edad, max_value=150, step=1)

# Validación de la edad a proyectar
edad_maxima = 150
edad_proyecto = st.number_input("Edad a proyectar", min_value=edad, max_value=edad_maxima, step=1)
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
    
aportacion_inicial = st.number_input("Aportación inicial", min_value=1000.0, step=100.0)
if not validar_aportación_inicial(aportacion_inicial):
    st.stop()

# Número de años para proyectar
anos_proyeccion = st.slider("Años de proyección", min_value=1, max_value=30, step=1)

# Dividir los portafolios en básicos y premier
portafolios_basicos = [
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

portafolios_premier = [
    "AZ China",	
    "AZ MSCI TAIWAN INDEX FD",	
    "AZ RUSSELL 2000",
    "AZ Brasil",
    "AZ MSCI UNITED KINGDOM",
    "AZ DJ US FINANCIAL SECT",
    "AZ BRIC",
    "AZ MSCI SOUTH KOREA IND",
    "AZ BARCLAYS AGGREGATE",
    "AZ Mercados Emergentes",
    "AZ MSCI EMU",
    "AZ FTSE/XINHUA CHINA 25",
    "AZ Oro",
    "AZ LATIXX MEX CETETRAC",
    "AZ QQQ NASDAQ 100",
    "AZ MSCI ASIA EX-JAPAN",
    "AZ LATIXX MEX M10TRAC",
    "AZ BARCLAYS 1-3 YEAR TR",
    "AZ MSCI ACWI INDEX FUND",	
    "AZ LATIXX MEXICO M5TRAC",	
    "AZ SILVER TRUST",
    "AZ MSCI HONG KONG INDEX",
    "AZ LATIXX MEX UDITRAC",	
    "AZ SPDR S&P 500 ETF TRUST",	
    "AZ MSCI JAPAN INDEX FD",
    "AZ BG EUR GOVT BOND 1-3",	
    "AZ SPDR DJIA TRUST",	
    "AZ MSCI FRANCE INDEX FD",	
    "AZ DJ US OIL & GAS EXPL",	
    "AZ VANGUARD EMERGING MARKET ETF",	
    "AZ MSCI AUSTRALIA INDEX",	
    "AZ IPC LARGE CAP T R TR",	
    "AZ FINANCIAL SELECT SECTOR SPDR",	
    "AZ MSCI CANADA",
    "AZ S&P LATIN AMERICA 40",	
    "AZ HEALTH CARE SELECT SECTOR",	
    "AZ MSCI GERMANY INDEX",
    "AZ DJ US HOME CONSTRUCT",
]

# Opción para elegir entre básico o premie
tipo_portafolio = st.selectbox("Selecciona el tipo de portafolio", ["Básico", "Premium"])

# Mostrar los portafolios disponibles según la selección
if tipo_portafolio == "Básico":
    portafolio_seleccionado = st.selectbox("Selecciona el portafolio", portafolios_basicos)
elif tipo_portafolio == "Premier":
    portafolio_seleccionado = st.selectbox("Selecciona el portafolio", portafolios_premier)

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
    "Allianz Global": 0.00,
    "AZ China": 0.00,	
    "AZ MSCI TAIWAN INDEX FD": 0.00,	
    "AZ RUSSELL 2000": 0.00,
    "AZ Brasil": 0.00,
    "AZ MSCI UNITED KINGDOM": 0.00,
    "AZ DJ US FINANCIAL SECT": 0.00,
    "AZ BRIC": 0.00,
    "AZ MSCI SOUTH KOREA IND": 0.00,
    "AZ BARCLAYS AGGREGATE": 0.00,
    "AZ Mercados Emergentes": 0.00,
    "AZ MSCI EMU": 0.00,
    "AZ FTSE/XINHUA CHINA 25": 0.00,
    "AZ Oro": 0.00,
    "AZ LATIXX MEX CETETRAC": 0.00,
    "AZ QQQ NASDAQ 100": 0.00,
    "AZ MSCI ASIA EX-JAPAN": 0.00,
    "AZ LATIXX MEX M10TRAC": 0.00,
    "AZ BARCLAYS 1-3 YEAR TR": 0.00,
    "AZ MSCI ACWI INDEX FUND": 0.00,	
    "AZ LATIXX MEXICO M5TRAC": 0.00,	
    "AZ SILVER TRUST": 0.00,
    "AZ MSCI HONG KONG INDEX": 0.00,
    "AZ LATIXX MEX UDITRAC": 0.00,	
    "AZ SPDR S&P 500 ETF TRUST": 0.00,	
    "AZ MSCI JAPAN INDEX FD": 0.00,
    "AZ BG EUR GOVT BOND 1-3": 0.00,	
    "AZ SPDR DJIA TRUST": 0.00,	
    "AZ MSCI FRANCE INDEX FD": 0.00,	
    "AZ DJ US OIL & GAS EXPL": 0.00,	
    "AZ VANGUARD EMERGING MARKET ETF": 0.00,	
    "AZ MSCI AUSTRALIA INDEX": 0.00,	
    "AZ IPC LARGE CAP T R TR": 0.00,	
    "AZ FINANCIAL SELECT SECTOR SPDR": 0.00,	
    "AZ MSCI CANADA": 0.00,
    "AZ S&P LATIN AMERICA 40": 0.00,	
    "AZ HEALTH CARE SELECT SECTOR": 0.00,	
    "AZ MSCI GERMANY INDEX": 0.00,
    "AZ DJ US HOME CONSTRUCT": 0.00,
}

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


    
