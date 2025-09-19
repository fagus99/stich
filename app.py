import streamlit as st
from PIL import Image, ImageDraw

st.title("💚 Stitch Progress App")

# Inputs
nombre = st.text_input("Escribí el nombre de la persona")
porcentaje = st.slider("Seleccioná porcentaje", 1, 100, 50)

# Cargar imagen (contorno)
base = Image.open("stich.png").convert("RGBA")
w, h = base.size

# Crear overlay de color proporcional
overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Colores con 85% de transparencia (alpha ~ 217)
if porcentaje <= 30:
    color = (0, 255, 0, 217)     # verde
elif porcentaje <= 60:
    color = (255, 165, 0, 217)   # naranja
else:
    color = (255, 0, 0, 217)     # rojo

# Dibujar rectángulo proporcional (relleno desde abajo)
altura_coloreada = int(h * (porcentaje / 100))
draw.rectangle([(0, h - altura_coloreada), (w, h)], fill=color)

# Usar el canal alfa del PNG como máscara (zonas transparentes no se pintan)
mask = base.getchannel("A")

# Aplicar máscara → colorear solo el interior
coloreado = Image.composite(overlay, Image.new("RGBA", base.size, (0, 0, 0, 0)), mask)

# Poner fondo blanco
fondo = Image.new("RGBA", base.size, (255, 255, 255, 255))

# Primero fondo + color, luego encima el contorno original
resultado = Image.alpha_composite(fondo, coloreado)
resultado = Image.alpha_composite(resultado, base)

# Mostrar
st.image(resultado, caption=f"{nombre} - {porcentaje}%")
