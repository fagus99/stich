import streamlit as st
from PIL import Image, ImageDraw, ImageOps

st.title("💚 Stitch Progress App")

# Inputs
nombre = st.text_input("Escribí el nombre de la persona")
porcentaje = st.slider("Seleccioná porcentaje", 1, 100, 50)

# Cargar imagen
base = Image.open("stich.png").convert("RGBA")
w, h = base.size

# Crear overlay de color proporcional
overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Definir color según porcentaje (con transparencia al 75% = alpha 191)
if porcentaje <= 30:
    color = (0, 255, 0, 191)     # verde
elif porcentaje <= 60:
    color = (255, 165, 0, 191)   # naranja
else:
    color = (255, 0, 0, 191)     # rojo

# Dibujar rectángulo proporcional (relleno desde abajo)
altura_coloreada = int(h * (porcentaje / 100))
draw.rectangle([(0, h - altura_coloreada), (w, h)], fill=color)

# Crear máscara desde el contorno (invertimos para que figura sea blanca)
mask = base.convert("L")
mask = ImageOps.invert(mask)

# Aplicar máscara al overlay → se pinta solo dentro del contorno
coloreado = Image.composite(overlay, Image.new("RGBA", base.size, (0, 0, 0, 0)), mask)

# Combinar con la base (mantiene contorno negro)
resultado = Image.alpha_composite(base, coloreado)

# Fondo blanco
fondo = Image.new("RGBA", base.size, (255, 255, 255, 255))
resultado_con_fondo = Image.alpha_composite(fondo, resultado)

# Mostrar
st.image(resultado_con_fondo, caption=f"{nombre} - {porcentaje}%")
