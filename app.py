import streamlit as st
from PIL import Image, ImageDraw

st.title("💙 Stitch Progress App")
# Inputs
nombre = st.text_input("Escribí el nombre de la persona")
porcentaje = st.slider("Seleccioná porcentaje", 1, 100, 50)
# Cargar imagen de contorno
base = Image.open("stich.png").convert("RGBA")
w, h = base.size
# Crear overlay de color
overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
# Definir color según porcentaje con 75% transparencia (alpha=192)
if porcentaje <= 30:
    color = (0, 128, 0, 192)   # verde
elif porcentaje <= 60:
    color = (255, 165, 0, 192) # naranja
else:
    color = (255, 0, 0, 192)   # rojo
# Dibujar área proporcional desde abajo
altura_coloreada = int(h * (porcentaje / 100))
draw.rectangle([(0, h - altura_coloreada), (w, h)], fill=color)
# Combinar con la base
resultado = Image.alpha_composite(base, overlay)
# Crear fondo blanco
fondo_blanco = Image.new("RGBA", base.size, (255, 255, 255, 255))
# Poner la imagen con transparencia encima del fondo blanco
final_img = Image.alpha_composite(fondo_blanco, resultado)
# Mostrar resultado
st.image(final_img, caption=f"{nombre} - {porcentaje}%")
