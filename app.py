"""
Supuesto 4 - Aplicación web de comunicación con pictogramas
Población: Niños/niñas con problemas de expresión oral
Objetivo: Incluir pictogramas, palabras y/o frases para facilitar
          la comunicación en contextos escolares y/o familiares.

Versión con perfiles de usuario:
  - Cada perfil tiene su propio historial, frase actual y frases rápidas.
  - Los pictogramas son globales y compartidos entre perfiles.
"""

import urllib.parse
from pathlib import Path

import streamlit as st
from PIL import Image

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="ComunicApp - Pictogramas",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f0f6ff; }

    .frase-box {
        background: #fff9c4;
        border-left: 6px solid #f9a825;
        border-radius: 10px;
        padding: 14px 20px;
        font-size: 20px;
        font-weight: bold;
        color: #333;
        min-height: 56px;
        margin-bottom: 10px;
        word-wrap: break-word;
    }

    .cat-header {
        background: linear-gradient(90deg, #4A90E2 0%, #7B61FF 100%);
        color: white;
        border-radius: 10px;
        padding: 8px 16px;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
        text-transform: capitalize;
    }

    .picto-nombre {
        font-size: 13px;
        font-weight: 700;
        text-align: center;
        color: #1a3a6b;
        text-transform: capitalize;
        margin-top: 2px;
        word-wrap: break-word;
    }

    .perfil-activo-box {
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 8px;
        text-align: center;
    }

    div[data-testid="stButton"] > button {
        border-radius: 10px;
        font-size: 14px;
        font-weight: 600;
        padding: 5px 10px;
    }

    h1 { color: #1a3a6b; }
    h2, h3 { color: #2c5282; }
</style>
""", unsafe_allow_html=True)

# ── Extensiones de imagen soportadas ────────────────────────────────────────
IMG_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

# ── Colores disponibles para los perfiles ───────────────────────────────────
COLORES_PERFIL = {
    "Azul":     {"bg": "#e6f0ff", "border": "#4A90E2", "text": "#1a3a6b"},
    "Verde":    {"bg": "#e6f9ef", "border": "#27ae60", "text": "#145a32"},
    "Naranja":  {"bg": "#fff3e0", "border": "#f39c12", "text": "#7d5a00"},
    "Rosa":     {"bg": "#fde8f5", "border": "#e056a0", "text": "#6b1444"},
    "Morado":   {"bg": "#f0e8ff", "border": "#7B61FF", "text": "#3a1a8b"},
    "Rojo":     {"bg": "#fdecea", "border": "#e74c3c", "text": "#7b1c1c"},
}

FRASES_RAPIDAS_DEFECTO = [
    "Quiero ir al baño",
    "Tengo hambre",
    "Tengo sed",
    "Me duele la cabeza",
    "Estoy cansado",
    "Necesito ayuda",
    "Quiero ir a casa",
    "Quiero jugar",
]


# ── Carga de pictogramas desde disco ────────────────────────────────────────
@st.cache_data(show_spinner=False)
def cargar_categorias(ruta_base: str) -> dict:
    base = Path(ruta_base)
    categorias = {}
    if not base.exists() or not base.is_dir():
        return categorias
    for subdir in sorted(base.iterdir()):
        if not subdir.is_dir():
            continue
        imagenes = sorted(
            f for f in subdir.iterdir()
            if f.is_file() and f.suffix.lower() in IMG_EXTS
        )
        if imagenes:
            nombre_cat = subdir.name.replace("_", " ").replace("-", " ").title()
            categorias[nombre_cat] = [
                {
                    "nombre": f.stem.replace("_", " ").replace("-", " ").capitalize(),
                    "ruta": str(f),
                }
                for f in imagenes
            ]
    return categorias


# ── Función auxiliar: mostrar un pictograma ──────────────────────────────────
def mostrar_picto(picto: dict, img_size: int, key: str):
    ruta = Path(picto["ruta"])
    try:
        img = Image.open(ruta)
        st.image(img, use_container_width=False, width=img_size)
    except Exception:
        st.markdown("🖼️", help="No se pudo cargar la imagen.")
    st.markdown(
        f'<p class="picto-nombre">{picto["nombre"]}</p>',
        unsafe_allow_html=True,
    )
    if st.button("＋ Añadir", key=key, use_container_width=True):
        perfil_activo()["frase_actual"].append(
            {"nombre": picto["nombre"], "ruta": picto["ruta"]}
        )
        st.rerun()


# ── Helpers de perfiles ──────────────────────────────────────────────────────
def perfil_activo() -> dict:
    """Devuelve el dict del perfil actualmente seleccionado."""
    pid = st.session_state.perfil_activo_id
    return st.session_state.perfiles[pid]


def crear_perfil(nombre: str, color: str) -> str:
    """Crea un nuevo perfil y devuelve su ID."""
    pid = f"p_{len(st.session_state.perfiles)}_{nombre.lower().replace(' ', '_')}"
    st.session_state.perfiles[pid] = {
        "nombre": nombre.strip(),
        "color": color,
        "frase_actual": [],
        "historial": [],
        "frases_rapidas": list(FRASES_RAPIDAS_DEFECTO),
    }
    return pid


# ── Inicialización del estado de sesión ─────────────────────────────────────
if "perfiles" not in st.session_state:
    st.session_state.perfiles = {}
    pid_default = crear_perfil("Usuario", "Azul")
    st.session_state.perfil_activo_id = pid_default

if "perfil_activo_id" not in st.session_state:
    st.session_state.perfil_activo_id = next(iter(st.session_state.perfiles))


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 👤 Perfiles de usuario")

    # Selector de perfil activo
    nombres_perfiles = {
        pid: datos["nombre"]
        for pid, datos in st.session_state.perfiles.items()
    }

    pid_sel = st.selectbox(
        "Perfil activo",
        options=list(nombres_perfiles.keys()),
        format_func=lambda pid: nombres_perfiles[pid],
        index=list(nombres_perfiles.keys()).index(st.session_state.perfil_activo_id),
        key="selector_perfil",
    )
    if pid_sel != st.session_state.perfil_activo_id:
        st.session_state.perfil_activo_id = pid_sel
        st.rerun()

    # Mostrar color del perfil activo
    p = perfil_activo()
    color_info = COLORES_PERFIL[p["color"]]
    st.markdown(
        f'<div class="perfil-activo-box" style="'
        f'background:{color_info["bg"]};'
        f'border:2px solid {color_info["border"]};'
        f'color:{color_info["text"]};">'
        f'✅ {p["nombre"]}'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    # Crear nuevo perfil
    with st.expander("➕ Crear nuevo perfil"):
        nuevo_nombre = st.text_input("Nombre del perfil", key="nuevo_nombre_input",
                                     placeholder="Ej. Ana, Pedro...")
        nuevo_color = st.selectbox("Color", list(COLORES_PERFIL.keys()), key="nuevo_color_sel")
        if st.button("Crear perfil", key="btn_crear_perfil"):
            if nuevo_nombre.strip():
                nuevo_pid = crear_perfil(nuevo_nombre.strip(), nuevo_color)
                st.session_state.perfil_activo_id = nuevo_pid
                st.success(f"Perfil '{nuevo_nombre.strip()}' creado.")
                st.rerun()
            else:
                st.warning("Escribe un nombre.")

    # Editar perfil activo
    with st.expander("✏️ Editar perfil activo"):
        edit_nombre = st.text_input(
            "Nuevo nombre", value=p["nombre"], key="edit_nombre_input"
        )
        edit_color = st.selectbox(
            "Color", list(COLORES_PERFIL.keys()),
            index=list(COLORES_PERFIL.keys()).index(p["color"]),
            key="edit_color_sel",
        )
        if st.button("Guardar cambios", key="btn_editar_perfil"):
            p["nombre"] = edit_nombre.strip() or p["nombre"]
            p["color"] = edit_color
            st.success("Perfil actualizado.")
            st.rerun()

    # Eliminar perfil
    if len(st.session_state.perfiles) > 1:
        with st.expander("🗑️ Eliminar perfil activo"):
            st.warning(f"¿Eliminar el perfil **{p['nombre']}**? Esta acción no se puede deshacer.")
            if st.button("Sí, eliminar", key="btn_eliminar_perfil"):
                del st.session_state.perfiles[st.session_state.perfil_activo_id]
                st.session_state.perfil_activo_id = next(iter(st.session_state.perfiles))
                st.rerun()

    st.divider()
    st.markdown("## ⚙️ Configuración")

    ruta_pictos = st.text_input(
        "📁 Ruta a la carpeta de pictogramas",
        value="pictogramas",
        help=(
            "Ruta absoluta o relativa al directorio donde ejecutas la app.\n"
            "Ejemplos:\n"
            "  ./pictogramas\n"
            "  C:/Users/Ana/pictogramas\n"
            "  /home/ana/pictogramas"
        ),
    )

    if st.button("🔄 Recargar pictogramas"):
        st.cache_data.clear()
        st.rerun()

    st.divider()
    num_cols = st.slider("Columnas por fila", min_value=2, max_value=6, value=4)
    img_size = st.slider("Tamaño imagen (px)", min_value=60, max_value=200, value=110, step=10)

    st.divider()
    st.markdown("### ℹ️ Estructura esperada")
    st.code(
        "pictogramas/\n"
        "  emociones/\n"
        "    contento.png\n"
        "    triste.jpg\n"
        "  casa/\n"
        "    cama.png\n"
        "  lugares/\n"
        "    parque.png",
        language="text",
    )


# ── Cargar pictogramas (globales) ─────────────────────────────────────────────
CATEGORIAS = cargar_categorias(ruta_pictos)

# ── Datos del perfil activo ──────────────────────────────────────────────────
perfil = perfil_activo()
color_info = COLORES_PERFIL[perfil["color"]]

# ── Cabecera con perfil activo ────────────────────────────────────────────────
col_titulo, col_perfil = st.columns([3, 1])
with col_titulo:
    st.markdown("# 💬 ComunicApp")
    st.markdown("**Aplicación de comunicación aumentativa con pictogramas**")
with col_perfil:
    st.markdown(
        f'<div style="margin-top:18px;padding:10px 14px;border-radius:10px;'
        f'background:{color_info["bg"]};border:2px solid {color_info["border"]};'
        f'text-align:center;font-weight:bold;color:{color_info["text"]};font-size:15px;">'
        f'👤 {perfil["nombre"]}</div>',
        unsafe_allow_html=True,
    )
st.divider()


# ── Barra de frase construida ────────────────────────────────────────────────
frase_texto = "  ·  ".join([item["nombre"] for item in perfil["frase_actual"]])
st.markdown(
    f'<div class="frase-box">{"..." if not frase_texto else frase_texto}</div>',
    unsafe_allow_html=True,
)

if perfil["frase_actual"]:
    n_mini = min(len(perfil["frase_actual"]), 12)
    mini_cols = st.columns(n_mini)
    for i, item in enumerate(perfil["frase_actual"][:12]):
        with mini_cols[i]:
            if item.get("ruta") and Path(item["ruta"]).exists():
                try:
                    st.image(Image.open(item["ruta"]), width=50)
                except Exception:
                    st.markdown("🖼️")
            st.markdown(
                f'<p style="font-size:10px;text-align:center;margin:0;color:#444;">'
                f'{item["nombre"]}</p>',
                unsafe_allow_html=True,
            )

col_b1, col_b2, col_b3, col_b4 = st.columns([2, 2, 2, 4])

with col_b1:
    if st.button("🔊 Leer en voz alta", use_container_width=True):
        if perfil["frase_actual"]:
            texto_plano = " ".join([item["nombre"] for item in perfil["frase_actual"]])
            encoded = urllib.parse.quote(texto_plano)
            st.components.v1.html(
                f'<script>'
                f'var m=new SpeechSynthesisUtterance(decodeURIComponent("{encoded}"));'
                f'm.lang="es-ES";m.rate=0.85;window.speechSynthesis.speak(m);'
                f'</script>',
                height=0,
            )
            st.success(f"🔊 '{texto_plano}'")
        else:
            st.warning("Selecciona pictogramas primero.")

with col_b2:
    if st.button("⬅️ Borrar último", use_container_width=True):
        if perfil["frase_actual"]:
            perfil["frase_actual"].pop()
            st.rerun()

with col_b3:
    if st.button("🗑️ Borrar todo", use_container_width=True):
        perfil["frase_actual"] = []
        st.rerun()

with col_b4:
    if st.button("💾 Guardar en historial", use_container_width=True):
        if perfil["frase_actual"]:
            texto_guardado = " · ".join([item["nombre"] for item in perfil["frase_actual"]])
            perfil["historial"].append(texto_guardado)
            perfil["frase_actual"] = []
            st.success("¡Frase guardada!")
            st.rerun()
        else:
            st.warning("No hay frase que guardar.")

st.divider()


# ── Pestañas principales ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["🖼️ Pictogramas", "⚡ Frases rápidas", "✏️ Texto libre", "📋 Historial"]
)


# ─── TAB 1: PICTOGRAMAS ───────────────────────────────────────────────────────
with tab1:
    if not CATEGORIAS:
        st.error(
            f"⚠️ No se encontraron pictogramas en **'{ruta_pictos}'**.\n\n"
            "Comprueba que:\n"
            "- La ruta es correcta.\n"
            "- Dentro hay subcarpetas con imágenes (png, jpg, jpeg, bmp, webp, gif).\n\n"
            "Puedes cambiar la ruta en el panel lateral izquierdo."
        )
    else:
        busqueda = st.text_input(
            "🔍 Buscar pictograma",
            placeholder="Escribe para filtrar por nombre...",
            label_visibility="collapsed",
        )

        if busqueda.strip():
            resultados = [
                picto
                for items in CATEGORIAS.values()
                for picto in items
                if busqueda.lower() in picto["nombre"].lower()
            ]
            st.markdown(f"**{len(resultados)} resultado(s) para «{busqueda}»**")
            cols = st.columns(num_cols)
            for i, picto in enumerate(resultados):
                with cols[i % num_cols]:
                    mostrar_picto(picto, img_size, key=f"busq_{i}")
        else:
            cat_seleccionada = st.selectbox(
                "Categoría",
                list(CATEGORIAS.keys()),
                label_visibility="collapsed",
            )
            n_pictos = len(CATEGORIAS[cat_seleccionada])
            st.markdown(
                f'<div class="cat-header">📂 {cat_seleccionada} '
                f'<span style="font-weight:normal;font-size:14px;">'
                f'({n_pictos} pictogramas)</span></div>',
                unsafe_allow_html=True,
            )
            cols = st.columns(num_cols)
            for i, picto in enumerate(CATEGORIAS[cat_seleccionada]):
                with cols[i % num_cols]:
                    mostrar_picto(picto, img_size, key=f"cat_{cat_seleccionada}_{i}")


# ─── TAB 2: FRASES RÁPIDAS ────────────────────────────────────────────────────
with tab2:
    st.markdown(f"### ⚡ Frases rápidas de **{perfil['nombre']}**")

    cols_r = st.columns(2)
    for i, frase in enumerate(perfil["frases_rapidas"]):
        with cols_r[i % 2]:
            col_fr, col_del_fr = st.columns([5, 1])
            with col_fr:
                if st.button(f"📢  {frase}", key=f"rapida_{i}", use_container_width=True):
                    for palabra in frase.split():
                        perfil["frase_actual"].append({"nombre": palabra, "ruta": None})
                    st.rerun()
            with col_del_fr:
                if st.button("🗑️", key=f"del_rapida_{i}", help="Eliminar esta frase rápida"):
                    perfil["frases_rapidas"].pop(i)
                    st.rerun()

    st.divider()
    st.markdown("#### ➕ Añadir frase rápida personalizada")
    nueva_frase = st.text_input("Nueva frase", key="nf_input", label_visibility="collapsed",
                                placeholder="Escribe la frase y pulsa Agregar")
    if st.button("Agregar frase", key="nf_btn"):
        if nueva_frase.strip():
            perfil["frases_rapidas"].append(nueva_frase.strip())
            st.success("Frase añadida.")
            st.rerun()
        else:
            st.warning("Escribe algo primero.")


# ─── TAB 3: TEXTO LIBRE ──────────────────────────────────────────────────────
with tab3:
    st.markdown(f"### ✏️ Mensaje de **{perfil['nombre']}**")
    texto_libre = st.text_area(
        "Mensaje",
        placeholder="Escribe aquí lo que quieres comunicar...",
        height=130,
        label_visibility="collapsed",
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔊 Leer texto", use_container_width=True):
            if texto_libre.strip():
                encoded = urllib.parse.quote(texto_libre.strip())
                st.components.v1.html(
                    f'<script>'
                    f'var m=new SpeechSynthesisUtterance(decodeURIComponent("{encoded}"));'
                    f'm.lang="es-ES";m.rate=0.85;window.speechSynthesis.speak(m);'
                    f'</script>',
                    height=0,
                )
                st.info(f"🔊 *{texto_libre.strip()}*")
            else:
                st.warning("Escribe algo primero.")
    with c2:
        if st.button("💾 Guardar en historial", key="guardar_libre", use_container_width=True):
            if texto_libre.strip():
                perfil["historial"].append(f"✏️ {texto_libre.strip()}")
                st.success("Guardado.")
            else:
                st.warning("Escribe algo primero.")

    st.markdown("---")
    st.markdown("#### 🎤 Reconocimiento de voz *(requiere Chrome o Edge)*")
    st.components.v1.html(
        """
        <button onclick="startRec()"
            style="padding:10px 22px;font-size:16px;border-radius:8px;
                   background:#4A90E2;color:white;border:none;cursor:pointer;">
            🎤 Iniciar dictado
        </button>
        <p id="st" style="color:#444;margin-top:10px;font-size:15px;"></p>
        <script>
        function startRec(){
            var SR=window.SpeechRecognition||window.webkitSpeechRecognition;
            if(!SR){document.getElementById('st').innerText='⚠️ Navegador no compatible.';return;}
            var r=new SR();r.lang='es-ES';r.interimResults=false;
            document.getElementById('st').innerText='🎙️ Escuchando...';
            r.onresult=function(e){
                document.getElementById('st').innerText='✅ '+e.results[0][0].transcript;
            };
            r.onerror=function(e){
                document.getElementById('st').innerText='❌ Error: '+e.error;
            };
            r.start();
        }
        </script>
        """,
        height=110,
    )


# ─── TAB 4: HISTORIAL ────────────────────────────────────────────────────────
with tab4:
    st.markdown(f"### 📋 Historial de **{perfil['nombre']}**")

    if not perfil["historial"]:
        st.info("Aún no hay mensajes guardados. Construye frases y pulsa '💾 Guardar'.")
    else:
        for idx, msg in enumerate(reversed(perfil["historial"])):
            real_idx = len(perfil["historial"]) - 1 - idx
            col_msg, col_del = st.columns([9, 1])
            with col_msg:
                st.markdown(
                    f'<div style="background:white;border-radius:10px;padding:10px 16px;'
                    f'margin-bottom:8px;box-shadow:0 1px 4px rgba(0,0,0,0.08);'
                    f'font-size:17px;">{msg}</div>',
                    unsafe_allow_html=True,
                )
            with col_del:
                if st.button("🗑️", key=f"del_{real_idx}"):
                    perfil["historial"].pop(real_idx)
                    st.rerun()

        st.divider()
        if st.button("🗑️ Limpiar historial completo"):
            perfil["historial"] = []
            st.rerun()

        st.download_button(
            label="⬇️ Descargar historial (.txt)",
            data="\n".join(perfil["historial"]),
            file_name=f"historial_{perfil['nombre'].lower().replace(' ', '_')}.txt",
            mime="text/plain",
        )


# ── Pie de página ─────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center;color:#888;font-size:13px;'>"
    "ComunicApp · Supuesto 4 · Necesidades del Paciente · "
    "Grado en Ingeniería de la Salud · Universidad de Burgos</p>",
    unsafe_allow_html=True,
)s