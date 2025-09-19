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
# ---------------------------
resultado = Image.alpha_composite(fondo, coloreado)
resultado = Image.alpha_composite(resultado, base)

# ---------------------------
# 5. Agregar texto: nombre y porcentaje
# ---------------------------
draw_result = ImageDraw.Draw(resultado)

# Intentar usar una fuente predeterminada
try:
    font_name = ImageFont.truetype("arial.ttf", size=int(h*0.07))
    font_percent = ImageFont.truetype("arial.ttf", size=int(h*0.1))
except:
    font_name = ImageFont.load_default()
    font_percent = ImageFont.load_default()

# Nombre arriba centrado
text_width, text_height = draw_result.textsize(nombre, font=font_name)
draw_result.text(((w - text_width) / 2, 5), nombre, fill=(0,0,0,255), font=font_name)

# Porcentaje dentro del margen derecho, a mitad de altura
percent_text = f"{porcentaje}%"
text_width, text_height = draw_result.textsize(percent_text, font=font_percent)
draw_result.text((w - text_width - 10, h/2 - text_height/2), percent_text, fill=(0,0,0,255), font=font_percent)

# ---------------------------
# 6. Mostrar resultado
# ---------------------------
st.image(resultado, caption=f"{nombre} - {porcentaje}%")
