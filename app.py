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

# Definir color según porcentaje
if porcentaje <= 30:
    color = (0, 0, 255, 180)   # azul
elif porcentaje <= 60:
    color = (255, 165, 0, 180) # naranja
else:
    color = (255, 0, 0, 180)   # rojo

# Dibujar área proporcional desde abajo
altura_coloreada = int(h * (porcentaje / 100))
draw.rectangle([(0, h - altura_coloreada), (w, h)], fill=color)

# Combinar con la base
resultado = Image.alpha_composite(base, overlay)

# Mostrar resultado
st.image(resultado, caption=f"{nombre} - {porcentaje}%")
