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
# 5. Agregar texto: nombre y mensaje vertical
# ---------------------------
draw_result = ImageDraw.Draw(resultado)

# Fuente grande (ajustar tamaño según tu imagen)
try:
    font_name = ImageFont.truetype("arial.ttf", 80)
    font_message = ImageFont.truetype("arial.ttf", 60)
except:
    font_name = ImageFont.load_default()
    font_message = ImageFont.load_default()

# Nombre arriba centrado
bbox = draw_result.textbbox((0, 0), nombre, font=font_name)
text_width = bbox[2] - bbox[0]
draw_result.text(((w - text_width) / 2, 10), nombre, fill=(0,0,0,255), font=font_name)

# Mensaje con porcentaje dentro del dibujo (vertical centrado)
mensaje = f"Tu porcentaje de maldad es del {porcentaje}%"
bbox = draw_result.textbbox((0, 0), mensaje, font=font_message)
text_width = bbox[2] - bbox[0]
text_height = bbox[50] - bbox[50]
draw_result.text(((w - text_width) / 2, h/2 - text_height/2), mensaje, fill=(0,0,0,255), font=font_message)

# ---------------------------
# 6. Mostrar resultado
# ---------------------------
st.image(resultado)


