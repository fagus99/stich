import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import base64
from io import BytesIO

st.set_page_config(layout="wide")
st.title("💚 Stitch Progress App")

# Inputs
nombre = st.text_input("Escribí el nombre de la persona")
porcentaje = st.slider("Seleccioná porcentaje", 1, 100, 50)

# Cargar imagen PNG
base = Image.open("stich.png").convert("RGBA")
w, h = base.size

# ---------------------------
# Relleno proporcional dentro del contorno
# ---------------------------
# Elegir color según porcentaje
if porcentaje <= 30:
    color = (0, 255, 0, 217)     # verde
elif porcentaje <= 60:
    color = (255, 165, 0, 217)   # naranja
else:
    color = (255, 0, 0, 217)     # rojo

# Crear máscara del interior
gray = base.convert("L")
inverted = ImageOps.invert(gray)
mask_interior = inverted.point(lambda p: 255 if p > 128 else 0)

# Crear overlay de color
overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
altura_coloreada = int(h * (porcentaje / 100))
draw.rectangle([(0, h - altura_coloreada), (w, h)], fill=color)

coloreado = Image.new("RGBA", base.size, (0,0,0,0))
coloreado.paste(overlay, (0,0), mask_interior)

# Fondo blanco
fondo = Image.new("RGBA", base.size, (255,255,255,255))

# Combinar: fondo + color + contorno original
resultado = Image.alpha_composite(fondo, coloreado)
resultado = Image.alpha_composite(resultado, base)

# ---------------------------
# Convertir imagen final a base64 para HTML
# ---------------------------
buffered = BytesIO()
resultado.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

# ---------------------------
# Mostrar imagen con texto superpuesto usando HTML/CSS
# ---------------------------
st.markdown(
f"""
<div style="position: relative; display: inline-block;">

    <!-- Imagen -->
    <img src="data:image/png;base64,{img_str}" style="display:block; max-width:100%;" />

    <!-- Nombre arriba centrado -->
    <div style="
        position: absolute;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(255, 255, 255, 0.7);
        padding: 10px 20px;
        font-size: 50px;
        font-weight: bold;
    ">
        {nombre}
    </div>

    <!-- Texto vertical en margen izquierdo -->
    <div style="
        position: absolute;
        top: 50%;
        left: 0px;
        transform: translateY(-50%) rotate(-90deg);
        transform-origin: left top;
        background-color: rgba(255, 255, 255, 0.7);
        padding: 10px 20px;
        font-size: 40px;
        font-weight: bold;
    ">
        Tu porcentaje de maldad es del {porcentaje}%
    </div>

</div>
""", unsafe_allow_html=True)
