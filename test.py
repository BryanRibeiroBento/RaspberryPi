import sys
import os
import time
import subprocess
from PIL import Image
import spidev
import RPi.GPIO as GPIO

# === Carrega caminho da música ===
audio_path = os.path.join(os.path.dirname(__file__), "jazz.wav")

# === Toca a música (bloqueia até o fim) ===
subprocess.run(["aplay", "-D", "hw:1,0", audio_path], check=True)

# === Carrega driver da tela ===
sys.path.append(os.path.join(os.path.dirname(__file__), 'library'))
from GC9A01 import GC9A01

# === Inicializa o display ===
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

# === Carrega imagem ===
img_path = os.path.join(os.path.dirname(__file__), "badbunny.png")
base_image = Image.open(img_path).convert("RGB").resize((240, 240))

# === Roda a animação durante 70 segundos ===
angle = 0
start_time = time.time()
duration = 70  # ajuste conforme necessário

while time.time() - start_time < duration:
    rotated = base_image.rotate(angle)
    display.display(rotated)
    angle = (angle + 5) % 360
    time.sleep(0.05)

# Mostra imagem estática ao final
display.display(base_image)