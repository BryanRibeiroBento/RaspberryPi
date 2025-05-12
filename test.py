import sys
import os
import time
import subprocess
import threading
from PIL import Image
import spidev
import RPi.GPIO as GPIO

# === Inicia thread para tocar a música usando WM8960 ===
def play_music():
    subprocess.run(["aplay", "-D", "hw:1,0", "jazz.wav"])

music_thread = threading.Thread(target=play_music)
music_thread.start()

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

# === Carrega e exibe imagem girando ===
img_path = "badbunny.png"
base_image = Image.open(img_path).convert("RGB").resize((240, 240))

# Roda a animação enquanto a música toca (ex: 70 segundos)
angle = 0
start_time = time.time()
duration = 70  # ajuste conforme duração da música

while time.time() - start_time < duration:
    rotated = base_image.rotate(angle)
    display.display(rotated)
    angle = (angle + 5) % 360
    time.sleep(0.05)

# Exibe imagem estática no fim
display.display(base_image)

# (Opcional) Reinicia o áudio após script:
# subprocess.run(["sudo", "systemctl", "restart", "alsa-utils.service"])