import sys
import os
import time
import subprocess
import threading
from PIL import Image
import spidev
import RPi.GPIO as GPIO

# === Função que toca o áudio via subprocess com aplay ===
def play_music():
    subprocess.run(["/usr/bin/aplay", "-D", "plughw:1,0", "jazz.wav"])

# Inicia a thread para tocar o áudio
music_thread = threading.Thread(target=play_music)
music_thread.start()

# Adiciona o caminho do driver GC9A01
sys.path.append(os.path.join(os.path.dirname(__file__), 'library'))
from GC9A01 import GC9A01

# Inicializa o display
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

# Carrega a imagem
img_path = "badbunny.png"
base_image = Image.open(img_path).convert("RGB").resize((240, 240))

# Define tempo aproximado da música (em segundos)
MUSIC_DURATION = 5  # ajuste conforme necessário

# Loop de animação
angle = 0
start_time = time.time()
while time.time() - start_time < MUSIC_DURATION:
    rotated = base_image.rotate(angle)
    display.display(rotated)
    angle = (angle + 5) % 360
    time.sleep(0.05)

# Mostra imagem parada após o fim da música
display.display(base_image)
os.system("sudo systemctl restart alsa-utils")