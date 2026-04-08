import streamlit as st

# 1. Configuración de página y Estilo (CSS)
st.set_page_config(page_title="Comunicador Infantil", layout="centered")

# Estilizamos los botones para que sean grandes y amigables
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        height: 150px;
        font-size: 24px;
        border-radius: 20px;
        border: 4px solid #ffffff;
        background-color: #f0f2f6;
    }
    .stApp {
        background-color: #FFA500; /* Naranja según tu ejemplo */
    }
    h1, h3 {
        color: white;
        text-shadow: 2px 2px 4px #000000;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialización del Estado
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"
if "frase" not in st.session_state:
    st.session_state.frase = []

# 3. Funciones de Ayuda
def seleccionar_picto(nombre, emoji):
    st.session_state.frase.append(f"{emoji} {nombre}")

# --- LÓGICA DE NAVEGACIÓN ---

# Pantalla de Inicio
if st.session_state.pantalla == "inicio":
    st.title("¿Qué quieres decir? 🗣️")
    
    # Mostrar la frase actual que se está construyendo
    if st.session_state.frase:
        st.success(f"Tu frase: {' + '.join(st.session_state.frase)}")
        if st.button("🗑️ Borrar Todo"):
            st.session_state.frase = []
            st.rerun()

    st.subheader("Elige una categoría:")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("👤\nYO"):
            st.session_state.pantalla = "yo"
            st.rerun()
    with col2:
        if st.button("😊\nEMOCIONES"):
            st.session_state.pantalla = "emociones"
            st.rerun()
    with col3:
        if st.button("🏠\nCASA"):
            st.session_state.pantalla = "casa"
            st.rerun()

# Pantalla: Yo
elif st.session_state.pantalla == "yo":
    st.title("👤 Categoría: Yo")
    cols = st.columns(3)
    
    opciones = [("Niño", "👦"), ("Niña", "👧"), ("Hambre", "🍕"), ("Sed", "💧")]
    
    for i, (nombre, icono) in enumerate(opciones):
        with cols[i % 3]:
            if st.button(f"{icono}\n{nombre}"):
                seleccionar_picto(nombre, icono)
    
    st.divider()
    if st.button("⬅️ VOLVER"):
        st.session_state.pantalla = "inicio"
        st.rerun()

# Pantalla: Emociones
elif st.session_state.pantalla == "emociones":
    st.title("😊 ¿Cómo te sientes?")
    cols = st.columns(3)
    
    emociones = [("Feliz", "😄"), ("Triste", "😢"), ("Enfadado", "😡"), ("Cansado", "😴")]
    
    for i, (nombre, icono) in enumerate(emociones):
        with cols[i % 3]:
            if st.button(f"{icono}\n{nombre}"):
                seleccionar_picto(nombre, icono)

    st.divider()
    if st.button("⬅️ VOLVER"):
        st.session_state.pantalla = "inicio"
        st.rerun()

# Pantalla: Casa
elif st.session_state.pantalla == "casa":
    st.title("🏠 En casa...")
    # Aquí puedes repetir la lógica de columnas con objetos del hogar
    if st.button("⬅️ VOLVER"):
        st.session_state.pantalla = "inicio"
        st.rerun()