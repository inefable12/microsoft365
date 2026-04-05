import streamlit as st
import random
import time

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(page_title="Juego Microsoft 365") #, layout="wide")

st.title("🎮 Juego: Relaciona Aplicaciones de Microsoft 365")

# =========================
# DATOS DEL JUEGO
# =========================
apps = {
    "Word": "Procesador de texto para crear documentos.",
    "Excel": "Hoja de cálculo para análisis de datos.",
    "PowerPoint": "Creación de presentaciones.",
    "Outlook": "Gestión de correos electrónicos y calendario.",
    "Teams": "Comunicación y colaboración en equipo.",
    "OneDrive": "Almacenamiento en la nube.",
    "SharePoint": "Gestión de contenido y colaboración.",
    "Copilot": "Asistente de inteligencia artificial.",
}

# =========================
# ESTADO DE SESIÓN
# =========================
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "game_data" not in st.session_state:
    st.session_state.game_data = []

# =========================
# GENERAR NUEVO JUEGO
# =========================
def generate_game():
    items = list(apps.items())
    random.shuffle(items)
    st.session_state.game_data = items
    st.session_state.start_time = time.time()

if st.button("🔄 Nuevo Juego"):
    generate_game()

if not st.session_state.game_data:
    generate_game()

# =========================
# TEMPORIZADOR
# =========================
elapsed_time = int(time.time() - st.session_state.start_time)
st.subheader(f"⏱ Tiempo: {elapsed_time} segundos")

# =========================
# INTERFAZ DEL JUEGO
# =========================
st.write("### Arrastra (simulado) cada aplicación a su descripción")

# NOTA: Streamlit no soporta drag-and-drop nativo.
# Se simula con selectbox.

results = {}

cols = st.columns(2)

with cols[0]:
    st.write("### Aplicaciones")
    app_names = [item[0] for item in st.session_state.game_data]
    random.shuffle(app_names)

with cols[1]:
    st.write("### Descripciones")
    descriptions = [item[1] for item in st.session_state.game_data]

# Selección simulada
for app in app_names:
    choice = st.selectbox(f"Selecciona la descripción para {app}", descriptions, key=app)
    results[app] = choice

# =========================
# VALIDACIÓN
# =========================
if st.button("✅ Verificar respuestas"):
    score = 0
    for app, desc in results.items():
        if apps[app] == desc:
            score += 1
    st.success(f"Puntaje: {score} / {len(apps)}")

# =========================
# TABLA DE REFERENCIA
# =========================
st.write("---")
st.write("### Tabla de Aplicaciones")

import pandas as pd

df = pd.DataFrame(list(apps.items()), columns=["Aplicación", "Descripción"])
st.dataframe(df)
