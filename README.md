![escudoUBU](imagenes/escudoUBU.png)

# 💬 ComunicApp — Comunicación Aumentativa con Pictogramas

Aplicación web diseñada para facilitar la comunicación de niños y niñas con dificultades en la expresión oral. Permite construir frases mediante pictogramas, texto libre y frases rápidas, con soporte de síntesis y reconocimiento de voz.

> **Asignatura:** Necesidades del Paciente — Grado en Ingeniería de la Salud  
> **Universidad de Burgos**

---

## 👥 Alumnos

| Nombre | Correo |
|---|---|
| Anna Lázaro | alc1020@alu.ubu.es |
| Minaya Moreno | mmr1047@alu.ubu.es |
| Miguel Soriano | mse1003@alu.ubu.es |
| Andrés Arribas | aaa1041@alu.ubu.es |
| Diego Vallina | dva1004@alu.ubu.es |

---

## 📋 Descripción

**ComunicApp** es una herramienta de comunicación aumentativa y alternativa (CAA) orientada a contextos escolares y familiares. Permite a los usuarios construir mensajes de forma visual e intuitiva combinando pictogramas (obtenidos de [ARASAAC](https://arasaac.org)), texto libre y frases preconfiguradas.

La aplicación soporta **múltiples perfiles de usuario**, cada uno con su propio historial, frase activa y frases rápidas personalizadas.

---

## ✨ Funcionalidades

- 🖼️ **Galería de pictogramas** organizada por categorías, con buscador integrado
- ⚡ **Frases rápidas** personalizables por perfil (p.ej. "Quiero ir al baño", "Tengo hambre")
- ✏️ **Texto libre** con síntesis de voz (español)
- 🎤 **Reconocimiento de voz** (compatible con Chrome y Edge)
- 🔊 **Lectura en voz alta** de las frases construidas
- 💾 **Historial** por perfil, descargable en `.txt`
- 👤 **Perfiles de usuario** con nombre y color personalizados

---

## 🗂️ Estructura de pictogramas

Los pictogramas deben colocarse en subcarpetas dentro de un directorio (por defecto `pictogramas/`). Cada subcarpeta es una categoría:

```
pictogramas/
  emociones/
    contento.png
    triste.jpg
  lugares/
    parque.png
  casa/
    cama.png
```

Formatos admitidos: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`

> Los pictogramas de ejemplo se pueden descargar gratuitamente desde [ARASAAC](https://arasaac.org).

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/alc1020/Necesidades_Supuesto4.git
cd Necesidades_Supuesto4
```

### 2. Instalar dependencias

```bash
pip install streamlit pillow
```

### 3. Añadir pictogramas

Crea la carpeta `pictogramas/` en el directorio del proyecto y añade subcarpetas con imágenes (ver estructura arriba).

### 4. Ejecutar la aplicación

```bash
streamlit run app.py
```

La app se abrirá automáticamente en el navegador en `http://localhost:8501`.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| [Streamlit](https://streamlit.io) | Framework de la aplicación web |
| [Pillow](https://python-pillow.org) | Carga y visualización de imágenes |
| Web Speech API | Síntesis y reconocimiento de voz (navegador) |
| Python 3.8+ | Lenguaje base |

---

## 📁 Estructura del proyecto

```
Necesidades_Supuesto4/
├── app.py                  # Código principal de la aplicación
├── pictogramas/            # Carpeta con los pictogramas (a añadir)
│   ├── emociones/
│   ├── casa/
│   └── ...
├── imagenes/
│   └── escudoUBU.png
└── README.md
```

---

## 📄 Licencia

Proyecto académico desarrollado para la Universidad de Burgos. Los pictogramas utilizados pertenecen a [ARASAAC](https://arasaac.org) bajo licencia Creative Commons BY-NC-SA.
