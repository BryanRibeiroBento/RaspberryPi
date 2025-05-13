import sys
import os
import time
import subprocess
from PIL import Image
import spidev
import RPi.GPIO as GPIO

# === Caminhos absolutos ===
base_dir = os.path.dirname(__file__)
audio_path = os.path.join(base_dir, "jazz.wav")
img_path = os.path.join(base_dir, "badbunny.png")

# === Toca o áudio de forma síncrona usando WM8960 (card 1) ===
subprocess.run(["aplay", "-D", "hw:1,0", audio_path], check=True)

# === Inicializa o display ===
sys.path.append(os.path.join(base_dir, "library"))
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

# === Carrega a imagem base ===
base_image = Image.open(img_path).convert("RGB").resize((240, 240))

# === Animação por 70 segundos ===
# angle = 0
# start_time = time.time()
# duration = 70  # segundos

# while time.time() - start_time < duration:
#     rotated = base_image.rotate(angle)
#     display.display(rotated)
#     angle = (angle + 5) % 360
#     time.sleep(0.05)

# Exibe imagem estática ao final
display.display(base_image)

# === Libera o dispositivo de som para próximas execuções ===
subprocess.run(["sudo", "fuser", "-k", "/dev/snd/pcmC1D0p"])