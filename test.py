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

# === Lê o arquivo de áudio ===
data, samplerate = sf.read(audio_path)

# === Função para tocar a música ===
def tocar_audio():
    print(f"▶️ Tocando '{audio_path}'")
    sd.play(data, samplerate)
    sd.wait()
    print("✅ Reprodução concluída.")

# === Thread para áudio ===
audio_thread = threading.Thread(target=tocar_audio)
audio_thread.start()

# === Duração estimada da música (ou use len(data)/samplerate) ===
duration = len(data) / samplerate  # em segundos

# === Loop de animação sincronizado com a música ===
angle = 0
start_time = time.time()

while time.time() - start_time < duration:
    rotated = base_image.rotate(angle)
    display.display(rotated)
    angle = (angle + 5) % 360
    time.sleep(0.05)

# === Exibe imagem estática ao final ===
display.display(base_image)