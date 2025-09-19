import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

st.title("💚 Stitch Progress App")

# Inputs
nombre = st.text_input("Escribí el nombre de la persona")
porcentaje = st.slider("Seleccioná porcentaje", 1, 100, 50)

# Cargar imagen (contorno)
base = Image.open("stich.png").convert("RGBA")
w, h = base.size

# Colores con 85% de transparencia (alpha ~ 217)
if porcentaje <= 30:
    color = (0, 255, 0, 217)     # verde
elif porcentaje <= 60:
    color = (255, 165, 0, 217)   # naranja
else:
    color = (255, 0, 0, 217)     # rojo

# ---------------------------
# 1. Crear máscara del interior del dibujo
# ---------------------------
gray = base.convert("L")
inverted = ImageOps.invert(gray)
mask_interior = inverted.point(lambda p: 255 if p > 128 else 0)

# ---------------------------
# 2. Crear overlay del color
# ---------------------------
overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
altura_coloreada = int(h * (porcentaje / 100))
draw.rectangle([(0, h - altura_coloreada), (w, h)], fill=color)

coloreado = Image.new("RGBA", base.size, (0, 0, 0, 0))
coloreado.paste(overlay, (0, 0), mask=mask_interior)

# ---------------------------
# 3. Fondo blanco
# ---------------------------
fondo = Image.new("RGBA", base.size, (255, 255, 255, 255))

# ---------------------------
# 4. Combinar: fondo + color + contorno original
# -----------------
