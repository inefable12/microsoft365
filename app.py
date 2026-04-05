import streamlit as st
import random
import time
import pandas as pd

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="Juego Microsoft 365") #, layout="wide")

st.title("🎮 Juego: Relaciona Aplicaciones con su Función")

# =========================
# DATOS
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
# ESTADO
# =========================
if "game_data" not in st.session_state:
    st.session_state.game_data = random.sample(list(apps.items()), len(apps))

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "answers" not in st.session_state:
    st.session_state.answers = {}

# =========================
# NUEVO JUEGO
# =========================
if st.button("🔄 Nuevo Juego"):
    st.session_state.game_data = random.sample(list(apps.items()), len(apps))
    st.session_state.start_time = time.time()
    st.session_state.answers = {}
    st.rerun()

# =========================
# TIMER
# =========================
elapsed = int(time.time() - st.session_state.start_time)
st.subheader(f"⏱ Tiempo: {elapsed} s")

# =========================
# INTERFAZ CON ICONOS
# =========================
st.write("### Relaciona cada icono con su descripción")

cols = st.columns(2)

# lista fija de descripciones (no cambia)
descriptions = [desc for _, desc in st.session_state.game_data]

with cols[0]:
    st.write("### Aplicaciones")
    for app, _ in st.session_state.game_data:
        try:
            st.image(f"icons/{app.lower()}.png", width=60)
        except:
            st.write(f"(Falta icono: {app})")

with cols[1]:
    st.write("### Selecciona la descripción correcta")
    for i, (app, _) in enumerate(st.session_state.game_data):
        selected = st.selectbox(
            f"Opción {i+1}",
            descriptions,
            key=f"select_{app}"
        )
        st.session_state.answers[app] = selected

# =========================
# VALIDAR
# =========================
if st.button("✅ Verificar"):
    score = 0
    for app, correct_desc in apps.items():
        if app in st.session_state.answers:
            if st.session_state.answers[app] == correct_desc:
                score += 1

    st.success(f"Puntaje: {score} / {len(apps)}")

# =========================
# TABLA
# =========================
st.write("---")
st.write("### Tabla de referencia")

df = pd.DataFrame(list(apps.items()), columns=["Aplicación", "Descripción"])
st.dataframe(df)
