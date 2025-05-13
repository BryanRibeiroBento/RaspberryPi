import os
import sys
import time
import threading
from PIL import Image
import sounddevice as sd
import soundfile as sf

# === Caminhos ===
base_dir = os.path.dirname(__file__)
audio_path = os.path.join(base_dir, "jazz.wav")
img_path = os.path.join(base_dir, "badbunny.png")

# === Lê o áudio
data, samplerate = sf.read(audio_path)
duration = len(data) / samplerate

# === Função para tocar o áudio ===
def tocar_audio():
    print("▶️ Tocando áudio...")
    sd.default.device = ('', 1)  # Define saída como WM8960
    sd.play(data, samplerate)
    sd.wait()
    print("✅ Áudio finalizado.")

# === Thread de reprodução ===
audio_thread = threading.Thread(target=tocar_audio)
audio_thread.start()

# Aguarda 1 segundo para garantir que o som começou antes de iniciar o display
time.sleep(1)

# === Agora inicializa o display ===
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

# === Mostra imagem girando enquanto o áudio ainda toca ===
base_image = Image.open(img_path).convert("RGB").resize((240, 240))
angle = 0
start_time = time.time()

# Loop por no máximo o tempo da música
while time.time() - start_time < duration:
    rotated = base_image.rotate(angle)
    display.display(rotated)
    angle = (angle + 5) % 360
    time.sleep(0.05)

# Exibe imagem final
display.display(base_image)