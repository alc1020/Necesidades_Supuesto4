"""
Supuesto 4 - Aplicación web de comunicación con pictogramas
Población: Niños/niñas con problemas de expresión oral
Objetivo: Incluir pictogramas, palabras y/o frases para facilitar
          la comunicación en contextos escolares y/o familiares.


La app detecta automáticamente las subcarpetas como categorías
y los archivos de imagen dentro como pictogramas.
El nombre del archivo (sin extensión) se usa como etiqueta.
"""

import streamlit as st
import urllib.parse
from pathlib import Path
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


# ── Carga de pictogramas desde disco ────────────────────────────────────────
@st.cache_data(show_spinner=False)
def cargar_categorias(ruta_base: str) -> dict:
    """
    Recorre ruta_base buscando subcarpetas.
    Cada subcarpeta = una categoría.
    Cada imagen dentro = un pictograma.
    Devuelve: { "Nombre Cat": [ {"nombre": str, "ruta": str}, ... ], ... }
    """
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


# ── Función auxiliar: mostrar un pictograma con imagen + botón ───────────────
def mostrar_picto(picto: dict, img_size: int, key: str):
    """Muestra la imagen del pictograma y un botón para añadirlo a la frase."""
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
        st.session_state.frase_actual.append(
            {"nombre": picto["nombre"], "ruta": picto["ruta"]}
        )
        st.rerun()


# ── Sidebar: configuración ───────────────────────────────────────────────────
with st.sidebar:
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


# ── Cargar datos ─────────────────────────────────────────────────────────────
CATEGORIAS = cargar_categorias(ruta_pictos)

# ── Estado de sesión ─────────────────────────────────────────────────────────
if "frase_actual" not in st.session_state:
    st.session_state.frase_actual = []   # lista de {"nombre": str, "ruta": str|None}
if "historial" not in st.session_state:
    st.session_state.historial = []
if "frases_rapidas" not in st.session_state:
    st.session_state.frases_rapidas = [
        "Quiero ir al baño",
        "Tengo hambre",
        "Tengo sed",
        "Me duele la cabeza",
        "Estoy cansado",
        "Necesito ayuda",
        "Quiero ir a casa",
        "Quiero jugar",
    ]


# ── Cabecera ─────────────────────────────────────────────────────────────────
st.markdown("# 💬 ComunicApp")
st.markdown("**Aplicación de comunicación aumentativa con pictogramas**")
st.divider()


# ── Barra de frase construida (siempre visible) ──────────────────────────────
frase_texto = "  ·  ".join([item["nombre"] for item in st.session_state.frase_actual])
st.markdown(
    f'<div class="frase-box">{"..." if not frase_texto else frase_texto}</div>',
    unsafe_allow_html=True,
)

# Miniaturas de la frase actual
if st.session_state.frase_actual:
    n_mini = min(len(st.session_state.frase_actual), 12)
    mini_cols = st.columns(n_mini)
    for i, item in enumerate(st.session_state.frase_actual[:12]):
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

# Botones de control de la frase
col_b1, col_b2, col_b3, col_b4 = st.columns([2, 2, 2, 4])

with col_b1:
    if st.button("🔊 Leer en voz alta", use_container_width=True):
        if st.session_state.frase_actual:
            texto_plano = " ".join([item["nombre"] for item in st.session_state.frase_actual])
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
        if st.session_state.frase_actual:
            st.session_state.frase_actual.pop()
            st.rerun()

with col_b3:
    if st.button("🗑️ Borrar todo", use_container_width=True):
        st.session_state.frase_actual = []
        st.rerun()

with col_b4:
    if st.button("💾 Guardar en historial", use_container_width=True):
        if st.session_state.frase_actual:
            texto_guardado = " · ".join(
                [item["nombre"] for item in st.session_state.frase_actual]
            )
            st.session_state.historial.append(texto_guardado)
            st.session_state.frase_actual = []
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
            "- La ruta es correcta (absoluta o relativa al directorio donde lanzas "
            "`streamlit run`).\n"
            "- Dentro hay subcarpetas con imágenes (png, jpg, jpeg, bmp, webp, gif).\n\n"
            "Puedes cambiar la ruta en el panel lateral izquierdo."
        )
    else:
        # Buscador
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
            # Selector de categoría
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
                    mostrar_picto(
                        picto, img_size,
                        key=f"cat_{cat_seleccionada}_{i}"
                    )


# ─── TAB 2: FRASES RÁPIDAS ────────────────────────────────────────────────────
with tab2:
    st.markdown("### ⚡ Frases de uso frecuente — un solo toque")

    cols_r = st.columns(2)
    for i, frase in enumerate(st.session_state.frases_rapidas):
        with cols_r[i % 2]:
            if st.button(f"📢  {frase}", key=f"rapida_{i}", use_container_width=True):
                for palabra in frase.split():
                    st.session_state.frase_actual.append({"nombre": palabra, "ruta": None})
                st.rerun()

    st.divider()
    st.markdown("#### ➕ Añadir frase rápida personalizada")
    nueva_frase = st.text_input("Nueva frase", key="nf_input", label_visibility="collapsed",
                                placeholder="Escribe la frase y pulsa Agregar")
    if st.button("Agregar frase", key="nf_btn"):
        if nueva_frase.strip():
            st.session_state.frases_rapidas.append(nueva_frase.strip())
            st.success("Frase añadida.")
            st.rerun()
        else:
            st.warning("Escribe algo primero.")


# ─── TAB 3: TEXTO LIBRE ──────────────────────────────────────────────────────
with tab3:
    st.markdown("### ✏️ Escribe o dicta un mensaje")
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
                st.session_state.historial.append(f"✏️ {texto_libre.strip()}")
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
    st.markdown("### 📋 Historial de comunicación")

    if not st.session_state.historial:
        st.info("Aún no hay mensajes guardados. Construye frases y pulsa '💾 Guardar'.")
    else:
        for idx, msg in enumerate(reversed(st.session_state.historial)):
            real_idx = len(st.session_state.historial) - 1 - idx
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
                    st.session_state.historial.pop(real_idx)
                    st.rerun()

        st.divider()
        if st.button("🗑️ Limpiar historial completo"):
            st.session_state.historial = []
            st.rerun()

        st.download_button(
            label="⬇️ Descargar historial (.txt)",
            data="\n".join(st.session_state.historial),
            file_name="historial_comunicacion.txt",
            mime="text/plain",
        )


# ── Pie de página ─────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center;color:#888;font-size:13px;'>"
    "ComunicApp · Supuesto 4 · Necesidades del Paciente · "
    "Grado en Ingeniería de la Salud · Universidad de Burgos</p>",
    unsafe_allow_html=True,
)