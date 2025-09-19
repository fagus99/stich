import streamlit as st
from PIL import Image, ImageDraw, ImageOps

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

# Crear overlay de color proporcional
overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
altura_coloreada = int(h * (porcentaje / 100))
draw.rectangle([(0, h - altura_coloreada), (w, h)], fill=color)

# Crear máscara binaria a partir del canal alfa del PNG
alpha = base.getchannel("A")
mask = alpha.point(lambda p: 255 if p > 0 else 0)  # todo lo que no es totalmente transparente

# Pegar overlay solo dentro del contorno
coloreado = Image.new("RGBA", base.size, (0, 0, 0, 0))
coloreado.paste(overlay, (0, 0), mask=mask)

# Fondo blanco
fondo = Image.new("RGBA", base.size, (255, 255, 255, 255))

# Combinar todo: fondo + color + contorno original
resultado = Image.alpha_composite(fondo, coloreado)
resultado = Image.alpha_composite(resultado, base)

# Mostrar
st.image(resultado, caption=f"{nombre} - {porcentaje}%")
