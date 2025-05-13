import os
import sys
import time
import threading
from PIL import Image
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio  # uso interno, mais controle

# === Caminhos ===
base_dir = os.path.dirname(__file__)
audio_path = os.path.join(base_dir, "jazz.wav")
img_path = os.path.join(base_dir, "badbunny.png")

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

# === Carrega a imagem ===
base_image = Image.open(img_path).convert("RGB").resize((240, 240))

# === Função para tocar a música ===
def tocar_musica():
    som = AudioSegment.from_wav(audio_path)
    playback = _play_with_simpleaudio(som)
    playback.wait_done()

# === Roda o áudio em uma thread ===
audio_thread = threading.Thread(target=tocar_musica)
audio_thread.start()

# === Animação enquanto a música toca ===
angle = 0
start_time = time.time()
duration = 70  # ajuste para a duração real da música

while time.time() - start_time < duration:
    rotated = base_image.rotate(angle)
    display.display(rotated)
    angle = (angle + 5) % 360
    time.sleep(0.05)

# Exibe imagem estática ao final
display.display(base_image)