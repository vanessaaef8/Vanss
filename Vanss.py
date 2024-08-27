{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "5d82de98-d26e-445e-a773-2b5ab5e38609",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\"[Vanessa\" no se reconoce como un comando interno o externo,\n",
      "programa o archivo por lotes ejecutable.\n"
     ]
    }
   ],
   "source": [
    "import streamlit as st\n",
    "\n",
    "![Vanessa Espinosa](https://github.com/vanessaaef8/Vanss.git)\n",
    "\n",
    "# Configuración de la página\n",
    "st.set_page_config(page_title=\"Currículum Vitae\", layout=\"wide\")\n",
    "\n",
    "# Título\n",
    "st.title(\"Vanessa Espinosa Fuentes\")\n",
    "\n",
    "# Información personal\n",
    "st.header(\"Contacto\")\n",
    "st.write(\"0239141@up.edu.mx\")\n",
    "st.write(\"+52 33 3462 0315\")\n",
    "st.write(\"Zapopan, Jalisco\")\n",
    "\n",
    "# Educación\n",
    "st.header(\"Educación\")\n",
    "st.subheader(\"Licenciatura en Administración y Finanzas\")\n",
    "st.write(\"Universidad Panamericana | Agosto 2020 - Diciembre 2024\")\n",
    "\n",
    "# Actividades extra-académicas\n",
    "st.header(\"Actividades extra-académicas\")\n",
    "st.write(\"Equipo Representativo de Voleibol de Sala | División 1 | Universidad Panamericana\")\n",
    "\n",
    "# Habilidades\n",
    "st.header(\"Habilidades\")\n",
    "st.write(\"- Trabajo en equipo\")\n",
    "st.write(\"- Reolución de problemas\")\n",
    "st.write(\"- Creatividad e innovación\")\n",
    "st.write(\"- Adaptabilidad\")\n",
    "\n",
    "# Conocimientos\n",
    "st.header(\"Conocimientos\")\n",
    "st.write(\"- SAP Software\")\n",
    "st.write(\"- Excel Avanzado\")\n",
    "st.write(\"- R Studio\")\n",
    "st.write(\"- Manejo de base de datos: Euromonitor, Facset, Kaggle\")\n",
    "\n",
    "# Idiomas\n",
    "st.header(\"Idiomas\")\n",
    "st.write(\"- Español (Nativo)\")\n",
    "st.write(\"- Inglés (Avanzado)\")\n",
    "st.write(\"- Francés (Básico)\")\n",
    "\n",
    "# Vinculación Social\n",
    "st.header(\"Vinculación Social\")\n",
    "st.subheader(\"Pequeños Nutriólogos A.C.\")\n",
    "st.write(\"Producción e imagen publicitaria en videos nutricionales\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
