import streamlit as st
import random
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Juego Microsoft 365")
st.title("🎮 ¿Qué APP Soy")
st.sidebar.image("icons/icono_logo.png", caption="Dr. Jesus Alvarado")

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
    st.session_state.game_data = random.sample(list(apps.items()), 5)

if "descriptions" not in st.session_state:
    desc = [d for _, d in st.session_state.game_data]
    random.shuffle(desc)
    st.session_state.descriptions = desc

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "score" not in st.session_state:
    st.session_state.score = None

# =========================
# NUEVO JUEGO
# =========================
if st.button("🔄 Nuevo Juego"):
    st.session_state.game_data = random.sample(list(apps.items()), 5)
    desc = [d for _, d in st.session_state.game_data]
    random.shuffle(desc)
    st.session_state.descriptions = desc
    st.session_state.answers = {}
    st.session_state.game_over = False
    st.session_state.score = None
    st.rerun()

# =========================
# BOTÓN FINALIZAR
# =========================
if not st.session_state.game_over:
    if st.button("⏹ Finalizar ahora"):
        st.session_state.game_over = True
        st.rerun()

# =========================
# INTERFAZ
# =========================
if not st.session_state.game_over:
    st.write("### Relaciona cada icono con una opción")

    cols = st.columns(2)

    with cols[0]:
        st.write("### Aplicación")
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
                st.session_state.descriptions,
                key=f"select_{app}"
            )
            st.session_state.answers[app] = selected

# =========================
# EVALUACIÓN
# =========================
if st.session_state.game_over and st.session_state.score is None:
    score = 0
    total = len(st.session_state.game_data)

    for app, correct_desc in st.session_state.game_data:
        if app in st.session_state.answers:
            if st.session_state.answers[app] == correct_desc:
                score += 1

    st.session_state.score = score

# =========================
# RESULTADOS
# =========================
if st.session_state.game_over:
    score = st.session_state.score
    total = len(st.session_state.game_data)

    st.write("---")

    if score == total:
        st.success(f"🎉 ¡GANASTE! Puntaje: {score}/{total}")
        st.balloons()
    else:
        st.error(f"💀 GAME OVER - Puntaje: {score}/{total}. Intenta otra vez")

# =========================
# TABLA (CONDICIONAL)
# =========================
if st.session_state.game_over:
    if st.session_state.score < len(st.session_state.game_data):
        st.write("---")
        st.write("### Tabla de referencia")
        df = pd.DataFrame(list(apps.items()), columns=["Aplicación", "Descripción"])
        st.dataframe(df)
