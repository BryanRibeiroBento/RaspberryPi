import os
from PIL import Image
import sys
import time

# === Inicializa display
sys.path.append(os.path.join(os.path.dirname(__file__), 'library'))
from GC9A01 import GC9A01

display = GC9A01(
    port=0,
    cs=0,
    dc=25,
    backlight=18,
    rst=24,
    width=240,
    height=240,
    rotation=0,
    spi_speed_hz=40000000
)

def mostrar_imagem(nome):
    img = Image.open(nome).convert("RGB").resize((240, 240))
    display.display(img)

# === Inicializa o TTS
nome = "eye.jpg"
mostrar_imagem(nome)