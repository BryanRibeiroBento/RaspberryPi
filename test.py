import os
import sys
import time
from PIL import Image
import sounddevice as sd
import soundfile as sf

# === Caminhos ===
base_dir = os.path.dirname(__file__)
audio_path = os.path.join(base_dir, "jazz.wav")
img_path = os.path.join(base_dir, "badbunny.png")

# === Lê o áudio
data, samplerate = sf.read(audio_path)
duration = len(data) / samplerate  # duração em segundos

# === Toca o áudio antes de mexer com o display
print("▶️ Tocando áudio...")
sd.default.device = ('', 1)  # garante que será a saída correta (WM8960)
sd.play(data, samplerate)
sd.wait()
print("✅ Áudio finalizado.")

# === Agora inicializa o display
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

# === Mostra imagem girando (opcional)
base_image = Image.open(img_path).convert("RGB").resize((240, 240))
angle = 0
start_time = time.time()

while time.time() - start_time < duration:
    rotated = base_image.rotate(angle)
    display.display(rotated)
    angle = (angle + 5) % 360
    time.sleep(0.05)

# Imagem final
display.display(base_image)